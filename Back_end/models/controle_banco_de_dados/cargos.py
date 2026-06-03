from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import BigInteger, Identity, ForeignKey, String

from helpers.database import db


class Cargo(db.Model):
    __tablename__ = "cargo"

    id: Mapped[int] = mapped_column(
        BigInteger,
        Identity(start=1),
        primary_key=True
    )

    role_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("role.id", ondelete="RESTRICT"),
        nullable=False
    )

    nome: Mapped[str] = mapped_column(
        String(128),
        unique=True,
        nullable=False
    )

    role: Mapped["Role"] = relationship(
        "Role",
        back_populates="cargos"
    )

    funcionarios: Mapped[list["Funcionario"]] = relationship(
        "Funcionario",
        back_populates="cargo"
    )