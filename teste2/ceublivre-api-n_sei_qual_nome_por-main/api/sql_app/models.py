from sqlalchemy import (Column, ForeignKey, String, Table, DateTime, DECIMAL,
                        Text)
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.orm import relationship

from .database import Base


courses_students = Table("association",
                         Base.metadata,
                         Column("student_id",
                                INTEGER(unsigned=True),
                                ForeignKey("students.id")),
                         Column("course_id",
                                INTEGER(unsigned=True),
                                ForeignKey("courses.id")))

pedido_produto = Table(
    'pedido_produto',
    Base.metadata,
    Column('pedido_id', INTEGER(unsigned=True), ForeignKey('pedidos.id')),
    Column('produto_id', INTEGER(unsigned=True), ForeignKey('produtos.id'))
)


class Pedido(Base):
    __tablename__ = "pedidos"

    id = Column(INTEGER(unsigned=True), primary_key=True,
                index=True, autoincrement=True)
    criado_em = Column(DateTime(),
                       server_default="CURRENT_TIMESTAMP",
                       nullable=False)
    valor_total = Column(DECIMAL(10, 2), nullable=False)
    valor_frete = Column(DECIMAL(10, 2), nullable=False)
    endereco_entrega = Column(String(255), nullable=False)
    produtos = relationship("Produto", secondary=pedido_produto)


class Produto(Base):
    __tablename__ = 'produtos'

    id = Column(INTEGER(unsigned=True), primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False)
    pedidos = relationship("Pedido", secondary=pedido_produto)
