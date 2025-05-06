from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import sqlite3
import os

app = FastAPI()

# Set up Jinja2 to use the templates directory
templates = Jinja2Templates(directory="templates")

# Database connection function
def get_data():
    conn = sqlite3.connect("database/food_delivery.db")
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM restaurants")
    restaurants = cursor.fetchall()

    # Get food items grouped by restaurant_idō
    restaurant_data = []
    for res in restaurants:
        cursor.execute("SELECT name, price, description FROM food_items WHERE restaurant_id = ?", (res[0],))
        food_items = cursor.fetchall()
        restaurant_data.append({
            "id": res[0],
            "name": res[1],
            "location": res[2],
            "rating": res[3],
            "food_items": food_items
        })
    
    conn.close()
    return restaurant_data

@app.get("/", response_class=HTMLResponse)
async def show_restaurants(request: Request):
    data = get_data()
    return templates.TemplateResponse("restaurants.html", {"request": request, "restaurants": data})
