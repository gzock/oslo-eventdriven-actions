# 概要

OpenStackのメッセージング基盤である`oslo.messaging`を使ってイベントドリブンに何かしらのアクションを実行するスクリプト。  
といっても具体的に実行する何かを実装しているわけではないのでテンプレート的なやつ。アイディア次第で色んなことに流用可能。

* 参考: https://wiki.openstack.org/wiki/Oslo

# 使用方法

* transport.confにMQ接続情報を指定
  * nova.confやneutron.confを見れば、それっぽい情報が書いてあるので、それをコピペ

```bash
$ cat transport.conf
[DEFAULT]
transport_url=rabbit://guest:guest@openstack.example.local:5672
ssl=False
```

* 補足したいイベントタイプを変更
  * デフォでは、インスタンス関連イベントをすべて捕まえる
  * インスタンス作成/削除/変更 etc.

```python
  filter_rule = oslo_messaging.NotificationFilter(
    publisher_id=".*",
    event_type="compute.instance.*")
```

* main.pyの`some actions`の部分にイベントに応じたアクションを実装

# 使いそうなシーン

* インスタンスやポートの作成/削除に応じたDNS連携
  * Designateを使えばDNSaaSできるが、一部のイベントに対応しておらず、レコードのゴミが残置してしまうことがある
* NW機器との連携
  * CiscoACIなどのようなSDNを導入している場合に有用かも
  * インスタンスへのFIP割り当てなどのイベントに応じて、SDNのAPIを叩いて必要なNW設定を行ったりなど
