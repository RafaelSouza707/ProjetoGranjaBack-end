from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import BigInteger, Identity, ForeignKey, TIMESTAMP, func, String

from helpers.database import db


class UsuarioAssociacao(db.Model):
    __tablename__ = "usuario_associacao"

    id: Mapped[int] = mapped_column(
        BigInteger,
        Identity(start=1),
        primary_key=True
    )

    usuario_origem_id = mapped_column(
            ForeignKey("usuario.id"),
            nullable=False
        )

    usuario_destino_id = mapped_column(
        ForeignKey("usuario.id"),
        nullable=False
    )

    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="PENDENTE"
    )

    created_at: Mapped[str] = mapped_column(
        TIMESTAMP,
        server_default=func.now()
    )

    updated_at: Mapped[str] = mapped_column(
        TIMESTAMP,
        server_default=func.now(),
        onupdate=func.now()
    )

    usuario_origem = relationship(
        "Usuario",
        foreign_keys=[usuario_origem_id],
        back_populates="associacoes_enviadas"
    )

    usuario_destino = relationship(
        "Usuario",
        foreign_keys=[usuario_destino_id],
        back_populates="associacoes_recebidas"
    )