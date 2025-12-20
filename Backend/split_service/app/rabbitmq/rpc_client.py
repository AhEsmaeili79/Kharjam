import json
import logging
import time
from typing import Any, Dict, Optional
from uuid import uuid4

import pika

from .config import rabbitmq_config
from .setup import RabbitMQSetup


logger = logging.getLogger(__name__)


class RabbitMQRPCClient:
    """Generic RabbitMQ RPC client using per-request exclusive reply queues."""

    def __init__(self) -> None:
        self.connection: Optional[pika.BlockingConnection] = None
        self.channel: Optional[pika.channel.Channel] = None
        self._setup = RabbitMQSetup()
        self._response: Optional[Dict[str, Any]] = None
        self._corr_id: Optional[str] = None

    def _connect(self) -> None:
        if self.connection and not self.connection.is_closed:
            return
        self.connection = self._setup.create_connection()
        self.channel = self.connection.channel()

    def _disconnect(self) -> None:
        try:
            if self.channel and not self.channel.is_closed:
                self.channel.close()
        finally:
            if self.connection and not self.connection.is_closed:
                self.connection.close()
        self.connection = None
        self.channel = None

    def call(
        self,
        exchange: str,
        routing_key: str,
        payload: Dict[str, Any],
        timeout: Optional[float] = None,
    ) -> Optional[Dict[str, Any]]:
        """Perform an RPC call and wait synchronously for the response.

        Returns the decoded JSON response dict, or None on timeout / failure.
        """
        self._connect()
        assert self.channel is not None

        timeout = timeout or rabbitmq_config.user_info_rpc_timeout
        self._response = None
        self._corr_id = str(uuid4())

        # Declare a temporary exclusive, auto-delete queue for the reply
        result = self.channel.queue_declare(queue="", exclusive=True, auto_delete=True)
        callback_queue = result.method.queue

        def on_response(ch, method, props, body):
            try:
                if props.correlation_id != self._corr_id:
                    # Not our response; requeue for whoever is waiting
                    ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)
                    return
                data = json.loads(body.decode("utf-8"))
                self._response = data
                ch.basic_ack(delivery_tag=method.delivery_tag)
            except json.JSONDecodeError as e:
                logger.error(f"Failed to decode RPC response JSON: {e}")
                ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
            except Exception as e:
                logger.error(f"Error handling RPC response: {e}", exc_info=True)
                ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)

        self.channel.basic_consume(
            queue=callback_queue, on_message_callback=on_response, auto_ack=False
        )

        body = json.dumps(payload)
        properties = pika.BasicProperties(
            reply_to=callback_queue,
            correlation_id=self._corr_id,
            delivery_mode=2,
            content_type="application/json",
        )

        logger.info(
            "Publishing RPC request to exchange=%s routing_key=%s correlation_id=%s",
            exchange,
            routing_key,
            self._corr_id,
        )

        try:
            self.channel.basic_publish(
                exchange=exchange,
                routing_key=routing_key,
                body=body,
                properties=properties,
            )
        except Exception as e:
            logger.error(f"Failed to publish RPC request: {e}", exc_info=True)
            # Cleanup consumer before returning
            self.channel.basic_cancel(consumer_tag=self.channel.consumer_tags[-1])
            return None

        start = time.time()
        try:
            while self._response is None:
                elapsed = time.time() - start
                if elapsed >= timeout:
                    logger.warning(
                        "RPC call timed out after %.2f seconds (corr_id=%s)",
                        elapsed,
                        self._corr_id,
                    )
                    break
                # Process incoming data events for a short time slice
                self.connection.process_data_events(time_limit=0.2)
        finally:
            try:
                # Cancel the consumer; queue is auto-deleted
                # Use consumer_tags list if available, otherwise cancel all
                if getattr(self.channel, "consumer_tags", None):
                    for tag in list(self.channel.consumer_tags):
                        self.channel.basic_cancel(consumer_tag=tag)
            except Exception:
                # Best-effort cleanup
                pass
            self._disconnect()

        return self._response


def get_rpc_client() -> RabbitMQRPCClient:
    """Convenience accessor for creating a new RPC client instance."""
    return RabbitMQRPCClient()


