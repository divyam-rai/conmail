from app.repository.models.base import Base
from sqlalchemy.orm import Mapped, mapped_column
from uuid import UUID, uuid4
from datetime import datetime, timezone

class Contact(Base):
    __tablename__ = "contacts"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    email: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(nullable=False, default=datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(nullable=False, default=datetime.now(timezone.utc))
    deleted_at: Mapped[datetime] = mapped_column(nullable=True)
    name_first: Mapped[str] = mapped_column()
    name_middle: Mapped[str] = mapped_column()
    name_last: Mapped[str] = mapped_column()
    address_street: Mapped[str] = mapped_column()
    address_city: Mapped[str] = mapped_column()
    address_country: Mapped[str] = mapped_column()
    address_zip: Mapped[int] = mapped_column()
    organization_id: Mapped[UUID] = mapped_column()