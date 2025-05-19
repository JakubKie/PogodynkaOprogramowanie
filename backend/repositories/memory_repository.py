from backend.models.schemas import Reading
from typing import List, Optional
from datetime import datetime

class InMemoryRepository:
    def __init__(self):
        self._readings: List[Reading] = []

    def add_reading(self, reading: Reading):
        self._readings.append(reading)

    def get_closest_reading(self, target: datetime) -> Optional[Reading]:
        if not self._readings:
            return None
        return min(self._readings, key=lambda r: abs(r.timestamp - target))
