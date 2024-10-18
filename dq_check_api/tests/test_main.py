import datetime
import random
import logging
from fastapi.testclient import TestClient
import pytest

from src.main import app

logging.basicConfig(level=logging.INFO)

lorem = open('lorem.txt').read().split()


def generate_data() -> dict:
    for _ in range(100):
        random_int = random.randint(1, 100)
        yield {
            'customer_id': random.choices([random_int, None])[0],
            'service_id': random.choices([random_int, None])[0],
            'timestamp': str(datetime.datetime.now()),
            'review_txt': ' '.join(lorem[random.randint(0, len(lorem) - 1):len(lorem) - 1]),
            'review_score': random.randint(1, 5)
        }

@pytest.mark.asyncio
async def test_main():
    with TestClient(app) as client:
        for data in generate_data():
            response = client.post('/receive', json=data)
            print(response)
            assert response.status_code == 201
            assert response.json() == {'msg': 'received'}
