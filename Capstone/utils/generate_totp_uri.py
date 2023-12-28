import pyotp


def generate_totp_uri(username):
    totp_secret = pyotp.random_base32()
    totp = pyotp.totp.TOTP(totp_secret)
    return totp.provisioning_uri(name=username, issuer_name="YourApp"), totp_secret