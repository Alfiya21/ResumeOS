from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import (
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
    Boolean,
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from app.database.base import BaseModel

if TYPE_CHECKING:
    from app.models.application_workspace import ApplicationWorkspace


class CoverLetter(BaseModel):
    """
    AI Generated Cover Letter.

    Multiple versions can exist for
    a single Application Workspace.
    """

    __tablename__ = "cover_letters"

    __table_args__ = (
        Index(
            "ix_cover_letter_workspace",
            "workspace_id",
        ),
    )

    # =====================================================
    # Relationships
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
        back_populates="cover_letters",
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

    company_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    role_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
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
            f"<CoverLetter("
            f"id={self.id}, "
            f"workspace_id={self.workspace_id}, "
            f"version={self.version}"
            f")>"
        )