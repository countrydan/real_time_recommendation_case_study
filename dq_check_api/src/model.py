from pydantic import BaseModel
from datetime import datetime


class DataIn(BaseModel):
    customer_id: int | None = None
    service_id: int | None = None
    timestamp: datetime | None = None
    review_txt: str | None = None
    review_score: int | None = None


class DataOut(DataIn):
    valid: bool
