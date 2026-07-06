from fastapi import APIRouter, Depends, HTTPException
from api_models.file import FileCreate, FileUpdate, FileOut
from db.file import File as DBFile
from sqlalchemy.orm import Session
from db.database import get_db

router = APIRouter(prefix="/files", tags=["files"])


@router.get("/", response_model=list[FileOut])
def list_files(name=None, folder_id: int = None, db: Session = Depends(get_db)) -> list[FileOut]:
    query = db.query(DBFile)
    if name:
        query = query.filter(DBFile.name.contains(name))
    if folder_id:
        query = query.filter(DBFile.folder_id == folder_id)
    return query.all()


@router.post("/", response_model=FileOut, status_code=201)
def create_file(file: FileCreate, db: Session = Depends(get_db)) -> FileOut:
    db_file = DBFile(**file.dict())
    db.add(db_file)
    db.commit()
    db.refresh(db_file)
    return FileOut.from_orm(db_file)


@router.get("/{file_id}", response_model=FileOut)
def get_file(file_id: int, db: Session = Depends(get_db)) -> FileOut:
    file = db.query(DBFile).filter(DBFile.id == file_id).first()
    if file is None:
        raise HTTPException(status_code=404, detail="File not found")
    return FileOut.from_orm(file)


@router.put("/{file_id}", response_model=FileOut)
def update_file(file_id: int, file_update: FileUpdate, db: Session = Depends(get_db)) -> FileOut:
    file = db.query(DBFile).filter(DBFile.id == file_id).first()
    if file is None:
        raise HTTPException(status_code=404, detail="File not found")

    update_data = file_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(file, key, value)
    db.commit()
    db.refresh(file)
    return FileOut.from_orm(file)


@router.delete("/{file_id}", status_code=204)
def delete_file(file_id: int, db: Session = Depends(get_db)) -> None:
    file = db.query(DBFile).filter(DBFile.id == file_id).first()
    if file is None:
        raise HTTPException(status_code=404, detail="File not found")
    db.delete(file)
    db.commit()
