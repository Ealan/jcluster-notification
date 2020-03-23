# アマチュア無線 記念局交信 LINE通知システム for jCluster

定期的に[jCluster](http://qrv.jp)をPythonでスクレイピングして特定のコールサインの交信ログをLINEに通知するシステムです。

動作環境を簡単に構築できるように[Docker](https://www.docker.com)を利用しています。

## 動作環境

* [Docker](https://www.docker.com)

## 利用方法

1. [LINE Notify](https://notify-bot.line.me/ja/)でトークンを作成してください。
1. data/token.txtに発行したトークンを記載してください。
1. 通知したいコールサインのprefixをdata/callsign_filter_list.txtに記載してください。
1. 下記のコマンドでビルドをしてください。
```
make build
```
1. 下記のコマンドで起動してください。
```
make up
```


## 停止方法

パソコンを再起動してもDockerが稼働している限り、自動的に稼働するようにしています。
停止したい場合は下記のコマンドを実行してください。
```
make down
```

