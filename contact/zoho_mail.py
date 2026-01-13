import os
import requests

ZOHO_TOKEN_URL = "https://accounts.zoho.in/oauth/v2/token"
ZOHO_MAIL_URL = "https://mail.zoho.in/api/accounts/{}/messages"


def get_access_token():
    res = requests.post(
        ZOHO_TOKEN_URL,
        data={
            "refresh_token": os.environ["ZOHO_REFRESH_TOKEN"],
            "client_id": os.environ["ZOHO_CLIENT_ID"],
            "client_secret": os.environ["ZOHO_CLIENT_SECRET"],
            "grant_type": "refresh_token",
        },
        timeout=10,
    )
    res.raise_for_status()
    return res.json()["access_token"]


def send_zoho_mail(subject, content, to_email): 
    access_token = get_access_token()

    headers = {
        "Authorization": f"Zoho-oauthtoken {access_token}",
        "Content-Type": "application/json",
    }

    payload = {
        "fromAddress": "hr@manovate.co.in",
        "toAddress": to_email,
        "subject": subject,
        "content": content,
    }

    url = ZOHO_MAIL_URL.format(os.environ["ZOHO_ACCOUNT_ID"])

    response = requests.post(url, json=payload, headers=headers, timeout=10)

    print("====== ZOHO MAIL DEBUG ======")
    print("STATUS:", response.status_code)
    print("RESPONSE:", response.text)
    print("================================")

    response.raise_for_status()
