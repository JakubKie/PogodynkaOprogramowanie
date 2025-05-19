from fastapi import Depends, HTTPException, Query
from fastapi_utils.inferring_router import InferringRouter
from fastapi_utils.cbv import cbv
from datetime import datetime

from backend.models.schemas import Reading
from backend.services.reading_service import ReadingService
from backend.repositories.memory_repository import InMemoryRepository

# ----------------------------------------------------
#  router i DI dla repozytorium + serwisu
# ----------------------------------------------------
router = InferringRouter()
shared_repository = InMemoryRepository()

def get_repository() -> InMemoryRepository:
    return shared_repository


def get_service(
    repo: InMemoryRepository = Depends(get_repository),
) -> ReadingService:
    return ReadingService(repo)

# ----------------------------------------------------
#  CBV: wszystkie endpointy w jednej klasie
# ----------------------------------------------------
@cbv(router)
class ReadingController:
    service: ReadingService = Depends(get_service)

    @router.post("/readings", status_code=201)
    def add_reading(self, reading: Reading):
        """
        Przyjmuje jeden odczyt (pogoda + zanieczyszczenia),
        wykonuje walidację (Pydantic) i zapisuje go w repozytorium.
        """
        self.service.add_reading(reading)
        return {"message": "Reading added"}

    @router.get("/readings", response_model=Reading)
    def get_closest(self, timestamp: datetime = Query(..., description="Timestamp w formacie ISO")):
        """
        Zwraca odczyt najbliższy podanej dacie/godzinie.
        """
        result = self.service.get_closest_reading(timestamp)
        if not result:
            raise HTTPException(status_code=404, detail="No reading found")
        return result

