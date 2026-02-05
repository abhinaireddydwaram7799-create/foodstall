from fastapi import FastAPI
app = FastAPI()
@app.get("/")
def root():
    return {"status": "ok"}
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict

app = FastAPI(title="Food Stall API 🍴")

menu_db: Dict[int, dict] = {}
order_db: Dict[int, dict] = {}

class FoodItem(BaseModel):
    name: str
    price: float
    available: bool = True

class Order(BaseModel):
    food_id: int
    quantity: int

@app.get("/")
def home():
    return {"message": "Welcome to Abhinai's Food Stall 🍕"}

@app.post("/menu/{food_id}")
def add_food(food_id: int, food: FoodItem):
    menu_db[food_id] = food
    return {"message": "Food item added", "food": food}

@app.get("/menu")
def view_menu():
    return menu_db

@app.get("/menu/{food_id}")
def get_food(food_id: int):
    if food_id not in menu_db:
        raise HTTPException(status_code=404, detail="Food not found")
    return menu_db[food_id]

@app.put("/menu/{food_id}")
def update_food(food_id: int, food: FoodItem):
    if food_id not in menu_db:
        raise HTTPException(status_code=404, detail="Food not found")
    menu_db[food_id] = food
    return {"message": "Food updated", "food": food}

@app.delete("/menu/{food_id}")
def delete_food(food_id: int):
    if food_id not in menu_db:
        raise HTTPException(status_code=404, detail="Food not found")
    return menu_db.pop(food_id)

@app.post("/order/{order_id}")
def place_order(order_id: int, order: Order):
    if order.food_id not in menu_db:
        raise HTTPException(status_code=404, detail="Food not available")

    food = menu_db[order.food_id]

    if not food.available:
        raise HTTPException(status_code=400, detail="Out of stock")

    total = food.price * order.quantity
    order_db[order_id] = {
        "food": food.name,
        "quantity": order.quantity,
        "total_price": total
    }
    return {"message": "Order placed 🍽️", "bill": order_db[order_id]}

@app.get("/orders")
def view_orders():
    return order_db



