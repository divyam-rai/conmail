from app.repository.models.base import Base
from sqlalchemy.orm import Mapped, mapped_column
from uuid import uuid4, UUID

class Organization(Base):
    __tablename__ = "organizations"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    name: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column()