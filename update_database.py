from dotenv import load_dotenv
load_dotenv()

import os
import pickle
import logging
from pyfcm import FCMNotification
from datetime import datetime
from fbEventUtils import get_event_list

#from apscheduler.schedulers.background import BackgroundScheduler
#from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore

from config import db
from models import Event, Speaker

logging.basicConfig(filename='update.log', level=logging.DEBUG)

fcm = FCMNotification(
    api_key=os.getenv("FCM_API_KEY")
)

'''
jobstores = {
    'default': SQLAlchemyJobStore(url='sqlite:///jobs.sqlite')
}

scheduler = BackgroundScheduler(jobstores=jobstores)
scheduler = BackgroundScheduler()
scheduler.start()
'''

def send_push_30m(event_id, event_name):
    message = "Event starting in 30 minutes"
    res1 = fcm.notify_topic_subscribers(topic_name=event_id, message_title=event_name, message_body=message)
    res2 = fcm.notify_topic_subscribers(topic_name="all", message_title=event_name, message_body=message)
    # Lazy check
    if res1['success'] and res2['success']:
        logging.info("Sent 30 minute push for {}: {}".format(event.id, event.name))
        return True
    else:
        logging.info("Failed to send 30 minute push for {}: {}: error {}, {}".format(event.id, event.name, res1, res2))
        return False

def update_db():
    # Data to update database with
    #eventData = get_event_list()
    logging.info("Retreived data from Facebook")

    # pickle dump for debugging
    #pickle.dump(eventData, open("eventData.p", "wb"))

    # pickle load for debugging
    eventData = pickle.load(open("eventData.p", "rb"))

    # iterate over the event structure and populate the database
    for event in eventData:
        q = db.session.query(Event)
        q = q.filter(Event.event_id == event.id)
        try:
            record = q.one()
            recordExists = True
        except:
            recordExists = False

        if recordExists:
            # already exists so update
            logging.info("Updating event {}: {}".format(event.id, event.name))

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
            logging.info("Creating event {}: {}".format(event.id, event.name))
            eventRow = Event(event_id=event.id, event_name=event.name, event_term=event.term, event_subtitle=event.subtitle, event_description=event.description, event_date=event.date, event_start=event.start,
                             event_end=event.end, event_going=event.going, event_interested=event.interested, event_start_timestamp=event.start_timestamp, event_status=event.status, event_type=event.type, event_open_to_all=event.open_to_all)

            if event.speakers:
                logging.info("Creating event {}: {} speakers: {}".format(event.id, event.name, event.speakers))
                for speaker in event.speakers:
                    eventRow.event_speakers.append(
                        Speaker(
                            speaker_name=speaker['name'],
                            speaker_type=speaker['type'],
                            speaker_description=speaker['desc']
                        )
                    )

            db.session.add(eventRow)
        
        db.session.commit()
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
                record.event_action_text = None
                #logging.info("Event {}: {} finished".format(event.id, event.name))
            elif record.event_start_timestamp <= now and event_end_timestamp >= now:
                record.event_status = 'live'
                #logging.info("Event {}: {} live".format(event.id, event.name))
            elif record.event_start_timestamp >= now:
                record.event_status = 'upcoming'
                #logging.info("Event {}: {} upcoming".format(event.id, event.name))
            else:
                record.event_status = 'undefined'
                #logging.info("Event {}: {} undefined".format(event.id, event.name))

            start_delta = record.event_start_timestamp - now
            if start_delta > 1680 and start_delta < 1920:
                send_push_30m(record.event_id, record.event_name)

    db.session.commit()

if __name__ == '__main__':
    logging.info("")
    logging.info("**** UPDATE STARTING ****")
    try:
        update_db()
    except Exception as e:
        logging.error(repr(e))
        exit()
    finally:
        logging.info("**** UPDATE EXITING ****")
        logging.info("")