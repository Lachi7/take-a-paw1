# seed.py
from app import create_app
from app.db import db
from app.models import Pet

SEED = [
    {
        "name": "Buddy", "species": "Dog", "breed": "Golden Retriever", "age": "2 years",
        "gender": "Male", "location": "Hope Animal Shelter, New York, NY",
        "description": "Friendly and energetic. Loves playing fetch! Great with kids and pets.",
        "image": "https://images.unsplash.com/photo-1552053831-71594a27632d?w=900&h=600&fit=crop",
        "adopted": False, "source": "catalog", "owner_id": None,
        "home_type": "apartment",
        "activity_level": "low",
        "experience": "some",
        "time_commitment": "1_3_hours",
        "family_situation": "yes",
        "contact_email_override": "shelter@example.com",
        "contact_phone_override": "+1 555 0100",
        "public_contact": True
    },
    {
        "name": "Luna", "species": "Cat", "breed": "Siamese", "age": "1 year",
        "gender": "Female", "location": "Paws Rescue Center, Los Angeles, CA",
        "description": "Affectionate and cuddly; prefers a calm home.",
        "image": "https://images.unsplash.com/photo-1514888286974-6c03e2ca1dba?w=900&h=600&fit=crop",
        "adopted": False, "source": "catalog", "owner_id": None,
        "home_type": "house",
        "activity_level": "medium",
        "experience": "some",
        "time_commitment": "1_3_hours",
        "family_situation": "no",
        "contact_email_override": "shelter@example.com",
        "contact_phone_override": "+1 555 0101",
        "public_contact": True
    },
    {
        "name": "Max", "species": "Dog", "breed": "Beagle", "age": "3 years",
        "gender": "Male", "location": "Happy Tails Sanctuary, Chicago, IL",
        "description": "Curious, friendly explorer who loves long walks.",
        "image": "https://images.pexels.com/photos/46505/swiss-shepherd-dog-dog-pet-portrait-46505.jpeg",
        "adopted": False, "source": "catalog", "owner_id": None,
        "home_type": "apartment",
        "activity_level": "high",
        "experience": "a_lot",
        "time_commitment": "more_than_3_hours",
        "family_situation": "yes",
        "contact_email_override": "shelter@example.com",
        "contact_phone_override": "+1 555 0102",
        "public_contact": True
    }
]


def main():
    app = create_app()
    with app.app_context():
        print("DB URI:", app.config["SQLALCHEMY_DATABASE_URI"])
        db.create_all()

        current = Pet.query.count()
        print("Existing pets:", current)

        if current == 0:
            for row in SEED:
                db.session.add(Pet(**row))
            db.session.commit()
            print(f"Seeded {len(SEED)} pets.")
        else:
            print("Pets already exist; skipping seed.")

        # Show a quick sample
        pets = Pet.query.all()
        print("Now total pets:", len(pets))
        for p in pets[:3]:
            print(" -", p.id, p.name, p.species, "(adopted=" + str(p.adopted) + ")")

if __name__ == "__main__":
    main()
