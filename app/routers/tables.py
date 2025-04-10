from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.table import Table
from app.schemas.table import TableCreate, TableOut, TableUpdate
from app.schemas.error import ErrorResponse

router = APIRouter(
    prefix="/tables",
    tags=["Tables"],
    responses={
        404: {"model": ErrorResponse, "description": "Стол не найден"},
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
    response_model=list[TableOut],
    summary="Получить список всех столов",
    description="Возвращает список всех доступных столов в ресторане"
)
def get_tables(db: Session = Depends(get_db)):
    return db.query(Table).all()

@router.get(
    "/{table_id}",
    response_model=TableOut,
    summary="Получить информацию о столе",
    description="Возвращает подробную информацию о конкретном столе"
)
def get_table(table_id: int, db: Session = Depends(get_db)):
    table = db.query(Table).filter(Table.id == table_id).first()
    if not table:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Стол с ID {table_id} не найден"
        )
    return table

@router.post(
    "/",
    response_model=TableOut,
    status_code=status.HTTP_201_CREATED,
    summary="Создать новый стол",
    description="Создает новый стол в ресторане"
)
def create_table(table: TableCreate, db: Session = Depends(get_db)):
    existing_table = db.query(Table).filter(Table.name == table.name).first()
    if existing_table:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Стол с названием '{table.name}' уже существует"
        )
    
    new_table = Table(**table.dict())
    db.add(new_table)
    db.commit()
    db.refresh(new_table)
    return new_table

@router.put(
    "/{table_id}",
    response_model=TableOut,
    summary="Обновить информацию о столе",
    description="Обновляет информацию о существующем столе"
)
def update_table(table_id: int, table_update: TableUpdate, db: Session = Depends(get_db)):
    db_table = db.query(Table).filter(Table.id == table_id).first()
    if not db_table:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Стол с ID {table_id} не найден"
        )
    
    update_data = table_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_table, field, value)
    
    db.commit()
    db.refresh(db_table)
    return db_table

@router.delete(
    "/{table_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удалить стол",
    description="Удаляет стол из системы"
)
def delete_table(table_id: int, db: Session = Depends(get_db)):
    table = db.query(Table).filter(Table.id == table_id).first()
    if not table:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Стол с ID {table_id} не найден"
        )
    
    db.delete(table)
    db.commit()
