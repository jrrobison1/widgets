from datetime import datetime
from typing import List, Optional
from sqlalchemy.orm import Session

from .models import WidgetDB, SessionLocal
from .schemas import Widget, WidgetResponse

class WidgetService:
    """Service layer for widget business logic and data conversion"""
    
    def _get_db(self) -> Session:
        """Internal method to get database session"""
        return SessionLocal()
    
    def get_all_widgets(self) -> List[WidgetResponse]:
        """Get all widgets from database"""
        db = self._get_db()
        try:
            widgets = db.query(WidgetDB).all()
            return [WidgetResponse.model_validate(widget) for widget in widgets]
        finally:
            db.close()
    
    def get_widget_by_id(self, widget_id: int) -> Optional[WidgetResponse]:
        """Get single widget by ID"""
        db = self._get_db()
        try:
            db_widget = db.query(WidgetDB).filter(WidgetDB.id == widget_id).first()
            if not db_widget:
                return None
            return WidgetResponse.model_validate(db_widget)
        finally:
            db.close()
    
    def create_widget(self, widget: Widget) -> WidgetResponse:
        """Create new widget."""
        db = self._get_db()
        try:
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
        finally:
            db.close()
    
    def update_widget(self, widget_id: int, widget: Widget) -> Optional[WidgetResponse]:
        """Update existing widget."""
        db = self._get_db()
        try:
            db_widget = db.query(WidgetDB).filter(WidgetDB.id == widget_id).first()
            if not db_widget:
                return None
            
            db_widget.name = widget.name
            db_widget.number_of_parts = widget.number_of_parts
            db_widget.updated_date = datetime.now()
            
            db.commit()
            db.refresh(db_widget)
            
            return WidgetResponse.model_validate(db_widget)
        finally:
            db.close()
    
    def delete_widget(self, widget_id: int) -> bool:
        """Delete widget by ID. Returns True if deleted, False if not found."""
        db = self._get_db()
        try:
            db_widget = db.query(WidgetDB).filter(WidgetDB.id == widget_id).first()
            if not db_widget:
                return False
            
            db.delete(db_widget)
            db.commit()
            return True
        finally:
            db.close()

widget_service = WidgetService() 