import pytest
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.widgets.models import Base, WidgetDB, SessionLocal
from src.widgets.schemas import Widget
from src.widgets.services import WidgetService


@pytest.fixture
def widget_service(monkeypatch):
    # Create in-memory database
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=engine)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    service = WidgetService()
    monkeypatch.setattr(service, '_get_db', TestingSessionLocal)
    
    return service


@pytest.fixture
def sample_widget():
    return Widget(name="Test Widget", number_of_parts=5)


class TestWidgetService:
    def test_create_widget(self, widget_service, sample_widget):
        result = widget_service.create_widget(sample_widget)
        
        assert result.id == 1
        assert result.name == "Test Widget"
        assert result.number_of_parts == 5
        assert result.created_date is not None
        assert result.updated_date is not None
        assert result.created_date == result.updated_date
    
    def test_get_all_widgets_empty(self, widget_service):
        result = widget_service.get_all_widgets()
        assert result == []
    
    def test_get_all_widgets_with_data(self, widget_service, sample_widget):
        created = widget_service.create_widget(sample_widget)
        
        result = widget_service.get_all_widgets()
        
        assert len(result) == 1
        assert result[0].id == created.id
        assert result[0].name == created.name
    
    def test_get_widget_by_id_exists(self, widget_service, sample_widget):
        created = widget_service.create_widget(sample_widget)
        
        result = widget_service.get_widget_by_id(created.id)
        
        assert result is not None
        assert result.id == created.id
        assert result.name == "Test Widget"
    
    def test_get_widget_by_id_not_exists(self, widget_service):
        result = widget_service.get_widget_by_id(999)
        assert result is None
    
    def test_update_widget_exists(self, widget_service, sample_widget):
        created = widget_service.create_widget(sample_widget)
        
        updated_widget = Widget(name="Updated Widget", number_of_parts=10)
        result = widget_service.update_widget(created.id, updated_widget)
        
        assert result is not None
        assert result.id == created.id
        assert result.name == "Updated Widget"
        assert result.number_of_parts == 10
        assert result.created_date == created.created_date  # Should stay the same
        assert result.updated_date > created.updated_date   # Should be newer
    
    def test_update_widget_not_exists(self, widget_service, sample_widget):
        result = widget_service.update_widget(999, sample_widget)
        assert result is None
    
    def test_delete_widget_exists(self, widget_service, sample_widget):
        created = widget_service.create_widget(sample_widget)
        
        result = widget_service.delete_widget(created.id)
        assert result is True
        
        deleted_widget = widget_service.get_widget_by_id(created.id)
        assert deleted_widget is None
    
    def test_delete_widget_not_exists(self, widget_service):
        result = widget_service.delete_widget(999)
        assert result is False 