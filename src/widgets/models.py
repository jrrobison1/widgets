from sqlalchemy import Column, DateTime, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLITE_DATABASE_URL = "sqlite:///./widgets.db"
engine = create_engine(
    SQLITE_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class WidgetDB(Base):
    __tablename__ = "widgets"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(64), nullable=False)
    number_of_parts = Column(Integer, nullable=False)
    created_date = Column(DateTime, nullable=False)
    updated_date = Column(DateTime, nullable=False)


# Create the database tables
Base.metadata.create_all(bind=engine)
