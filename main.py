from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional, List
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

SQLITE_DATABASE_URL = "sqlite:///./widgets.db"
engine = create_engine(SQLITE_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# DB Widget
class WidgetDB(Base):
    __tablename__ = "widgets"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(64), nullable=False)
    number_of_parts = Column(Integer, nullable=False)
    created_date = Column(DateTime, nullable=False)
    updated_date = Column(DateTime, nullable=False)

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Widgets API", description="A CRUD REST API for managing Widgets")

# API models
class Widget(BaseModel):
    name: str = Field(..., max_length=64, description="UTF8 string, limited to 64 chars")
    number_of_parts: int = Field(..., description="Integer, Number of parts in the widget")

class WidgetResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    name: str
    number_of_parts: int
    created_date: datetime
    updated_date: datetime

# Database dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/widgets")
def list_widgets(db: Session = Depends(get_db)):
    """List all widgets"""
    widgets = db.query(WidgetDB).all()
    
    return [WidgetResponse.model_validate(widget) for widget in widgets]

@app.post("/widgets")
def create_widget(widget: Widget, db: Session = Depends(get_db)):
    """Create a new widget"""
    now = datetime.now()
    
    db_widget = WidgetDB(
        name=widget.name,
        number_of_parts=widget.number_of_parts,
        created_date=now,
        updated_date=now
    )
    
    db.add(db_widget)
    db.commit()
    db.refresh(db_widget)
    
    return WidgetResponse.model_validate(db_widget)

@app.put("/widgets/{widget_id}")
def update_widget(widget_id: int, widget: Widget, db: Session = Depends(get_db)):
    """Update an existing widget"""
    db_widget = db.query(WidgetDB).filter(WidgetDB.id == widget_id).first()
    if not db_widget:
        raise HTTPException(status_code=404, detail="Widget not found")
    
    db_widget.name = widget.name
    db_widget.number_of_parts = widget.number_of_parts
    db_widget.updated_date = datetime.now()
    
    db.commit()
    db.refresh(db_widget)
    
    return WidgetResponse.model_validate(db_widget)

@app.get("/widgets/{widget_id}")
def get_widget(widget_id: int, db: Session = Depends(get_db)):
    """Retrieve a widget by ID"""
    db_widget = db.query(WidgetDB).filter(WidgetDB.id == widget_id).first()
    if not db_widget:
        raise HTTPException(status_code=404, detail="Widget not found")
    
    return WidgetResponse.model_validate(db_widget)

@app.delete("/widgets/{widget_id}")
def delete_widget(widget_id: int, db: Session = Depends(get_db)):
    """Delete a widget by ID"""
    db_widget = db.query(WidgetDB).filter(WidgetDB.id == widget_id).first()
    if not db_widget:
        raise HTTPException(status_code=404, detail="Widget not found")
    
    db.delete(db_widget)
    db.commit()
    
    return {"message": f"Widget {widget_id} deleted"} 