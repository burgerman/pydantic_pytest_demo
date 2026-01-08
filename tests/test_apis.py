import fastapi
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_feed_data_valid():
    valid_payload = [
        {
            "transaction_id":"tx01",
            "type":"type1",
            "counterparty":"TD",
            "amount":1000.50,
            "tags":['food', 'utilities'],
            "transaction_timestamp":"2025-12-24 13:30:15"
        },
        {
            "transaction_id": "tx02",
            "type": "type1",
            "counterparty": "RBC",
            "amount": 500.60,
            "tags": ['groceries', 'transport'],
            "transaction_timestamp": "2025-12-24 18:00:52"
        }
    ]
    response = client.post("/transactions/feed", json=valid_payload)
    assert response.status_code == 201
    assert response.json()['status'] == "data ingested"
    assert response.json()['data_size'] == 2

def test_feed_data_invalid():
    # Test with invalid type (not in VALID_TYPES) and invalid amount (negative)
    invalid_payload = [
        {
            "transaction_id": "tx02",
            "type": "invalid_type",
            "counterparty": "gts",
            "amount": -10.5,
            "tags": ['tag1'],
            "transaction_timestamp": "2025-12-23 15:10:15"
        }
    ]
    response = client.post("/transactions/feed", json=invalid_payload)
    assert response.status_code == 422
    
    # Optional: verify specific error messages in the detail
    detail = response.json()["detail"]
    error_types = [err["type"] for err in detail]
    assert "value_error" in error_types or "greater_than" in error_types

@pytest.mark.parametrize("invalid_payload", [
    # case 1: invalid type
    {
        "transaction_id": "tx02",
        "type": "invalid_type",
        "counterparty": "gts",
        "amount": 100.0,
        "tags": ['tag1'],
        "transaction_timestamp": "2025-12-23 18:20:10"
    },
    # case 2: invalid amount
    {
        "transaction_id": "tx03",
        "type": "type1",
        "counterparty": "gts",
        "amount": -80.5,
        "tags": ['tag2'],
        "transaction_timestamp": "2025-12-23 20:00:10"
    },
    # case 3: invalid tags type
    {
        "transaction_id": "tx03",
        "type": "type1",
        "counterparty": "gts",
        "amount": 50.0,
        "tags": 'tag1',
        "transaction_timestamp": "2025-12-23 21:05:30"
    },

    # case 4: missing timestamp
    {
            "transaction_id": "tx03",
            "type": "type2",
            "counterparty": "gts",
            "amount": 500.0,
            "tags": ['tag1', 'tag2']
    },

    # case 5: empty
    {},

    # case 6: transaction_id too long
    {
        "transaction_id": "this_is_a_very_long_transaction_id_exceeding_15_chars",
        "type": "type1",
        "counterparty": "gts",
        "amount": 100.0,
        "tags": ['tag1'],
        "transaction_timestamp": "2025-12-23 22:00:00"
    }
])
def test_feed_api_invalid_with_parametrized(invalid_payload):
    # single invalid_payload in a list.
    response = client.post("/transactions/feed", json=[invalid_payload])
    assert response.status_code == 422

    errors = response.json().get("detail")
    assert errors is not None
    assert len(errors) > 0
    # verify that the errors are related to the fields
    expected_error_types = ['value_error', 'greater_than', 'list_type', 'missing', 'string_too_long']
    for error in errors:
        assert error['type'] in expected_error_types
    # error_messages = [str(err['msg']) for err in errors]
    # print(error_messages)
    # error_types = [str(err['type']) for err in errors]
    # print(error_types)

def test_get_connection():
    response = client.get("/connect")
    assert response.status_code == 200
    assert response.json()['status'] == "connected"