import sys
import os
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from app import app, local_pets

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

def test_pet_detail_route(client):
    """Test individual pet page"""
    response = client.get('/pet/101')
    assert response.status_code == 200
    assert b'Buddy' in response.data

def test_search_pets(client):
    """Test pet search functionality"""
    response = client.get('/search?species=dog')
    assert response.status_code == 200
    
    response = client.get('/search?breed=Golden')
    assert response.status_code == 200

def test_quiz_route(client):
    """Test quiz page"""
    response = client.get('/quiz')
    assert response.status_code == 200
    assert b'Find Your Perfect Pet Match' in response.data

def test_api_pets(client):
    """Test pets API endpoint"""
    response = client.get('/api/pets')
    assert response.status_code == 200
    assert response.is_json

def test_api_stats(client):
    """Test stats API endpoint"""
    response = client.get('/api/status')
    assert response.status_code == 200
    assert response.is_json
    data = response.get_json()
    assert 'cat_api_working' in data

def test_add_pet_route(client):
    """Test add pet page"""
    response = client.get('/add-pet')
    assert response.status_code == 200

def test_pet_data_structure():
    """Test that pet data has required fields"""
    for pet in local_pets:
        assert 'id' in pet
        assert 'name' in pet
        assert 'species' in pet
        assert 'adopted' in pet

def test_test_endpoint(client):
    """Test test endpoint exists"""
    response = client.get('/test')
    assert response.status_code == 200
    assert response.is_json
    data = response.get_json()
    assert data['status'] == 'success'

def test_debug_endpoint(client):
    """Test debug endpoint exists"""
    response = client.get('/debug')
    assert response.status_code == 200
    assert response.is_json
    data = response.get_json()
    assert 'total_pets' in data
    assert 'local_pets' in data
    assert 'api_pets' in data

def test_favorites_route(client):
    """Test favorites page"""
    response = client.get('/favorites')
    assert response.status_code == 200

def test_admin_routes(client):
    """Test admin routes (they should work with session)"""
    with client.session_transaction() as sess:
        sess['is_admin'] = True
    
    response = client.get('/admin')
    assert response.status_code == 200
    
    response = client.get('/admin/adoptions')
    assert response.status_code == 200

def test_adoption_flow(client):
    """Test adoption form access"""
    response = client.get('/adopt/101')
    assert response.status_code == 200
    assert b'Adoption Application' in response.data

def test_quiz_results_post(client):
    """Test quiz results with POST data"""
    response = client.post('/quiz/results', data={
        'home_type': 'apartment',
        'activity_level': 'medium',
        'experience': 'first_time',
        'time_commitment': 'medium',
        'family_situation': 'alone'
    })
    assert response.status_code == 200