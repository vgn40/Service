# Service Microservice API

This is a RESTful API built using Flask to manage service records in a car subscription system. It enables users to create, retrieve, update, and delete service records, with security ensured through JWT authentication. The service also provides filtering capabilities and interactive API documentation via Swagger.

---

## Features

- **Create a Service**: Add a new service record with details like vehicle ID, service type, cost, and more.
- **Get Services**: Retrieve all service records or filter them using various criteria.
- **Update a Service**: Modify details of an existing service record.
- **Delete a Service**: Remove a service record from the system by its ID.
- **Swagger UI**: Interactive API documentation available for testing and exploration.
- **JWT Authentication**: Secure access to endpoints using JWT tokens.

---

## Installation

### Prerequisites

- Python 3.x  
- pip (Python package installer)  
- SQLite  

### Steps to Run

1. Clone this repository or download the code.

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt

# Service Microservice API Setup and Endpoints

## Set up your `.env` file with the following environment variables:

```makefile
DATABASE=service.db
SECRET_KEY=your_jwt_secret_key
```
# Service Microservice API

## Initialize the database:

```bash
python -c "from db import init_db; init_db()"

Run the Flask app:
bash
Kopier kode
python app.py
The API will be available at http://localhost:5000.

API Endpoints
Authentication
All endpoints require a valid JWT token passed in the Authorization header. The token must be prefixed with Bearer.

Endpoints
POST /services
plaintext
Kopier kode
Description: Create a new service record.
Requires Authentication: ✅
Parameters (JSON body):
- vehicle_id: (integer) ID of the vehicle.
- service_date: (string) Date of the service in YYYY-MM-DD format.
- service_type: (string) Type of the service (e.g., "Oil Change").
- milage_at_service: (integer) Mileage of the vehicle at the time of service.
- service_provider: (string) Name of the service provider.
- cost: (number) Cost of the service.
Response: Returns the service_id of the newly created record and a success message.
GET /services
plaintext
Kopier kode
Description: Retrieve all service records or filter them by criteria.
Requires Authentication: ✅
Query Parameters:
- vehicle_id: Filter by vehicle ID.
- service_type: Filter by service type.
- service_provider
