import hashlib
import hmac
import base64
import time
import json
import uuid
import requests
from datetime import date


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
        
    def luhn(self, card_number):
        singled_digits = list(card_number[-1::-2])
        doubled_digits = ''.join([str(2*int(i)) for i in list(card_number[-2::-2])])

        double_num = sum([int(i) for i in doubled_digits])
        single_num = sum([int(i) for i in singled_digits])

        return (double_num + single_num) % 10 == 0

    def validate_cc_number(self, card_number):
        cc_length = len(card_number)

        if cc_length < 13 or cc_length > 16:
            # no valid cards exist of this length
            return False, None
        
        if card_number[0] == "4" and (cc_length == 16 or cc_length == 13):
            card_type = "Visa"
        elif int(card_number[:2]) in range(51,56) and cc_length == 16:
            card_type = "MasterCard"
        elif card_number[:2] in ["34", "37"] and cc_length == 15:
            card_type = "Amex"
        elif card_number[:5] == "6011" and cc_length == 16:
            card_type = "Discover"
        elif card_number[0] == "3" and cc_length == 16:
            card_type = "JCB"
        elif card_number[:5] in ["2123","1800"] and cc_length == 15:
            card_type = "JCB"
        elif card_number[:2] in ["36", "38"] and cc_length == 14:
            card_type = "Diners Club"
        elif int(card_number[:3]) in range(300,306) and cc_length == 14:
            card_type = "Diners Club"
        else:
            return False, None
        
        return self.luhn(card_number), card_type
        

        
    def make_dummy_cc_request(self, amount, card_number, expiration_month, expiration_year, security_code):
        is_cc_valid, card_type = self.validate_cc_number(card_number)
        last_cc_day = date(int(expiration_year), int(expiration_month)+1, 1)
        today = date.today()

        if is_cc_valid and last_cc_day > today:
            approval_status = 'APPROVED'
        else:
            approval_status = 'NOT_APPROVED'

        response_body = {
            "paymentReceipt": {
                "approvedAmount": {
                    "total": amount,
                    "currency": "USD"
                },
            "processorResponseDetails": {
                "approvalStatus": approval_status,
                "cardType": card_type
                }
            }
        }

        return json.dumps(response_body)


    def make_cc_request(self, amount, card_number, expiration_month, expiration_year, security_code):
        timestamp = int(time.time() * 1000)
        client_request_id = str(uuid.uuid4())

        # Replace this with your actual request body
        request_body = {
            "amount": {
                "total": amount,
                "currency": "USD"
            },
            "source": {
                "sourceType": "PaymentCard",
                "card": {
                    "cardData": card_number,
                    "expirationMonth": expiration_month,
                    "expirationYear": expiration_year,
                    "securityCode": security_code
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
        return requests.post(url, headers=headers, json=request_body)
    
    def make_ach_request(self, amount, account_number, routing_number):
        valid_routes = ["0" + str(i) for i in range(1,10)] + [str(i) for i in range(21,33)] + [str(i) for i in range(61,73)] + ['11', '12', '80']
        validate_sum = (3*(int(routing_number[0])+int(routing_number[3])+int(routing_number[6])) + 7*(int(routing_number[1])+int(routing_number[4])+int(routing_number[7])) + (int(routing_number[2])+int(routing_number[5])+int(routing_number[8])))%10 
        if not validate_sum == 0:
            # The routing number is invalid, the request should fail
            approval_status = "NOT_APPROVED"
        elif not routing_number[:2] in valid_routes:
            # the routing number is invalid, the request should fail
            print("we made it ")
            approval_status = "NOT_APPROVED"
        else:
            # the routing number is valid, the request should pass
            approval_status = "APPROVED"


        response_body = {
            "paymentReceipt": {
                "approvedAmount": {
                    "total": amount,
                    "currency": "USD"
                },
            "processorResponseDetails": {
                "approvalStatus": approval_status,
                }
            }
        }

        return json.dumps(response_body)
        

