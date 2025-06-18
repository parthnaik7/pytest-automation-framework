import pytest
import requests
import yaml
from utils.auth import get_oauth_token
from utils.schema_validator import validate_schema

@pytest.fixture(scope="module")
def token(request):
    environment = request.config.getoption("--env")
    return get_oauth_token(environment)

@pytest.mark.parametrize("test_case", yaml.safe_load(open('config/test_data.yaml'))['tests'])
def test_api_endpoints(token, test_case):
    headers = test_case.get('headers', {})
    headers['Authorization'] = f"Bearer {token}"

    response = requests.request(
        method=test_case['method'],
        url=test_case['endpoint'],
        headers=headers,
        json=test_case.get('body')
    )

    assert response.status_code == test_case['expected_status'], f"Unexpected status code: {response.status_code}"

    if 'schema' in test_case:
        assert validate_schema(response.json(), test_case['schema']), "Response schema validation failed"