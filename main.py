from fastapi import FastAPI

from router import router as notes_router


app = FastAPI(title="тестовый HTTP SERVER")
app.include_router(notes_router)
