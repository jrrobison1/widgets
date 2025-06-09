from fastapi import FastAPI, HTTPException
from typing import List

from .schemas import Widget, WidgetResponse
from .services import widget_service

app = FastAPI(title="Widgets API", description="A CRUD REST API for managing Widgets")

@app.get("/widgets", response_model=List[WidgetResponse])
def list_widgets():
    """List all widgets"""
    return widget_service.get_all_widgets()

@app.post("/widgets", response_model=WidgetResponse)
def create_widget(widget: Widget):
    """Create a new widget"""
    return widget_service.create_widget(widget)

@app.put("/widgets/{widget_id}", response_model=WidgetResponse)
def update_widget(widget_id: int, widget: Widget):
    """Update an existing widget"""
    updated_widget = widget_service.update_widget(widget_id, widget)
    if not updated_widget:
        raise HTTPException(status_code=404, detail="Widget not found")
    return updated_widget

@app.get("/widgets/{widget_id}", response_model=WidgetResponse)
def get_widget(widget_id: int):
    """Retrieve a widget by ID"""
    widget = widget_service.get_widget_by_id(widget_id)
    if not widget:
        raise HTTPException(status_code=404, detail="Widget not found")
    return widget

@app.delete("/widgets/{widget_id}")
def delete_widget(widget_id: int):
    """Delete a widget by ID"""
    deleted = widget_service.delete_widget(widget_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Widget not found")
    return {"message": f"Widget {widget_id} deleted"} 