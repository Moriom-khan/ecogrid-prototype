import uuid

from app.common.events import Event
from app.common.observability import log_event
from app.marketplace.models import EnergyOffer, Trade


class MarketplaceService:

    def __init__(self, broker):
        self.broker = broker

        # Marketplace owns its own data.
        self.offers = {}
        self.trades = {}

        broker.subscribe(
            "EnergyAvailable",
            self.handle_energy_available
        )

    def handle_energy_available(self, event: Event):

        payload = event.payload

        if payload["surplus_kwh"] <= 0:
            return

        offer_id = str(uuid.uuid4())

        offer = EnergyOffer(
            offer_id=offer_id,
            seller_id=payload["homeowner_id"],
            energy_kwh=payload["surplus_kwh"],
            price_per_kwh=0.25,
            created_at=event.created_at
        )

        self.offers[offer_id] = offer

        log_event(
            f"Energy offer created: {offer_id}",
            event.correlation_id
        )

    def create_trade(
        self,
        offer_id: str,
        buyer_id: str,
        energy_kwh: float
    ):

        offer = self.offers.get(offer_id)

        if not offer:
            raise ValueError("Offer does not exist")

        if energy_kwh > offer.energy_kwh:
            raise ValueError("Requested energy exceeds offer")

        trade_id = str(uuid.uuid4())

        total_amount = round(
            energy_kwh * offer.price_per_kwh,
            2
        )

        trade = Trade(
            trade_id=trade_id,
            buyer_id=buyer_id,
            seller_id=offer.seller_id,
            energy_kwh=energy_kwh,
            total_amount=total_amount
        )

        self.trades[trade_id] = trade

        event = Event(
            event_type="SettlementRequested",
            payload={
                "trade_id": trade_id,
                "buyer_id": buyer_id,
                "seller_id": offer.seller_id,
                "energy_kwh": energy_kwh,
                "total_amount": total_amount
            }
        )

        self.broker.publish(event)

        log_event(
            f"Trade created: {trade_id}",
            event.correlation_id
        )

        return trade
