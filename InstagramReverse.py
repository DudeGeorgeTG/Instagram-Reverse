import requests
from user_agent import generate_user_agent
import re
import random
import string


def get_cookies(user_agent: str) -> str | None:
    url = "https://www.instagram.com/accounts/emailsignup/"

    headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "en-US,en;q=0.9",
        "Connection": "keep-alive",
        "Content-Type": "application/x-www-form-urlencoded",
        "Host": "www.instagram.com",
        "Origin": "https://www.instagram.com",
        "Referer": "https://www.instagram.com/accounts/emailsignup/",
        "User-Agent": user_agent,
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        js_datr_match = re.search(r'"_js_datr":\s*{\s*"value":\s*"([^"]+)"', response.text)
        if js_datr_match:
            return js_datr_match.group(1)
    return None


def __int_to_base(x: int, base: int) -> str:
    base_36 = string.digits + string.ascii_letters
    if x < 0:
        sign = -1
    elif x == 0:
        return base_36[0]
    else:
        sign = 1

    x *= sign
    digits = []
    while x:
        digits.append(base_36[x % base])
        x = x // base
    if sign < 0:
        digits.append("-")
    digits.reverse()
    return "".join(digits)


def generate_x_mid() -> str:
    return "".join([__int_to_base(random.randint(2**29, 2**32), 36) for _ in range(8)])


def get_headers(user_agent=None) -> dict:
    user_agent = user_agent or generate_user_agent()
    js_datr_value = get_cookies(user_agent)

    base_headers = {
        "authority": "www.instagram.com",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "accept-language": "en",
        "cache-control": "no-cache",
        "pragma": "no-cache",
        "sec-ch-ua": '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "none",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": user_agent
    }

    try:
        response = requests.get("https://www.instagram.com/", headers=base_headers)
        response.raise_for_status()
        data = response.text

        fbapp_id = re.search(r'"appID":\s*(\d+)', data)
        device_id = re.search(r'"device_id":\s*"([^"]+)"', data)
        crsf = re.search(r'"csrf_token":\s*"([^"]+)"', data)
        rollout_hash = re.search(r'"rollout_hash":\s*"([^"]+)"', data)

        if not all([fbapp_id, device_id, crsf, rollout_hash]):
            print("Failed to extract one or more required values.")
            return {}

        raw_device_id = device_id.group(1)
        clean_device_id_match = re.search(
            r"[0-9A-Fa-f]{8}-[0-9A-Fa-f]{4}-[0-9A-Fa-f]{4}-[0-9A-Fa-f]{4}-[0-9A-Fa-f]{12}",
            raw_device_id
        )
        clean_device_id = clean_device_id_match.group(0) if clean_device_id_match else raw_device_id

        custom_headers = {
            "X-Mid": generate_x_mid(),
            "X-CSRFToken": crsf.group(1),
            "X-IG-App-ID": fbapp_id.group(1),
            "X-Web-Device-ID": clean_device_id,
            "X-Instagram-AJAX": rollout_hash.group(1),
            "User-Agent": base_headers["user-agent"],
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "en-US,en;q=0.9",
            "Connection": "keep-alive",
            "Referer": "https://www.instagram.com/",
            "Host": "www.instagram.com",
        }

        custom_headers["Cookie"] = (
            f"csrftoken={custom_headers['X-CSRFToken']}; "
            f"datr={js_datr_value}; "
            f"mid={custom_headers['X-Mid']}; "
            f"ig_did={clean_device_id}"
        )

        return custom_headers

    except Exception as e:
        print(f"\nError occurred: {e}")
        return {}


if __name__ == "__main__":
    headers = get_headers()
    print("\nGenerated Headers and Cookies:\n")
    for key, value in headers.items():
        print(f"{key}: {value}")
