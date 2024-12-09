# Service Microservice

Denne microservice er udviklet med Flask og tilbyder CRUD-operationer for entiteten "Service" i et bilabonnementssystem. Den anvender JWT-autentifikation for at sikre, at kun autoriserede brugere kan oprette, læse, opdatere og slette serviceposter. Derudover integrerer microservicen Swagger via Flasgger for at give en nem og interaktiv dokumentation af API’et.

## Funktionalitet

1. **Autentifikation med JWT**  
   Alle endpoints kræver et gyldigt JWT-token i headeren `Authorization: Bearer <token>`. Dette sikrer, at kun brugere med rette rettigheder kan foretage ændringer eller hente data.

2. **CRUD-operationer for Services**  
   - **POST /services**: Opretter en ny servicepost ved at sende et JSON-body med de krævede felter (`vehicle_id`, `service_date`, `service_type`, `milage_at_service`, `service_provider`, `cost`). Returnerer et JSON-svar med det oprettede `service_id` og en succesbesked.
   
   - **GET /services**: Henter en liste af serviceposter. Understøtter filtrering ved hjælp af query-parametre som `vehicle_id`, `service_type`, `service_provider`, `max_cost`, `before_date` og `after_date`. Returnerer JSON med en liste af serviceposter.
   
   - **PUT /services/<service_id>**: Opdaterer en eksisterende servicepost. Der sendes et JSON-body med de felter, der skal ændres. Hvis `service_id` ikke findes, returneres 404. Returnerer en succesbesked ved vellykket opdatering.
   
   - **DELETE /services/<service_id>**: Sletter en eksisterende servicepost. Hvis `service_id` ikke findes, returneres 404. Ellers slettes posten og returnerer en succesbesked.

3. **Database**  
   Microservicen benytter en SQLite-database, hvis navn og placering angives via en `.env` fil (`DATABASE=service.db`). Ved opstart initialiseres databasen via `init_db()`-funktionen, som sikrer at tabellerne findes og eventuelt indsætter sample data.

4. **Miljøvariabler (.env)**  
   `.env`-filen indeholder mindst følgende variabler:
   - `DATABASE` - stien eller navnet på databasefilen (f.eks. `service.db`)
   - `SECRET_KEY` - en hemmelig nøgle, der bruges til at signere JWT-tokens

   `load_dotenv()` henter disse variabler inden appen starter.

5. **Swagger-Dokumentation**  
   Microservicen bruger Flasgger til at generere en Swagger UI-baseret dokumentation ved at læse docstrings i koden. Når appen kører, kan dokumentationen ses på `/apidocs/`. Dette giver en brugervenlig grænseflade til at teste endpoints, se hvilke parametre de tager, og hvilke svar de returnerer.

## Kørsel

** For at køre microservicen: **

6. **Sørg for at have en `.env` fil i samme directory som `app.py`:**
   ```env
   DATABASE=service.db
   SECRET_KEY=din_hemmelige_noegle

7. **Kør appen:**
python app.py

Microservicen kører nu typisk på http://127.0.0.1:5000.

Swagger UI: http://127.0.0.1:5000/apidocs/
Endpoints kræver JWT-token i Authorization-headeren.
