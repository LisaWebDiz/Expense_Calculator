### Expense Calculator Pet Project 2025
### Description


### Quick start via Docker

```bash
git clone https://github.com/yourusername/expense_calculator_pet_project_2025.git
cd expense_calculator_pet_project_2025

cp example.env .env
DEBUG=True
SECRET_KEY=your-secret-key
POSTGRES_DB=exp_calc
POSTGRES_USER=your_user
POSTGRES_PASSWORD=your_password
DB_HOST=db
DB_PORT=5432

```bash
docker-compose up --build
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser

Enjoy!
