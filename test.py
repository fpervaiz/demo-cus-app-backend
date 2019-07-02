import requests
import json

from facebook_sdk.exceptions import FacebookResponseException
from facebook_sdk.facebook import Facebook
from datetime import datetime

page_id = '/TheCambridgeUnion/events'
time_param = '?time_filter='
count_param = '?fields=attending_count,maybe_count'

app_id = '636985933445299'
app_secret = '48fff212b34f1368740b1a8684030cc8'
page_token = 'EAAJDVdhKOLMBAL7QlQwAOlQGo3KwBe5ZCd9JrD5966wY7KxXXjJfAZBGVbWmht4RCNYILtXKSrr48ZCcKWSmrM4pwL2lqkDVO1ybaCtOgNKoPtXARPKtHSE2gDKwAi6j0X3I7VlZAbqtgjTvFHwFKDnYFVpfROvZCWLk2qhBxkAZDZD'

facebook = Facebook(
    app_id=app_id,
    app_secret=app_secret
)

facebook.set_default_access_token(access_token=page_token)

class UnionEvent:
    def __init__(self, name, id, description, date, start, end, going, interested, timestamp):
        self.name = name
        self.id = id
        self.description = description
        self.date = date
        self.start = start
        self.end = end
        self.going = going
        self.interested = interested
        self.timestamp = timestamp

    def __lt__(self, other):
        return self.timestamp < other.timestamp

    def __repr__(self):
        a = '\nName: ' + self.name
        b = 'Date: ' + self.date
        c = 'Times: ' + self.start + ' ' + self.end
        d = 'Going & Interested: ' + self.going + ' ' + self.interested
        e = 'Description: ' + self.description
        sep = '\n'
        return sep.join([a, b, c, d, e])

def fbGet(url):
    try:
        response = facebook.get(endpoint=url)
    except FacebookResponseException as e:
        print(e.message)
    else:
        try:
            return response.json_body['data']
        except KeyError:
            return response.json_body

def processEvents(event_list_get):
    events = list()
    for event in event_list_get:
        event_name = event['name']
        event_id = event['id']
        event_description = event['description']

        date_string, event_start_time = event['start_time'].split('T')
        dt_object = datetime.strptime(date_string, '%Y-%m-%d')
        event_date = dt_object.strftime('%A %d %B')
        
        start_time_string = event['start_time']
        dt_object = datetime.strptime(start_time_string, '%Y-%m-%dT%H:%M:%S%z')
        event_timestamp = datetime.timestamp(dt_object)

        event_start_time = event_start_time.split('+')[0][:5]
        event_end_time = event['end_time'].split('T')[1].split('+')[0][:5]

        attendance_data = fbGet('/' + event_id + count_param)

        event_going = str(attendance_data['attending_count'])
        event_interested = str(attendance_data['maybe_count'])

        event = UnionEvent(event_name, event_id, event_description, event_date, event_start_time, event_end_time, event_going, event_interested, event_timestamp)
        
        events.append(event)

    return events

upcoming_events_get = fbGet(page_id + time_param + 'upcoming')
upcoming_events = processEvents(upcoming_events_get)

past_events_get = fbGet(page_id + time_param + 'past')
past_events = processEvents(past_events_get)

for event in upcoming_events:
    print(event)

for event in past_events:
    print(event)