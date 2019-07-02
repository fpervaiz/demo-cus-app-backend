import os
from datetime import datetime
from config import db
from models import Event
from fbEventUtils import getEventList

# Data to initialize database with
eventData = getEventList()

# Delete database file if it exists currently
if os.path.exists("data.db"):
    os.remove("data.db")

# Create the database
db.create_all()

# iterate over the PEOPLE structure and populate the database
for event in eventData:
    eventRow = Event(event_id=event.id, event_name=event.name, event_description=event.description, event_date=event.date, event_start=event.start, event_end=event.end, event_going=event.going, event_interested=event.interested, event_start_timestamp=event.start_timestamp, event_status=event.status)

    db.session.add(eventRow)

db.session.commit()
