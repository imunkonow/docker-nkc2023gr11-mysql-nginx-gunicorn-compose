# nkc2023gr11 卒業研究

https://nkc2023gr11.pythonanywhere.com/

# 環境構築
1. python環境の構築
    - ダウンロード&インストール
        - (公式サイト)(Python3.8以上を推奨)
            - https://www.python.org/downloads/
1. アプリのダウンロード
    - `clone https://github.com/imunkonow/nkc2023gr11.git`
    <br>or<br>
    - https://github.com/imunkonow/nkc2023gr11/archive/refs/heads/master.zip
1. gitリポジトリに移動
    - `cd nkc2023gr11`
1. 必要ライブラリのインストール
    - `python -m pip install -r requirements.txt`
1. manage.pyのディレクトリへ変更
    - `cd mysite`
1. 起動
    - `python manage.py runsslserver`
    <br>or<br>
    - `python manage.py runserver`
1. ブラウザ
    - `python manage.py runsslserver`の場合
        - https://127.0.0.1:8000
    - `python manage.py runserver`の場合
        - http://127.0.0.1:8000
    > urlはお使いの環境によります。'起動'時の出力コマンドをご確認ください。
    
## 不足ファイル
- nkc2023gr11\mysite\interview\secret.py
    - 以下の内容を記述
        - ``` subscription="your azure subscription key ```
- nkc2023gr11\mysite\interview\static\.secretcsv\.all.csv
    - 以下の内容を記述
        - 出席番号,氏名,4月集計欠席,4月集計欠課,4月集計遅刻,4月年間累計欠席,4月年間累計欠課,4月年間累計遅刻,4月年間累計欠席換算,5月集計欠席,5月集計欠課,5月集計遅刻,5月年間累計欠席,5月年間累計欠課,5月年間累計遅刻,5月年間累計欠席換算,6月集計欠席,6月集計欠課,6月集計遅刻,6月年間累計欠席,6月年間累計欠課,6月年間累計遅刻,6月年間累計欠席換算,7月集計欠席,7月集計欠課,7月集計遅刻,7月年間累計欠席,7月年間累計欠課,7月年間累計遅刻,7月年間累計欠席換算,9月集計欠席,9月集計欠課,9月集計遅刻,9月年間累計欠席,9月年間累計欠課,9月年間累計遅刻,9月年間累計欠席換算,10月集計欠席,10月集計欠課,10月集計遅刻,10月年間累計欠席,10月年間累計欠課,10月年間累計遅刻,10月年間累計欠席換算
1,氏名,,,,,,,0.0,,,,,,,0.0,,2.0,,,2.0,,0.33,,,,,2.0,,0.33,,,,,2.0,,0.33,,,1.0,,2.0,1.0,0.42
