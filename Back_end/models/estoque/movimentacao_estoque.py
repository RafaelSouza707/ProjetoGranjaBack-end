from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import (
    BigInteger,
    Identity,
    ForeignKey,
    Numeric,
    String,
    TIMESTAMP,
    func
)

from helpers.database import db


class MovimentacaoEstoque(db.Model):
    __tablename__ = "movimentacao_estoque"

    id: Mapped[int] = mapped_column(
        BigInteger,
        Identity(start=1),
        primary_key=True
    )

    produto_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("produto.id", ondelete="RESTRICT"),
        nullable=False
    )

    producao_id: Mapped[int | None] = mapped_column(
        BigInteger,
        ForeignKey("producao.id", ondelete="RESTRICT"),
        nullable=True
    )

    item_venda_id: Mapped[int | None] = mapped_column(
        BigInteger,
        ForeignKey("item_venda.id", ondelete="RESTRICT"),
        nullable=True
    )

    tipo_movimentacao_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("tipo_movimentacao.id", ondelete="RESTRICT"),
        nullable=False
    )

    quantidade = mapped_column(
        Numeric(15, 3),
        nullable=False
    )

    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP,
        server_default=func.now(),
        nullable=False
    )

    observacao: Mapped[str | None] = mapped_column(
        String(256)
    )

    produto: Mapped["Produto"] = relationship(
        "Produto",
        back_populates="movimentacoes"
    )

    producao: Mapped["Producao"] = relationship(
        "Producao",
        back_populates="movimentacoes",
    )

    item_venda: Mapped["ItemVenda"] = relationship(
        "ItemVenda",
        back_populates="movimentacoes"
    )

    tipo_movimentacao: Mapped["TipoMovimentacao"] = relationship(
        "TipoMovimentacao",
        back_populates="movimentacoes"
    )