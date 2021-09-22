#################################################################################
# Author : G. HUSSON - Liberasys - contact_dataconnect _@_ liberasys.com - 2019 #
# License : EUPL v1.2 - see : https://eupl.eu/1.2/en/                           #
#################################################################################

# This is a simple Python code in order to tests requests to the
# Enedis data connect test API

import requests
import json
import re
import sys
import os
from urllib import parse as urlparse


# Before launch this script you must export your credentials
print(f"{os.environ['client_id']}\n{os.environ['redirect_uri']}")
client_id = os.environ['client_id']
client_secret = os.environ['client_secret']
redirect_uri = os.environ['redirect_uri']


authorize_url = "https://gw.hml.api.enedis.fr/group/espace-particuliers/consentement-linky/oauth2/authorize"
endpoint_token_url = "https://gw.hml.api.enedis.fr/v1/oauth2/token"
metering_data_base_url = "https://gw.hml.api.enedis.fr"


def pretty_print_request(req):
    print('{}\n{}\n{}\n{}\n{}\n'.format(
        '-----------REQ START-----------',
        req.method + ' ' + req.url,
        '\n'.join('{}: {}'.format(k, v) for k, v in req.headers.items()),
        req.body,
        '-----------REQ STOP-----------',
    ))

########### Authorize (green button, call back by the customer browser)
print("################################################################################")
print("# Authorize ((green button, call back by the customer browser)                 #")
print("################################################################################")

authorize_duration = "P1Y4M"
state = 'abcd12e'

req_params = {
             'client_id': client_id,
             'response_type': 'code',
             'redirect_uri':redirect_uri,
             'state': state,
             'duration': authorize_duration
             }

# Forge and print request
http_request = requests.Request("GET", authorize_url, params=req_params)
http_request_prepared = http_request.prepare()
pretty_print_request(http_request_prepared)

# Send request
http_session = requests.Session()
http_return = http_session.send(http_request_prepared)

# Print request result
print(http_return.status_code)
print(http_return.text)
#print(http_return.json)

# Parse request result
callback_found = re.findall(r'var url = \".*\"', http_return.text)
callback_url = callback_found[0].split('\"')[1]
callback_url_parsed = urlparse.urlparse(callback_url)
callback_authorize_code = urlparse.parse_qs(callback_url_parsed.query, True)['code'][0]
callback_state = urlparse.parse_qs(callback_url_parsed.query, True)['state'][0]
callback_usage_point_id = urlparse.parse_qs(callback_url_parsed.query, True)['usage_point_id'][0]
print ("callback auth_code = ", callback_authorize_code)
print ("callback state = ", callback_state)
print ("callback usage_point_id = ", callback_usage_point_id)


print("################################################################################")
print("# Request new Endpoint Token ###################################################")
print("################################################################################")

req_head = {
           'Content-Type': 'application/x-www-form-urlencoded',
           'Accept': 'text/html'
           }
req_params = {
             'redirect_uri': redirect_uri,
            }
req_data = {
           'grant_type': 'authorization_code',
           'client_id': client_id,
           'client_secret': client_secret,
           'code': callback_authorize_code
           }

# Forge and print request
http_request = requests.Request("POST", endpoint_token_url, headers=req_head, params=req_params, data=req_data)
http_request_prepared = http_request.prepare()
pretty_print_request(http_request_prepared)

# Send request
http_session = requests.Session()
http_return = http_session.send(http_request_prepared)

# Print request result
print(http_return.status_code)
print(http_return.text)
#print(http_return.json)

# Parse request result
endpoint_token_returned_json = json.loads(http_return.text)


print("################################################################################")
print("# Request data : consumption max power #########################################")
print("################################################################################")
start_date = '2021-09-14'
end_date = '2021-09-15'
metering_data_api_path = f'/v4/metering_data/daily_consumption_max_power'
request_url = metering_data_base_url + metering_data_api_path
token_type = endpoint_token_returned_json['token_type']
token = endpoint_token_returned_json['access_token']

req_head = {
           'Accept': 'application/json',
           'Authorization': token_type + ' ' + token
           }

req_params = {
           'start': start_date,
           'end': end_date,
           'usage_point_id':callback_usage_point_id
           }

# Forge and print request
http_request = requests.Request("GET", request_url, headers=req_head, params=req_params)
http_request_prepared = http_request.prepare()
pretty_print_request(http_request_prepared)

# Send request
http_session = requests.Session()
http_return = http_session.send(http_request_prepared)

# Print request result
print(http_return.status_code)
print(http_return.text)
#print(http_return.json)



print("################################################################################")
print("# Request data : consumption load curve ########################################")
print("################################################################################")
start_date = '2021-09-14'
end_date = '2021-09-15'
metering_data_api_path = '/v4/metering_data/consumption_load_curve'
request_url = metering_data_base_url + metering_data_api_path
token_type = endpoint_token_returned_json['token_type']
token = endpoint_token_returned_json['access_token']

req_head = {
           'Accept': 'application/json',
           'Authorization': token_type + ' ' + token
           }

req_params = {
           'start': start_date,
           'end': end_date,
           'usage_point_id':callback_usage_point_id
           }

# Forge and print request
http_request = requests.Request("GET", request_url, headers=req_head, params=req_params)
http_request_prepared = http_request.prepare()
pretty_print_request(http_request_prepared)

# Send request
http_session = requests.Session()
http_return = http_session.send(http_request_prepared)

# Print request result
print(http_return.status_code)
print(http_return.text)
#print(http_return.json)



print("################################################################################")
print("# Request data : daily consumption ########################################")
print("################################################################################")
start_date = '2021-09-14'
end_date = '2021-09-15'
metering_data_api_path = f'/v4/metering_data/daily_consumption'
request_url = metering_data_base_url + metering_data_api_path
token_type = endpoint_token_returned_json['token_type']
token = endpoint_token_returned_json['access_token']

req_head = {
           'Accept': 'application/json',
           'Authorization': token_type + ' ' + token
           }

req_params = {
           'start': start_date,
           'end': end_date,
           'usage_point_id':callback_usage_point_id
           }

# Forge and print request
http_request = requests.Request("GET", request_url, headers=req_head, params=req_params)
http_request_prepared = http_request.prepare()
pretty_print_request(http_request_prepared)

# Send request
http_session = requests.Session()
http_return = http_session.send(http_request_prepared)

# Print request result
print(http_return.status_code)
print(http_return.text)
#print(http_return.json)
