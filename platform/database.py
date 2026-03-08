from functools import lru_cache
from typing import Iterator
from sqlalchemy import inspect, text
from sqlmodel import Session, SQLModel, create_engine
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
    if "idea" in inspector.get_table_names():
        idea_cols = {col["name"] for col in inspector.get_columns("idea")}
        if "status" not in idea_cols:
                _exec_sql(engine, "ALTER TABLE idea ADD COLUMN status VARCHAR NOT NULL DEFAULT 'submitted'")
        if "status_updated_at" not in idea_cols:
            _exec_sql(engine, "ALTER TABLE idea ADD COLUMN status_updated_at TIMESTAMP")
        if "status_updated_by" not in idea_cols:
            _exec_sql(engine, "ALTER TABLE idea ADD COLUMN status_updated_by INTEGER")
def _exec_sql(engine, statement: str) -> None:
    with engine.begin() as connection:
        connection.execute(text(statement))
