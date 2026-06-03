from datetime import date

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import (
    BigInteger,
    Identity,
    ForeignKey,
    String,
    Date,
    Boolean,
    func
)

from helpers.database import db


class ContaADM(db.Model):
    __tablename__ = "conta_adm"

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
        nullable=False
    )

    email: Mapped[str] = mapped_column(
        String(128),
        unique=True,
        nullable=False
    )

    senha: Mapped[str] = mapped_column(
        String(256),
        nullable=False
    )

    cpf: Mapped[str] = mapped_column(
        String(11),
        unique=True,
        nullable=False
    )

    ativo: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True
    )

    data_cadastro: Mapped[date] = mapped_column(
        Date,
        server_default=func.current_date(),
        nullable=False
    )

    role: Mapped["Role"] = relationship(
        "Role",
        back_populates="contas_adm"
    )