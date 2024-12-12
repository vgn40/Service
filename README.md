# Service Microservice API

This is a RESTful API built using Flask for managing service records within a car subscription system. It provides the ability to create, retrieve, update, and delete service entries, while ensuring security through JWT authentication. The service supports filtering service records and comes with detailed, interactive API documentation via Swagger.

## Features
- **Create a Service Record:** Add a new service entry by providing the required details.
- **Get Services:** Retrieve all service records, or filter them by various parameters (e.g., vehicle ID, service type, date).
- **Update a Service Record:** Modify the details of an existing service record.
- **Delete a Service Record:** Remove an existing service entry by its ID.
- **JWT Authentication:** Secure access to endpoints using JWT tokens.
- **Swagger UI:** Automatically generated interactive API documentation.

## Installation

### Prerequisites
- Python 3.x
- pip (Python package installer)
- SQLite

### Steps to Run
1. **Clone this repository or download the source code.**

2. **Install the required dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your `.env` file with the following environment variables:**
   ```
   DATABASE=service.db
   SECRET_KEY=your_jwt_secret_key
   ```

4. **Initialize the database (if not already done by the application):**
   ```bash
   python -c "from db import init_db; init_db()"
   ```

5. **Run the Flask app:**
   ```bash
   python app.py
   ```
   
   The API will be available at `http://localhost:5000`.

## API Endpoints

### Authentication
All endpoints require a valid JWT token to be passed in the `Authorization` header. The token must be prefixed with `Bearer `.

### Endpoints

#### POST /services
Create a new service record.
**Requires authentication (JWT).**

**Request Body:**
- `vehicle_id`: ID of the vehicle
- `service_date`: Date of the service
- `service_type`: Type of the service performed
- `milage_at_service`: The mileage on the vehicle at the time of service
- `service_provider`: The service provider or garage
- `cost`: The cost of the service

**Response:**
- Returns the `service_id` of the created record and a success message.

#### GET /services
Get a list of service records.
**Requires authentication (JWT).**

**Query Parameters:**
- `vehicle_id`: Filter by vehicle ID
- `service_type`: Filter by type of service
- `service_provider`: Filter by service provider
- `max_cost`: Filter by maximum allowed service cost
- `before_date`: Filter services before a specific date
- `after_date`: Filter services after a specific date

**Response:**
- Returns a JSON array of service records that match the filters.

#### PUT /services/<int:service_id>
Update an existing service record by its ID.
**Requires authentication (JWT).**

**Request Body (Any fields you want to update):**
- `vehicle_id`
- `service_date`
- `service_type`
- `milage_at_service`
- `service_provider`
- `cost`

**Response:**
- Returns a success message upon successful update.
- Returns 404 if `service_id` is not found.

#### DELETE /services/<int:service_id>
Delete a service record by its ID.
**Requires authentication (JWT).**

**Response:**
- Returns a success message upon successful deletion.
- Returns 404 if `service_id` is not found.

### GET /endpoints
List all available endpoints in the API.
**No authentication required.**

## API Documentation
Swagger UI is available at `/apidocs/` for detailed API documentation. It provides an interactive interface to test the API endpoints, view parameter descriptions, and examine response formats.

## Database
The microservice uses a SQLite database for storing service records. The database file location is specified by the `DATABASE` variable in the `.env` file. The `init_db()` function ensures that the necessary tables exist and can insert sample data if desired.
