import os
import sys
import glob

# Ensure backend root is in python path
backend_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if backend_root not in sys.path:
    sys.path.insert(0, backend_root)

from sqlalchemy import text
from app.core.database import engine
from app.core.logger_config import logger

def run_migrations():
    migrations_dir = os.path.join(backend_root, "..", "supabase", "migrations")
    migration_files = sorted(glob.glob(os.path.join(migrations_dir, "*.sql")))

    if not migration_files:
        raise FileNotFoundError(f"No SQL migration files found in: {migrations_dir}")

    for migration_file in migration_files:
        filename = os.path.basename(migration_file)
        logger.info(f"Executing Supabase migration: {filename}")
        with open(migration_file, "r", encoding="utf-8") as f:
            sql_script = f.read()

        with engine.connect() as conn:
            with conn.begin():
                conn.execute(text(sql_script))
        logger.info(f"Migration {filename} completed successfully!")

if __name__ == "__main__":
    run_migrations()
