from fastapi import FastAPI, status, HTTPException, BackgroundTasks
from .data_services import TradeService
from .schemas import TransactionData
app = FastAPI()
service = TradeService()


@app.post("/transactions/feed", status_code=status.HTTP_201_CREATED)
async def feed_data(data:list[TransactionData]):
    # background_tasks.add_task(service.ingest(), data)
    result = service.ingest(data)
    return {"status": "data ingested", "data_size": result}

@app.get("/connect", status_code=status.HTTP_200_OK)
def get_connection():
    return {"status": "connected"}

@app.get("/transactions/get/{transaction_id}")
def get_transaction(transaction_id: str):
    return {"status": f"Found transaction {transaction_id}"}
