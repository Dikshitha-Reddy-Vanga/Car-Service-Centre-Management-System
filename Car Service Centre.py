#Install MySQL Connector
import mysql.connector
from datetime import datetime, timedelta
from decimal import Decimal

#Connect MySQL to Python in IDLE
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="dikshitha"
)
cursor = mydb.cursor()

#Create the Database and Tables
cursor.execute("CREATE DATABASE IF NOT EXISTS CarServiceCentre")
cursor.execute("USE CarServiceCentre")

# Car Types
cursor.execute("""
CREATE TABLE IF NOT EXISTS CarTypes (
    CarTypeID INT AUTO_INCREMENT PRIMARY KEY,
    Brand VARCHAR(50),
    Model VARCHAR(50),
    FuelType VARCHAR(20)
)
""")

# Services
cursor.execute("""
CREATE TABLE IF NOT EXISTS Services (
    ServiceID INT AUTO_INCREMENT PRIMARY KEY,
    ServiceName VARCHAR(100),
    Cost DECIMAL(10, 2)
)
""")

# Customers
cursor.execute("""
CREATE TABLE IF NOT EXISTS Customers (
    CustomerID INT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(100),
    Phone VARCHAR(15),
    Email VARCHAR(100),
    IsRegular BOOLEAN DEFAULT FALSE
)
""")

# Vehicles (linking car types to customers)
cursor.execute("""
CREATE TABLE IF NOT EXISTS Vehicles (
    VehicleID INT AUTO_INCREMENT PRIMARY KEY,
    CustomerID INT,
    CarTypeID INT,
    LicensePlate VARCHAR(20),
    FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID),
    FOREIGN KEY (CarTypeID) REFERENCES CarTypes(CarTypeID)
)
""")

# Bills
cursor.execute("""
CREATE TABLE IF NOT EXISTS Bills (
    BillID INT AUTO_INCREMENT PRIMARY KEY,
    VehicleID INT,
    TotalAmount DECIMAL(10, 2),
    DiscountApplied DECIMAL(10,2),
    FinalAmount DECIMAL(10, 2),
    BillDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (VehicleID) REFERENCES Vehicles(VehicleID)
)
""")

# BillItems (one bill can include many services)
cursor.execute("""
CREATE TABLE IF NOT EXISTS BillItems (
    BillItemID INT AUTO_INCREMENT PRIMARY KEY,
    BillID INT,
    ServiceID INT,
    Quantity INT DEFAULT 1,
    FOREIGN KEY (BillID) REFERENCES Bills(BillID),
    FOREIGN KEY (ServiceID) REFERENCES Services(ServiceID)
)
""")

# Reminders
cursor.execute("""
CREATE TABLE IF NOT EXISTS Reminders (
    ReminderID INT AUTO_INCREMENT PRIMARY KEY,
    CustomerID INT,
    ReminderDate DATE,
    Message TEXT,
    IsSent BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID)
)
""")

# Discounts (for regulars or offers)
cursor.execute("""
CREATE TABLE IF NOT EXISTS Discounts (
    DiscountID INT AUTO_INCREMENT PRIMARY KEY,
    Description VARCHAR(100),
    DiscountPercent DECIMAL(5, 2)
)
""")

mydb.commit()
print("Database and tables created successfully.")

#Reminder Message Script
def send_reminders():
    cursor.execute("""
        SELECT Name, Email, ReminderDate, Message 
        FROM Customers
        JOIN Reminders ON Customers.CustomerID = Reminders.CustomerID
        WHERE IsSent = FALSE AND ReminderDate <= CURDATE()
    """)
    for (name, email, date, msg) in cursor.fetchall():
        print(f"Send reminder to {name} ({email}) - {msg}")
        # mark as sent (in real system, send email or SMS)
        cursor.execute("UPDATE Reminders SET IsSent = TRUE WHERE ReminderDate = %s AND Message = %s", (date, msg))
    mydb.commit()

#Add Car Type
def add_car_type(brand, model, fuel_type):
    cursor.execute("INSERT INTO CarTypes (Brand, Model, FuelType) VALUES (%s, %s, %s)", (brand, model, fuel_type))
    mydb.commit()
    print("Car Type added.")

#Add Service
def add_service(service_name, cost):
    cursor.execute("INSERT INTO Services (ServiceName, Cost) VALUES (%s, %s)", (service_name, cost))
    mydb.commit()
    print("Service added.")

#Add Customer
def add_customer(name, phone, email, is_regular=False):
    cursor.execute("INSERT INTO Customers (Name, Phone, Email, IsRegular) VALUES (%s, %s, %s, %s)",
                   (name, phone, email, is_regular))
    mydb.commit()
    print("Customer added.")

#Add Vehicle
def add_vehicle(customer_id, car_type_id, license_plate):
    cursor.execute("INSERT INTO Vehicles (CustomerID, CarTypeID, LicensePlate) VALUES (%s, %s, %s)",
                   (customer_id, car_type_id, license_plate))
    mydb.commit()
    print("Vehicle added.")

