from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import BigInteger, Identity, String, ForeignKey

from helpers.database import db

class StatusLoteFrango(db.Model):
    __tablename__ = "status_lote_frango"

    id: Mapped[int] = mapped_column(
        BigInteger,
        Identity(start=1),
        primary_key=True
    )

    granja_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("granja.id", ondelete="CASCADE"),
        nullable=False
    )

    nome: Mapped[str] = mapped_column(
        String(20),
        nullable=False
    )

    __table_args__ = (
    db.UniqueConstraint(
        "granja_id",
        "nome",
        name="uq_status_lote_frango_granja_nome"
    ),
)

    lotes: Mapped[list["LoteFrango"]] = relationship(
        "LoteFrango",
        back_populates="status_lote_frango"
    )

    granja: Mapped["Granja"] = relationship(
        "Granja",
        back_populates="status_lote_frango"
    )