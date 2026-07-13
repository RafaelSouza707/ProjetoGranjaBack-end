from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Date, ForeignKey, BigInteger, Numeric, Identity, String, DateTime, func
from datetime import datetime
from decimal import Decimal
from helpers.database import db


class Receita(db.Model):
    __tablename__ = "receita"

    id: Mapped[int] = mapped_column(BigInteger, Identity(start=1), primary_key=True)

    tipo_receita_id: Mapped[int] = mapped_column(
        BigInteger, 
        ForeignKey("tipo_receita.id", ondelete="RESTRICT"),
        nullable=False
    )
    
    status_financas_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("status_financas.id", ondelete="RESTRICT"),
        nullable=False
    )

    venda_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("venda.id", ondelete="RESTRICT"),
        nullable=True
    )

    granja_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("granja.id", ondelete="CASCADE"),
        nullable=False
    )

    data: Mapped[Date] = mapped_column(Date, nullable=False)

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

    venda: Mapped["Venda"] = relationship(
        "Venda",
        back_populates="receita"
    )

    tipo_receita: Mapped["TipoReceita"] = relationship(
        "TipoReceita",
        back_populates="receita"
    )

    granja: Mapped["Granja"] = relationship(
        "Granja",
        back_populates="receitas"
    )

    status_financas: Mapped["StatusFinancas"] = relationship(
        "StatusFinancas",
        back_populates="receitas"
    )