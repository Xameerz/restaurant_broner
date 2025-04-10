from sqlalchemy import text
from sqlalchemy.orm import Session
from app.models.reservation import Reservation
from datetime import timedelta

def is_table_available(
    db: Session,
    table_id: int,
    start_time,
    duration_minutes: int,
    exclude_reservation_id: int = None
) -> bool:

    end_time = start_time + timedelta(minutes=duration_minutes)
    
    
    query = db.query(Reservation).filter(
        Reservation.table_id == table_id,
        Reservation.reservation_time < end_time,
        text("(reservation_time + (interval '1 minute' * duration_minutes)) > :start_time")
    ).params(start_time=start_time)
    
    if exclude_reservation_id:
        query = query.filter(Reservation.id != exclude_reservation_id)
    
    conflicts = query.all()
    return len(conflicts) == 0
