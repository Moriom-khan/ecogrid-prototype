from dataclasses import dataclass
from datetime import datetime


@dataclass
class MeterReading:
    meter_id: str
    homeowner_id: str
    generation_kwh: float
    consumption_kwh: float
    timestamp: datetime

    @property
    def surplus_kwh(self) -> float:
        return max(
            self.generation_kwh - self.consumption_kwh,
            0
        )
