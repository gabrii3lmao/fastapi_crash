from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.engine import URL
from fast_zero.settings import Settings

url = URL.create(
    drivername="postgresql+psycopg",
    username=Settings().DB_USER,
    password=Settings().DB_PASSWORD,
    host=Settings().DB_HOST,
    port=Settings().DB_PORT,
    database=Settings().DB_NAME
)

engine = create_async_engine(url)


async def get_session():
    async with AsyncSession(engine, expire_on_commit=False) as session:
        yield session
