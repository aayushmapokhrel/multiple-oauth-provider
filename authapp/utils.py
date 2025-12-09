import random


def send_verification_email(user):
    # TODO: implement email sending
    return True


def send_otp(user):
    # TODO: Twilio or email OTP
    otp = random.randint(100000, 999999)
    return otp
