from dataclasses import dataclass
from datetime import datetime


@dataclass
class EnergyOffer:
    offer_id: str
    seller_id: str
    energy_kwh: float
    price_per_kwh: float
    created_at: datetime
    status: str = "AVAILABLE"


@dataclass
class Trade:
    trade_id: str
    buyer_id: str
    seller_id: str
    energy_kwh: float
    total_amount: float
    status: str = "CREATED"
