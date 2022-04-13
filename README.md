■コマンド
docker container exec -it api bash
pip install -r requirements.txt

■ディレクトリ構成
alembic マイグレーション管理フォルダ
cluds データベースのcurd操作フォルダ
models データベースのモデル定義フォルダ
schemas APIにリクエストした際に実行される実関数
routes ルート定義フォルダ
database_setting.py データベースアクセス定義ファイル

■テストコマンド
python -m pytest