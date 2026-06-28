from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import (
    BigInteger,
    Identity,
    ForeignKey,
    Integer,
    Date,
    String
)

from helpers.database import db

class LoteFrango(db.Model):
    __tablename__ = "lote_frango"

    id: Mapped[int] = mapped_column(
        BigInteger,
        Identity(start=1),
        primary_key=True
    )

    status_lote_frango_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("status_lote_frango.id", ondelete="RESTRICT"),
        nullable=False
    )

    granja_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("granja.id", ondelete="RESTRICT"),
        nullable=False
    )

    identificacao: Mapped[str] = mapped_column(
        String(32),
        nullable=False,
        unique=True
    )

    quantidade_inicial: Mapped[int] = mapped_column(
        Integer,
        nullable=True
    )

    data_alojamento: Mapped[Date] = mapped_column(
        Date,
        nullable=False
    )

    fornecedor: Mapped[str] = mapped_column(
        String(128),
        nullable=True
    )

    quantidade_atual: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    observacao: Mapped[str] = mapped_column(
        String(512),
        nullable=True
    )

    status_lote_frango: Mapped["StatusLoteFrango"] = relationship(
        "StatusLoteFrango",
        back_populates="lotes"
    )

    mortalidades: Mapped[list["Mortalidade"]] = relationship(
        "Mortalidade",
        back_populates="lote_frango"
    )

    consumos: Mapped[list["ConsumoLoteDiaria"]] = relationship(
        "ConsumoLoteDiaria",
        back_populates="lote_frango"
    )

    producoes: Mapped[list["Producao"]] = relationship(
        "Producao",
        back_populates="lote_frango"
    )

    despesa: Mapped["Despesa"] = relationship(
        "Despesa",
        back_populates="lote_frango"
    )

    granja: Mapped["Granja"] = relationship(
        "Granja",
        back_populates="lotes_frango"
    )