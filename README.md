# coding_yusha

## Overview

これは、勇者パーティの行動をプログラミングして敵を倒していくRPGです。

多くのRPGの戦闘では、プレイヤーが毎ターン味方の行動を細かく選択します。  
しかし、このゲームではそれができません！⚠️

ではどうするのでしょうか？🤔

毎ターン命令する代わりに、**事前に各ユニットの行動パターンをプログラミングしておく**のです！  
これは、プレイヤーが**ガチのソースコードを書く**ということを意味しています。

襲いかかる敵に挑み、その行動を分析し、倒し方を考える。  
そして、その倒し方 == 攻略アルゴリズムを味方ユニットに実装する。  
実装ができたら、また敵に挑む...

攻略のしかた、実装のしかたはあなたの自由です！  
もちろん、ステータスはいじっちゃダメですよ😉

これは、そんな攻略とプログラミングを楽しむゲームです。  
さあ、**あなただけの最高に賢い勇者パーティ**を作ってみてください👍

このゲームはPythonで実装されており、CLI (Command Line Interface) で動作します。  
つまり、**プレイヤーによるプログラミングはPythonでおこないます。**

## Usage

```sh
poetry run python coding_yusha.py <stage> [ally_py_files]
```

For example,

```sh
poetry run python coding_yusha.py hello_world workshop/hello_world/warrior.py
```

## Philosophy

このプロジェクトは、制作者が「何かゲーム型のプログラミング学習教材を作りたい」と考えていて思いついたものです。  
そのため、以下のような思想があります。

- プログラミングの初級者から上級者まで楽しめるものにする
- チームで取り組めるものにする
- シンタックスのレクチャーは重視しない  
  プレイヤーはすでに基本の構文・記述方法を修得しているものとする。
- シナリオを重視しない
- グラフィックを重視しない

## For Contributors

### ユニットテスト

```sh
$ poetry run pytest
```

### コードのフォーマット

```sh
$ poetry run autopep8 --in-place --aggressive --recursive coding_yusha/
```

### lint

```sh
$ poetry run flake8
```

### インポート文のソート

```sh
$ poetry run isort .
```

## Tips

### Gitフックの設定

Gitフックを設定することでコミット前にコードベースの検証ができる。
そのために、まずpre-commit実行ファイルを作成する。

```sh
$ touch .git/hooks/pre-commit
$ chmod +x .git/hooks/pre-commit
```

作成した実行ファイルに下記の内容を書き込んで保存。
この設定によって`poetry run pytest && poetry run flake8`がコミット時に実行され、コマンドが成功したらコミット出来るようになる。

```sh
#!/bin/sh

poetry run flake8 && poetry run isort --check-only . && poetry run pytest
```
