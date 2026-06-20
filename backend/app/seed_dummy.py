import random
import sys
from pathlib import Path

# Add backend directory to path so imports work
sys.path.append(str(Path(__file__).resolve().parent.parent))

from app.database import SessionLocal, Base, engine
from app.models import Client, Candidate, Score, Feedback, ArchetypeEnum
from app.crud import submit_scores, submit_feedback
from app.schemas import ScoreCreate, FeedbackCreate
from faker import Faker

fake = Faker()

# Sample expectations based on archetype
CONSULTING_EXPECTATIONS = [
    "Requires high executive presence, structured thinking, and slide design competence.",
    "Candidates must show strong Minto Pyramid communication and formal consulting background.",
    "Expects detailed case analysis, business valuation capability, and client management skill.",
]

STARTUP_EXPECTATIONS = [
    "Needs a highly scrappy builder. Bias for action over perfect planning.",
    "Looking for candidates comfortable with wearing multiple hats and high ambiguity.",
    "Strong technical execution speed and comfort working with rapid release cycles.",
]

REASONS_REJECTED = [
    "communication_soft_skills",
    "technical_capability",
    "alignment_cultural_vibe",
]

REASONS_ACCEPTED = [
    "technical_capability",
    "alignment_cultural_vibe",
    "communication_soft_skills",
]

def clear_db():
    print("Clearing existing database tables...")
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    print("Database tables recreated successfully.")

def seed():
    db = SessionLocal()
    try:
        # Create 6 Clients (3 Consulting, 3 Startup)
        print("Seeding clients...")
        clients = []
        for i in range(3):
            # Consulting Client
            client = Client(
                name=f"{fake.company()} Consulting",
                archetype=ArchetypeEnum.consulting,
                expectations=random.choice(CONSULTING_EXPECTATIONS),
                min_communication=random.choice([4, 5]),
                min_adaptability=random.choice([3, 4]),
                min_collaboration=random.choice([3, 4, 5]),
                min_problem_solving=random.choice([3, 4, 5]),
                min_leadership=random.choice([3, 4]),
            )
            db.add(client)
            clients.append(client)
            
            # Startup Client
            client = Client(
                name=f"{fake.company()} Tech",
                archetype=ArchetypeEnum.startup,
                expectations=random.choice(STARTUP_EXPECTATIONS),
                min_communication=random.choice([3, 4]),
                min_adaptability=random.choice([4, 5]),
                min_collaboration=random.choice([3, 4]),
                min_problem_solving=random.choice([3, 4, 5]),
                min_leadership=random.choice([4, 5]),
            )
            db.add(client)
            clients.append(client)
        
        db.commit()
        for c in clients:
            db.refresh(c)
            print(f"  Created client: {c.name} ({c.archetype.value})")

        # Create candidates for each client
        print("\nSeeding candidates, scores, and feedbacks...")
        for client in clients:
            # Generate 4-7 candidates per client
            num_candidates = random.randint(4, 7)
            for _ in range(num_candidates):
                candidate = Candidate(
                    name=fake.name(),
                    email=fake.email(),
                    recruiter_notes=fake.paragraph(nb_sentences=2),
                    client_id=client.id
                )
                db.add(candidate)
                db.commit()
                db.refresh(candidate)
                
                # 85% chance candidate gets scored
                if random.random() < 0.85:
                    score_data = ScoreCreate(
                        communication=random.randint(2, 5),
                        adaptability=random.randint(2, 5),
                        collaboration=random.randint(2, 5),
                        problem_solving=random.randint(2, 5),
                        leadership=random.randint(2, 5)
                    )
                    submit_scores(db, candidate.id, score_data)
                    db.refresh(candidate)
                    
                    # 75% chance scored candidate gets feedback
                    if random.random() < 0.75:
                        outcome = random.choice(["accepted", "rejected"])
                        if outcome == "accepted":
                            reason = random.choice(REASONS_ACCEPTED)
                            notes = f"Strong candidate. Demonstrates good cultural alignment and fits requirements."
                        else:
                            reason = random.choice(REASONS_REJECTED)
                            notes = f"Failed to meet client expectations regarding {reason.replace('_', ' ')}."
                            
                        feedback_data = FeedbackCreate(
                            outcome=outcome,
                            primary_reason=reason,
                            client_notes=notes
                        )
                        submit_feedback(db, candidate.id, feedback_data)
                
                db.commit()
            print(f"  Completed seeding candidates for: {client.name}")
            
        print("\n--- Seeding Completed Successfully! ---")
    except Exception as e:
        print(f"Error during seeding: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    clear_db()
    seed()
