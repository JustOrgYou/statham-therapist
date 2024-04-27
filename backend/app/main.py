from typing import Annotated
from fastapi import Depends, FastAPI, Form
from fastapi.responses import JSONResponse

from .database import Database
from .dependencies import get_db

app = FastAPI()


@app.get("/healthcheck")
def healthcheck():
    return {"status": "ok"}


@app.get("/favorites")
def get_favorites(user_id: str, db: Database = Depends(get_db)):
    return [row[0] for row in db.get_favorites(user_id)]


@ app.post("/favorites")
def add_favorite(user_id: Annotated[str, Form()], response: Annotated[str, Form()], db: Database = Depends(get_db)):
    db.add_favorite(user_id, response)
    return JSONResponse({"user_id": user_id, "response": response})
