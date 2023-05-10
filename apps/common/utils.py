import random


def generate_otp(length=4):
    """
    Generates a random OTP of the specified length (default 6 digits).
    """
    digits = "0123456789"
    otp = ""

    for i in range(length):
        otp += random.choice(digits)

    return otp
