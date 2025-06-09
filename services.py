from datetime import datetime
from typing import List, Optional
from sqlalchemy.orm import Session

from models import WidgetDB
from schemas import Widget, WidgetResponse

class WidgetService:
    """Service layer for widget business logic and data conversion"""
    
    def get_all_widgets(self, db: Session) -> List[WidgetResponse]:
        """Get all widgets from database"""
        widgets = db.query(WidgetDB).all()
        return [WidgetResponse.model_validate(widget) for widget in widgets]
    
    def get_widget_by_id(self, db: Session, widget_id: int) -> Optional[WidgetResponse]:
        """Get single widget by ID"""
        db_widget = db.query(WidgetDB).filter(WidgetDB.id == widget_id).first()
        if not db_widget:
            return None
        return WidgetResponse.model_validate(db_widget)
    
    def create_widget(self, db: Session, widget: Widget) -> WidgetResponse:
        """Create new widget."""
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
    
    def update_widget(self, db: Session, widget_id: int, widget: Widget) -> Optional[WidgetResponse]:
        """Update existing widget."""
        db_widget = db.query(WidgetDB).filter(WidgetDB.id == widget_id).first()
        if not db_widget:
            return None
        
        db_widget.name = widget.name
        db_widget.number_of_parts = widget.number_of_parts
        db_widget.updated_date = datetime.now()
        
        db.commit()
        db.refresh(db_widget)
        
        return WidgetResponse.model_validate(db_widget)
    
    def delete_widget(self, db: Session, widget_id: int) -> bool:
        """Delete widget by ID. Returns True if deleted, False if not found."""
        db_widget = db.query(WidgetDB).filter(WidgetDB.id == widget_id).first()
        if not db_widget:
            return False
        
        db.delete(db_widget)
        db.commit()
        return True

widget_service = WidgetService() 