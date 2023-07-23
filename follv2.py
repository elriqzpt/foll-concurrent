import uuid
import requests
import json
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

user_agent = "android.zepeto_global/3.25.100 (android; U; Android OS 7.1.2 / API-25 (NRD90M/G9550ZHU1AQEE); id-ID; occ-ID; samsung SM-G988N)"
x_zepeto_duid = str(uuid.uuid4())
session = requests.Session()

find_url = "https://gw-napi.zepeto.io/FriendNicknameSearchWithFeedInfo"
keyword = input("Masukkan code ZEPETO: ")
payload = json.dumps({
  "size": 30,
  "cursor": "",
  "place": "home",
  "keyword": keyword
})
headers = {
  'Content-Type':
  'application/json',
  'Authorization':
  'Bearer 9LdQ88iIkoFDRo21xhFY/hQyZuzINjjBcu2oda8LvZeG39S+uiAkIfH0J6g+hcTPgE5bgn1lq7J5qMihaeq9cXxypXsDPqaJwsxRr2tidAw=\\1\\bS4qM83NhdSmhxT8M8rgBj3zBjPzEQ7XEm36'
}
response = session.request("POST", find_url, headers=headers, data=payload)

jsondata = response.json()

if 'result' in jsondata:
  result = jsondata['result'][0]
  user_id = result['userId']
  print(user_id)


def follow_request(user_id):
  x_zepeto_duid = str(uuid.uuid4())
  device_id = str(uuid.uuid4())

  b_url = "https://gw-napi.zepeto.io/DeviceAuthenticationRequest"
  payload = {"deviceId": device_id}
  headers = {
    "X-Zepeto-Duid": x_zepeto_duid,
    "User-Agent": user_agent,
    "Content-Type": "application/json",
    "Accept-Language": "application/json; charset=utf-8",
    "Content-Length": "51",
  }
  response = session.post(b_url, headers=headers, data=json.dumps(payload))
  if response.status_code != 200:
    raise Exception("Device authentication failed")

  json_data = json.loads(response.text)
  auth_token = json_data.get("authToken")

  if not auth_token:
    # Retry up to max_attempts times if authToken is not received
    max_attempts = 5
    for _ in range(max_attempts):
      response = session.post(b_url, headers=headers, data=json.dumps(payload))
      if response.status_code != 200:
        raise Exception("Device authentication failed")

      json_data = json.loads(response.text)
      auth_token = json_data.get("authToken")

      if auth_token:
        break
    else:
      raise Exception("Failed to receive authToken after multiple attempts")

  accusr_url = 'https://gw-napi.zepeto.io/AccountUser_v5'
  payload = {
    'creatorAllItemsVersion': '_',
    'creatorHotItemGroupId': '_',
    'creatorHotItemsVersion': '_',
    'creatorNewItemsVersion': '_',
    'params': {
      'appVersion': '3.32.100',
      'itemVersion': '_',
      'language': '_',
      'platform': '_'
    },
    'timeZone': 'Asia/Jakarta'
  }
  headers = {
    'Content-Type': 'application/json; charset=utf-8',
    'User-Agent': user_agent,
    "X-Zepeto-Duid": x_zepeto_duid,
    "Authorization": "Bearer " + auth_token,
  }

  response = session.post(accusr_url, headers=headers, json=payload)
  if response.status_code == 200:
    # Mengubah respons
    modified_response = response.json()
    # Lakukan manipulasi pada modified_response sesuai kebutuhan Anda
    modified_response["isOfficialAccount"] = "true"
    modified_response["officialAccountType"] = "EVENT"
    modified_response["isGreeter"] = "true"
  else:
    print("Gagal menerima respons dari gw-napi.zepeto.io")

  savep_url = 'https://gw-napi.zepeto.io/SaveProfileRequest_v2'
  payload = {"job": "", "name": "ㅤㅤㅤ", "nationality": "", "statusMessage": ""}
  headers = {
    'Content-Type': 'application/json; charset=utf-8',
    'User-Agent': user_agent,
    "X-Zepeto-Duid": x_zepeto_duid,
    "Authorization": "Bearer " + auth_token,
  }

  response = session.post(savep_url, headers=headers, json=payload)
  print(response.text)

  savepp_url = 'https://gw-napi.zepeto.io/CopyCharacterByHashcode'
  payload = {'hashCode': 'ZPT221', 'characterId': ''}
  headers = {
    'Content-Type': 'application/json; charset=utf-8',
    'User-Agent': user_agent,
    "X-Zepeto-Duid": x_zepeto_duid,
    "Authorization": "Bearer " + auth_token,
  }

  response = session.post(savepp_url, headers=headers, json=payload)

  c_url = 'https://gw-napi.zepeto.io/FollowRequest_v2'
  payload = {'followUserId': user_id}
  headers = {
    'Content-Type': 'application/json; charset=utf-8',
    'User-Agent': user_agent,
    "X-Zepeto-Duid": x_zepeto_duid,
    "Authorization": "Bearer " + auth_token,
  }

  response = session.post(c_url, headers=headers, json=payload)

  if response.status_code != 200:
    raise Exception("Follow request failed")

  print(response.text)


# Menggunakan ThreadPoolExecutor untuk memanggil fungsi follow_request dengan beberapa ID pengguna

user_id = input("Masukkan user ID: ")
jumlah_follow_request = int(input("Masukkan jumlah followers: "))

success_count = 0
max_attempts = 10

# Executor 1
executor_1 = ThreadPoolExecutor(
  max_workers=10)  # Increase the max_workers value for more concurrency
future_to_user_id_1 = {
  executor_1.submit(follow_request, user_id): user_id
  for _ in range(jumlah_follow_request)
}

# Executor 2
executor_2 = ThreadPoolExecutor(
  max_workers=10)  # Increase the max_workers value for more concurrency
future_to_user_id_2 = {
  executor_2.submit(follow_request, user_id): user_id
  for _ in range(jumlah_follow_request)
}

# Executor 3
executor_3 = ThreadPoolExecutor(
  max_workers=100)  # Increase the max_workers value for more concurrency
future_to_user_id_3 = {
  executor_3.submit(follow_request, user_id): user_id
  for _ in range(jumlah_follow_request)
}

# Collect results from Executor 1
for future in as_completed(future_to_user_id_1):
  try:
    future.result()
    success_count += 1
  except Exception as e:
    print(f"Error: {e}")
  finally:
    # Add a 2-second delay after each iteration
    time.sleep(2)

# Collect results from Executor 2
for future in as_completed(future_to_user_id_2):
  try:
    future.result()
    success_count += 1
  except Exception as e:
    print(f"Error: {e}")
  finally:
    # Add a 2-second delay after each iteration
    time.sleep(2)

# Collect results from Executor 3
for future in as_completed(future_to_user_id_3):
  try:
    future.result()
    success_count += 1
  except Exception as e:
    print(f"Error: {e}")
  finally:
    # Add a 2-second delay after each iteration
    time.sleep(2)

print(f"Successful follow requests: {success_count}/{jumlah_follow_request}")
