import requests
import json
import time
import base64

DELETE_URL = "https://analytics.eu.amplitude.com/api/2/deletions/users"

def divide_chunks(l, n=100):
  for i in range(0, len(l), n): 
    yield l[i:i + n]

class Delete():
  def __init__(self, api_key: str, secret_key: str):
    self.auth = self.__auth(api_key, secret_key)

  def __auth(self, api_key: str, secret_key: str):
    return base64.b64encode(bytes(f"{api_key}:{secret_key}", encoding="utf-8")).decode("utf-8")

  def get_deletion_jobs(self, date: str):
    """
    Gets deletion jobs for the given date.
    """
    headers = {
      'Authorization': f"Basic {self.auth}",
      'Accept': 'application/json'
    }

    response = requests.get(DELETE_URL, params={'start_day': date, 'end_day': date}, headers=headers)
    data = response.json()

    if len(data) == 1:
      return data[0]
    else:
      return {}

  def delete_amplitude_ids(self, amplitude_ids: list[str]):
    """
    Takes a list of `amplitude_id`s, splits them into chunks of 100, and sends off delete requests.
    Between each request, the function sleeps for 2 seconds to comply with the Amplitude API limits:
    see: https://www.docs.developers.amplitude.com/analytics/apis/user-privacy-api/#limits
    """
    first = True
    expected_deletion_date = None
    for chunk in divide_chunks(amplitude_ids):
        payload = json.dumps({
          "amplitude_ids": chunk,
          "ignore_invalid_id": "true",
          "delete_from_org": "false",
          "requester": "navikt/ampdelete"
        })
        headers = {
          'Authorization': f"Basic {self.auth}",
          'Content-Type': 'application/json'
        }

        response = requests.request("POST", DELETE_URL, headers=headers, data=payload)

        data = response.json()
        if first and len(data) == 1:
          first = False
          print("Deletion scheduled at:", data[0]["day"])
          expected_deletion_date = data[0]["day"]
        
        time.sleep(2)
        return expected_deletion_date
        # TODO: commit response to some place, contains potentially interesting stuff
        # see: https://www.docs.developers.amplitude.com/analytics/apis/user-privacy-api/#response