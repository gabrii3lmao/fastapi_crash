import asyncio
from logging.config import fileConfig

from alembic import context
from sqlalchemy import pool
from sqlalchemy.engine import URL
from sqlalchemy.ext.asyncio import create_async_engine

from fast_zero.models import table_registry
from fast_zero.settings import Settings

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = table_registry.metadata

# Monta a URL de forma segura com o SQLAlchemy
database_url = URL.create(
    drivername="postgresql+psycopg",
    username=Settings().DB_USER,
    password=Settings().DB_PASSWORD,
    host=Settings().DB_HOST,
    port=Settings().DB_PORT,
    database=Settings().DB_NAME,
)


def do_run_migrations(connection):
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations():
    # Passa o objeto URL direto para a engine, ignorando o configparser do .ini
    connectable = create_async_engine(
        database_url,
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    context.configure(
        url=database_url.render_as_string(hide_password=False),
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()