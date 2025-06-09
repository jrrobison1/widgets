from fastapi import FastAPI, HTTPException, Depends
from typing import List

from .schemas import Widget, WidgetResponse
from .services import WidgetService, widget_service

app = FastAPI(title="Widgets API", description="A CRUD REST API for managing Widgets")

# Service dependency
def get_widget_service() -> WidgetService:
    return widget_service

@app.get("/widgets", response_model=List[WidgetResponse])
def list_widgets(service: WidgetService = Depends(get_widget_service)):
    """List all widgets"""
    return service.get_all_widgets()

@app.post("/widgets", response_model=WidgetResponse)
def create_widget(widget: Widget, service: WidgetService = Depends(get_widget_service)):
    """Create a new widget"""
    return service.create_widget(widget)

@app.put("/widgets/{widget_id}", response_model=WidgetResponse)
def update_widget(widget_id: int, widget: Widget, service: WidgetService = Depends(get_widget_service)):
    """Update an existing widget"""
    updated_widget = service.update_widget(widget_id, widget)
    if not updated_widget:
        raise HTTPException(status_code=404, detail="Widget not found")
    return updated_widget

@app.get("/widgets/{widget_id}", response_model=WidgetResponse)
def get_widget(widget_id: int, service: WidgetService = Depends(get_widget_service)):
    """Retrieve a widget by ID"""
    widget = service.get_widget_by_id(widget_id)
    if not widget:
        raise HTTPException(status_code=404, detail="Widget not found")
    return widget

@app.delete("/widgets/{widget_id}")
def delete_widget(widget_id: int, service: WidgetService = Depends(get_widget_service)):
    """Delete a widget by ID"""
    deleted = service.delete_widget(widget_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Widget not found")
    return {"message": f"Widget {widget_id} deleted"} 