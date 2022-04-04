#poetry 
FROM python:3.7

WORKDIR /src
ADD requirements.txt .
# requirements.txtにリストされたパッケージをインストールする
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# コンテナ起動後、FastAPIを実行し8000ポートで待機
#poetry install前
CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]
# poetry install後
# CMD ["poetry", "run" ,"uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]