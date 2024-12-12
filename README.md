# Service Management API

This is a Flask-based RESTful API for managing vehicle service records.

## Features

- JWT Authentication (except for root and docs endpoints)
- CRUD operations on service records
- Filter services by various criteria
- Auto-generated Swagger documentation

## Endpoints

**Protected (require JWT):**
- **POST** `/add` - Add new service record
- **GET** `/list` - List services with optional filters
- **PUT** `/update/<int:service_id>` - Update an existing service
- **DELETE** `/remove/<int:service_id>` - Delete a service

**Unprotected:**
- **GET** `/` - List all endpoints
- **GET** `/apidocs/` - Swagger UI documentation

## Setup

1. Create a `.env` file with:
   ```
   DATABASE=services.db
   SECRET_KEY=your_jwt_secret
   ```
2. Run `pip install -r requirements.txt`.
3. Start the server with `python app.py`.
4. Access docs at `http://localhost:5000/apidocs/`.

## Authentication

Include a valid JWT in the `Authorization` header:  
`Authorization: Bearer <token>`

## Example Requests

**Add a Service (Requires JWT):**
```bash
curl -X POST http://localhost:5000/add \
-H "Content-Type: application/json" \
-H "Authorization: Bearer <your_token>" \
-d '{
  "vehicle_id": 123,
  "service_date": "2024-12-12",
  "service_type": "Oil Change",
  "milage_at_service": 15000,
  "service_provider": "QuickFix",
  "cost": 89.99
}'
```

## License

MIT License
