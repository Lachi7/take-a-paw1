import os
import requests
import random
import urllib.parse
from flask import Flask, render_template, jsonify, request, session, redirect, url_for, flash
from datetime import datetime
from dotenv import load_dotenv
from time import monotonic

load_dotenv()

app = Flask(__name__)
APP_START_MONO = monotonic()
APP_START_ISO = datetime.now().isoformat()
APP_VERSION = os.getenv("APP_VERSION", "0.1.0")
app.secret_key = os.getenv('SECRET_KEY', 'dev-secret-key')

print("🚀 Take A Paw application starting...")

class PetAPI: 
    def __init__(self):
        self.cat_api_key = os.getenv('CAT_API_KEY')
        self.dog_api_key = os.getenv('DOG_API_KEY')
        self.api_pets_cache = []  # Cache for API pets to keep them consistent
    
    def get_cats(self, limit=5):
        """Get real cat data from The Cat API"""
        try:
            url = f"https://api.thecatapi.com/v1/images/search?limit={limit}&has_breeds=1"
            headers = {'x-api-key': self.cat_api_key}
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            cats = []
            for i, cat_data in enumerate(response.json()):
                breed = cat_data.get('breeds', [{}])[0] if cat_data.get('breeds') else {}
                # Create unique but consistent ID
                cat_id = f"api_cat_{i+1000}"
                cats.append({
                    'id': cat_id,
                    'name': self._generate_pet_name(breed.get('name'), 'cat'),
                    'species': 'Cat',
                    'breed': breed.get('name', 'Mixed Breed'),
                    'age': self._get_realistic_age('cat'),
                    'gender': self._get_realistic_gender(),
                    'location': self._get_shelter_location(),
                    'description': breed.get('description', 'A lovely cat looking for a home.')[:200] + '...',
                    'image': cat_data['url'],
                    'adopted': False,
                    'source': 'api',
                    'personality': self._get_cat_personality(breed.get('temperament', ''))
                })
            return cats
        except Exception as e:
            print(f"Cat API error: {e}")
            return []
    
    def get_dogs(self, limit=5):
        """Get real dog data from The Dog API"""
        try:
            url = f"https://api.thedogapi.com/v1/images/search?limit={limit}&has_breeds=1"
            headers = {'x-api-key': self.dog_api_key}
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            dogs = []
            for i, dog_data in enumerate(response.json()):
                breed = dog_data.get('breeds', [{}])[0] if dog_data.get('breeds') else {}
                # Create unique but consistent ID
                dog_id = f"api_dog_{i+2000}"
                dogs.append({
                    'id': dog_id,
                    'name': self._generate_pet_name(breed.get('name'), 'dog'),
                    'species': 'Dog',
                    'breed': breed.get('name', 'Mixed Breed'),
                    'age': self._get_realistic_age('dog'),
                    'gender': self._get_realistic_gender(),
                    'location': self._get_shelter_location(),
                    'description': breed.get('description', 'A friendly dog looking for a forever home.')[:200] + '...',
                    'image': dog_data['url'],
                    'adopted': False,
                    'source': 'api',
                    'personality': self._get_dog_personality(breed.get('temperament', ''))
                })
            return dogs
        except Exception as e:
            print(f"Dog API error: {e}")
            return []
    
    def _generate_pet_name(self, breed_name, species):
        """Generate realistic individual pet names"""
        cat_names = ['Luna', 'Bella', 'Lucy', 'Kitty', 'Chloe', 'Sophie', 'Lily', 'Molly', 'Nala', 'Cleo']
        dog_names = ['Buddy', 'Max', 'Charlie', 'Cooper', 'Jack', 'Bear', 'Duke', 'Tucker', 'Rocky', 'Bailey']
        
        if species == 'cat':
            return random.choice(cat_names)
        else:
            return random.choice(dog_names)
    
    def _get_realistic_age(self, species):
        """More realistic age distribution"""
        ages = {
            'young': ['4 months', '6 months', '8 months', '1 year'],
            'adult': ['1 year', '2 years', '3 years', '4 years', '5 years'],
            'senior': ['6 years', '7 years', '8 years', '9 years', '10 years']
        }
        age_group = random.choices(['young', 'adult', 'senior'], weights=[0.3, 0.5, 0.2])[0]
        return random.choice(ages[age_group])
    
    def _get_realistic_gender(self):
        """Realistic gender distribution"""
        return random.choice(['Male', 'Male', 'Female', 'Female'])  # Equal distribution
    
    def _get_shelter_location(self):
        """Realistic shelter names with locations"""
        shelters = [
            'Hope Animal Shelter, New York, NY',
            'Paws Rescue Center, Los Angeles, CA', 
            'Happy Tails Sanctuary, Chicago, IL',
            'Second Chance Pets, Houston, TX',
            'Furry Friends Rescue, Phoenix, AZ',
            'Animal Haven, Philadelphia, PA',
            'Safe Haven Rescue, San Antonio, TX',
            'Pet Promise, San Diego, CA'
        ]
        return random.choice(shelters)
    
    def _get_cat_personality(self, temperament):
        if not temperament:
            return ['affectionate', 'playful', 'gentle']
        traits = temperament.lower().split(', ')
        return [trait.strip() for trait in traits if trait.strip()][:5]  # Limit to 5 traits
    
    def _get_dog_personality(self, temperament):
        if not temperament:
            return ['friendly', 'loyal', 'playful']
        traits = temperament.lower().split(', ')
        return [trait.strip() for trait in traits if trait.strip()][:5]  # Limit to 5 traits
    
    def get_all_pets(self):
        """Get both cats and dogs from real APIs - with caching"""
        # Only fetch from API if cache is empty
        if not self.api_pets_cache:
            print("🔄 Fetching fresh data from APIs...")
            cats = self.get_cats(5)
            dogs = self.get_dogs(5)
            self.api_pets_cache = cats + dogs
            print(f"✅ Cached {len(self.api_pets_cache)} API pets")
        else:
            print(f"✅ Using cached {len(self.api_pets_cache)} API pets")
        
        return self.api_pets_cache.copy()  # Return a copy to prevent modification
    
    def _uptime_seconds() -> float:
        return round(monotonic() - APP_START_MONO, 2)


