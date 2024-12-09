import sqlite3
import os
from dotenv import load_dotenv

load_dotenv()
DATABASE = os.getenv("DATABASE")

def init_db():
    """Initializes the database and ensures required tables exist."""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS services (
        service_id INTEGER PRIMARY KEY AUTOINCREMENT,
        vehicle_id INTEGER NOT NULL,
        service_date DATE NOT NULL,
        service_type TEXT NOT NULL,
        milage_at_service INTEGER NOT NULL,
        service_provider TEXT NOT NULL,
        cost REAL NOT NULL,
        FOREIGN KEY (vehicle_id) REFERENCES vehicles(vehicle_id)
    );
    """)

    sample_data_services = [
     (1, "2024-12-01", "Oil Change", 100000, "ServicePartnerA", 499.99),
         (2, "2024-11-15", "Brake Repair", 50000, "ServicePartnerB", 1299.50)
     ]
    cursor.executemany("""
     INSERT INTO services (vehicle_id, service_date, service_type, milage_at_service, service_provider, cost)
     VALUES (?, ?, ?, ?, ?, ?)
     """, sample_data_services)

    conn.commit()
    conn.close()
    print("Database initialized and tables ensured.")

if __name__ == "__main__":
    init_db()