#Generate Bill
def generate_bill(vehicle_id, service_items, discount_percent=0):
    # Calculate total
    total_amount = 0
    for service_id, quantity in service_items:
        cursor.execute("SELECT Cost FROM Services WHERE ServiceID = %s", (service_id,))
        cost = cursor.fetchone()[0]
        total_amount += cost * quantity

    discount_amount = total_amount * (Decimal(discount_percent) / Decimal(100))
    final_amount = total_amount - discount_amount

    # Insert into Bills table
    cursor.execute("INSERT INTO Bills (VehicleID, TotalAmount, DiscountApplied, FinalAmount) VALUES (%s, %s, %s, %s)",
                   (vehicle_id, total_amount, discount_amount, final_amount))
    bill_id = cursor.lastrowid

    # Insert into BillItems
    for service_id, quantity in service_items:
        cursor.execute("INSERT INTO BillItems (BillID, ServiceID, Quantity) VALUES (%s, %s, %s)",
                       (bill_id, service_id, quantity))
    mydb.commit()
    print(f"Bill Generated. Total: ₹{total_amount}, Final: ₹{final_amount} (Discount: ₹{discount_amount})")

#Add Reminder Message
def add_reminder(customer_id, days_from_now, message):
    reminder_date = datetime.now().date() + timedelta(days=days_from_now)
    cursor.execute("INSERT INTO Reminders (CustomerID, ReminderDate, Message) VALUES (%s, %s, %s)",
                   (customer_id, reminder_date, message))
    mydb.commit()
    print("Reminder added.")

#Send Reminders
def send_reminders():
    cursor.execute("""
        SELECT Customers.Name, Customers.Email, ReminderDate, Message, ReminderID
        FROM Customers
        JOIN Reminders ON Customers.CustomerID = Reminders.CustomerID
        WHERE IsSent = FALSE AND ReminderDate <= CURDATE()
    """)
    for name, email, date, message, reminder_id in cursor.fetchall():
        print(f"Reminder: {name} - {email} - {message} on {date}")
        cursor.execute("UPDATE Reminders SET IsSent = TRUE WHERE ReminderID = %s", (reminder_id,))
    mydb.commit()

#Add Car Types
car_types = [
    ("Hyundai", "Creta", "Petrol"),
    ("Maruti", "Swift", "Petrol"),
    ("Toyota", "Fortuner", "Diesel"),
    ("Honda", "City", "Petrol"),
    ("Tata", "Nexon", "Petrol"),
    ("Mahindra", "XUV700", "Diesel")
]
for brand, model, fuel in car_types:
    add_car_type(brand, model, fuel)

#Add Services
services = [
    ("Oil Change", 1000),
    ("Wheel Alignment", 700),
    ("AC Service", 1200),
    ("General Checkup", 500),
    ("Brake Inspection", 800),
    ("Car Wash", 400)
]
for name, cost in services:
    add_service(name, cost)
    

#Add Customers and Vehicles
customers = [
    ("John Doe", "9876543210", "john@example.com", True),
    ("Alice Smith", "9123456789", "alice@example.com", False),
    ("Bob Martin", "9988776655", "bob@example.com", True),
    ("Priya Shah", "9012345678", "priya@example.com", False),
    ("Ravi Kumar", "9345678901", "ravi@example.com", True),
    ("Sneha Iyer", "9456789012", "sneha@example.com", False),
    ("Amit Verma", "9567890123", "amit@example.com", True),
    ("Neha Gupta", "9678901234", "neha@example.com", False),
    ("Karthik Reddy", "9789012345", "karthik@example.com", True),
    ("Divya Menon", "9890123456", "divya@example.com", True)
]
for name, phone, email, regular in customers:
    add_customer(name, phone, email, regular)
vehicles = [
    (1, 1, "AP01AB1111"),
    (2, 2, "AP01AB2222"),
    (3, 3, "TS09CD3333"),
    (4, 4, "TS10EF4444"),
    (5, 5, "AP02GH5555"),
    (6, 6, "AP03IJ6666"),
    (7, 1, "TS04KL7777"),
    (8, 2, "AP05MN8888"),
    (9, 3, "TS06OP9999"),
    (10, 4, "AP07QR0000")
]
for cust_id, car_type_id, plate in vehicles:
    add_vehicle(cust_id, car_type_id, plate)

#Generate Bills
# Format: (vehicle_id, [(service_id, quantity)], discount_percent)

bills = [
    (1, [(1,1), (2,1)], 10),
    (2, [(3,1), (6,1)], 0),
    (3, [(1,1), (4,1), (5,1)], 15),
    (4, [(2,1), (6,1)], 5),
    (5, [(4,1), (1,1)], 10),
    (6, [(5,1)], 0),
    (7, [(1,1), (6,1), (3,1)], 20),
    (8, [(2,1), (4,1)], 0),
    (9, [(1,1), (2,1), (3,1), (6,1)], 15),
    (10, [(4,1), (5,1)], 10)
]
for vehicle_id, services_used, discount in bills:
    generate_bill(vehicle_id, services_used, discount)

#Add Reminders
reminders = [
    (1, 15, "Next oil change in 15 days."),
    (3, 30, "Annual AC checkup due in 30 days."),
    (5, 10, "Time for general checkup."),
    (7, 25, "Brake inspection reminder."),
    (9, 20, "Wheel alignment check due."),
]
for cust_id, days, msg in reminders:
    add_reminder(cust_id, days, msg)

#Send Reminders
send_reminders()

