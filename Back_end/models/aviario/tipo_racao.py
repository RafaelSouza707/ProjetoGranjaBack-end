from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import BigInteger, Identity, String, ForeignKey

from helpers.database import db

class TipoRacao(db.Model):
    __tablename__ = "tipo_racao"

    id: Mapped[int] = mapped_column(
        BigInteger,
        Identity(start=1),
        primary_key=True
    )

    granja_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("granja.id", ondelete="RESTRICT"),
        nullable=False
    )

    nome: Mapped[str] = mapped_column(
        String(64),
        nullable=False,
        unique=True
    )

    descricao: Mapped[str] = mapped_column(
        String(256),
        nullable=True
    )

    lotes_racao: Mapped[list["LoteRacao"]] = relationship(
        "LoteRacao",
        back_populates="tipo_racao"
    )

    granja: Mapped["Granja"] = relationship(
        "Granja",
        back_populates="tipos_racao"
    )