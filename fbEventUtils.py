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

# Need to come up with a specification for consistently
# identifying event type from Facebook event title
debate_identifiers = ['thb', 'thw', 'debate']
panel_identifiers = ['panel']
speaker_identifiers = ['|']

open_identifiers = ['open to all', 'all university members']

facebook = Facebook(
    app_id=app_id,
    app_secret=app_secret
)

facebook.set_default_access_token(access_token=page_token)

class UnionEvent:
    def __init__(self, name, subtitle, id, description, date, start, end, going, interested, status, start_timestamp, event_type, open_to_all, speakers):
        self.name = name
        self.subtitle = subtitle
        self.id = id
        self.description = description
        self.date = date
        self.start = start
        self.end = end
        self.going = going
        self.interested = interested
        self.status = status
        self.start_timestamp = start_timestamp
        self.type = event_type
        self.open_to_all = open_to_all
        self.speakers = speakers

    def __lt__(self, other):
        return other.start_timestamp < self.start_timestamp

    def __repr__(self):
        a = '\nName: ' + self.name
        b = 'Date, Status: ' + self.date + ' ' + self.status
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

def parse_speakers(text):
    # TODO SPECIFICATION NEEDED
    # Remove blank lines and strip end of line colons/spaces   
    text = text.split('\n')
    lines = [line.strip() for line in text if not line == '']
    for i in range(len(lines)):
        if lines[i].endswith(':'):
            lines[i] = lines[i].replace(':', '')
            
    # Find start and end of speaker descriptions
    prop_i = lines.index('Proposition')
    opp_i = lines.index('Opposition')
    # end_i = lines.index('***') # to be implemented

    # Create list of speaker dictionaries
    prop_lines = lines[prop_i+1:opp_i]
    prop_names = prop_lines[::2]
    prop_desc = prop_lines[1::2]

    # opp_lines = lines[opp_i+1:end_i]
    # opp_names = opp_lines[::2]
    # opp_desc = opp_lines[1::2]

    event_speakers = list()

    for i in range(len(prop_names)):
        speaker = dict()
        try:
            speaker['name'] = prop_names[i]
            speaker['desc'] = prop_desc[i]
            speaker['type'] = 'prop'
        except (IndexError, ValueError):
            speaker['name'] = 'Error speaker {}'.format(i+1)
            speaker['desc'] = 'Error speaker {} description'.format(i+1)
            speaker['type'] = 'prop'
        event_speakers.append(speaker)
        
    # TODO
    # for i in range(len(opp_names)):
    for i in range(3):
        speaker = dict()
        speaker['name'] = 'Opp Speaker {}'.format(i+1) # opp_names[i]
        speaker['desc'] = 'Opp Speaker {}'.format(i+1) # opp_desc[i]
        speaker['type'] = 'opp'
        event_speakers.append(speaker)
    

    return event_speakers
            

def processEvents(event_list_get):
    events = list()
    for event in event_list_get:
        event_name = event['name']
        event_id = int(event['id'])
        event_description = event['description']

        date_string, event_start_time = event['start_time'].split('T')
        dt_object = datetime.strptime(date_string, '%Y-%m-%d')
        event_date = dt_object.strftime('%A %d %B')
        
        start_time_string = event['start_time']
        dt_object = datetime.strptime(start_time_string, '%Y-%m-%dT%H:%M:%S%z')
        event_start_timestamp = datetime.timestamp(dt_object)
        end_time_string = event['start_time']
        dt_object = datetime.strptime(end_time_string, '%Y-%m-%dT%H:%M:%S%z')
        event_end_timestamp = datetime.timestamp(dt_object)

        now = datetime.now().timestamp()
        if event_end_timestamp <= now:
            event_status = 'finished'
        elif event_start_timestamp <= now and event_end_timestamp >= now:
            event_status = 'live'
        elif event_start_timestamp >= now:
            event_status = 'upcoming'
        else:
            event_status = 'undefined'

        event_start_time = event_start_time.split('+')[0][:5]
        event_end_time = event['end_time'].split('T')[1].split('+')[0][:5]

        attendance_data = fbGet('/' + str(event_id) + count_param)

        event_going = str(attendance_data['attending_count'])
        event_interested = str(attendance_data['maybe_count'])

        if any(identifier in event_name.lower() for identifier in debate_identifiers):
            event_type = 'debate'
        elif any(identifier in event_name.lower() for identifier in panel_identifiers):
            event_type = 'panel'
        elif any(identifier in event_name.lower() for identifier in speaker_identifiers):
            event_type = 'speaker'
        else:
            event_type = 'other'

        if any(identifier in event_description.lower() for identifier in open_identifiers):
            event_open_to_all = 'true'
        else:
            event_open_to_all = 'false'

        if event_type == 'debate':
            # Parse description to extract speakers
            try:
                event_speakers = parse_speakers(event_description)
            except ValueError:
                print('Error processing {}'.format(event_name))
                print(event_description)
                event_speakers = None
        else:
            event_speakers = None

        if '|' in event_name:
            a, b = event_name.split('|')
            event_name = a.strip()
            event_subtitle = b.strip()
        else:
            event_subtitle = None
        
        event = UnionEvent(event_name, event_subtitle, event_id, event_description, event_date, event_start_time, event_end_time, event_going, event_interested, event_status, event_start_timestamp, event_type, event_open_to_all, event_speakers)
        
        events.append(event)

    return sorted(events)

def getEventList():
    events_get = fbGet(page_id)
    events = processEvents(events_get)
    return events

#print(getEventList()[0].__dict__)

