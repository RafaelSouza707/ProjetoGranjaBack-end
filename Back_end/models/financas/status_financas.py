from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Date, ForeignKey, BigInteger, Numeric, Identity, String
from decimal import Decimal
from helpers.database import db

class StatusFinancas(db.Model):
    __tablename__ = "status_financas"

    id: Mapped[int] = mapped_column(BigInteger, Identity(start=1), primary_key=True)

    nome: Mapped[str] = mapped_column(String(32), nullable=False, unique=True)

    despesa: Mapped[list["Despesa"]] = relationship("Despesa", back_populates="status_financas")