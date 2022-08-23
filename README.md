> ■CreateEnvironment 環境構築<br>
> docker-compose build<br>
> docker-compose up -d<br>
> docker container exec -it backend bash<br>

---

> ■LibraryInstall<br>
> pip install -r requirements.txt<br>

---

> ■TestCommand テストコマンド<br>
> python -m pytest<br>

---

> ■Create Mygration File マイグレーションファイル自動生成<br>
> alembic revision --autogenerate -m "create tables"<br>

---

> ■ Reflect Migration マイグレーション反映<br>
> alembic upgrade head<br>

---

> ■ Migration Down Grade マイグレーションダウングレード<br>
> alembic downgrade -1<br>
