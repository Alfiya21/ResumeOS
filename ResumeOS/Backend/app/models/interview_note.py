from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from app.database.base import BaseModel

if TYPE_CHECKING:
    from app.models.application_workspace import (
        ApplicationWorkspace,
    )


class InterviewNote(BaseModel):
    """
    Stores interview history and notes
    for a particular job application.
    """

    __tablename__ = "interview_notes"

    __table_args__ = (
        Index(
            "ix_interview_workspace",
            "workspace_id",
        ),
    )

    # =====================================================
    # Relationship
    # =====================================================

    workspace_id: Mapped[int] = mapped_column(
        ForeignKey(
            "application_workspaces.id",
            ondelete="CASCADE",
        ),
        nullable=False,
    )

    workspace: Mapped["ApplicationWorkspace"] = relationship(
        "ApplicationWorkspace",
        back_populates="interview_notes",
    )

    # =====================================================
    # Interview Details
    # =====================================================

    round_number: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    round_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    interview_type: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    interviewer_name: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    interviewer_email: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    scheduled_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    duration_minutes: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    meeting_link: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    location: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    # =====================================================
    # Interview Content
    # =====================================================

    questions_asked: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    answers_given: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    feedback: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    strengths: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    weaknesses: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    # =====================================================
    # Evaluation
    # =====================================================

    rating: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    result: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
    )
    # Pending
    # Selected
    # Rejected
    # Hold
    # Next Round

    next_round: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    # =====================================================
    # Status
    # =====================================================

    completed: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    # =====================================================
    # Helper Methods
    # =====================================================

    def mark_completed(self) -> None:
        self.completed = True

    def update_rating(self, rating: int) -> None:
        self.rating = rating

    def __repr__(self) -> str:
        return (
            f"<InterviewNote("
            f"id={self.id}, "
            f"round={self.round_number}, "
            f"workspace_id={self.workspace_id}"
            f")>"
        )