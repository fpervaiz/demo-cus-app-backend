import os
import pickle
from datetime import datetime
from config import db
from models import Event, Speaker
from fbEventUtils import get_event_list

# Data to update database with
eventData = get_event_list()

# pickle dump for debugging
pickle.dump(eventData, open("eventData.p", "wb"))

# pickle load for debugging
#eventData = pickle.load(open("eventData.p", "rb"))

# iterate over the event structure and populate the database
for event in eventData:
    q = db.session.query(Event)
    q = q.filter(Event.event_id==event.id)
    try:
        record = q.one()
        recordExists = True
    except:
        recordExists = False
    
    if recordExists:
        # already exists so update
        if record.event_type != 'debate':
            record.event_name = event.name
            record.event_description = event.description
        record.event_term = event.term
        #record.event_subtitle = event.subtitle
        record.event_date = event.date
        record.event_start = event.start
        record.event_end = event.end
        record.event_going = event.going
        record.event_interested = event.interested
        record.event_start_timestamp = event.start_timestamp
        record.event_status = event.status

    else:
        # create
        eventRow = Event(event_id=event.id, event_name=event.name, event_term=event.term, event_subtitle=event.subtitle, event_description=event.description, event_date=event.date, event_start=event.start, event_end=event.end, event_going=event.going, event_interested=event.interested, event_start_timestamp=event.start_timestamp, event_status=event.status, event_type=event.type, event_open_to_all = event.open_to_all)

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

    q = db.session.query(Event)
    #q = q.filter(Event.event_id=='upcoming')
    
    now = datetime.now().timestamp()
    for record in q:

        # Ugly hack
        if record.event_type == 'debate':
            event_end_timestamp = record.event_start_timestamp + 5400
        else:
            event_end_timestamp = record.event_start_timestamp + 3600

        if event_end_timestamp <= now:
            record.event_status = 'finished'
        elif record.event_start_timestamp <= now and event_end_timestamp >= now:
            record.event_status = 'live'
        elif record.event_start_timestamp >= now:
            record.event_status = 'upcoming'
        else:
            record.event_status = 'undefined'

db.session.commit()
