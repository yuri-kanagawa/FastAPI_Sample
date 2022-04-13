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
    #データ0件
    #assert response_obj == []
    assert response_obj == [{"anime_id": 1}]
    

def test_get_specific_votes():
    response = client.get('/animevote/ranking/11')
    assert response.status_code == 200, response.text
    response_obj = response.json()
    assert response_obj == []