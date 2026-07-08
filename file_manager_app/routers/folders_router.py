from fastapi import APIRouter, Depends, HTTPException
from typing import List, Optional
from sqlalchemy.orm import Session
from db.folder import Folder as DBFolder
from api_models.folder import Folder, FolderCreate, FolderUpdate
from db.database import get_db

router = APIRouter(prefix="/folders", tags=["folders"])


@router.post("/", response_model=Folder)
def create_folder(folder: FolderCreate, db: Session = Depends(get_db)):
    existing_folder = (
        db.query(DBFolder)
        .filter(DBFolder.name == folder.name, DBFolder.parent_id == folder.parent_id)
        .first()
    )
    if existing_folder:
        raise HTTPException(status_code=400, detail="Folder already exists")
    if folder.parent_id:
        parent_folder = db.query(DBFolder).get(folder.parent_id)
        if not parent_folder:
            raise HTTPException(status_code=404, detail="Parent folder not found")
    if not folder.parent_id:
        folder.parent_id = 0
    db_folder = DBFolder(**folder.model_dump())
    db.add(db_folder)
    db.commit()
    db.refresh(db_folder)
    return db_folder


@router.get("/", response_model=List[Folder])
def list_folders(parent_id: Optional[int] = None, db: Session = Depends(get_db)):
    query = db.query(DBFolder)
    if parent_id is not None:
        query = query.filter(DBFolder.parent_id == parent_id)
    return query.all()


@router.get("/{folder_id}", response_model=Folder)
def get_folder(folder_id: int, db: Session = Depends(get_db)):
    folder = db.query(DBFolder).get(folder_id)
    if not folder:
        raise HTTPException(status_code=404, detail="Folder not found")
    return folder


@router.put("/{folder_id}", response_model=Folder)
def update_folder(
    folder_id: int, folder_update: FolderUpdate, db: Session = Depends(get_db)
):
    folder = db.query(DBFolder).get(folder_id)
    if not folder:
        raise HTTPException(status_code=404, detail="Folder not found")

    for field, value in folder_update.dict(exclude_unset=True).items():
        setattr(folder, field, value)

    db.commit()
    db.refresh(folder)
    return folder


@router.delete("/{folder_id}", response_model=Folder)
def delete_folder(folder_id: int, db: Session = Depends(get_db)):
    folder = db.query(DBFolder).get(folder_id)
    if not folder:
        raise HTTPException(status_code=404, detail="Folder not found")

    db.delete(folder)
    db.commit()
    return folder
