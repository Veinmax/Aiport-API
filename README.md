# Airport API

API service for airport management written on DRF

## Installing using GitHub

1. Install PostgresSQL and create a database.

   ```bash
   git clone https://github.com/Veinmax/Airport-API.git
   cd Airport-API
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
   Configure Environment Variables:ad
- Create a .env file in the project root.
- Make sure it includes all the variables listed in the .env.sample file.
- Ensure that the variable names and values match those in the sample file.
   ```bash
   set POSTGRES_HOST=<your db hostname>
   set POSTGRES_DB=<your db name>
   set POSTGRES_USER=<your db username>
   set POSTGRES_PASSWORD=<your db user password>
   set SECRET_KEY=<your secret key>
   python manage.py migrate
   ```
  Load Initial Data:
   ```bash
    python manage.py loaddata my_data.json
    ```
- After loading data from fixture you can use following superuser (or create another one by yourself):
  - email: `admin@admin.com`
  - Password: `1qazcde3`

Run the Server:
```bash
python manage.py runserver
```

# Run with Docker
Docker should be installed
```bash
docker-compose build
docker-compose up
```

# Getting access
- create user via /api/user/register/
- get access token via /api/user/token/

# Features
- JWT authenticated
- Admin panel /admin/
- Documentation is located at /api/doc/swagger/
- Managing orders and tickets
- Creating routes with source and destination
- Creating airplanes with airplane types
- Adding flights
- Filtering flights by departure time, airplanes and crews
