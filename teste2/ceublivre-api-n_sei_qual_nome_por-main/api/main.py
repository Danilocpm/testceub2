from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from api.sql_app import models, schemas, crud
from api.sql_app.database import SessionLocal, engine


app = FastAPI()


# Dependency for getting a database session
def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


# Create


@app.post("/pedidos/")
def create_pedido(pedido: schemas.PedidoCreate,
                  ids_produtos: List[int],
                  db: Session = Depends(get_db)):
    # Gets list of produtos from database
    db_produtos = []
    for id_produto in ids_produtos:
        db_produto = crud.get_produto(db, id_produto)
        if not db_produto:
            raise HTTPException(status_code=404,
                                detail=f"Produto {id_produto} não encontrado")
        db_produtos.append(db_produto)
    db_pedido = crud.create_pedido(db, pedido, db_produtos)

    return db_pedido


# Update


@app.put("/pedidos/{pedido_id}")
def update_pedido(pedido_id: int,
                  pedido_update: schemas.PedidoUpdate,
                  db: Session = Depends(get_db)):
    pedido = crud.update_pedido(db, pedido_id, pedido_update)
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")

    return pedido


# Get

@app.get("/pedidos/", response_model=list[schemas.Pedido])
def get_pedidos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    pedidos = crud.get_pedidos(db, skip=skip, limit=limit)
    return pedidos