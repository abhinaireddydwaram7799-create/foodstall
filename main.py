from fastapi import FastAPI

app = FastAPI(title="Food Stall API 🍴")

@app.get("/")
def home():
    return {"message": "Welcome to Abhinai's Food Stall 🍕"}
