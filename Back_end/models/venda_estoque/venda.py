from datetime import date

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import (
    BigInteger,
    Identity,
    ForeignKey,
    Numeric,
    Date
)

from helpers.database import db


class Venda(db.Model):
    __tablename__ = "venda"

    id: Mapped[int] = mapped_column(
        BigInteger,
        Identity(start=1),
        primary_key=True
    )

    cliente_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("cliente.id", ondelete="RESTRICT"),
        nullable=False
    )

    status_venda_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("status_venda.id", ondelete="RESTRICT"),
        nullable=False
    )

    valor_total = mapped_column(
        Numeric(15, 2),
        nullable=False
    )

    data_venda: Mapped[date] = mapped_column(
        Date,
        nullable=False
    )

    cliente: Mapped["Cliente"] = relationship(
        "Cliente",
        back_populates="vendas"
    )

    status_venda: Mapped["StatusVenda"] = relationship(
        "StatusVenda",
        back_populates="vendas"
    )

    itens: Mapped[list["ItemVenda"]] = relationship(
        "ItemVenda",
        back_populates="venda",
        cascade="all, delete-orphan"
    )