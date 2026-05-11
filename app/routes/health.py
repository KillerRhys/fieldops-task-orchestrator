from flask import Blueprint, jsonify
from sqlalchemy import text

from app.extensions import db

health_bp = Blueprint("health", __name__)


@health_bp.get("/health")
def health_check():
    database_status = "unknown"

    try:
        db.session.execute(text("SELECT 1"))
        database_status = "connected"
    except Exception:
        database_status = "disconnected"

    return jsonify(
        {
            "status": "ok",
            "service": "fieldops-task-orchestrator",
            "database": database_status,
        }
    )
