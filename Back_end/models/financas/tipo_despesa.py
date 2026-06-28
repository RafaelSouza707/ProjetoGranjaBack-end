from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Date, ForeignKey, BigInteger, Numeric, Identity, String
from decimal import Decimal
from helpers.database import db

class TipoDespesa(db.Model):
    __tablename__ = "tipo_despesa"

    id: Mapped[int] = mapped_column(BigInteger, Identity(start=1), primary_key=True)

    granja_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("granja.id", ondelete="RESTRICT"),
        nullable=False
    )

    nome: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)

    despesa: Mapped[list["Despesa"]] = relationship(
        "Despesa",
        back_populates="tipo_despesa"
    )

    granja: Mapped["Granja"] = relationship(
        "Granja",
        back_populates="tipos_despesa"
    )