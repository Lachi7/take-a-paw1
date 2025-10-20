import sys
import os
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from app import app, pet_api

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_index_route(client):
    """Test the home page returns successfully"""
    response = client.get('/')
    assert response.status_code == 200
    assert b'Find Your Perfect Pet Companion' in response.data

def test_pet_api_real_data():
    """Test PetAPI real data generation"""
    pets = pet_api.get_all_pets()
    assert isinstance(pets, list)

def test_breeds_api(client):
    """Test breeds API endpoints"""
    response = client.get('/api/pets')
    assert response.status_code == 200
    assert response.is_json

def test_petfinder_api(client):
    """Test PetFinder-like API endpoint"""
    response = client.get('/api/pets')
    assert response.status_code == 200
    assert response.is_json

def test_placeholder_images():
    """Test placeholder image generation"""
    from app import get_placeholder_image
    dog_image = get_placeholder_image('dog', 'Labrador')
    cat_image = get_placeholder_image('cat', 'Siamese')
    
    assert 'unsplash.com' in dog_image
    assert 'unsplash.com' in cat_image

def test_real_apis_connection(client):
    """Test that real APIs are accessible"""
    response = client.get('/api/status')
    assert response.status_code == 200
    data = response.get_json()
    assert 'cat_api_working' in data
    assert 'dog_api_working' in data

def test_pet_api_integration():
    """Test PetAPI class methods"""
    from app import pet_api
    # Test that API methods don't crash
    cats = pet_api.get_cats(1)
    dogs = pet_api.get_dogs(1)
    # We're just testing that the methods run without errors
    assert isinstance(cats, list)
    assert isinstance(dogs, list)

def test_search_pets(client):
    """Test pet search functionality"""
    response = client.get('/search?species=dog')
    assert response.status_code == 200
    
    response = client.get('/search?breed=Golden')
    assert response.status_code == 200

def test_health_endpoint(client):
    """Test health check endpoint"""
    response = client.get('/health')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'healthy'