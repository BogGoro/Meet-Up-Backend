from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from . import models

async def get_event(db: AsyncSession, event_id: int):
    result = await db.execute(select(models.Event).filter(models.Event.id == event_id))
    return result.scalar_one_or_none()

async def get_all_events(db: AsyncSession):
    result = await db.execute(select(models.Event))
    return result.scalars().all()

async def create_event(db: AsyncSession, title: str, description: str, address: str, date, time, authorID: int):
    new_event = models.Event(
        title=title,
        description=description,
        address=address,
        date=date,
        time=time,
        authorID=authorID
    )
    db.add(new_event)
    await db.commit()
    await db.refresh(new_event)
    return new_event

async def delete_event(db: AsyncSession, event_id: int):
    event = await get_event(db, event_id)
    if event:
        await db.delete(event)
        await db.commit()
