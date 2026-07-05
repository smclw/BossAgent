from __future__ import annotations

import json
import sqlite3
from dataclasses import asdict
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from .config import DATA_DIR
from .orchestrator import AgentRun


DB_PATH = DATA_DIR / "bossagent.db"


def init_db() -> None:
    DATA_DIR.mkdir(exist_ok=True)
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                created_at TEXT NOT NULL,
                task_type TEXT NOT NULL,
                user_goal TEXT NOT NULL,
                uploaded_files TEXT NOT NULL,
                agent_outputs TEXT NOT NULL,
                final_report TEXT NOT NULL
            )
            """
        )
        conn.commit()


def save_task(
    task_type: str,
    user_goal: str,
    uploaded_files: List[str],
    agent_outputs: List[AgentRun],
    final_report: str,
) -> int:
    init_db()
    payload = [asdict(item) for item in agent_outputs]
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.execute(
            """
            INSERT INTO tasks (created_at, task_type, user_goal, uploaded_files, agent_outputs, final_report)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                datetime.now().isoformat(timespec="seconds"),
                task_type,
                user_goal,
                json.dumps(uploaded_files, ensure_ascii=False),
                json.dumps(payload, ensure_ascii=False),
                final_report,
            ),
        )
        conn.commit()
        return int(cursor.lastrowid)


def list_tasks() -> List[Dict[str, Any]]:
    init_db()
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        rows = conn.execute(
            "SELECT id, created_at, task_type, user_goal, uploaded_files FROM tasks ORDER BY id DESC"
        ).fetchall()
    return [dict(row) for row in rows]


def get_task(task_id: int) -> Optional[Dict[str, Any]]:
    init_db()
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        row = conn.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
    if row is None:
        return None
    task = dict(row)
    task["uploaded_files"] = json.loads(task["uploaded_files"])
    task["agent_outputs"] = json.loads(task["agent_outputs"])
    return task
