from fastapi import FastAPI
from app.routes import clustering_router

# Initialize FastAPI app
app = FastAPI()

# Include the clustering router
app.include_router(clustering_router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Day Trip Optimization API!"}