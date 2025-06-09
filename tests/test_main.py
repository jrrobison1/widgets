import pytest
from datetime import datetime
from unittest.mock import Mock
from fastapi import HTTPException

from src.widgets.main import list_widgets, create_widget, update_widget, get_widget, delete_widget
from src.widgets.schemas import Widget, WidgetResponse


@pytest.fixture
def mock_service():
    return Mock()


@pytest.fixture
def sample_widget():
    return Widget(name="Test Widget", number_of_parts=5)


@pytest.fixture
def sample_widget_response():
    return WidgetResponse(
        id=1,
        name="Test Widget", 
        number_of_parts=5,
        created_date=datetime.now(),
        updated_date=datetime.now()
    )


class TestWidgetControllers:
    def test_list_widgets_success(self, mock_service, sample_widget_response):
        mock_service.get_all_widgets.return_value = [sample_widget_response]
        
        result = list_widgets(service=mock_service)
        
        assert len(result) == 1
        assert result[0] == sample_widget_response
        mock_service.get_all_widgets.assert_called_once()
    
    def test_list_widgets_empty(self, mock_service):
        mock_service.get_all_widgets.return_value = []
        
        result = list_widgets(service=mock_service)
        
        assert result == []
        mock_service.get_all_widgets.assert_called_once()
    
    def test_create_widget_success(self, mock_service, sample_widget, sample_widget_response):
        mock_service.create_widget.return_value = sample_widget_response
        
        result = create_widget(widget=sample_widget, service=mock_service)
        
        assert result == sample_widget_response
        mock_service.create_widget.assert_called_once_with(sample_widget)
    
    def test_get_widget_success(self, mock_service, sample_widget_response):
        widget_id = 1
        mock_service.get_widget_by_id.return_value = sample_widget_response
        
        result = get_widget(widget_id=widget_id, service=mock_service)
        
        assert result == sample_widget_response
        mock_service.get_widget_by_id.assert_called_once_with(widget_id)
    
    def test_get_widget_not_found(self, mock_service):
        widget_id = 999
        mock_service.get_widget_by_id.return_value = None
        
        with pytest.raises(HTTPException) as exc_info:
            get_widget(widget_id=widget_id, service=mock_service)
        
        assert exc_info.value.status_code == 404
        assert exc_info.value.detail == "Widget not found"
        mock_service.get_widget_by_id.assert_called_once_with(widget_id)
    
    def test_update_widget_success(self, mock_service, sample_widget, sample_widget_response):
        widget_id = 1
        updated_response = WidgetResponse(
            id=1,
            name="Updated Widget",
            number_of_parts=10,
            created_date=sample_widget_response.created_date,
            updated_date=datetime.now()
        )
        mock_service.update_widget.return_value = updated_response
        
        result = update_widget(widget_id=widget_id, widget=sample_widget, service=mock_service)
        
        assert result == updated_response
        mock_service.update_widget.assert_called_once_with(widget_id, sample_widget)
    
    def test_update_widget_not_found(self, mock_service, sample_widget):
        widget_id = 999
        mock_service.update_widget.return_value = None
        
        with pytest.raises(HTTPException) as exc_info:
            update_widget(widget_id=widget_id, widget=sample_widget, service=mock_service)
        
        assert exc_info.value.status_code == 404
        assert exc_info.value.detail == "Widget not found"
        mock_service.update_widget.assert_called_once_with(widget_id, sample_widget)
    
    def test_delete_widget_success(self, mock_service):
        widget_id = 1
        mock_service.delete_widget.return_value = True
        
        result = delete_widget(widget_id=widget_id, service=mock_service)
        
        assert result == {"message": f"Widget {widget_id} deleted"}
        mock_service.delete_widget.assert_called_once_with(widget_id)
    
    def test_delete_widget_not_found(self, mock_service):
        widget_id = 999
        mock_service.delete_widget.return_value = False
        
        with pytest.raises(HTTPException) as exc_info:
            delete_widget(widget_id=widget_id, service=mock_service)
        
        assert exc_info.value.status_code == 404
        assert exc_info.value.detail == "Widget not found"
        mock_service.delete_widget.assert_called_once_with(widget_id) 