from urllib import response
from uuid import uuid4
from public.lib.blockchain import Blockchain
import uvicorn
from fastapi import FastAPI, Response, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel

class Transaction(BaseModel):
    sender: str
    recipient: str
    amount: int

app = FastAPI()

# Генерирует уникальный на глобальном уровне адрес для этого узла
node_identifier = str(uuid4()).replace('-', '')

# Создаём экземпляр блокейна
blockchain = Blockchain()

@app.get("/")
async def root():
    return JSONResponse({"message": "Hello World"})

@app.get("/items/")
def items_list():
    items_list = {
        'Bull': {"animal": "bull", "sound": "moo"},
        'Seagull': {"animal": "seagull", "sound": "AAAA"}
    }
    return JSONResponse(items_list)

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return JSONResponse({"item_id": item_id, "q": q})

@app.get('/mine')
def mine():
    # Запускаем алгоритм подтверждения работы, чтобы получить следующее подтверждение
    last_block = blockchain.last_block
    last_proof = last_block['proof']
    proof = blockchain.proof_of_work(last_proof)

    # Мы должны получить вознаграждение за найденное подтверждение
    # Отправитель "0" означает, что узел заработал крипто-монету
    blockchain.new_transaction(
        sender=0,
        recipient=node_identifier,
        amount=1
    )

    # Создаём новый блок, путём внесения его в цепь
    previous_hash = blockchain.hash(last_block)
    block = blockchain.new_block(proof, previous_hash)

    response = {
        'message': "New Block Forged",
        'index': block['index'],
        'transactions': block['transactions'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash']
    }
    return JSONResponse(response, status.HTTP_200_OK)

@app.post('/transaction/new')
def new_transaction(transaction: Transaction, response: Response):
    values = transaction.json

    #Убедитесь в то, что необходимые поля находятся в POST
    required = ['sender', 'recipient', 'amount']
    if not all(k in values for k in required):
        response.status_code = status.HTTP_400_BAD_REQUEST
        return 'Missing values'

    # Создание новой транзакции
    index = blockchain.new_transaction(values['sender'], values['recipient'], values['amount'])

    response = {'message': f'Transaction will be added to Block {index}'}
    return JSONResponse(response, status_code=status.HTTP_201_CREATED)

@app.get('/chain')
def full_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain)
    }
    return JSONResponse(response)

if __name__ == "__main__":
    uvicorn.run(app, port=8000)