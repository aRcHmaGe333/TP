from functools import lru_cache
from typing import Iterator

from sqlalchemy import inspect, text
from sqlmodel import Session, SQLModel, create_engine

try:
    from . import config
except ImportError:  # pragma: no cover - local-module execution fallback
    import config


def _build_engine():
    database_url = config.get_database_url()
    if not database_url:
        # Runtime config validation handles non-dev enforcement.
        database_url = "sqlite:///./platform.db"
    connect_args = {"check_same_thread": False} if database_url.startswith("sqlite") else {}
    return create_engine(database_url, connect_args=connect_args)


def get_engine():
    return _build_engine()


@lru_cache
def get_cached_engine():
    return _build_engine()


def init_db() -> None:
    engine = get_cached_engine()
    SQLModel.metadata.create_all(engine)
    _run_lightweight_migrations(engine)


def get_session() -> Iterator[Session]:
    with Session(get_cached_engine()) as session:
        yield session


def _run_lightweight_migrations(engine) -> None:
    inspector = inspect(engine)
    dialect = engine.dialect.name

    if "user" in inspector.get_table_names():
        user_cols = {col["name"] for col in inspector.get_columns("user")}
        if "is_admin" not in user_cols:
            if dialect == "postgresql":
                _exec_sql(engine, 'ALTER TABLE "user" ADD COLUMN is_admin BOOLEAN NOT NULL DEFAULT FALSE')
            else:
                _exec_sql(engine, "ALTER TABLE user ADD COLUMN is_admin BOOLEAN NOT NULL DEFAULT 0")
        if "legal_name" not in user_cols:
            _exec_sql(engine, 'ALTER TABLE "user" ADD COLUMN legal_name VARCHAR')
        if "identity_provider" not in user_cols:
            _exec_sql(engine, 'ALTER TABLE "user" ADD COLUMN identity_provider VARCHAR')
        if "identity_subject_key" not in user_cols:
            _exec_sql(engine, 'ALTER TABLE "user" ADD COLUMN identity_subject_key VARCHAR')
        if "identity_country_code" not in user_cols:
            _exec_sql(engine, 'ALTER TABLE "user" ADD COLUMN identity_country_code VARCHAR')
        if "identity_verified_at" not in user_cols:
            _exec_sql(engine, 'ALTER TABLE "user" ADD COLUMN identity_verified_at TIMESTAMP')

        indexes = {index["name"] for index in inspector.get_indexes("user")}
        if "ix_user_identity_provider_subject" not in indexes:
            _exec_sql(
                engine,
                'CREATE UNIQUE INDEX IF NOT EXISTS ix_user_identity_provider_subject ON "user" (identity_provider, identity_subject_key)',
            )

    if "idea" in inspector.get_table_names():
        idea_cols = {col["name"] for col in inspector.get_columns("idea")}
        if "status" not in idea_cols:
            if dialect == "postgresql":
                _exec_sql(engine, "ALTER TABLE idea ADD COLUMN status VARCHAR NOT NULL DEFAULT 'submitted'")
            else:
                _exec_sql(engine, "ALTER TABLE idea ADD COLUMN status VARCHAR NOT NULL DEFAULT 'submitted'")
        if "status_updated_at" not in idea_cols:
            _exec_sql(engine, "ALTER TABLE idea ADD COLUMN status_updated_at TIMESTAMP")
        if "status_updated_by" not in idea_cols:
            _exec_sql(engine, "ALTER TABLE idea ADD COLUMN status_updated_by INTEGER")


def _exec_sql(engine, statement: str) -> None:
    with engine.begin() as connection:
        connection.execute(text(statement))
