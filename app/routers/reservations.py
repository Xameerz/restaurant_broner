from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.reservation import Reservation
from app.schemas.reservation import ReservationCreate, ReservationOut, ReservationUpdate
from app.schemas.error import ErrorResponse
from app.services.reservation_service import is_table_available

router = APIRouter(
    prefix="/reservations",
    tags=["Reservations"],
    responses={
        404: {"model": ErrorResponse, "description": "Бронирование не найдено"},
        400: {"model": ErrorResponse, "description": "Неверные данные"},
        409: {"model": ErrorResponse, "description": "Конфликт данных"}
    }
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get(
    "/",
    response_model=list[ReservationOut],
    summary="Получить список всех бронирований",
    description="Возвращает список всех бронирований в ресторане"
)
def get_reservations(db: Session = Depends(get_db)):
    return db.query(Reservation).all()

@router.get(
    "/{reservation_id}",
    response_model=ReservationOut,
    summary="Получить информацию о бронировании",
    description="Возвращает подробную информацию о конкретном бронировании"
)
def get_reservation(reservation_id: int, db: Session = Depends(get_db)):
    reservation = db.query(Reservation).filter(Reservation.id == reservation_id).first()
    if not reservation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Бронирование с ID {reservation_id} не найдено"
        )
    return reservation

@router.post(
    "/",
    response_model=ReservationOut,
    status_code=status.HTTP_201_CREATED,
    summary="Создать новое бронирование",
    description="Создает новое бронирование стола"
)
def create_reservation(reservation: ReservationCreate, db: Session = Depends(get_db)):
    if not is_table_available(db, reservation.table_id, reservation.reservation_time, reservation.duration_minutes):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Стол уже забронирован на указанное время"
        )
    
    new_res = Reservation(**reservation.dict())
    db.add(new_res)
    db.commit()
    db.refresh(new_res)
    return new_res

@router.put(
    "/{reservation_id}",
    response_model=ReservationOut,
    summary="Обновить информацию о бронировании",
    description="Обновляет информацию о существующем бронировании"
)
def update_reservation(reservation_id: int, reservation_update: ReservationUpdate, db: Session = Depends(get_db)):
    db_reservation = db.query(Reservation).filter(Reservation.id == reservation_id).first()
    if not db_reservation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Бронирование с ID {reservation_id} не найдено"
        )
    
    update_data = reservation_update.dict(exclude_unset=True)
    if 'table_id' in update_data or 'reservation_time' in update_data or 'duration_minutes' in update_data:
        table_id = update_data.get('table_id', db_reservation.table_id)
        reservation_time = update_data.get('reservation_time', db_reservation.reservation_time)
        duration_minutes = update_data.get('duration_minutes', db_reservation.duration_minutes)
        
        if not is_table_available(db, table_id, reservation_time, duration_minutes, exclude_reservation_id=reservation_id):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Стол уже забронирован на указанное время"
            )
    
    for field, value in update_data.items():
        setattr(db_reservation, field, value)
    
    db.commit()
    db.refresh(db_reservation)
    return db_reservation

@router.delete(
    "/{reservation_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удалить бронирование",
    description="Удаляет бронирование из системы"
)
def delete_reservation(reservation_id: int, db: Session = Depends(get_db)):
    reservation = db.query(Reservation).filter(Reservation.id == reservation_id).first()
    if not reservation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Бронирование с ID {reservation_id} не найдено"
        )
    
    db.delete(reservation)
    db.commit()
