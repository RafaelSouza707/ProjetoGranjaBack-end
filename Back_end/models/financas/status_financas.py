from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Date, ForeignKey, BigInteger, Numeric, Identity, String
from decimal import Decimal
from helpers.database import db

class StatusFinancas(db.Model):
    __tablename__ = "status_financas"

    id: Mapped[int] = mapped_column(BigInteger, Identity(start=1), primary_key=True)

    granja_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("granja.id", ondelete="CASCADE"),
        nullable=False
    )

    nome: Mapped[str] = mapped_column(
        String(32), 
        nullable=False,
    )

    despesa: Mapped[list["Despesa"]] = relationship(
        "Despesa", 
        back_populates="status_financas"
    )

    venda: Mapped["Venda"] = relationship(
        "Venda",
        back_populates="status_financas"
    )

    granja: Mapped["Granja"] = relationship(
        "Granja",
        back_populates="status_financas"
    )

    receitas: Mapped["Receita"] = relationship(
        "Receita",
        back_populates="status_financas"
    )