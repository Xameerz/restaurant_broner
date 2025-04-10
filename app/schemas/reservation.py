from pydantic import BaseModel, Field, validator
from datetime import datetime, timedelta, timezone
from typing import Optional

class ReservationBase(BaseModel):
    customer_name: str = Field(..., description="Имя клиента", min_length=1, max_length=100)
    table_id: int = Field(..., description="ID стола", gt=0)
    reservation_time: datetime = Field(..., description="Время бронирования")
    duration_minutes: int = Field(..., description="Длительность бронирования в минутах", gt=0, le=240)

    @validator('reservation_time', pre=True)
    def ensure_timezone_aware_and_future(cls, v):
        if isinstance(v, str):
            v = datetime.fromisoformat(v)
        
        # Если datetime без tzinfo — делаем его UTC
        if v.tzinfo is None:
            v = v.replace(tzinfo=timezone.utc)
        else:
            # Переводим во временную зону UTC
            v = v.astimezone(timezone.utc)
        
        # Сравниваем с текущим временем в UTC
        if v < datetime.now(timezone.utc):
            raise ValueError('Время бронирования не может быть в прошлом')
        
        return v

    @validator('duration_minutes')
    def duration_must_be_reasonable(cls, v):
        if v < 30:
            raise ValueError('Минимальная длительность бронирования - 30 минут')
        if v > 240:
            raise ValueError('Максимальная длительность бронирования - 4 часа')
        return v

class ReservationCreate(ReservationBase):
    pass

class ReservationUpdate(BaseModel):
    customer_name: Optional[str] = Field(None, description="Имя клиента", min_length=1, max_length=100)
    table_id: Optional[int] = Field(None, description="ID стола", gt=0)
    reservation_time: Optional[datetime] = Field(None, description="Время бронирования")
    duration_minutes: Optional[int] = Field(None, description="Длительность бронирования в минутах", gt=0, le=240)

class ReservationOut(ReservationBase):
    id: int = Field(..., description="ID бронирования")

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "id": 1,
                "customer_name": "Иван Иванов",
                "table_id": 1,
                "reservation_time": "2024-04-08T19:00:00",
                "duration_minutes": 120
            }
        }
