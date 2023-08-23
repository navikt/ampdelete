import requests
import json
import time

DELETE_URL = "https://amplitude.com/api/2/deletions/users"

def divide_chunks(l, n=100):
    for i in range(0, len(l), n): 
        yield l[i:i + n]

def delete_amplitude_ids(amplitude_ids: list[str]):
    """
    Takes a list of `amplitude_id`s, splits them into chunks of 100, and sends off delete requests.
    Between each request, the function sleeps for 2 seconds to comply with the Amplitude API limits:
    see: https://www.docs.developers.amplitude.com/analytics/apis/user-privacy-api/#limits
    """

    for chunk in divide_chunks(amplitude_ids):
        payload = json.dumps({
          "amplitude_ids": chunk,
          "ignore_invalid_id": "true",
          "delete_from_org": "false",
          "requester": "ampdelete@nav.no" # TODO: do we have to specify an email, or can this be anything? ampdelete@nav.no isn't a registered email
        })
        headers = {
          'Authorization': 'Basic {{api-key}}:{{secret-key}}', # base64 encoded credentials, TODO: get them from some place safe
          'Content-Type': 'application/json'
        }

        response = requests.request("POST", DELETE_URL, headers=headers, data=payload)
        time.sleep(2)
        # TODO: commit response to some place, contains potentially interesting stuff
        # see: https://www.docs.developers.amplitude.com/analytics/apis/user-privacy-api/#response