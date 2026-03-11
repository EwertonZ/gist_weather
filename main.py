from fastapi import FastAPI
from api.routes.gist import router as gist_router


app = FastAPI(title="Gist Weather API", description="A simple weather API built with FastAPI to comment on GitHub Gists.")
app.include_router(gist_router)