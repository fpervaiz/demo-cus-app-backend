import os
from datetime import datetime
from config import db
from models import Event, Speaker
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
    eventRow = Event(event_id=event.id, event_name=event.name, event_subtitle=event.subtitle, event_description=event.description, event_date=event.date, event_start=event.start, event_end=event.end, event_going=event.going, event_interested=event.interested, event_start_timestamp=event.start_timestamp, event_status=event.status, event_type=event.type, event_open_to_all = event.open_to_all)

    if event.speakers:
        for speaker in event.speakers:
            eventRow.event_speakers.append(
                Speaker(
                    speaker_name = speaker['name'],
                    speaker_type = speaker['type'],
                    speaker_description = speaker['desc']
                )
            )
    
    db.session.add(eventRow)

db.session.commit()
