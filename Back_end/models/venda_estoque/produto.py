from datetime import date

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import (
    BigInteger,
    Identity,
    ForeignKey,
    String,
    Boolean,
    Date
)

from helpers.database import db


class Produto(db.Model):
    __tablename__ = "produto"

    id: Mapped[int] = mapped_column(
        BigInteger,
        Identity(start=1),
        primary_key=True
    )

    tipo_produto_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("tipo_produto.id", ondelete="RESTRICT"),
        nullable=False
    )

    tipo_unidade_medida_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("tipo_unidade_medida.id", ondelete="RESTRICT"),
        nullable=False
    )

    descricao: Mapped[str] = mapped_column(
        String(120),
        nullable=False
    )

    ativo: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True
    )

    data_cadastro: Mapped[date] = mapped_column(
        Date,
        nullable=False
    )

    tipo_produto: Mapped["TipoProduto"] = relationship(
        "TipoProduto",
        back_populates="produtos"
    )

    tipo_unidade_medida: Mapped["TipoUnidadeMedida"] = relationship(
        "TipoUnidadeMedida",
        back_populates="produtos"
    )

    estoque: Mapped["Estoque"] = relationship(
        "Estoque",
        back_populates="produto",
        uselist=False
    )

    producoes: Mapped[list["Producao"]] = relationship(
        "Producao",
        back_populates="produto"
    )

    itens_venda: Mapped[list["ItemVenda"]] = relationship(
        "ItemVenda",
        back_populates="produto"
    )

    movimentacoes: Mapped[list["MovimentacaoEstoque"]] = relationship(
        "MovimentacaoEstoque",
        back_populates="produto"
    )