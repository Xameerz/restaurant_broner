from pydantic import BaseModel, Field, validator
from typing import Optional

class TableBase(BaseModel):
    name: str = Field(..., description="Название стола", min_length=1, max_length=100)
    seats: int = Field(..., description="Количество мест", gt=0, le=20)
    location: str = Field(..., description="Расположение стола", min_length=1, max_length=100)

    @validator('name')
    def name_must_not_contain_special_chars(cls, v):
        if not v.replace(' ', '').isalnum():
            raise ValueError('Название может содержать только буквы, цифры и пробелы')
        return v

class TableCreate(TableBase):
    pass

class TableUpdate(BaseModel):
    name: Optional[str] = Field(None, description="Название стола", min_length=1, max_length=100)
    seats: Optional[int] = Field(None, description="Количество мест", gt=0, le=20)
    location: Optional[str] = Field(None, description="Расположение стола", min_length=1, max_length=100)

class TableOut(TableBase):
    id: int = Field(..., description="ID стола")

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "id": 1,
                "name": "Стол у окна",
                "seats": 4,
                "location": "Зал 1"
            }
        }
