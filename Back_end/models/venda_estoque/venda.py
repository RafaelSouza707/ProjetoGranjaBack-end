from datetime import date, datetime

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import (
    BigInteger,
    Identity,
    ForeignKey,
    Numeric,
    Date,
    DateTime,
    func
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
        nullable=True
    )

    status_financas_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("status_financas.id", ondelete="RESTRICT"),
        nullable=False
    )

    tipo_venda_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("tipo_venda.id", ondelete="RESTRICT"),
        nullable=False
    )
    
    granja_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("granja.id", ondelete="RESTRICT"),
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

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )

    cliente: Mapped["Cliente"] = relationship(
        "Cliente",
        back_populates="vendas"
    )

    tipo_venda: Mapped["TipoVenda"] = relationship(
        "TipoVenda",
        back_populates="vendas"
    )

    itens: Mapped[list["ItemVenda"]] = relationship(
        "ItemVenda",
        back_populates="venda",
        cascade="all, delete-orphan"
    )

    receita: Mapped["Receita"] = relationship(
        "Receita",
        back_populates="venda",
        cascade="all, delete-orphan"
    )

    status_financas: Mapped["StatusFinancas"] = relationship(
        "StatusFinancas",
        back_populates="venda",
    )

    granja: Mapped["Granja"] = relationship(
        "Granja",
        back_populates="vendas"
    )