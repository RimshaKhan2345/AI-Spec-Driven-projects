from sqlmodel import SQLModel
from database import engine
from models import User, Todo  # Import all models to register them with SQLModel


def create_db_and_tables():
    """
    Creates the database and all tables based on the defined models.
    This function should be called on application startup.
    """
    SQLModel.metadata.create_all(bind=engine)


if __name__ == "__main__":
    create_db_and_tables()
    print("Database and tables created successfully!")