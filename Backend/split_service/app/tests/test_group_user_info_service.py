from app.services.group_user_info_service import fetch_group_users
from app.schemas.group_schema import UserInfo


class DummyRPCClient:
    def __init__(self, response):
        self._response = response
        self.calls = []

    def call(self, exchange, routing_key, payload, timeout=None):
        self.calls.append(
            {"exchange": exchange, "routing_key": routing_key, "payload": payload}
        )
        return self._response


def test_fetch_group_users_maps_response(monkeypatch):
    from app import rabbitmq as rmq_module

    response = {
        "request_id": "req-1",
        "group_id": "group-1",
        "users": [
            {
                "user_id": "u1",
                "name": "Alice",
                "avatar_url": None,
                "card_number": None,
                "card_holder_name": None,
                "created_at": None,
            }
        ],
    }

    dummy_client = DummyRPCClient(response)
    monkeypatch.setattr(
        rmq_module, "get_rpc_client", lambda: dummy_client
    )

    result = fetch_group_users(["u1", "u1"], "group-1")

    assert "u1" in result
    assert isinstance(result["u1"], UserInfo)
    assert result["u1"].name == "Alice"


