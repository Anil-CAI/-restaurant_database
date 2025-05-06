import sqlite3

# Function to connect to the SQLite database
def connect_db():
    conn = sqlite3.connect('database/food_delivery.db')
    return conn

# Function to create tables if they don't exist
def create_tables():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS restaurants (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        location TEXT NOT NULL,
        rating INTEGER NOT NULL
    );
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS food_items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        description TEXT,
        price REAL NOT NULL,
        restaurant_id INTEGER,
        FOREIGN KEY(restaurant_id) REFERENCES restaurants(id)
    );
    ''')

    conn.commit()
    conn.close()

# Function to add a new restaurant
def add_restaurant(name, location, rating):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute('''
    INSERT INTO restaurants (name, location, rating)
    VALUES (?, ?, ?);
    ''', (name, location, rating))

    conn.commit()
    conn.close()
    print(f"Restaurant '{name}' added successfully!")

# Function to add a new food item
def add_food_item(name, description, price, restaurant_id):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute('''
    INSERT INTO food_items (name, description, price, restaurant_id)
    VALUES (?, ?, ?, ?);
    ''', (name, description, price, restaurant_id))

    conn.commit()
    conn.close()
    print(f"Food item '{name}' added successfully!")

# Function to view restaurants
def view_restaurants():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM restaurants')
    restaurants = cursor.fetchall()

    if restaurants:
        print("\nRestaurants List:")
        for row in restaurants:
            print(f"ID: {row[0]}, Name: {row[1]}, Location: {row[2]}, Rating: {row[3]}")
    else:
        print("No restaurants found.")
    conn.close()

# Function to view food items for a specific restaurant
def view_food_items(restaurant_id):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM food_items WHERE restaurant_id = ?', (restaurant_id,))
    food_items = cursor.fetchall()

    if food_items:
        print(f"\nFood Items for Restaurant ID {restaurant_id}:")
        for row in food_items:
            print(f"ID: {row[0]}, Name: {row[1]}, Description: {row[2]}, Price: {row[3]}")
    else:
        print(f"No food items found for restaurant ID {restaurant_id}.")
    conn.close()

# Main menu for interaction
def main():
    create_tables()
    
    while True:
        print("\nWelcome to the Restaurant and Food Item Manager")
        print("1. Add New Restaurant")
        print("2. Add New Food Item")
        print("3. View All Restaurants")
        print("4. View Food Items of a Restaurant")
        print("5. Exit")
        
        choice = input("Enter your choice (1-5): ")

        if choice == '1':
            name = input("Enter the restaurant name: ")
            location = input("Enter the restaurant location: ")
            rating = int(input("Enter the restaurant rating (1-5): "))
            add_restaurant(name, location, rating)
        
        elif choice == '2':
            view_restaurants()
            restaurant_id = int(input("Enter the restaurant ID to add food items: "))
            name = input("Enter the food item name: ")
            description = input("Enter the food item description: ")
            price = float(input("Enter the food item price: "))
            add_food_item(name, description, price, restaurant_id)
        
        elif choice == '3':
            view_restaurants()
        
        elif choice == '4':
            restaurant_id = int(input("Enter the restaurant ID to view food items: "))
            view_food_items(restaurant_id)
        
        elif choice == '5':
            print("Exiting the application.")
            break
        
        else:
            print("Invalid choice. Please try again.")

if __name__ == '__main__':
    main()
