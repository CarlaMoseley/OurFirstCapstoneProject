import hashlib
import hmac
import base64
import time
import json
import uuid
import requests

class PaymentService:
    def __init__(self):
        # Replace these values with your actual API key and other required information
        self.api_key = "9y2JnAIowGH2WBccw8HjOdTlAt5ClV7w"
        self.secret = "8WAAnoi0EL6GBAleNgrowHQEtwVN1jSULNCivGegvBe"
        self.merchant_id = "100008000003683"
        self.terminal_id = "10000001"

    def generate_auth_token(self, data, key):
        try:
            key_bytes = key.encode('utf-8')
            data_bytes = data.encode('utf-8')
            hashed = hmac.new(key_bytes, data_bytes, hashlib.sha256)
            return base64.b64encode(hashed.digest()).decode('utf-8')
        except Exception as e:
            print(f"Error Generating Auth Token: {str(e)}")
            return None

    def make_payment_request(self):
        timestamp = int(time.time() * 1000)
        client_request_id = str(uuid.uuid4())

        # Replace this with your actual request body
        request_body = {
            "amount": {
                "total": 12.04,
                "currency": "USD"
            },
            "source": {
                "sourceType": "PaymentCard",
                "card": {
                    "cardData": "4005550000000019",
                    "expirationMonth": "02",
                    "expirationYear": "2035",
                    "securityCode": "123"
                }
            },
            "transactionDetails": {
                "captureFlag": True
            },
            "merchantDetails": {
                "merchantId": "100008000003683",
                "terminalId": "10000001"
            }
        }

        # Convert the request body to a JSON string
        json_request_body = json.dumps(request_body)

        # Replace this with the actual URL of the API endpoint
        url = "https://cert.api.fiservapps.com/ch/payments/v1/charges"

        # Construct the raw signature
        raw_signature = f'{self.api_key}{client_request_id}{timestamp}{json_request_body}'

        # Hash the raw signature using HMAC-SHA256
        hashed_signature = hmac.new(self.secret.encode(), raw_signature.encode(), hashlib.sha256).digest()

        # Encode the hashed signature using Base64
        computed_hmac = self.generate_auth_token(raw_signature, self.secret)

        # Set the headers
        headers = {
            'Content-Type': 'application/json',
            'Client-Request-Id': client_request_id,
            'Api-Key': self.api_key,
            'Timestamp': str(timestamp),
            'Auth-Token-Type': 'HMAC',
            'Authorization': computed_hmac
        }

        # Make the API request
        response = requests.post(url, headers=headers, json=request_body)

        # Print the response status code and content
        print("Response Status Code:", response.status_code)
        print("Response Content:", response.json())

# Example Usage:
payment_service = PaymentService()
payment_service.make_payment_request()
