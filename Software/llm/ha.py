from requests import get, post
import sys


class HomeAssistant:

    def __init__(self, ha_access_token, ha_base_url):

        self.access_token = ha_access_token
        self.base_url = ha_base_url  # "http://aeassistant.lan:8123/"

        self.switch_entity_ids = {
            'air_conditioner': 'switch.qdhkl_ac_0146_switch_status',
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
        headers = {"Authorization": 'Bearer ' + self.access_token}
        data = {"entity_id": _entity_id}

        response = post(url, headers=headers, json=data)
        return response

    def turn_on_air_conditioner(self, args):
        self.setup_switch('on', self.switch_entity_ids['air_conditioner'])
        return 'Frank have turned on the air conditioner for human.'

    def turn_off_air_conditioner(self, args):
        self.setup_switch('off', self.switch_entity_ids['air_conditioner'])
        return 'Frank have turned off the air conditioner for human.'


if __name__ == '__main__':
    ha = HomeAssistant()
    ha.setup_switch('off', ha.entity_ids['light'])
