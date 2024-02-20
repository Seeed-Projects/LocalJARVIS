from requests import get, post
import sys


class HomeAssistant:

    def __init__(self):

        self.access_token = (
            'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiI2MzQ1MDM4ZTk5MmI0NmEzOGJkOGQ1NWY0MjE5NmMxOCI'
            'sImlhdCI6MTcwNTkwNDM2NCwiZXhwIjoyMDIxMjY0MzY0fQ.nMVjHoQGMhSXJt9guTaQBmQJDVgCWvN6xGqYWETrHcA'
        )
        self.base_url = "http://aeassistant.lan:8123/"

        self.entity_ids = {
            'light': 'switch.living_room_1',
        }

    def setup_switch(self, state, _entity_id):
        url = self.base_url
        if state == 'on':
            url += 'api/services/switch/turn_on'
        elif state == 'off':
            url += 'api/services/switch/turn_off'
        else:
            print("ERROR: Switch state must be 'on' or 'off'.")
            sys.exit()
        headers = {"Authorization": self.access_token}
        data = {"entity_id": _entity_id}

        response = post(url, headers=headers, json=data)
        return response


if __name__ == '__main__':
    ha = HomeAssistant()
    ha.setup_switch('off', ha.entity_ids['light'])