# Initialize the API 
pet_api = PetAPI()

# Your existing local pets data
local_pets = [ 
    {
        'id': 101, 'name': 'Buddy', 'species': 'Dog', 'breed': 'Golden Retriever', 
        'age': '2 years', 'gender': 'Male', 'location': 'Hope Animal Shelter, New York, NY',
        'description': 'Friendly and energetic. Loves playing fetch! Great with kids and other pets.',
        'image': 'https://images.unsplash.com/photo-1552053831-71594a27632d?w=400&h=300&fit=crop',
        'adopted': False, 'source': 'local', 
        'personality': ['active', 'friendly', 'playful', 'family-friendly', 'easy']
    },
    {
        'id': 102, 'name': 'Luna', 'species': 'Cat', 'breed': 'Siamese', 
        'age': '1 year', 'gender': 'Female', 'location': 'Paws Rescue Center, Los Angeles, CA',
        'description': 'Affectionate and loves cuddles. Prefers a quiet home without other pets.',
        'image': 'https://images.unsplash.com/photo-1514888286974-6c03e2ca1dba?w=400&h=300&fit=crop',
        'adopted': False, 'source': 'local', 
        'personality': ['calm', 'affectionate', 'independent', 'quiet']
    },
    {
        'id': 103, 'name': 'Max', 'species': 'Dog', 'breed': 'Beagle',
        'age': '3 years', 'gender': 'Male', 'location': 'Happy Tails Sanctuary, Chicago, IL', 
        'description': 'Curious and friendly, great with kids. Loves exploring and long walks.',
        'image': 'https://images.pexels.com/photos/46505/swiss-shepherd-dog-dog-pet-portrait-46505.jpeg',
        'adopted': False, 'source': 'local', 
        'personality': ['friendly', 'curious', 'family-friendly', 'active', 'easy']
    }
]

