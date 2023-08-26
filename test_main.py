from fastapi.testclient import TestClient
from main import app
from helpers import validate_json_response
from models import ResponseDirection
import datetime

client = TestClient(app)

today = datetime.datetime.now().date()
yesterday = today - datetime.timedelta(days=1)
#should be set automatically
csv_id = "1e808762-16ea-4bbf-8620-180bb9c6b652"
set_id = "64ea23a7c6fbe121745fac73"

direction_test_dict = {"location": "novi sad","place_type":"museum","date": today.isoformat()}
direction_test_dict_wrong_date = {"location": "novi sad","place_type":"museum","date": yesterday.isoformat()}



def test_check_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "alive"}

def test_post_directions():
    response = client.post("/directions", json=direction_test_dict)
    assert response.status_code == 201

def test_post_directions_invalid_date():
    response = client.post("/directions", json=direction_test_dict_wrong_date)
    assert response.status_code == 400

def test_get_single_location():
    response = client.get(f"/locations/{set_id}")
    assert response.status_code == 200

def test_get_single_location_invalid():
    response = client.get("/locations/22332")
    assert response.status_code == 404

def test_get_csv():
    response = client.get(f"/downloads/{csv_id}")
    assert response.status_code == 200

def test_get_csv_invalid():
    response = client.get("/downloads/aaaaaa")
    assert response.status_code == 404
