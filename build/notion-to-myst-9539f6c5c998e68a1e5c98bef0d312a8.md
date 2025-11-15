---
title: Notion から Myst へ部分的に移行する
date: "2025-11-02"
author: kinotate
description: Myst の良さを布教します
---

# Notion から Myst へ部分的に移行する

エディタで編集できて，デザインにあまり気を使わなくて良いモノが好きです．はじめは，一般的なマークダウン形式でメモを書いたりしていました．４年前に Notion を使い始めましたが，LaTeX のように footnote や bib.tex を使えないのがとても不便でした．そこで目をつけたのが Mystです．

## Myst の利便性

使い始めたばかりなのでわかっていることは少ないですが，Myst でできることには以下のようなものがあります．

- footnote がつけられる[^1]
- DOI をペーストするだけでリッチな引用ができる[^quote]
- すると勝手にreferences を作ってくれる
- bib.tex を使用することもできる (らしい)
- md -> tex ができる (マークダウンで論文が書ける)
- Jupyter Notebook がそのまま静的サイトのページになる
- Executable Documents なるものを作成できる (らしい)
- もちろん数式が使える {math}`u(c) = \frac{c^{1-\sigma} -1}{1 - \sigma}`
- 方程式にラベルがつけられる

```{math}
:label: hoge
Y_{t+h} = \Gamma_h Y_t + \sum_{j = 1}^P A_j Y_{t-j} + u_h
```

この式 {eq}`hoge` は ... のように LaTeX ばりに便利です．


[^1]: こんな感じでね！
[^quote]: こんな感じ -> {cite}`https://doi.org/10.2307/1912017`

## Myst の SSG (Static Site Generation) 機能をうまく使ってブログサイトを構築する


そして，Myst にはMyst形式のファイルからサイトを作成する機能もあります．この機能はブログ用というよりは，論文を公開したり，ライブラリのドキュメントに使われたりすることを想定しているようです．現在はデフォルトでブログ用の theme を用意しているわけではありません．

そこで，[この記事](https://chrisholdgraf.com/blog/2024/mystmd-with-the-blog/) とこの記事のソースとなっている [GitHub リポジトリ](https://github.com/choldgraf/choldgraf.github.io)を参考に Myst でブログサイトを構築しました[^checked]．Chris Holdgraf[^thanks] さんには頭が上がりません．本当にありがとうございます．

[^thanks]: https://chrisholdgraf.com/
[^checked]: 真似する上でちゃんとLICENSEの確認はしました

## 以上

以上，最初のデプロイのための意味のない記事でした．
