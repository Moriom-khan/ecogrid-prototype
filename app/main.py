from app.common.events import Event
from app.infrastructure.event_broker import EventBroker
from app.smart_meter.service import SmartMeterService
from app.smart_meter.simulator import generate_reading
from app.marketplace.service import MarketplaceService
from app.settlement.service import SettlementService


def main():

    print("\n===================================")
    print(" EcoGrid Energy Prototype")
    print("===================================\n")

    # Infrastructure
    broker = EventBroker()

    # Bounded contexts
    smart_meter = SmartMeterService(broker)

    marketplace = MarketplaceService(broker)

    settlement = SettlementService(broker)

    # Generate smart-meter telemetry
    print("Generating smart-meter readings...\n")

    for meter_number in range(1, 6):

        reading = generate_reading(
            meter_id=f"METER-{meter_number:03}",
            homeowner_id=f"HOME-{meter_number:03}"
        )

        smart_meter.ingest(reading)

    print("\nAvailable Marketplace Offers:")

    for offer in marketplace.offers.values():

        print(
            f"{offer.offer_id} | "
            f"Seller={offer.seller_id} | "
            f"Energy={offer.energy_kwh} kWh | "
            f"Price=£{offer.price_per_kwh}"
        )

    # Create a trade using first available offer
    if marketplace.offers:

        offer = next(
            iter(marketplace.offers.values())
        )

        print("\nCreating trade...\n")

        trade = marketplace.create_trade(
            offer_id=offer.offer_id,
            buyer_id="BUYER-001",
            energy_kwh=min(
                offer.energy_kwh,
                1.0
            )
        )

        print(
            f"Trade ID: {trade.trade_id}"
        )

        print(
            f"Amount: £{trade.total_amount}"
        )

        # Duplicate-event demonstration
        print("\nTesting duplicate settlement event...\n")

        duplicate_event = Event(
            event_type="SettlementRequested",
            payload={
                "trade_id": trade.trade_id,
                "buyer_id": trade.buyer_id,
                "seller_id": trade.seller_id,
                "energy_kwh": trade.energy_kwh,
                "total_amount": trade.total_amount
            }
        )

        settlement.process_settlement(duplicate_event)

        print(
            "Total settlements:",
            len(settlement.settlements)
        )

    print("\nSettlements:")

    for settlement_record in settlement.settlements.values():

        print(
            f"{settlement_record.settlement_id} | "
            f"Trade={settlement_record.trade_id} | "
            f"Status={settlement_record.status} | "
            f"Amount=£{settlement_record.amount}"
        )

    print("\nDead Letter Queue:")

    print(
        len(broker.get_dead_letters()),
        "events"
    )


if __name__ == "__main__":
    main()
