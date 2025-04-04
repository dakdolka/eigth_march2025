
from sqlalchemy import text, insert, select, func, cast, Integer, and_, update
from data.database import async_engine, async_session_factory
# from db.models import metadata_obj
from sqlalchemy.orm import aliased
from data.database import Base
from sqlalchemy.orm import joinedload, selectinload, contains_eager
from data.models import Man, Woman

class Orm:
    @staticmethod
    async def create_all():
        async with async_engine.begin() as conn:
            async_engine.echo = False
            # await conn.run_sync(Base.metadata.drop_all)
            # print('tables dropped')
            await conn.run_sync(Base.metadata.create_all)
            print('tables created')
            async_engine.echo = True
            
    @staticmethod
    async def enable_wal():
        async with async_engine.connect() as connection:
            await connection.execute(text('PRAGMA journal_mode = WAL;'))
        
    @staticmethod
    async def add_woman_to_test():
        async with async_session_factory() as session:
            await session.execute(insert(Woman).values(tg_id=123, description='test', name='test', surname='test'))
            await session.commit()
            
    