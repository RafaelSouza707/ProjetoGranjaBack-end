from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import BigInteger, Identity, String

from helpers.database import db


class Permissao(db.Model):
    __tablename__ = "permissao"

    id: Mapped[int] = mapped_column(
        BigInteger,
        Identity(start=1),
        primary_key=True
    )

    nome: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False
    )

    roles: Mapped[list["RolePermissao"]] = relationship(
        "RolePermissao",
        back_populates="permissao",
        cascade="all, delete-orphan"
    )