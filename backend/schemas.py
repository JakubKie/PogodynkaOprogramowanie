from pydantic import BaseModel, Field, field_validator
from datetime import datetime

class Reading(BaseModel):
    timestamp: datetime = Field(..., description="Czas odczytu (ISO)")
    temperature: float = Field(..., description="Temperatura [°C]")
    pressure: float = Field(..., description="Ciśnienie [hPa]")
    pm10: float | None = Field(None, description="PM10 [µg/m³]")
    pm2_5: float | None = Field(None, description="PM2.5 [µg/m³]")
    carbon_monoxide: float | None = Field(None, description="CO [µg/m³]")

    @field_validator("temperature", mode="after")
    @classmethod
    def validate_temperature(cls, v):
        if not -50 <= v <= 60:
            raise ValueError("Temperature out of realistic range.")
        return v

    @field_validator("pressure", mode="after")
    @classmethod
    def validate_pressure(cls, v):
        if not 870 <= v <= 1080:
            raise ValueError("Pressure out of realistic range.")
        return v

    @field_validator("carbon_monoxide", mode="after")
    @classmethod
    def validate_co(cls, v):
        if v is not None and v < 0:
            raise ValueError("CO level must be non-negative.")
        return v
