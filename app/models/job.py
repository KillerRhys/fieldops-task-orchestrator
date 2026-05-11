import uuid
from datetime import datetime, timezone
from enum import Enum

from sqlalchemy.dialects.postgresql import JSONB, UUID

from app.extensions import db


class JobStatus(str, Enum):
    PENDING = "PENDING"
    PROCESSING = "PROCESSING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


class Job(db.Model):
    __tablename__ = "jobs"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    task_type = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(30), nullable=False, default=JobStatus.PENDING.value)

    idempotency_key = db.Column(db.String(255), nullable=False, unique=True, index=True)

    payload = db.Column(JSONB, nullable=False, default=dict)
    result_metadata = db.Column(JSONB, nullable=False, default=dict)

    celery_task_id = db.Column(db.String(255), nullable=True)

    created_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc)
    )
    updated_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )
    started_at = db.Column(db.DateTime(timezone=True), nullable=True)
    completed_at = db.Column(db.DateTime(timezone=True), nullable=True)

    def to_dict(self):
        return {
            "id": str(self.id),
            "task_type": self.task_type,
            "status": self.status,
            "idempotency_key": self.idempotency_key,
            "payload": self.payload,
            "result_metadata": self.result_metadata,
            "celery_task_id": self.celery_task_id,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
        }