# User favorites and session data - FIXED: Initialize with default user
users_favorites = {'default': []}
adoption_requests = []

# Global cache for all pets
all_pets_cache = []

def get_all_available_pets():
    """Get all pets with persistent caching - FIXED VERSION"""
    global all_pets_cache
    
    # Always include local_pets and refresh API pets if cache is empty
    if not all_pets_cache:
        print("🔄 Initializing pet cache...")
        try:
            api_pets = pet_api.get_all_pets()
            all_pets_cache = local_pets + api_pets
            print(f"✅ Total pets in cache: {len(all_pets_cache)}")
            
            # Print API pets for debugging
            api_pets_list = [p for p in all_pets_cache if p.get('source') == 'api']
            print(f"🔍 API Pets: {[p['name'] + ' (ID: ' + str(p['id']) + ')' for p in api_pets_list]}")
            
        except Exception as e:
            print(f"❌ Error fetching pets: {e}")
            all_pets_cache = local_pets.copy()
    else:
        # Always ensure local_pets are included (for newly added pets)
        current_local_ids = [p['id'] for p in local_pets]
        current_cache_ids = [p['id'] for p in all_pets_cache]
        
        # Add any local pets that are missing from cache
        for local_pet in local_pets:
            if local_pet['id'] not in current_cache_ids:
                all_pets_cache.append(local_pet)
                print(f"✅ Added missing local pet to cache: {local_pet['name']}")
    
    return [pet for pet in all_pets_cache if not pet.get('adopted', False)]

def find_pet_by_id(pet_id):
    """Find pet by ID in the persistent cache"""
    available_pets = get_all_available_pets()
    
    # Try exact match
    for pet in available_pets:
        if str(pet['id']) == str(pet_id):
            print(f"✅ Found pet: {pet['name']} (ID: {pet['id']})")
            return pet
    
    print(f"❌ Pet not found: {pet_id}")
    print(f"🔍 Available IDs: {[p['id'] for p in available_pets]}")
    return None

# Routes
@app.route('/')
def index():
    """Homepage with pets from both local data and real APIs"""
    available_pets = get_all_available_pets()
    print(f"🏠 Displaying {len(available_pets)} pets on homepage")
    print(f"🔍 Local pets: {[p['name'] for p in available_pets if p.get('source') == 'local']}")
    return render_template('index.html', pets=available_pets, title="Available Pets")

@app.route('/search')
def search_pets():
    """Search pets by criteria"""
    species = request.args.get('species', '')
    breed = request.args.get('breed', '')
    location = request.args.get('location', '')
    
    available_pets = get_all_available_pets()
    
    if species:
        available_pets = [p for p in available_pets if p['species'].lower() == species.lower()]
    
    if breed:
        available_pets = [p for p in available_pets if breed.lower() in p['breed'].lower()]
    
    if location:
        available_pets = [p for p in available_pets if location.lower() in p['location'].lower()]
    
    return render_template('index.html', pets=available_pets, title="Search Results")

@app.route('/pet/<pet_id>')
def pet_detail(pet_id):
    """Individual pet profile page"""
    print(f"🔍 Looking for pet: {pet_id}")
    pet = find_pet_by_id(pet_id)
    
    if not pet:
        flash('Pet not found', 'error')
        return redirect(url_for('index'))
    
    return render_template('pet_detail.html', pet=pet)

@app.route('/adopt/<pet_id>')
def adopt_pet_form(pet_id):
    """Adoption form page"""
    print(f"🔍 Adoption form for pet: {pet_id}")
    pet = find_pet_by_id(pet_id)
    
    if not pet:
        flash('Pet not found', 'error')
        return redirect(url_for('index'))
    
    if pet.get('adopted'):
        flash('This pet has already been adopted!', 'error')
        return redirect(url_for('pet_detail', pet_id=pet_id))
    
    print(f"✅ Showing adoption form for: {pet['name']}")
    return render_template('adopt_form.html', pet=pet)

