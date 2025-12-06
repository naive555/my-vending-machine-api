import sys
import os
from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool
from alembic import context
from dotenv import load_dotenv

# -------------------------
# Fix Python path
# -------------------------
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, BASE_DIR)

from app.core.database import Base
from app.models import product, product_stock, cash_stock

# -------------------------
# Alembic Config
# -------------------------
config = context.config

# Load .env first
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is not set in .env")

# Inject env var into alembic.ini internal config
config.set_main_option("sqlalchemy.url", DATABASE_URL)

# Logging
if config.config_file_name:
    fileConfig(config.config_file_name)

# Metadata used for autogenerate
target_metadata = Base.metadata


def run_migrations_offline():
    context.configure(
        url=DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    # engine_from_config requires a **dict[str, Any]**, so force it
    section = dict(config.get_section(config.config_ini_section) or {})
    if DATABASE_URL is None:
        raise RuntimeError("DATABASE_URL is none")

    section["sqlalchemy.url"] = DATABASE_URL

    connectable = engine_from_config(
        section,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )
        with context.begin_transaction():
            context.run_migrations()


# -------------------------
# Dispatcher
# -------------------------
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
