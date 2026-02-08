from sqlmodel import SQLModel
from database import engine
# Import all models to register them with SQLModel
# Import in a way that avoids circular imports
from models import User, Todo, Conversation, Message


def create_db_and_tables():
    """
    Creates the database and all tables based on the defined models.
    This function should be called on application startup.
    """
    SQLModel.metadata.create_all(bind=engine)


if __name__ == "__main__":
    create_db_and_tables()
    print("Database and tables created successfully!")