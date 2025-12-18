import logging
from typing import Dict, List
from uuid import uuid4

from app.rabbitmq.config import rabbitmq_config
from app.rabbitmq.rpc_client import get_rpc_client
from app.schemas.group_schema import UserInfo


logger = logging.getLogger(__name__)


def fetch_group_users(user_ids: List[str], group_id: str) -> Dict[str, UserInfo]:
    """Fetch user info for a batch of user IDs via RabbitMQ RPC.

    Returns a mapping of user_id -> UserInfo.
    """
    # Deduplicate and clean IDs
    unique_ids = list({uid for uid in user_ids if uid})
    if not unique_ids:
        return {}

    request_id = str(uuid4())

    payload = {
        "request_id": request_id,
        "group_id": group_id,
        "user_ids": unique_ids,
    }

    logger.info(
        "Sending batched user info RPC request_id=%s group_id=%s user_count=%d",
        request_id,
        group_id,
        len(unique_ids),
    )

    rpc_client = get_rpc_client()
    try:
        response = rpc_client.call(
            exchange=rabbitmq_config.user_info_exchange,
            routing_key=rabbitmq_config.user_info_request_routing_key,
            payload=payload,
            timeout=rabbitmq_config.user_info_rpc_timeout,
        )
    except Exception as e:
        logger.error(
            "Error during user info RPC call request_id=%s group_id=%s: %s",
            request_id,
            group_id,
            e,
            exc_info=True,
        )
        return {}

    if not response:
        logger.warning(
            "No response for user info RPC request_id=%s group_id=%s", request_id, group_id
        )
        return {}

    users_data = response.get("users") or []
    result: Dict[str, UserInfo] = {}

    for raw in users_data:
        try:
            info = UserInfo(**raw)
            result[info.user_id] = info
        except Exception as e:
            logger.error(
                "Failed to parse UserInfo from RPC response for request_id=%s: %s; data=%s",
                request_id,
                e,
                raw,
            )

    logger.info(
        "User info RPC completed request_id=%s group_id=%s requested=%d returned=%d",
        request_id,
        group_id,
        len(unique_ids),
        len(result),
    )

    return result


