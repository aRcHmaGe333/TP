import argparse
from sqlmodel import SQLModel, Session, create_engine, select
ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from database import _run_lightweight_migrations  # noqa: E402
from models import AuditEvent, Comment, Idea, MergeRecord, User, Vote  # noqa: E402
MODELS = [User, Idea, Comment, Vote, MergeRecord, AuditEvent]
def connect_args_for(url: str) -> dict:
    return {"check_same_thread": False} if url.startswith("sqlite") else {}
def main() -> None:
    parser = argparse.ArgumentParser(
        description="One-time migration utility from SQLite to PostgreSQL."
    parser.add_argument(
        "--source",
        default="sqlite:///./platform.db",
        help="Source SQLAlchemy URL (default: sqlite:///./platform.db)",
        "--target",
        required=True,
        help="Target PostgreSQL SQLAlchemy URL",
    args = parser.parse_args()
    source_engine = create_engine(args.source, connect_args=connect_args_for(args.source))
    target_engine = create_engine(args.target, connect_args=connect_args_for(args.target))
    SQLModel.metadata.create_all(source_engine)
    _run_lightweight_migrations(source_engine)
    SQLModel.metadata.create_all(target_engine)
    _run_lightweight_migrations(target_engine)
    with Session(target_engine) as target_session:
        for model in MODELS:
            existing = target_session.exec(select(model).limit(1)).first()
            if existing:
                raise RuntimeError(
                    f"Target database is not empty for model {model.__name__}. "
                    "Use an empty target database for this one-time migration."
                )
    with Session(source_engine) as source_session, Session(target_engine) as target_session:
            rows = source_session.exec(select(model)).all()
            for row in rows:
                target_session.add(model(**row.dict()))
            target_session.commit()
            print(f"Migrated {len(rows)} row(s) for {model.__name__}")
    print("Migration completed successfully.")
if __name__ == "__main__":
    main()
