import requests
import json
import facebook

page_token = 'EAAJDVdhKOLMBAL7QlQwAOlQGo3KwBe5ZCd9JrD5966wY7KxXXjJfAZBGVbWmht4RCNYILtXKSrr48ZCcKWSmrM4pwL2lqkDVO1ybaCtOgNKoPtXARPKtHSE2gDKwAi6j0X3I7VlZAbqtgjTvFHwFKDnYFVpfROvZCWLk2qhBxkAZDZD'

fb = facebook.GraphAPI(page_token)


event_list = fb.get_object(id='TheCambridgeUnion', fields='events')
print(event_list)
