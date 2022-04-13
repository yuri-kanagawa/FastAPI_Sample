# from fastapi import FastAPI
from typing import List
from urllib import response
import pytest
from fastapi.testclient import TestClient

from main import app
# from schemas import anime_vote_schema

client = TestClient(app)

#データ空の時テスト
def test_list_vote():
    response = client.get('/animevote')
    assert response.status_code == 200, response.text
    response_obj = response.json()
    assert response_obj == []
    