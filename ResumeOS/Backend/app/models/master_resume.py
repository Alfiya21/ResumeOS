from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import (
    Boolean,
    ForeignKey,
    Index,
    Integer,
    JSON,
    String,
    Text,
)

from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import BaseModel

if TYPE_CHECKING:
    from app.models.generated_resume import GeneratedResume
    from app.models.user import User


class MasterResume(BaseModel):
    """
    User's master resume.

    This resume is never tailored to a specific company.

    Every generated resume is derived from one Master Resume.
    """

    __tablename__ = "master_resumes"

    __table_args__ = (
        Index(
            "ix_master_resume_user",
            "user_id",
        ),
    )

    # -----------------------------------------------------
    # Owner
    # -----------------------------------------------------

    user_id: Mapped[int] = mapped_column(
        ForeignKey(
            "users.id",
            ondelete="CASCADE",
        ),
        nullable=False,
    )

    # -----------------------------------------------------
    # File Metadata
    # -----------------------------------------------------

    original_filename: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    stored_filename: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    storage_path: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
    )

    mime_type: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    file_size: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    # -----------------------------------------------------
    # Parsed Content
    # -----------------------------------------------------

    resume_text: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    parsed_json: Mapped[dict] = mapped_column(
        JSON,
        nullable=False,
    )

    # -----------------------------------------------------
    # Versioning
    # -----------------------------------------------------

    version: Mapped[int] = mapped_column(
        default=1,
        nullable=False,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    is_deleted: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    # -----------------------------------------------------
    # Relationships
    # -----------------------------------------------------

    user: Mapped["User"] = relationship(
        back_populates="master_resumes",
    )

    generated_resumes: Mapped[list["GeneratedResume"]] = relationship(
        back_populates="master_resume",
        cascade="all, delete-orphan",
        lazy="selectin",
    )

    # -----------------------------------------------------
    # Helpers
    # -----------------------------------------------------

    def activate(self) -> None:
        self.is_active = True

    def deactivate(self) -> None:
        self.is_active = False

    def soft_delete(self) -> None:
        self.is_deleted = True

    def restore(self) -> None:
        self.is_deleted = False

    def __repr__(self) -> str:
        return (
            f"MasterResume("
            f"id={self.id}, "
            f"user_id={self.user_id}, "
            f"version={self.version}"
            f")"
        )