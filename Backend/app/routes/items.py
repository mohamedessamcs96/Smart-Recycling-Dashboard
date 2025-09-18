from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
import os, uuid, aiofiles
from sqlalchemy.orm import Session
from ..db import SessionLocal
from .. import crud, schemas
from ..config import settings
from ..ml.model import predict_image

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/upload", response_model=schemas.ItemRead)
async def upload_image(file: UploadFile = File(...), db: Session = Depends(get_db)):
    ext = os.path.splitext(file.filename)[1]
    fname = f"{uuid.uuid4().hex}{ext}"
    fpath = os.path.join(settings.UPLOAD_DIR, fname)
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)

    async with aiofiles.open(fpath, "wb") as out:
        content = await file.read()
        await out.write(content)

    result = predict_image(fpath)
    decision = "Accept" if result["confidence"] >= 0.8 else "Reject"

    item = schemas.ItemCreate(
        image_path=f"/uploads/{fname}",
        type=result["type"],
        brand=result["brand"],
        confidence=result["confidence"],
        decision=decision,
        reasoning=result["reasoning"],
    )
    return crud.create_item(db, item)

@router.get("/items", response_model=list[schemas.ItemRead])
def list_items(
    type: str = None,
    brand: str = None,
    decision: str = None,
    db: Session = Depends(get_db),
):
    filters = {"type": type, "brand": brand, "decision": decision}
    return crud.get_items(db, filters=filters)

@router.get("/items/{item_id}", response_model=schemas.ItemRead)
def get_item(item_id: int, db: Session = Depends(get_db)):
    item = crud.get_item(db, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item
