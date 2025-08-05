# Car Service Centre Management System

A complete **Python + MySQL** based management system to handle operations of a car service centre, including:

- Customer & Vehicle Management
- Services & Billing
- Discounts & Reminders
- Timestamp-based Tracking
- Modular functions for easy extension



## Tech Stack:

- **Language:** Python 3.x
- **Database:** MySQL
- **Connector:** `mysql-connector-python`
- **IDE:** Python IDLE (or any Python environment)



## Features:

- Add & manage car types, services, and customers
- Track customer vehicles
- Generate itemized bills with discounts
- Send automated service reminders
- Store bill timestamps
- Modular functions for easy scalability



## Requirements:

- Install the MySQL connector for Python:
`pip install mysql-connector-python`
- Also ensure MySQL Server is installed and running on your system.



## How to Run:

Create a MySQL database connection in the script  
Run the Python file in IDLE or any Python IDE.  
The script will:
- Create the database & all tables
- Insert demo data (10 customers, vehicles, services)
- Generate bills
- Set reminders & print notifications



## Database Tables:

- **CarTypes-**  Stores brand, model, fuel type
- **Services-**  List of service names and costs
- **Customers-**  Customer details with contact info
- **Vehicles-**  Links customer to vehicle
- **Bills-**  Tracks service visits with amounts
- **BillItems-**  Items in each bill
- **Reminders-**  Stores due-service messages
- **Discounts-**  Optional discount slabs



## Extensions (Optional Ideas):

- Add Employee Table & Role Management
- Generate PDF invoices or CSV reports
- Build a Tkinter GUI frontend
- Send real-time SMS/Email using Twilio or SMTP
- Add login system for admin and staff



## Project Structure:

Car-Service-Centre-Management-System/  
├── Car Service Centre.py      # Main script  
└── README.md                  # Project documentation



## License:

This project is open-source for educational and learning purposes.



## Author:

**Dikshitha Reddy Vanga**  
Feel free to fork this repository and build on it!
