from decimal import Decimal

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import BigInteger, Identity, ForeignKey, Numeric, Date, func
from helpers.database import db

class ConsumoLoteDiaria(db.Model):
    __tablename__ = "consumo_lote_diaria"

    id: Mapped[int] = mapped_column(
        BigInteger,
        Identity(start=1),
        primary_key=True
    )

    lote_frango_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("lote_frango.id", ondelete="CASCADE"),
        nullable=False
    )

    lote_racao_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("lote_racao.id", ondelete="CASCADE"),
        nullable=False
    )

    data: Mapped[Date] = mapped_column(
        Date,
        server_default=func.current_date(),
        nullable=False
    )

    quilos: Mapped[Decimal] = mapped_column(
        Numeric(15, 3),
        nullable=False
    )

    lote_frango: Mapped["LoteFrango"] = relationship(
        "LoteFrango",
        back_populates="consumos",
    )

    lote_racao: Mapped["LoteRacao"] = relationship(
        "LoteRacao",
        back_populates="consumos",
    )