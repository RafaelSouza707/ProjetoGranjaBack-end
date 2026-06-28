from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import BigInteger, Identity, String
from helpers.database import db 

class Role(db.Model):
    __tablename__ = "role"

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

    cargos: Mapped[list["Cargo"]] = relationship(
        "Cargo",
        back_populates="role"
    )

    permissoes: Mapped[list["RolePermissao"]] = relationship(
        "RolePermissao",
        back_populates="role",
        cascade="all, delete-orphan"
    )