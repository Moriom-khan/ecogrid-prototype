import random
from datetime import datetime

from app.smart_meter.models import MeterReading


def generate_reading(meter_id: str, homeowner_id: str):

    generation = round(
        random.uniform(1.0, 8.0),
        2
    )

    consumption = round(
        random.uniform(0.5, 5.0),
        2
    )

    return MeterReading(
        meter_id=meter_id,
        homeowner_id=homeowner_id,
        generation_kwh=generation,
        consumption_kwh=consumption,
        timestamp=datetime.utcnow()
    )
