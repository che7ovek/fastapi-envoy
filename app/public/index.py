from uuid import uuid4
import json
from public.lib.blockchain import Blockchain
import uvicorn
from fastapi import FastAPI

app = FastAPI()

# Генерирует уникальный на глобальном уровне адрес для этого узла
node_identifier = str(uuid4()).replace('-', '')

# Создаём экземпляр блокейна
blockchain = Blockchain()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/items/")
def items_list():
    items_list = {
        'Bull': {"animal": "bull", "sound": "moo"},
        'Seagull': {"animal": "seagull", "sound": "AAAA"}
    }
    return items_list

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}

@app.get('/mine')
def mine():
    return "We'll mine a new Block"

@app.post('/transaction/new')
def new_transaction():
    return "We'll add a new transaction"

@app.get('/chain')
def full_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain)
    }
    return response

if __name__ == "__main__":
    uvicorn.run(app, port=8000)