from sqlalchemy.orm import Session
from typing import List
from . import models, schemas


# Create


def create_pedido(
    db: Session,
    pedido: schemas.PedidoCreate,
    db_produtos: List[schemas.Produto]
):
    db_pedido = models.Pedido(**pedido.dict())
    db_pedido.produtos = db_produtos
    db.add(db_pedido)
    db.commit()
    db.refresh(db_pedido)
    return db_pedido


# Read


def get_produto(db: Session, produto_id: int):
    return (db
            .query(models.Produto)
            .filter(models.Produto.id == produto_id)
            .first())
    
def get_pedidos(db: Session, skip: int = 0, limit: int = 100):
    pedidos = db.query(models.Pedido).offset(skip).limit(limit).all()
    return schemas.PedidoList(pedidos=pedidos)


# Update


def update_pedido(
    db: Session,
    pedido_id: int,
    pedido_update: schemas.PedidoUpdate
):
    db_pedido = (db
                 .query(models.Pedido)
                 .filter(models.Pedido.id == pedido_id)
                 .first())
    if not db_pedido:
        return None
    db_pedido.endereco_entrega = pedido_update.endereco_entrega
    db.commit()
    db.refresh(db_pedido)
    return db_pedido
