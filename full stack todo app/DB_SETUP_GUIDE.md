# Setting up Neon PostgreSQL for the Todo App

## Why Tables May Not Appear to be Created

The application was initially configured to use SQLite for local development. If you check the `.env` file, you'll see it was set to:

```
DATABASE_URL=sqlite:///./todo_app.db
```

This creates a local SQLite database file named `todo_app.db` in the backend directory, where the tables are actually created.

## Switching to Neon PostgreSQL

To use Neon PostgreSQL instead of SQLite:

1. **Sign up for Neon**: Go to [Neon](https://neon.tech/) and create an account

2. **Create a Project**: Create a new Neon project and database

3. **Get Connection Details**: From your Neon dashboard, copy the connection string

4. **Update .env file**: Replace the placeholder in `backend/.env`:
   ```
   DATABASE_URL=postgresql://username:password@ep-xxx.us-east-1.aws.neon.tech/dbname?sslmode=require
   DATABASE_URL_BETTER_AUTH=postgresql://username:password@ep-xxx.us-east-1.aws.neon.tech/dbname?sslmode=require
   ```

5. **Install PostgreSQL driver** (already done):
   ```
   pip install asyncpg
   ```

6. **Run the application**: The tables will be automatically created when the application starts

## How Table Creation Works

The table creation happens in `init_db.py`:

```python
def create_db_and_tables():
    """
    Creates the database and all tables based on the defined models.
    This function should be called on application startup.
    """
    SQLModel.metadata.create_all(bind=engine)
```

This function is called on startup via the FastAPI event handler in `main.py`:

```python
@app.on_event("startup")
def on_startup():
    create_db_and_tables()
```

## Troubleshooting

- If tables still don't appear to be created, check that:
  1. Your Neon PostgreSQL connection string is correct
  2. Your database credentials are accurate
  3. The database server is accessible
  4. You have the necessary permissions to create tables

- If using the local SQLite version, check for the `todo_app.db` file in the backend directory