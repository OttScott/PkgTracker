import importlib
import sys
import types
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

class DummyResponse:
    def __init__(self, data=None):
        self._data = data or {}
    def raise_for_status(self):
        pass
    def json(self):
        return self._data


def test_get_oauth_token_cached(monkeypatch):
    calls = []
    def fake_post(url, headers=None, data=None, auth=None):
        calls.append(1)
        return DummyResponse({"access_token": "abc", "expires_in": 3600})
    monkeypatch.setenv("UPS_CLIENT_ID", "id")
    monkeypatch.setenv("UPS_CLIENT_SECRET", "secret")
    requests_stub = types.SimpleNamespace(post=fake_post)
    sys.modules['requests'] = requests_stub
    http_client = importlib.import_module('tracker.http_client')
    http_client._token_cache = {"token": None, "expires_at": 0}
    token1 = http_client.get_oauth_token()
    token2 = http_client.get_oauth_token()
    assert token1 == token2 == "abc"
    assert len(calls) == 1


def test_fetch_ups_status_authorization(monkeypatch):
    collected = {}
    def fake_get(url, headers=None):
        collected.update(headers or {})
        return DummyResponse({})
    requests_stub = types.SimpleNamespace(get=fake_get)
    sys.modules['requests'] = requests_stub
    fetch_status = importlib.import_module('tracker.fetch_status')
    assert fetch_status.requests is requests_stub
    monkeypatch.setattr(fetch_status, 'get_oauth_token', lambda: 'xyz')
    fetch_status.fetch_ups_status("1Z999")
    assert collected.get("Authorization") == "Bearer xyz"
