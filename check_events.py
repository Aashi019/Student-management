from app import app
from models import Event

with app.app_context():
    events = Event.query.all()
    print(f"Total events in database: {len(events)}")
    print("\nAll events:")
    for event in events:
        print(f"- {event.title}")
        print(f"  Date: {event.event_date.date()}")
        print(f"  Type: {event.event_type}")
        print(f"  Location: {event.location}")
        print("---")