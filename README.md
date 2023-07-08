# stam-prolog

[![Editorconfig](https://github.com/traP-jp/h23s-stam-prolog/actions/workflows/editorconfig.yml/badge.svg)](https://github.com/traP-jp/h23s-stam-prolog/actions/workflows/editorconfig.yml)
[![Python](https://github.com/traP-jp/h23s-stam-prolog/actions/workflows/python.yml/badge.svg)](https://github.com/traP-jp/h23s-stam-prolog/actions/workflows/python.yml)
[![LICENSE](https://img.shields.io/github/license/traP-jp/h23s-stam-prolog)](https://github.com/traP-jp/h23s-stam-prolog/blob/main/LICENSE)

- :ton:で終わったら宣言
- :arrow_right:が途中にあれば条件付き(if-then)
    - if節、then節は1文字スタンプを変数として扱う
    - if節でマッチしたら対応するthen節が宣言される
    - :and:でifの積、複数のthenを定義できる
- 変数は1つ以上のスタンプにマッチする
- :hatena:で終わったらクエリ
    - クエリのスタンプ列では変数が使える
    - クエリに変数が含まれない場合は完全一致するスタンプ列が宣言されているかどうかが返る(T/F)
    - クエリに変数が含まれる場合は、宣言されているスタンプ列の中でマッチするもの全てが列挙される
    - :arrow_right:を含むクエリは、、、忘れた

## development

[Poetry](https://python-poetry.org)が必要です。

```bash
# venvセットアップ
$ poetry install
# BOTサーバー実行
$ poetry run bot
# or, PythonのREPL実行
$ poetry run python3
```

## 参考

- [すごーい！ きみはプログラミング言語を実装できるフレンズなんだね - Qiita](https://qiita.com/vain0x/items/6d3b75f667d3ec7f1d2a)
- [vain0x/friends-lang: PL for friends in the Japaripark (Logical programming language with Japanese animation-reference joke syntax)](https://github.com/vain0x/friends-lang)
