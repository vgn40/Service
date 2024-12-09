from flask import Flask, request, jsonify
import sqlite3
from flasgger import Swagger
import os
from dotenv import load_dotenv
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
from db import init_db

load_dotenv()

app = Flask(__name__)


DATABASE = os.getenv("DATABASE")
SECRET_KEY = os.getenv('SECRET_KEY')

app.config['JWT_SECRET_KEY'] = SECRET_KEY
jwt = JWTManager(app)

# comment
swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": "apispec",
            "route": "/apispec.json",
            "rule_filter": lambda rule: True,
            "model_filter": lambda tag: True,
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/apidocs/",
    "securityDefinitions": {
        "BearerAuth": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
            "description": "Enter your JWT token in the format **Bearer &lt;token&gt;**.",
        }
    },
    "security": [{"BearerAuth": []}],
}
swagger = Swagger(app, config=swagger_config)


# Initialiser database
init_db()

@app.route('/services', methods=['POST'])
@jwt_required()
def add_service():
    """
    Add a new service record to the database.
    
    ---
    tags:
      - Service
    parameters:
      - name: body
        in: body
        required: true
        description: Service details
        schema:
          type: object
          properties:
            vehicle_id:
              type: integer
            service_date:
              type: string
              format: date
            service_type:
              type: string
            milage_at_service:
              type: integer
            service_provider:
              type: string
            cost:
              type: number
    responses:
      201:
        description: Service successfully added.
      400:
        description: Missing required fields.
    """
    data = request.get_json()
    required_fields = ["vehicle_id", "service_date", "service_type", "milage_at_service", "service_provider", "cost"]
    
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    conn = sqlite3.connect(DATABASE)
    cursor = conn.execute("""
        INSERT INTO services (vehicle_id, service_date, service_type, milage_at_service, service_provider, cost)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (data["vehicle_id"], data["service_date"], data["service_type"], data["milage_at_service"], data["service_provider"], data["cost"]))
    conn.commit()
    service_id = cursor.lastrowid
    conn.close()

    return jsonify({"id": service_id, "message": "Service added successfully"}), 201


@app.route('/services', methods=['GET'])
@jwt_required()
def get_services():
    """
    Retrieve service details with optional filters.

    ---
    tags:
      - Service
    security:
      - BearerAuth: []  # Require Authorization header
    parameters:
      - name: vehicle_id
        in: query
        type: integer
        required: false
        description: Filter by vehicle ID.
      - name: service_type
        in: query
        type: string
        required: false
        description: Filter by service type (e.g., 'Oil Change', 'Repair').
      - name: service_provider
        in: query
        type: string
        required: false
        description: Filter by service provider name.
      - name: max_cost
        in: query
        type: number
        required: false
        description: Filter by maximum cost.
      - name: before_date
        in: query
        type: string
        format: date
        required: false
        description: Filter services before this date (YYYY-MM-DD).
      - name: after_date
        in: query
        type: string
        format: date
        required: false
        description: Filter services after this date (YYYY-MM-DD).
    responses:
      200:
        description: List of services.
    """
    filters = []
    query = "SELECT * FROM services WHERE 1=1"

    vehicle_id = request.args.get('vehicle_id')
    if vehicle_id:
        query += " AND vehicle_id = ?"
        filters.append(vehicle_id)

    service_type = request.args.get('service_type')
    if service_type:
        query += " AND service_type = ?"
        filters.append(service_type)

    service_provider = request.args.get('service_provider')
    if service_provider:
        query += " AND service_provider = ?"
        filters.append(service_provider)

    max_cost = request.args.get('max_cost')
    if max_cost:
        query += " AND cost <= ?"
        filters.append(max_cost)

    before_date = request.args.get('before_date')
    if before_date:
        query += " AND date(service_date) <= date(?)"
        filters.append(before_date)

    after_date = request.args.get('after_date')
    if after_date:
        query += " AND date(service_date) >= date(?)"
        filters.append(after_date)

    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    cursor = conn.execute(query, filters)
    services = [dict(row) for row in cursor.fetchall()]
    conn.close()

    return jsonify(services), 200

@app.route('/services/<int:service_id>', methods=['PUT'])
@jwt_required()
def update_service(service_id):
    """
    Update service details by ID.
    
    ---
    tags:
      - Service
    parameters:
      - name: service_id
        in: path
        type: integer
        required: true
        description: ID of the service to update.
      - name: body
        in: body
        required: true
        description: Updated service details.
        schema:
          type: object
          properties:
            vehicle_id:
              type: integer
            service_date:
              type: string
              format: date
            service_type:
              type: string
            milage_at_service:
              type: integer
            service_provider:
              type: string
            cost:
              type: number
    responses:
      200:
        description: Service successfully updated.
      404:
        description: Service not found.
      400:
        description: No fields to update.
    """
    data = request.get_json()
    updates = []
    params = []

    for key in ["vehicle_id", "service_date", "service_type", "milage_at_service", "service_provider", "cost"]:
        if key in data:
            updates.append(f"{key} = ?")
            params.append(data[key])
    
    if not updates:
        return jsonify({"error": "No fields to update"}), 400
    
    query = f"UPDATE services SET {', '.join(updates)} WHERE service_id = ?"
    params.append(service_id)

    conn = sqlite3.connect(DATABASE)
    cursor = conn.execute(query, params)
    conn.commit()
    row_count = cursor.rowcount
    conn.close()
    
    if row_count == 0:
        return jsonify({"error": "Service not found"}), 404
    
    return jsonify({"message": "Service updated successfully"}), 200

@app.route('/services/<int:service_id>', methods=['DELETE'])
@jwt_required()
def delete_service(service_id):
    """
    Delete a service by ID.
    
    ---
    tags:
      - Service
    parameters:
      - name: service_id
        in: path
        type: integer
        required: true
        description: ID of the service to delete.
    responses:
      200:
        description: Service successfully deleted.
      404:
        description: Service not found.
    """
    conn = sqlite3.connect(DATABASE)
    cursor = conn.execute("DELETE FROM services WHERE service_id = ?", (service_id,))
    conn.commit()
    row_count = cursor.rowcount
    conn.close()
    
    if row_count == 0:
        return jsonify({"error": "Service not found"}), 404
    
    return jsonify({"message": "Service deleted successfully"}), 200


if __name__ == '__main__':
    app.run(debug=True)
