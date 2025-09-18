from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .db import Base, engine
from .routes import items,stats
from fastapi.staticfiles import StaticFiles


def create_app():
    Base.metadata.create_all(bind=engine)
    app = FastAPI(title="Smart Recycling API")
    app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

    #  Allow React frontend to call FastAPI
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:5173"],  # frontend dev server
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include your routes
    app.include_router(items.router)
    app.include_router(stats.router)   # ← add this line

    return app


app = create_app()
