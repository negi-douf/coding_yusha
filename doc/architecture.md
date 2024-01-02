# coding_yushaのアーキテクチャ

## ディレクトリ構成

ディレクトリ構成は下記の通り。

```
coding_yusha/
    ├── controller/ 
    │ └── core/ 
    └── asset/
dist/
```

- coding_yusha/controller  
    Humble Object。クラスの実態などを扱ったり副作用などでテストし辛いロジックをまとめる。ドメインモデルを使用して計算するモジュール群。
- coding_yusha/controller/core  
    ドメインモデル。できるだけ純粋関数で記述し、テスタブルにする。coding_yushaに必要となる基本的なロジック群はここにまとめる。抽象クラスもここにまとめる。
- coding_yusha/asset  
    coding_yusha全体で使用する静的アセットの管理。敵のパラメータとかのyamlファイルはここで管理。
- dist  
    ユーザーに配布するファイルを保存するディレクトリ。サンプルファイルやAPIのインタフェースなど。