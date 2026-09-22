from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import (
    DateTime,
    ForeignKey,
    Float,
    Index,
    Integer,
    JSON,
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
    from app.models.application_workspace import ApplicationWorkspace


class AIGeneration(BaseModel):
    """
    Stores metadata for every AI generation
    performed within ResumeOS.
    """

    __tablename__ = "ai_generations"

    __table_args__ = (
        Index(
            "ix_ai_generation_workspace",
            "workspace_id",
        ),
        Index(
            "ix_ai_generation_model",
            "model_name",
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
        back_populates="ai_generations",
    )

    # =====================================================
    # Request Information
    # =====================================================

    task_type: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )
    # resume_generation
    # ats_analysis
    # match_analysis
    # cover_letter
    # recruiter_email

    provider: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="OpenAI",
    )

    model_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    temperature: Mapped[float] = mapped_column(
        Float,
        default=0.3,
    )

    # =====================================================
    # Prompt Data
    # =====================================================

    system_prompt: Mapped[str | None] = mapped_column(
        Text,
    )

    user_prompt: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    response_text: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    # =====================================================
    # Usage Metrics
    # =====================================================

    prompt_tokens: Mapped[int] = mapped_column(
        Integer,
        default=0,
    )

    completion_tokens: Mapped[int] = mapped_column(
        Integer,
        default=0,
    )

    total_tokens: Mapped[int] = mapped_column(
        Integer,
        default=0,
    )

    estimated_cost: Mapped[float] = mapped_column(
        Float,
        default=0.0,
    )

    latency_seconds: Mapped[float | None] = mapped_column(
        Float,
    )

    # =====================================================
    # Execution Status
    # =====================================================

    status: Mapped[str] = mapped_column(
        String(50),
        default="SUCCESS",
    )

    error_message: Mapped[str | None] = mapped_column(
        Text,
    )

    metadata: Mapped[dict] = mapped_column(
        JSON,
        default=dict,
        nullable=False,
    )

    generated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        nullable=False,
    )

    # =====================================================
    # Helper Methods
    # =====================================================

    def total_usage(self) -> int:
        return self.prompt_tokens + self.completion_tokens

    def mark_failed(self, message: str) -> None:
        self.status = "FAILED"
        self.error_message = message

    def __repr__(self) -> str:
        return (
            f"<AIGeneration("
            f"id={self.id}, "
            f"task='{self.task_type}', "
            f"model='{self.model_name}')>"
        ) 