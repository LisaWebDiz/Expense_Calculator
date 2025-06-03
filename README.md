# Expense Calculator Pet Project 2025
### Description


### Quick start via Docker

```bash
git clone https://github.com/yourusername/expense_calculator_pet_project_2025.git
cd expense_calculator_pet_project_2025
cp example.env .env
docker-compose up --build
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
```
Enjoy!

### Api Documentation
    • Swagger: http://localhost:8000/swagger/
    • Redoc: http://localhost:8000/redoc/

### Features
    • User registration and login via Djoser
    • Django admin panel for managing data
    • Fully documented REST API
    • Data storage using PostgreSQL
    • pgAdmin for database viewing: http://localhost:5050
    • Admin panel: http://localhost:8000/admin/
    • Registration/Authentication: out-of-the-box with Django and Djoser API

### Pages
