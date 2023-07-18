import uuid
import requests
import json
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

  a_url = "https://postman-echo.com/post"
  payload = {"randomValue": "{{randomString}}"}
  headers = {"Content-Type": "application/json"}
  response = session.post(a_url, headers=headers, json=payload)
  device_id = response.json()["json"]["randomValue"]

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
  auth_token = json_data["authToken"]

  accusr_url = 'https://gw-napi.zepeto.io/AccountUser_v5'
  payload = {
    'creatorAllItemsVersion': '_',
    'creatorHotItemGroupId': '_',
    'creatorHotItemsVersion': '_',
    'creatorNewItemsVersion': '_',
    'params': {
      'appVersion': '3.29.100',
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
  print(response.text)

  savep_url = 'https://gw-napi.zepeto.io/SaveProfileRequest_v2'
  payload = { "job":"\uD83D\uDCBB hckr",
  "name":"Elriq",
  "nationality":"404",
  "statusMessage":"zepeto \uD83D\uDC95\n\uD83D\uDCF3 order : t.me/elriq\n\uD83E\uDD1E\uD83C\uDFFB ready. upfoll, uplike."}
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
  print(response.text)

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

executor = ThreadPoolExecutor(
  max_workers=100)  # Increase the max_workers value for more concurrency

user_id = input("Masukkan user ID: ")
jumlah_follow_request = int(input("Masukkan jumlah followers: "))

success_count = 0
max_attempts = 5

future_to_user_id = {
  executor.submit(follow_request, user_id): user_id
  for _ in range(jumlah_follow_request)
}

for future in as_completed(future_to_user_id):
  try:
    future.result()
    success_count += 1
  except Exception as e:
    print(f"Error: {e}")

print(f"Successful follow requests: {success_count}/{jumlah_follow_request}")