@app.route('/adopt/<pet_id>/submit', methods=['POST'])
def submit_adoption(pet_id):
    """Process adoption form submission"""
    print(f"🔍 Processing adoption for pet: {pet_id}")
    pet = find_pet_by_id(pet_id)
    
    if not pet:
        flash('Pet not found', 'error')
        return redirect(url_for('index'))
    
    if pet.get('adopted'):
        flash('This pet has already been adopted!', 'error')
        return redirect(url_for('pet_detail', pet_id=pet_id))
    
    # Collect adoption data - STORE ALL PET INFO
    adoption_data = {
        'pet_id': str(pet['id']),
        'pet_name': pet['name'],
        'pet_species': pet['species'],
        'pet_breed': pet['breed'],
        'pet_age': pet['age'],
        'pet_image': pet['image'],
        'pet_source': pet.get('source', 'unknown'),
        'timestamp': datetime.now().isoformat(),
        'status': 'pending',
        'applicant_info': {
            'full_name': request.form.get('full_name'),
            'email': request.form.get('email'),
            'phone': request.form.get('phone'),
            'address': request.form.get('address'),
            'city': request.form.get('city'),
            'state': request.form.get('state'),
            'zip_code': request.form.get('zip_code'),
            'housing_type': request.form.get('housing_type'),
            'has_yard': request.form.get('has_yard'),
            'has_other_pets': request.form.get('has_other_pets'),
            'other_pets_details': request.form.get('other_pets_details'),
            'experience_with_pets': request.form.get('experience_with_pets'),
            'hours_alone': request.form.get('hours_alone'),
            'adoption_reason': request.form.get('adoption_reason'),
            'vet_reference': request.form.get('vet_reference')
        }
    }
    
    # Store adoption request
    adoption_requests.append(adoption_data)
    
    # Mark pet as adopted in cache
    for p in all_pets_cache:
        if str(p['id']) == str(pet_id):
            p['adopted'] = True
            print(f"✅ Marked {p['name']} as adopted")
            break
    
    return redirect(url_for('adoption_confirmation', request_id=len(adoption_requests)-1))

@app.route('/adoption/confirmation/<int:request_id>')
def adoption_confirmation(request_id):
    """Adoption confirmation page - FIXED VERSION"""
    if request_id >= len(adoption_requests):
        flash('Invalid adoption request', 'error')
        return redirect(url_for('index'))
    
    adoption_request = adoption_requests[request_id]
    
    # Create pet object from adoption data - DON'T rely on cache
    pet = {
        'id': adoption_request['pet_id'],
        'name': adoption_request['pet_name'],
        'species': adoption_request.get('pet_species', 'Unknown'),
        'breed': adoption_request.get('pet_breed', 'Unknown'),
        'age': adoption_request.get('pet_age', 'Unknown'),
        'image': adoption_request.get('pet_image', '/static/placeholder-pet.jpg'),
        'adopted': True,
        'source': adoption_request.get('pet_source', 'api')
    }
    
    print(f"✅ Showing confirmation for: {pet['name']}")
    
    return render_template('adoption_confirmation.html', 
                         adoption_request=adoption_request, 
                         pet=pet,
                         request_id=request_id)

@app.route('/quiz')
def quiz():
    return render_template('quiz.html')

@app.route('/quiz/results', methods=['POST'])
def quiz_results():
    answers = {
        'home_type': request.form.get('home_type'),
        'activity_level': request.form.get('activity_level'),
        'experience': request.form.get('experience'),
        'time_commitment': request.form.get('time_commitment'),
        'family_situation': request.form.get('family_situation')
    }
    
    available_pets = get_all_available_pets()
    matched_pets = []
    
    for pet in available_pets:
        if not pet.get('adopted', False):
            score = 0
            
            if answers['activity_level'] == 'high' and 'active' in pet.get('personality', []):
                score += 2
            elif answers['activity_level'] == 'low' and 'calm' in pet.get('personality', []):
                score += 2
            elif answers['activity_level'] == 'medium':
                score += 1
            
            if answers['home_type'] == 'apartment' and pet['species'] == 'Cat':
                score += 2
            elif answers['home_type'] == 'house' and pet['species'] == 'Dog':
                score += 1
            
            if answers['experience'] == 'first_time' and 'easy' in pet.get('personality', []):
                score += 2
            elif answers['experience'] == 'experienced' and pet['species'] == 'Dog':
                score += 1
            
            if answers['family_situation'] == 'children' and 'family-friendly' in pet.get('personality', []):
                score += 2
            elif answers['family_situation'] == 'other_pets' and 'friendly' in pet.get('personality', []):
                score += 1
            
            if score > 0:
                pet['match_score'] = min(score, 5)
                matched_pets.append(pet)
    
    matched_pets.sort(key=lambda x: x.get('match_score', 0), reverse=True)
    return render_template('quiz_results.html', pets=matched_pets, answers=answers)

