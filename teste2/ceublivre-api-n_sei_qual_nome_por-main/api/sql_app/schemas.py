from datetime import datetime
from decimal import Decimal
from typing import List, Optional
from pydantic import BaseModel


# PEDIDO


class PedidoBase(BaseModel):
    valor_total: Optional[Decimal]
    valor_frete: Optional[Decimal]
    endereco_entrega: str


class PedidoCreate(PedidoBase):
    pass


class PedidoUpdate(BaseModel):
    endereco_entrega: str


class Pedido(PedidoBase):
    id: int
    criado_em: datetime
    produtos: List['Produto'] = []

    class Config:
        orm_mode = True
        

# PRODUTO


class ProdutoBase(BaseModel):
    nome: str


class ProdutoCreate(ProdutoBase):
    pass


class Produto(ProdutoBase):
    id: int
    pedidos: List[Pedido] = []

    class Config:
        orm_mode = True
