from dataclasses import asdict

from app.common.events import Event
from app.common.observability import log_event
from app.smart_meter.models import MeterReading


class SmartMeterService:

    def __init__(self, broker):
        self.broker = broker
        self.readings = []

    def ingest(self, reading: MeterReading):

        self.readings.append(reading)

        log_event(
            f"Meter reading received: {reading.meter_id}"
        )

        event = Event(
            event_type="EnergyAvailable",
            payload={
                "meter_id": reading.meter_id,
                "homeowner_id": reading.homeowner_id,
                "generation_kwh": reading.generation_kwh,
                "consumption_kwh": reading.consumption_kwh,
                "surplus_kwh": reading.surplus_kwh,
                "timestamp": reading.timestamp.isoformat()
            }
        )

        self.broker.publish(event)
