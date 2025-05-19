from backend.models.schemas import Reading
from backend.repositories.memory_repository import InMemoryRepository
from datetime import datetime

class ReadingService:
    def __init__(self, repository: InMemoryRepository):
        self._repo = repository

    def add_reading(self, reading: Reading):
        self._repo.add_reading(reading)

    def get_closest_reading(self, timestamp: datetime):
        return self._repo.get_closest_reading(timestamp)
