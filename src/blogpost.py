#!/usr/bin/env python3
"""
Copied from:
https://github.com/choldgraf/choldgraf.github.io/blob/main/src/blogpost.py
"""
import argparse
import json
import sys
from yaml import safe_load
from pathlib import Path
from datetime import datetime, timezone
from feedgen.feed import FeedGenerator
import unist as u

DEFAULTS = {"number": 10}

root = Path(__file__).parent.parent

# Aggregate all posts from the markdown and ipynb files
posts = []
for ifile in root.rglob("blog/**/*.md"):
    if "drafts" in str(ifile):
        continue

    text = ifile.read_text()
    try:
        _, meta, content = text.split("---", 2)
    except Exception:
        print(f"Skipping file with error: {ifile}", file=sys.stderr)
        continue

    # Load in YAML metadata
    meta = safe_load(meta)
    meta["path"] = ifile.relative_to(root).with_suffix("")
    if "title" not in meta:
        lines = text.splitlines()
        for ii in lines:
            if ii.strip().startswith("#"):
                meta["title"] = ii.replace("#", "").strip()
                break

    # Summarize content
    skip_lines = ["#", "--", "%", "++"]
    content = "\n".join(
        ii
        for ii in content.splitlines()
        if not any(ii.startswith(char) for char in skip_lines)
    )
    N_WORDS = 50
    words = " ".join(content.split(" ")[:N_WORDS])
    if not "author" in meta or not meta["author"]:
        meta["author"] = "kinotate"
    meta["content"] = meta.get("description", words)
    posts.append(meta)
# Convert string dates to datetime objects and filter out invalid dates
valid_posts = []
for post in posts:
    if post.get("date"):
        try:
            # Parse date - support various formats
            date_str = str(post["date"]).replace("Z", "+00:00")
            if "T" in date_str:
                date_obj = datetime.fromisoformat(date_str)
                # Ensure timezone info exists
                if date_obj.tzinfo is None:
                    date_obj = date_obj.replace(tzinfo=timezone.utc)
            else:
                # Try parsing date-only format
                date_obj = datetime.strptime(date_str.split()[0], "%Y-%m-%d")
                # Add timezone info for RSS feed
                date_obj = date_obj.replace(tzinfo=timezone.utc)
            post["date"] = date_obj
            valid_posts.append(post)
        except (ValueError, TypeError):
            continue  # Skip posts with invalid dates

# Sort posts by date (newest first)
posts = sorted(valid_posts, key=lambda x: x["date"], reverse=True)

# Generate an RSS feed
fg = FeedGenerator()
fg.id("http://kinotate.com")
fg.title("kintotate blog")
fg.author({"name": "kinotate", "email": ""})
fg.link(href="http://kinotate.com", rel="alternate")
fg.logo("http://kinotate.com/_static/kinotate.png")
fg.subtitle("kinotate's blog")
fg.description("kinotate's personal blog about macroeconomics")
# fg.link(href="http://chrisholdgraf.com/rss.xml", rel="self")
fg.language("ja")

# Add all my posts to it
for irow in posts:
    fe = fg.add_entry()
    fe.id(f"http://chrisholdgraf.com/{irow['path']}")
    fe.published(irow["date"])
    fe.title(irow["title"])
    fe.link(href=f"http://chrisholdgraf.com/{irow['path']}")
    fe.content(content=irow["content"])

# Write an RSS feed with latest posts
fg.atom_file(root / "atom.xml", pretty=True)
fg.rss_file(root / "rss.xml", pretty=True)

plugin = {
    "name": "Blog Post list",
    "directives": [
        {
            "name": "postlist",
            "doc": "An example directive for showing a nice random image at a custom size.",
            "alias": ["bloglist"],
            "arg": {},
            "options": {
                "number": {
                    "type": "int",
                    "doc": "The number of posts to include",
                }
            },
        }
    ],
}

children = []
for irow in posts:
    children.append(
        {
            "type": "card",
            "url": f"/{irow['path'].with_suffix('')}",
            "children": [
                {"type": "cardTitle", "children": [u.text(irow["title"])]},
                {"type": "paragraph", "children": [u.text(irow["content"])]},
                {
                    "type": "footer",
                    "children": [
                        u.strong([u.text("Date: ")]),
                        u.text(f"{irow['date']:%B %d, %Y} | "),
                        u.strong([u.text("Author: ")]),
                        u.text(f"{irow['author']}"),
                    ],
                },
            ],
        }
    )


def declare_result(content):
    """Declare result as JSON to stdout

    :param content: content to declare as the result
    """

    # Format result and write to stdout
    json.dump(content, sys.stdout, indent=2)
    # Successfully exit
    raise SystemExit(0)


def run_directive(name, data):
    """Execute a directive with the given name and data

    :param name: name of the directive to run
    :param data: data of the directive to run
    """
    assert name == "postlist"
    opts = data["node"].get("options", {})
    number = int(opts.get("number", DEFAULTS["number"]))
    output = children[:number]
    return output


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--role")
    group.add_argument("--directive")
    group.add_argument("--transform")
    args = parser.parse_args()

    if args.directive:
        data = json.load(sys.stdin)
        declare_result(run_directive(args.directive, data))
    elif args.transform:
        raise NotImplementedError
    elif args.role:
        raise NotImplementedError
    else:
        declare_result(plugin)
