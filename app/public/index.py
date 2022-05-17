import uvicorn
from fastapi import FastAPI

app = FastAPI()


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

if __name__ == "__main__":
    uvicorn.run(app, port=8000)