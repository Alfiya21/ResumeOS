from __future__ import annotations

import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import (
    DateTime,
    ForeignKey,
    Index,
    String,
    Text,
    func,
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from app.core.constants import ApplicationStatus
from app.database.base import BaseModel

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.job_description import JobDescription
    from app.models.generated_resume import GeneratedResume
    from app.models.cover_letter import CoverLetter
    from app.models.recruiter_message import RecruiterMessage
    from app.models.interview_note import InterviewNote


class ApplicationWorkspace(BaseModel):

    __tablename__ = "application_workspaces"

    __table_args__ = (
        Index("ix_workspace_company", "company_name"),
        Index("ix_workspace_status", "status"),
        Index("ix_workspace_workspace_id", "workspace_id"),
    )

    workspace_id: Mapped[str] = mapped_column(
        String(36),
        unique=True,
        default=lambda: str(uuid.uuid4()),
        nullable=False,
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey(
            "users.id",
            ondelete="CASCADE",
        ),
        nullable=False,
    )

    company_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    role_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    location: Mapped[str | None] = mapped_column(
        String(255),
    )

    employment_type: Mapped[str | None] = mapped_column(
        String(100),
    )

    job_url: Mapped[str | None] = mapped_column(
        Text,
    )

    application_source: Mapped[str | None] = mapped_column(
        String(100),
    )

    priority: Mapped[str] = mapped_column(
        String(20),
        default="Medium",
    )

    status: Mapped[ApplicationStatus] = mapped_column(
        default=ApplicationStatus.DRAFT,
    )

    deadline: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
    )

    notes: Mapped[str | None] = mapped_column(
        Text,
    )

    last_generated_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    # Relationships

    user: Mapped["User"] = relationship(
        back_populates="application_workspaces",
    )

    job_description: Mapped["JobDescription"] = relationship(
        back_populates="workspace",
        uselist=False,
        cascade="all, delete-orphan",
        lazy="selectin",
    )

    generated_resumes: Mapped[list["GeneratedResume"]] = relationship(
        back_populates="workspace",
        cascade="all, delete-orphan",
        lazy="selectin",
    )

    cover_letters: Mapped[list["CoverLetter"]] = relationship(
        back_populates="workspace",
        cascade="all, delete-orphan",
        lazy="selectin",
    )

    recruiter_messages: Mapped[list["RecruiterMessage"]] = relationship(
        back_populates="workspace",
        cascade="all, delete-orphan",
        lazy="selectin",
    )

    interview_notes: Mapped[list["InterviewNote"]] = relationship(
        back_populates="workspace",
        cascade="all, delete-orphan",
        lazy="selectin",
    )