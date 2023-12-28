import time
import uuid
import hashlib
import hmac
import base64
import http.client
import json

conn = http.client.HTTPSConnection("cert.api.fiservapps.com")
url = "/ch/payments/v1/charges"
api_key = "9A0mjfAe9rA9SjDEKe4k6hkRqotalAQi"
secret = "1KR7klWWrie75AK98gRJhWuwoq0kmTUen26G9hmGAJ3"
merchant_id = "100008000003683"
terminal_id = "10000001"
timestamp = str(int(time.time() * 1000))  # Convert to string
client_request_id = str(uuid.uuid4())
amount_card = input("enter rent")
card_data = input("enter card number")
expiration_date =input("enter exp month")
expiration_year = input("enter expiration year")
security_code=input("enter cvv")
payload = {
    "amount": {
        "total": float(amount_card),
        "currency": "USD"
    },
    "source": {
    "sourceType": "PaymentCard",
        "card": {
        "cardData": card_data,
        "expirationMonth": expiration_date,
        "expirationYear": expiration_year,
        "securityCode": security_code
        }
    },
    "transactionDetails": {
        "captureFlag": True
    },
    "merchantDetails": {
        "merchantId": str(merchant_id),
        "terminalId": str(terminal_id)
    }
}

# Convert payload to JSON string
payload_json = json.dumps(payload)

# Construct the raw signature
raw_signature = f'{api_key}{client_request_id}{timestamp}{payload_json}'

def generate_auth_token(data, key):
    try:
        key_bytes = key.encode()
        data_bytes = data.encode()
        hashed = hmac.new(key_bytes, msg=data_bytes, digestmod=hashlib.sha256)
        return base64.b64encode(hashed.digest()).decode()
    except Exception as e:
        print(f"Error Generating Auth Token: {str(e)}")
        return None

# Encode the hashed signature using Base64
computed_hmac = generate_auth_token(raw_signature, secret)

headers = {
    "Content-Type": "application/json",
    "Client-Request-Id": client_request_id,
    "Api-Key": api_key,
    "Timestamp": str(timestamp),
    "Accept-Language": "en-US",
    "Auth-Token-Type": "HMAC",
    "Authorization": computed_hmac,
    "Content-Length": len(payload_json)
}

conn.request("POST", url, payload_json, headers)

res = conn.getresponse()
data = res.read()
print(data.decode("utf-8"))


