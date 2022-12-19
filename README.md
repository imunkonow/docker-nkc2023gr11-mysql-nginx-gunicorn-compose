# 環境構築(docker)
## Docker 登録、ログイン
1. dockerのインストール
    - https://docs.docker.com/engine/
        - docker公式サイト(エディションは各環境に合わせてください。)
1. docker hubの登録
    - https://hub.docker.com/signup
1. dockerにログイン(コンソール)
    - `docker login`
        - IDとパスワードの入力

## Docker 登録、ログイン後
1. アプリをダウンロード
    - https://github.com/imunkonow/docker-nkc2023gr11-mysql-nginx-gunicorn-compose/archive/refs/heads/master.zip
1. アプリを展開
    - docker-nkc2023gr11-mysql-nginx-gunicorn-compose-master.zip
1. リポジトリに移動(docker-compose.yamlの階層)
    - `cd docker-nkc2023gr11-mysql-nginx-gunicorn-compose-master`
1. docker build
    - `docker-compose build`
1. docker compose
    - `docker-compose up -d`
        - 初回起動時(もしくは再起動 or 再度compose up)
            - `docker-compose exec gunicorn python manage.py migrate --noinput`
1. 動作確認(ブラウザ)
    - http://127.0.0.1

## AWS EC2上で動かす(ディスク容量に気を付ける(推定約5GB以上は必要))
1. セキュリティグループで80番ポートの解放
1. EC2インスタンスの作成(ubuntu)
1. EC2インスタンスに接続(コンソール)
1. アップデート&dockerインストール
    - `sudo su -`
    - `sudo apt update && sudo apt upgrade -y`
    - `sudo apt install docker docker-compose -y`
1. アプリをダウンロード
    - https://github.com/imunkonow/docker-nkc2023gr11-mysql-nginx-gunicorn-compose/archive/refs/heads/master.zip
1. アプリを展開
    - docker-nkc2023gr11-mysql-nginx-gunicorn-compose-master.zip
1. リポジトリに移動(docker-compose.yamlの階層)
    - `cd docker-nkc2023gr11-mysql-nginx-gunicorn-compose-master`
1. docker用に権限を変更
    - `chmod +x ./*`
1. docker build
    - `docker-compose build`
1. docker compose
    - `docker-compose up -d`
        - データベース操作(データベース作成が完了までエラー、30秒ほど待つと正常に実行される)
            1. 初回起動時(もしくは再起動 or 再度compose up)
                - `docker-compose exec gunicorn python manage.py migrate --noinput`
            1. 管理者ユーザーの作成
                - `docker-compose exec gunicorn python manage.py createsuperuser`
1. 動作確認(ブラウザ)
    - `http://パブリックIPアドレス`
        - httpsではなくhttp
---
# 環境構築(非docker)
1. python環境の構築
    - ダウンロード&インストール
        - (公式サイト)(Python3.8以上を推奨)
            - https://www.python.org/downloads/
1. アプリをダウンロード
    - https://github.com/imunkonow/docker-nkc2023gr11-mysql-nginx-gunicorn-compose/archive/refs/heads/master.zip
1. アプリを展開
    - docker-nkc2023gr11-mysql-nginx-gunicorn-compose-master.zip
1. リポジトリに移動
    - `cd docker-nkc2023gr11-mysql-nginx-gunicorn-compose-master`
1. 必要ライブラリのインストール
    - `python -m pip install -r requirements.txt`
1. 起動
    - `python manage.py runsslserver`
1. ブラウザ
    - https://127.0.0.1:8000
        - 詳細情報をクリック
            - 127.0.0.1にアクセスする（安全ではありません)をクリック
    > セキュリティ警告の表示がありますが、ローカル環境にアクセスしているので問題はないと思われます。
    
## 不足ファイル
- nkc2023gr11\mysite\interview\secret.py
    - 以下の内容を記述
        - ``` subscription = 'your azure subscription key' ```
