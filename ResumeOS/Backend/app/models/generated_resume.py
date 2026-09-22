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

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from app.database.base import BaseModel

if TYPE_CHECKING:
    from app.models.master_resume import MasterResume
    from app.models.application_workspace import ApplicationWorkspace
    from app.models.ats_report import ATSReport
    from app.models.match_report import MatchReport


class GeneratedResume(BaseModel):
    """
    AI-generated resume tailored for a specific job application.
    """

    __tablename__ = "generated_resumes"

    __table_args__ = (
        Index(
            "ix_generated_resume_workspace",
            "workspace_id",
        ),
        Index(
            "ix_generated_resume_master",
            "master_resume_id",
        ),
    )

    # ======================================================
    # Relationships
    # ======================================================

    workspace_id: Mapped[int] = mapped_column(
        ForeignKey(
            "application_workspaces.id",
            ondelete="CASCADE",
        ),
        nullable=False,
    )

    master_resume_id: Mapped[int] = mapped_column(
        ForeignKey(
            "master_resumes.id",
            ondelete="CASCADE",
        ),
        nullable=False,
    )

    # ======================================================
    # Resume Metadata
    # ======================================================

    version: Mapped[int] = mapped_column(
        Integer,
        default=1,
        nullable=False,
    )

    resume_title: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    original_filename: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    stored_filename: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    pdf_path: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
    )

    docx_path: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    # ======================================================
    # Resume Content
    # ======================================================

    generated_text: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    parsed_json: Mapped[dict] = mapped_column(
        JSON,
        default=dict,
        nullable=False,
    )

    ai_metadata: Mapped[dict] = mapped_column(
        JSON,
        default=dict,
        nullable=False,
    )

    # ======================================================
    # Statistics
    # ======================================================

    ats_score: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    match_score: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    download_count: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )

    is_deleted: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    # ======================================================
    # Relationships
    # ======================================================

    workspace: Mapped["ApplicationWorkspace"] = relationship(
        "ApplicationWorkspace",
        back_populates="generated_resumes",
    )

    master_resume: Mapped["MasterResume"] = relationship(
        "MasterResume",
        back_populates="generated_resumes",
    )

    ats_report: Mapped["ATSReport"] = relationship(
        "ATSReport",
        back_populates="generated_resume",
        uselist=False,
        cascade="all, delete-orphan",
    )

    match_report: Mapped["MatchReport"] = relationship(
        "MatchReport",
        back_populates="generated_resume",
        uselist=False,
        cascade="all, delete-orphan",
    )
    # Helper Methods

    def increment_download(self) -> None:
        self.download_count += 1

    def soft_delete(self) -> None:
        self.is_deleted = True

    def restore(self) -> None:
        self.is_deleted = False

    def __repr__(self) -> str:
        return (
            f"<GeneratedResume("
            f"id={self.id}, "
            f"version={self.version}, "
            f"workspace_id={self.workspace_id}"
            f")>"
        )