@app.route('/favorites')
def view_favorites():
    """View favorite pets - FIXED VERSION"""
    user_id = session.get('user_id', 'default')
    available_pets = get_all_available_pets()
    
    # Get the user's favorite pet IDs
    favorite_ids = users_favorites.get(user_id, [])
    print(f"🔍 User {user_id} favorites: {favorite_ids}")
    print(f"🔍 Available pets: {[p['id'] for p in available_pets]}")
    
    # Filter pets that are in favorites
    favorite_pets = [pet for pet in available_pets if str(pet['id']) in favorite_ids]
    print(f"✅ Found {len(favorite_pets)} favorite pets: {[p['name'] for p in favorite_pets]}")
    
    return render_template('favorites.html', pets=favorite_pets)

@app.route('/favorite/<pet_id>', methods=['POST'])
def favorite_pet(pet_id):
    """Add pet to favorites - FIXED VERSION"""
    user_id = session.get('user_id', 'default')
    
    # Ensure user exists in favorites
    if user_id not in users_favorites:
        users_favorites[user_id] = []
    
    # Convert to string to ensure consistent comparison
    pet_id_str = str(pet_id)
    
    if pet_id_str not in users_favorites[user_id]:
        users_favorites[user_id].append(pet_id_str)
        print(f"✅ Added {pet_id_str} to favorites for user {user_id}")
        print(f"📊 Current favorites: {users_favorites[user_id]}")
        return jsonify({'success': True, 'message': 'Added to favorites', 'favorites': users_favorites[user_id]})
    else:
        # Remove from favorites if already there (toggle)
        users_favorites[user_id].remove(pet_id_str)
        print(f"✅ Removed {pet_id_str} from favorites for user {user_id}")
        print(f"📊 Current favorites: {users_favorites[user_id]}")
        return jsonify({'success': True, 'message': 'Removed from favorites', 'favorites': users_favorites[user_id]})

@app.route('/add-pet', methods=['GET', 'POST'])
def add_pet():
    """Add new pet page - FIXED VERSION"""
    if request.method == 'POST':
        # Handle form submission
        new_pet_id = max([p['id'] for p in local_pets]) + 1 if local_pets else 1000
        new_pet = {
            'id': new_pet_id,
            'name': request.form.get('name'),
            'species': request.form.get('species'),
            'breed': request.form.get('breed'),
            'age': request.form.get('age'),
            'gender': request.form.get('gender'),
            'location': request.form.get('location'),
            'description': request.form.get('description'),
            'image': get_placeholder_image(request.form.get('species'), request.form.get('breed')),
            'adopted': False,
            'source': 'local',
            'personality': ['friendly', 'loving']  # Default personality
        }
        local_pets.append(new_pet)
        
        # Clear cache to force refresh including new pet
        global all_pets_cache
        all_pets_cache = []
        
        print(f"✅ Added new pet: {new_pet['name']} (ID: {new_pet_id})")
        print(f"📊 Total local pets now: {len(local_pets)}")
        
        flash(f'{new_pet["name"]} has been added to the platform!', 'success')
        return redirect(url_for('index'))
    
    # Mock breed data for the form - FIXED: Use simple lists
    dog_breeds = ['Labrador Retriever', 'German Shepherd', 'Golden Retriever', 'Bulldog', 'Beagle', 'Other']
    cat_breeds = ['Siamese', 'Persian', 'Maine Coon', 'Bengal', 'Ragdoll', 'Other']
    
    return render_template('add_pet.html', dog_breeds=dog_breeds, cat_breeds=cat_breeds)

