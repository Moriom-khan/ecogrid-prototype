from datetime import datetime

from app.infrastructure.event_broker import EventBroker
from app.smart_meter.service import SmartMeterService
from app.marketplace.service import MarketplaceService
from app.smart_meter.models import MeterReading


def test_energy_reading_creates_offer():

    broker = EventBroker()

    smart_meter = SmartMeterService(broker)
    marketplace = MarketplaceService(broker)

    reading = MeterReading(
        meter_id="METER-001",
        homeowner_id="HOME-001",
        generation_kwh=5,
        consumption_kwh=2,
        timestamp=datetime.utcnow()
    )

    smart_meter.ingest(reading)

    assert len(marketplace.offers) == 1
