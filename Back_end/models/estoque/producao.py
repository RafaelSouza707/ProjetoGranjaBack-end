from datetime import date

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import (BigInteger, Identity, ForeignKey, Numeric, Date, String)
from decimal import Decimal

from helpers.database import db


class Producao(db.Model):
    __tablename__ = "producao"

    id: Mapped[int] = mapped_column(
        BigInteger,
        Identity(start=1),
        primary_key=True
    )

    lote_frango_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("lote_frango.id", ondelete="RESTRICT"),
        nullable=False
    )

    produto_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("produto.id", ondelete="CASCADE"),
        nullable=False
    )

    quantidade: Mapped[Decimal] = mapped_column(
        Numeric(15, 3),
        nullable=False
    )

    data_producao: Mapped[date] = mapped_column(
        Date,
        nullable=False
    )

    observacao: Mapped[str | None] = mapped_column(
        String(512)
    )

    produto: Mapped["Produto"] = relationship(
        "Produto",
        back_populates="producoes"
    )

    lote_frango: Mapped["LoteFrango"] = relationship(
        "LoteFrango",
        back_populates="producoes"
    )

    movimentacoes: Mapped[list["MovimentacaoEstoque"]] = relationship(
        "MovimentacaoEstoque",
        back_populates="producao",
        cascade="all, delete-orphan"
    )