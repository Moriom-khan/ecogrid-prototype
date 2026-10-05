import uuid

from app.common.events import Event
from app.common.observability import log_event
from app.settlement.models import Settlement


class SettlementService:

    def __init__(self, broker):
        self.broker = broker

        # Settlement owns its own data.
        self.settlements = {}

        # Used for idempotency.
        self.processed_trade_ids = set()

        broker.subscribe(
            "SettlementRequested",
            self.process_settlement
        )

    def process_settlement(self, event: Event):

        payload = event.payload

        trade_id = payload["trade_id"]

        # Idempotency protection.
        if trade_id in self.processed_trade_ids:

            log_event(
                f"Duplicate settlement ignored: {trade_id}",
                event.correlation_id
            )

            return

        self.processed_trade_ids.add(trade_id)

        settlement_id = str(uuid.uuid4())

        settlement = Settlement(
            settlement_id=settlement_id,
            trade_id=trade_id,
            amount=payload["total_amount"],
            status="COMPLETED",
            created_at=event.created_at
        )

        self.settlements[settlement_id] = settlement

        result_event = Event(
            event_type="SettlementCompleted",
            payload={
                "trade_id": trade_id,
                "settlement_id": settlement_id,
                "amount": settlement.amount
            },
            correlation_id=event.correlation_id
        )

        self.broker.publish(result_event)

        log_event(
            f"Settlement completed: {settlement_id}",
            event.correlation_id
        )
