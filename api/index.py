from fastapi import FastAPI, Depends, HTTPException
from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import AsyncSession
from .database import SessionLocal, engine, init_db
from . import crud
from pydantic import BaseModel
from datetime import date, time, datetime
from typing import List

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield
    print('End')

app = FastAPI(lifespan=lifespan)

async def get_db():
    async with SessionLocal() as session:
        yield session

class EventCreate(BaseModel):
    title: str
    description: str
    address: str
    date: date
    time: time
    authorID: int

class EventRead(BaseModel):
    id: int
    title: str
    description: str
    address: str
    date: date
    time: time
    authorID: int
    created_at: datetime

@app.post("/api/events/", response_model=EventCreate)
async def create_event(event: EventCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create_event(
        db=db,
        title=event.title,
        description=event.description,
        address=event.address,
        date=event.date,
        time=event.time,
        authorID=event.authorID
    )

@app.get("/api/events/", response_model=List[EventRead])
async def get_all_events(db: AsyncSession = Depends(get_db)):
    events = await crud.get_all_events(db)
    return events

@app.get("/api/events/{event_id}", response_model=EventRead)
async def get_event_by_id(event_id: int, db: AsyncSession = Depends(get_db)):
    event = await crud.get_event(db, event_id)
    if event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    return event

@app.delete("/api/events/{event_id}", response_model=dict)
async def delete_event_by_id(event_id: int, db: AsyncSession = Depends(get_db)):
    deleted = await crud.delete_event(db, event_id)
    if deleted == 0:
        raise HTTPException(status_code=404, detail="Event not found")
    return {"message": "Event deleted successfully"}
