from datetime import datetime

def ps():
    with open('desc.txt', 'r') as f:
        text = f.read()
    # Remove blank lines and strip end of line colons    
    text = text.split('\n')
    lines = [line for line in text if not line == '']
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
    print(prop_names)
    print(prop_desc)
    # opp_lines = lines[opp_i+1:end_i]
    # opp_names = opp_lines[::2]
    # opp_desc = opp_lines[1::2]

    event_speakers = list()

    for i in range(len(prop_names)):
        speaker = dict()
        speaker['name'] = prop_names[i]
        speaker['desc'] = prop_desc[i]
        speaker['type'] = 'prop'
        event_speakers.append(speaker)
        
    '''
    for i in range(len(opp_names)):
        speaker = dict()
        speaker['name'] = opp_names[i]
        speaker['desc'] = opp_desc[i]
        speaker['type'] = 'opp'
        event_speakers.append(speaker)
    '''

    return event_speakers

terms = [
    {
        'name': 'Easter 2019',
        'start': datetime.strptime('2019-04-20', '%Y-%m-%d'),
    },
    {
        'name': 'Long Vacation 2019',
        'start': datetime.strptime('2019-07-01', '%Y-%m-%d'),
        
    },
    {
        'name': 'Michaelmas 2019',
        'start': datetime.strptime('2019-10-01', '%Y-%m-%d'),
    },
    {
        'name': 'Christmas Break 2019/20',
        'start': datetime.strptime('2019-12-10', '%Y-%m-%d'),
    },
    {
        'name': 'Lent 2020',
        'start': datetime.strptime('2020-01-10', '%Y-%m-%d'),
    },
    {
        'name': 'Easter Break 2020',
        'start': datetime.strptime('2020-03-25', '%Y-%m-%d'),
    }
]

def gt(st):
    event_start_timestamp = datetime.timestamp(datetime.strptime(st, '%Y-%m-%d'))
    i = 0
    while i < len(terms) and event_start_timestamp > datetime.timestamp(terms[i]['start']):
        event_term = terms[i]['name']
        i += 1
    return '\nEvent term: {}'.format(event_term)

while True:
    inp = input('\n> ')
    print(gt(inp))