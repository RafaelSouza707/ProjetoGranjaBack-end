from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import (
    BigInteger,
    Identity,
    ForeignKey,
    Numeric
)

from helpers.database import db


class ItemVenda(db.Model):
    __tablename__ = "item_venda"

    id: Mapped[int] = mapped_column(
        BigInteger,
        Identity(start=1),
        primary_key=True
    )

    venda_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("venda.id", ondelete="CASCADE"),
        nullable=False
    )

    produto_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("produto.id", ondelete="RESTRICT"),
        nullable=False
    )

    quantidade = mapped_column(
        Numeric(15, 3),
        nullable=False
    )

    valor_unitario = mapped_column(
        Numeric(15, 2),
        nullable=False
    )

    subtotal = mapped_column(
        Numeric(15, 2),
        nullable=False
    )

    venda: Mapped["Venda"] = relationship(
        "Venda",
        back_populates="itens"
    )

    produto: Mapped["Produto"] = relationship(
        "Produto",
        back_populates="itens_venda"
    )

    movimentacoes: Mapped[list["MovimentacaoEstoque"]] = relationship(
        "MovimentacaoEstoque",
        back_populates="item_venda"
    )