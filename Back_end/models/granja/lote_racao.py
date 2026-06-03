from decimal import Decimal

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import (
    BigInteger,
    Identity,
    ForeignKey,
    Numeric,
    Date,
    String
)

from helpers.database import db

class LoteRacao(db.Model):
    __tablename__ = "lote_racao"

    id: Mapped[int] = mapped_column(
        BigInteger,
        Identity(start=1),
        primary_key=True
    )

    tipo_racao_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("tipo_racao.id", ondelete="RESTRICT"),
        nullable=False
    )

    fornecedor: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    data_compra: Mapped[Date] = mapped_column(
        Date,
        nullable=False
    )

    quilos: Mapped[Decimal] = mapped_column(
        Numeric(15, 3),
        nullable=False
    )

    valor: Mapped[Decimal] = mapped_column(
        Numeric(15, 2),
        nullable=False
    )

    tipo_racao: Mapped["TipoRacao"] = relationship(
        "TipoRacao",
        back_populates="lotes_racao"
    )

    consumos: Mapped[list["ConsumoLoteDiaria"]] = relationship(
        "ConsumoLoteDiaria",
        back_populates="lote_racao"
    )