from datetime import date
from datetime import datetime
# ForeignKey

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import (
    BigInteger,
    Identity,
    String,
    DateTime,
    func
)

from helpers.database import db

class Granja(db.Model):
    __tablename__ = "granja"

    id: Mapped[int] = mapped_column(BigInteger, Identity(start=1), primary_key=True)

    identificacao: Mapped[str] = mapped_column(String(32), nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )

    usuarios: Mapped[list["UsuarioGranja"]] = relationship (
        "UsuarioGranja",
        back_populates="granja"
    )

    lotes_frango: Mapped[list["LoteFrango"]] = relationship(
        "LoteFrango",
        back_populates="granja"
    )

    lotes_racao: Mapped[list["LoteRacao"]] = relationship(
        "LoteRacao",
        back_populates="granja"
    )

    status_lote_frango: Mapped[list["StatusLoteFrango"]] = relationship(
        "StatusLoteFrango",
        back_populates="granja"
    )

    tipos_produto: Mapped[list["TipoProduto"]] = relationship(
        "TipoProduto",
        back_populates="granja"
    )

    tipos_racao: Mapped[list["TipoRacao"]] = relationship(
        "TipoRacao",
        back_populates="granja"
    )

    despesas: Mapped[list["Despesa"]] = relationship(
        "Despesa",
        back_populates="granja"
    )

    receitas: Mapped[list["Receita"]] = relationship(
        "Receita",
        back_populates="granja"
    )

    status_financas: Mapped[list["StatusFinancas"]] = relationship(
        "StatusFinancas",
        back_populates="granja"
    )

    tipos_despesa: Mapped[list["TipoDespesa"]] = relationship(
        "TipoDespesa",
        back_populates="granja"
    )

    tipos_receita: Mapped[list["TipoReceita"]] = relationship(
        "TipoReceita",
        back_populates="granja"
    )
    
    produtos: Mapped[list["Produto"]] = relationship(
        "Produto",
        back_populates="granja"
    )

    tipos_venda: Mapped[list["TipoVenda"]] = relationship(
        "TipoVenda",
        back_populates="granja"
    )

    vendas: Mapped[list["Venda"]] = relationship(
        "Venda",
        back_populates="granja"
    )

    tipos_unidade_medida: Mapped[list["TipoUnidadeMedida"]] = relationship(
        "TipoUnidadeMedida",
        back_populates="granja"
    )

    tipos_movimentacoes: Mapped[list["TipoMovimentacao"]] = relationship(
        "TipoMovimentacao",
        back_populates="granja"
    )

    cliente: Mapped[list["Cliente"]] = relationship(
        "Cliente",
        back_populates="granja"
    )