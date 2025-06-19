from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool, create_engine
from alembic import context

from app.core.database import Base
import app.models.dish
import app.models.order

config = context.config
fileConfig(config.config_file_name)
target_metadata = Base.metadata


def get_url():
    return config.get_main_option("sqlalchemy.url")


def run_migrations_offline():
    url = get_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection):
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    connectable = create_engine(
        get_url(),
        poolclass=pool.NullPool,
        future=True,
    )

    with connectable.connect() as connection:
        do_run_migrations(connection)


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
