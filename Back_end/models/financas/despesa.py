from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Date, ForeignKey, BigInteger, Numeric, Identity, String, DateTime, func
from datetime import datetime
from decimal import Decimal
from helpers.database import db

class Despesa(db.Model):
    __tablename__ = "despesa"

    id: Mapped[int] = mapped_column(BigInteger, Identity(start=1), primary_key=True)
    
    tipo_despesa_id: Mapped[int] = mapped_column(
        BigInteger, 
        ForeignKey("tipo_despesa.id", ondelete="RESTRICT"), 
        nullable=False
    )

    status_financas_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("status_financas.id", ondelete="RESTRICT"),
        nullable=False
    )
    
    lote_frango_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("lote_frango.id", ondelete="RESTRICT"),
        nullable=True
    )

    granja_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("granja.id", ondelete="RESTRICT"),
        nullable=False
    )

    data: Mapped[Date] = mapped_column(Date, nullable=False)
    data_vencimento: Mapped[Date | None] = mapped_column(Date, nullable=True)
    valor: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False)
    descricao: Mapped[str] = mapped_column(String(256), nullable=True)

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

    tipo_despesa: Mapped["TipoDespesa"] = relationship(
        "TipoDespesa",
        back_populates="despesa"
    )

    status_financas: Mapped["StatusFinancas"] = relationship(
        "StatusFinancas",
        back_populates="despesa"
    )
    
    lote_frango: Mapped["LoteFrango"] = relationship(
        "LoteFrango",
        back_populates="despesa"
    )

    granja: Mapped["Granja"] = relationship(
        "Granja",
        back_populates="despesas"
    )