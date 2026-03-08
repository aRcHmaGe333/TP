import os
import subprocess
from sqlmodel import Session, create_engine, select
PLATFORM_DIR = ROOT / "platform"
if str(PLATFORM_DIR) not in sys.path:
    sys.path.insert(0, str(PLATFORM_DIR))
import database
from models import User
def test_migrate_script_copies_rows(tmp_path: pathlib.Path, monkeypatch):
    source_db = tmp_path / "source.db"
    target_db = tmp_path / "target.db"
    source_url = _sqlite_url(source_db)
    target_url = _sqlite_url(target_db)
    monkeypatch.setenv("PLATFORM_DATABASE_URL", source_url)
    with Session(database.get_cached_engine()) as session:
        session.add(
            User(
                display_name="source-user",
                email="source@test.local",
                password_hash="h",
                password_salt="s",
                signing_key="c2lnbg==",
                fingerprint="FPR-1234567890abcdef123456",
                is_admin=False,
            )
        )
        session.commit()
    env = os.environ.copy()
    env["PYTHONPATH"] = str(PLATFORM_DIR)
    completed = subprocess.run(
        [
            sys.executable,
            "scripts/migrate_sqlite_to_postgres.py",
            "--source",
            source_url,
            "--target",
            target_url,
        ],
        cwd=str(PLATFORM_DIR),
        env=env,
        capture_output=True,
        text=True,
    )
    assert completed.returncode == 0, completed.stderr
    target_engine = create_engine(target_url, connect_args={"check_same_thread": False})
    with Session(target_engine) as session:
        users = session.exec(select(User)).all()
    assert len(users) == 1
    assert users[0].display_name == "source-user"
