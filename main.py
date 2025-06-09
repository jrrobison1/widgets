from fastapi import FastAPI
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

app = FastAPI(title="Widgets API", description="A CRUD REST API for managing Widgets")


class Widget(BaseModel):
    name: str = Field(..., max_length=64, description="UTF8 string, limited to 64 chars")
    number_of_parts: int = Field(..., description="Integer, Number of parts in the widget")
    created_date: Optional[datetime] = Field(None, description="Created date")
    updated_date: Optional[datetime] = Field(None, description="Updated date")


@app.get("/widgets")
def list_widgets():
    """List all widgets"""
    return {"widgets": []}


@app.post("/widgets")
def create_widget(widget: Widget):
    """Create a new widget"""
    now = datetime.now()
    widget.created_date = now
    widget.updated_date = now
    
    return {"message": "Widget created", "widget": widget}


@app.put("/widgets/{widget_id}")
def update_widget(widget_id: int, widget: Widget):
    """Update an existing widget"""
    widget.updated_date = datetime.now()
    
    return {"message": f"Widget {widget_id} updated", "widget": widget} 

@app.get("/widgets/{widget_id}")
def get_widget(widget_id: int):
    """Retrieve a widget by ID"""
    
    mock_widget = Widget(
        name=f"Widget {widget_id}",
        number_of_parts=5,
        created_date=datetime.now(),
        updated_date=datetime.now()
    )
    return {"widget": mock_widget}


@app.delete("/widgets/{widget_id}")
def delete_widget(widget_id: int):
    """Delete a widget by ID"""
    return {"message": f"Widget {widget_id} deleted"} 