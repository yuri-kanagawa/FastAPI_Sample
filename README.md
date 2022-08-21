>■CreateEnvironment 環境構築<br>
>docker-compose build
>ocker-compose up -d
>docker container exec -it backend bash

---

>■LibraryInstall
>pip install -r requirements.txt

---

>■TestCommand テストコマンド
>python -m pytest

---

>■Create Mygration File マイグレーションファイル自動生成
>alembic revision --autogenerate -m "create tables"

---

>■ Reflect Migration マイグレーション反映
>alembic upgrade head

---

>■ Migration Down Grade マイグレーションダウングレード
>alembic downgrade -1
