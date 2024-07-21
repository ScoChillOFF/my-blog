import asyncio
import sys

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import articles, tags, utilities


app = FastAPI()
app.include_router(articles.router)
app.include_router(tags.router)
app.include_router(utilities.router)

# Boilerplate for Windows
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
# ------------------------


# Temp CORS solution
app.add_middleware(
  CORSMiddleware,
  allow_origins=["*"],
  allow_methods=["*"],
  allow_headers=["*"]
)
# -------------------
