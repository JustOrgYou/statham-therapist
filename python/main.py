from fastapi import FastAPI, Request

app = FastAPI()


@app.get('/')
async def index(_: Request):
    """
    Function that gets invoked on loading index page
    """

    return 200
