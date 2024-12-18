from .models import async_session
from .models import User
from sqlalchemy import select, update, delete


async def set_new_user(tg_id, name, city, prefer_prod, prefer_stor):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        if not user:
            session.add(User(tg_id=tg_id, name=name, city=city, prefer_prod=prefer_prod, prefer_stor=prefer_stor))
            await session.commit()
        else:
            user.name = name
            user.city = city
            user.prefer_prod = prefer_prod
            user.prefer_stor = prefer_stor

            await session.commit()


async def get_user(tg_id: int):
    async with async_session() as session:
        #user = await session.scalar(select(User).where(User.tg_id == tg_id))
        return await session.scalar(select(User).where(User.tg_id == tg_id))
