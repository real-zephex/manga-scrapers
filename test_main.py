import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_homepage():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the manganato scraper"}

def test_read_root_head():
    response = client.head("/")
    assert response.status_code == 200
    assert response.headers.get("Custom-Header") == "Value"

def test_manganato_search():
    response = client.get("/manganato/search/naruto")
    assert response.status_code == 200
    # Add more assertions based on the expected response

def test_manganato_info():
    response = client.get("/manganato/info/some_id")
    assert response.status_code == 200
    # Add more assertions based on the expected response

def test_mangareader_search():
    response = client.get("/mangareader/search/naruto")
    assert response.status_code == 200
    # Add more assertions based on the expected response

def test_mangareader_genre_list():
    response = client.get("/mangareader/genre-list/")
    assert response.status_code == 200
    assert response.json()["genres"] == ["Action, Adventure, Comedy, Cooking, Doujinshi, Drama, Erotica, Fantasy, Gender Bender, Harem, Historical, Horror, Isekai, Josei, Manhua, Manhwa, Martial arts, Mature, Mecha, Medical, Mystery, One shot, Pornographic, Pschological, Romance, School life, Sci fi, Seinen, Shoujo, Shounen ai, Slice of life, Smut, Sports, Supernatural, Tragedy, Webtoons, Yaoi, Yuri"]

def test_mangapill_search():
    response = client.get("/mangapill/search/naruto")
    assert response.status_code == 200
    # Add more assertions based on the expected response

def test_asurascans_search():
    response = client.get("/asurascans/search/naruto")
    assert response.status_code == 200
    # Add more assertions based on the expected response

def test_flamescans_search():
    response = client.get("/flamescans/search/naruto")
    assert response.status_code == 200
    # Add more assertions based on the expected response

# Add more tests for other endpoints and categories as needed
