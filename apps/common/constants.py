REGEX = {
    "first_name": r'^[a-zA-Z]+$',
    "last_name": r'^[a-zA-Z]+$',
    "username": r'^(?=.*[!@#$%^&*()_+|~=`{}\[\]:";\'<>?,.\/])(?=.*[a-zA-Z0-9])'
                r'[a-zA-Z0-9!@#$%^&*()_+|~=`{}\[\]:";\'<>?,.\/]{8,}$',
    "contact": r'^\d+$',
    "password": r'^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[!@#$%^&*()_+=-])[0-9a-zA-Z!@#$%^&*()_+=-]{8,16}$',
}

OTP_LENGTH = 4
FP_TOKEN_LENGTH = 10
PASSWORD_RESET_TIME = (2 * 60)