def get_placeholder_image(species, breed=None):
    """Get placeholder image"""
    if species.lower() == 'dog':
        return 'https://images.unsplash.com/photo-1552053831-71594a27632d?w=400&h=300&fit=crop'
    else:
        return 'https://images.unsplash.com/photo-1514888286974-6c03e2ca1dba?w=400&h=300&fit=crop'

# Admin routes
@app.route('/admin')
def admin_dashboard():
    session['is_admin'] = True
    available_pets = get_all_available_pets()
    adopted_pets = [pet for pet in available_pets if pet.get('adopted')]
    available_pets = [pet for pet in available_pets if not pet.get('adopted')]
    return render_template('admin.html', adopted_pets=adopted_pets, available_pets=available_pets)

@app.route('/admin/adoptions')
def admin_adoptions():
    session['is_admin'] = True
    return render_template('admin_adoptions.html', adoption_requests=adoption_requests)

# API endpoints
@app.route('/api/status')
def api_status():
    try:
        cat_test = len(pet_api.get_cats(1)) > 0
        dog_test = len(pet_api.get_dogs(1)) > 0
        return jsonify({
            'cat_api_working': cat_test,
            'dog_api_working': dog_test,
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({
            'cat_api_working': False,
            'dog_api_working': False,
            'error': str(e)
        }), 500

@app.route('/api/pets')
def api_pets():
    available_pets = get_all_available_pets()
    return jsonify(available_pets)

@app.route('/test')
def test():
    return jsonify({"status": "success", "message": "Take A Paw is working! 🐾"})

# Debug route
@app.route('/debug')
def debug():
    available_pets = get_all_available_pets()
    return jsonify({
        "total_pets": len(available_pets),
        "local_pets": len([p for p in available_pets if p.get('source') == 'local']),
        "api_pets": len([p for p in available_pets if p.get('source') == 'api']),
        "pet_ids": [{"id": p['id'], "name": p['name'], "source": p.get('source')} for p in available_pets],
        "favorites": users_favorites,
        "local_pets_list": [{"id": p['id'], "name": p['name']} for p in local_pets]
    })

# Route to clear cache and refresh API data
@app.route('/refresh-pets')
def refresh_pets():
    global all_pets_cache
    all_pets_cache = []  # Clear cache
    pet_api.api_pets_cache = []  # Clear API cache
    flash('Pet data refreshed from APIs!', 'success')
    return redirect(url_for('index'))
def _health_view():
    available_pets = get_all_available_pets()
    total = len(available_pets)
    local_count = sum(1 for p in available_pets if p.get('source') == 'local')
    api_count  = sum(1 for p in available_pets if p.get('source') == 'api')
    return jsonify({
        "status": "ok",
        "service": "take-a-paw",
        "time": datetime.now().isoformat(),
        "caches": {
            "all_pets_cache_size": len(all_pets_cache),
            "api_pets_cache_size": len(pet_api.api_pets_cache)
        },
        "pets": {
            "total_available": total,
            "local_available": local_count,
            "api_available": api_count
        }
    }), 200

# Decorator registration
@app.route("/api/health", methods=["GET"])
def api_health():
    return _health_view()

# Explicit add_url_rule registration (works even if decorators got skipped earlier)
app.add_url_rule("/api/health", endpoint="api_health_alt", view_func=_health_view, methods=["GET"])


# Error handlers
@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500

if __name__ == '__main__':
    print("🎯 Starting Flask development server...")
    print("🌐 App will be available at: http://localhost:5000")
    print("📱 And also at: http://127.0.0.1:5000")
    print("🛑 Press Ctrl+C to stop the server")
    
    try:
        app.run(host='0.0.0.0', port=5000, debug=True)
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        app.run(host='0.0.0.0', port=5001, debug=True)