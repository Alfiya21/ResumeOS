from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import (
    Boolean,
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
    from app.models.application_workspace import ApplicationWorkspace


class RecruiterMessage(BaseModel):
    """
    Stores AI-generated recruiter communication templates.
    """

    __tablename__ = "recruiter_messages"

    __table_args__ = (
        Index(
            "ix_recruiter_message_workspace",
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
        back_populates="recruiter_messages",
    )

    # =====================================================
    # Metadata
    # =====================================================

    version: Mapped[int] = mapped_column(
        Integer,
        default=1,
        nullable=False,
    )

    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    message_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )
    # Examples:
    # linkedin_connection
    # cold_email
    # follow_up
    # thank_you
    # referral_request

    subject: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    # =====================================================
    # Content
    # =====================================================

    content: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    # =====================================================
    # Status
    # =====================================================

    is_default: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    is_deleted: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    # =====================================================
    # Helper Methods
    # =====================================================

    def mark_default(self) -> None:
        self.is_default = True

    def remove_default(self) -> None:
        self.is_default = False

    def soft_delete(self) -> None:
        self.is_deleted = True

    def restore(self) -> None:
        self.is_deleted = False

    def __repr__(self) -> str:
        return (
            f"<RecruiterMessage("
            f"id={self.id}, "
            f"type='{self.message_type}', "
            f"workspace_id={self.workspace_id}"
            f")>"
        )