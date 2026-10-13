import pytest
import urllib.request
import json

def test_local_brain_connection():
    """Test connection to local llamafile server if active"""
    url = 'http://127.0.0.1:8080/v1/chat/completions'
    payload = {'messages': [{'role': 'user', 'content': 'ping'}]}
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
    
    try:
        with urllib.request.urlopen(req, timeout=2) as response:
            assert response.status == 200
    except Exception as e:
        pytest.skip(f'Local llamafile server not running on port 8080: {e}')
