from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime

class Widget(BaseModel):
    """API model for creating/updating widgets"""
    name: str = Field(..., max_length=64, description="UTF8 string, limited to 64 chars")
    number_of_parts: int = Field(..., description="Integer, Number of parts in the widget")

class WidgetResponse(BaseModel):
    """API model for widget responses"""
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    name: str
    number_of_parts: int
    created_date: datetime
    updated_date: datetime 