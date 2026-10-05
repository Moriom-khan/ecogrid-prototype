from app.infrastructure.event_broker import EventBroker
from app.settlement.service import SettlementService
from app.common.events import Event


def test_duplicate_trade_does_not_create_duplicate_settlement():

    broker = EventBroker()

    settlement = SettlementService(broker)

    event = Event(
        event_type="SettlementRequested",
        payload={
            "trade_id": "TRADE-001",
            "buyer_id": "BUYER-001",
            "seller_id": "SELLER-001",
            "energy_kwh": 2,
            "total_amount": 0.50
        }
    )

    settlement.process_settlement(event)

    settlement.process_settlement(event)

    assert len(settlement.settlements) == 1
