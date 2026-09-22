from __future__ import annotations

import uuid
from datetime import UTC, datetime
from typing import TYPE_CHECKING

from sqlalchemy import (
    Boolean,
    Enum,
    Index,
    String,
    DateTime,
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from app.core.constants import UserRole
from app.database.base import BaseModel

if TYPE_CHECKING:
    from app.models.master_resume import MasterResume
    from app.models.application_workspace import ApplicationWorkspace


class User(BaseModel):
    """
    ResumeOS User.

    Every user owns:

    • Master Resume(s)
    • Application Workspaces

    Everything else belongs to a Workspace.
    """

    __tablename__ = "users"

    __table_args__ = (
        Index("ix_user_email", "email"),
        Index("ix_user_public_id", "public_id"),
    )

    # =====================================================
    # Public Identifier
    # =====================================================

    public_id: Mapped[str] = mapped_column(
        String(36),
        default=lambda: str(uuid.uuid4()),
        unique=True,
        nullable=False,
    )

    # =====================================================
    # Profile
    # =====================================================

    first_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    last_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
    )

    password_hash: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    phone_number: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True,
    )

    profile_image: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    # =====================================================
    # Account
    # =====================================================

    role: Mapped[UserRole] = mapped_column(
        Enum(UserRole),
        default=UserRole.USER,
        nullable=False,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    is_verified: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    last_login_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    password_changed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    # =====================================================
    # Relationships
    # =====================================================

    master_resumes: Mapped[list["MasterResume"]] = relationship(
        "MasterResume",
        back_populates="user",
        cascade="all, delete-orphan",
        lazy="selectin",
    )

    application_workspaces: Mapped[
        list["ApplicationWorkspace"]
    ] = relationship(
        "ApplicationWorkspace",
        back_populates="user",
        cascade="all, delete-orphan",
        lazy="selectin",
    )

    # =====================================================
    # Helper Properties
    # =====================================================

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    # =====================================================
    # Business Methods
    # =====================================================

    def activate(self) -> None:
        self.is_active = True

    def deactivate(self) -> None:
        self.is_active = False

    def verify(self) -> None:
        self.is_verified = True

    def update_last_login(self) -> None:
        self.last_login_at = datetime.now(UTC)

    def password_changed(self) -> None:
        self.password_changed_at = datetime.now(UTC)

    def __repr__(self) -> str:
        return (
            f"<User("
            f"id={self.id}, "
            f"email='{self.email}', "
            f"role='{self.role.value}'"
            f")>"
        )