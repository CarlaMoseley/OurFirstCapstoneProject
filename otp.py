import pyotp
import qrcode
from PIL import Image

#generate a long phrase for the keys
key = "THEELEPHANTINTHEROOM572"

#we start calling the time generating OTP... only last 30 seconds 
totp = pyotp.TOTP(key)

#Generate the URI for the user name and the issuer_name
url =totp.provisioning_uri(name="@katashi1995", issuer_name="MACK")

#create qr code from URI
qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L, 
    box_size=10,
    border=4
    )
qr.add_data(url)
qr.make(fit=True)

#create image from QR code
img=qr.make_image(fill_color="black", back_color="white")

while True:
    img.show()
    
    user_MSG = input("Please enter your Google OTP code: ")
    try:
        generated_otp = totp.now()
        if int(user_MSG) == int(generated_otp):
                print("Valid OTP")
        else:
            print("Wrong. Access denied")
    except ValueError:
        print("Invalid input.")
    