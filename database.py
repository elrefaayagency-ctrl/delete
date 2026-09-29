import sqlite3
from datetime import datetime

from config import DATABASE_FILE


def connection():
    return sqlite3.connect(
        DATABASE_FILE
    )


def init_db():

    db = connection()

    db.execute("""
        CREATE TABLE IF NOT EXISTS job (
            id INTEGER PRIMARY KEY,
            status TEXT NOT NULL,
            completed INTEGER NOT NULL DEFAULT 0,
            failed INTEGER NOT NULL DEFAULT 0,
            last_error TEXT,
            updated_at TEXT NOT NULL
        )
    """)

    db.execute("""
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            level TEXT NOT NULL,
            message TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)

    row = db.execute(
        "SELECT id FROM job WHERE id = 1"
    ).fetchone()

    if row is None:

        db.execute(
            """
            INSERT INTO job
            (id, status, completed, failed, updated_at)
            VALUES (1, 'IDLE', 0, 0, ?)
            """,
            (datetime.utcnow().isoformat(),)
        )

    db.commit()
    db.close()


def get_status():

    db = connection()

    row = db.execute(
        """
        SELECT
            status,
            completed,
            failed,
            last_error,
            updated_at
        FROM job
        WHERE id = 1
        """
    ).fetchone()

    db.close()

    return {
        "status": row[0],
        "completed": row[1],
        "failed": row[2],
        "last_error": row[3],
        "updated_at": row[4]
    }


def set_status(
    status,
    error=None
):

    db = connection()

    db.execute(
        """
        UPDATE job
        SET status = ?,
            last_error = ?,
            updated_at = ?
        WHERE id = 1
        """,
        (
            status,
            error,
            datetime.utcnow().isoformat()
        )
    )

    db.commit()
    db.close()


def increment_completed():

    db = connection()

    db.execute(
        """
        UPDATE job
        SET completed = completed + 1,
            updated_at = ?
        WHERE id = 1
        """,
        (datetime.utcnow().isoformat(),)
    )

    db.commit()
    db.close()


def increment_failed(error):

    db = connection()

    db.execute(
        """
        UPDATE job
        SET failed = failed + 1,
            last_error = ?,
            updated_at = ?
        WHERE id = 1
        """,
        (
            error,
            datetime.utcnow().isoformat()
        )
    )

    db.commit()
    db.close()


def add_log(
    level,
    message
):

    db = connection()

    db.execute(
        """
        INSERT INTO logs
        (level, message, created_at)
        VALUES (?, ?, ?)
        """,
        (
            level,
            message,
            datetime.utcnow().isoformat()
        )
    )

    db.commit()
    db.close()


def recent_logs(limit=10):

    db = connection()

    rows = db.execute(
        """
        SELECT level, message, created_at
        FROM logs
        ORDER BY id DESC
        LIMIT ?
        """,
        (limit,)
    ).fetchall()

    db.close()

    return rows
