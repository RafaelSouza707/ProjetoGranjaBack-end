from datetime import date

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import (
    BigInteger,
    Identity,
    ForeignKey,
)

from helpers.database import db

class UsuarioGranja(db.Model):
    __tablename__ = "usuario_granja"

    id: Mapped[int] = mapped_column(BigInteger, Identity(start=1), primary_key=True,)

    usuario_id: Mapped[int] = mapped_column(
        BigInteger, 
        ForeignKey("usuario.id", ondelete="RESTRICT"),
        nullable=False
    )

    granja_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("granja.id", ondelete="RESTRICT"),
        nullable=False
    )

    cargo_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("cargo.id", ondelete="RESTRICT"),
        nullable=True
    )

    ativo: Mapped[bool] = mapped_column(nullable=False)

    usuario: Mapped["Usuario"] = relationship(
        "Usuario",
        back_populates="granjas"
    )

    granja: Mapped["Granja"] = relationship(
        "Granja",
        back_populates="usuarios"
    )

    cargo: Mapped["Cargo"] = relationship(
        "Cargo",
        back_populates="usuarios"
    )