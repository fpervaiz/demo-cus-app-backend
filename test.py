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