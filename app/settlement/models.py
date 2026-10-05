from dataclasses import dataclass
from datetime import datetime


@dataclass
class Settlement:
    settlement_id: str
    trade_id: str
    amount: float
    status: str
    created_at: datetime
