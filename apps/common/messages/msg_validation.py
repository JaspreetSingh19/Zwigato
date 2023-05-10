VALIDATION = {
    'first_name': {
        "blank": "first name can not be blank",
        "invalid": "first name must contain only alphabets",
        "required": "first name required",
    },
    'last_name': {
        "blank": "last name can not be blank",
        "invalid": "last name must contains only alphabets",
        "required": "last name required",
    },
    'username': {
        "blank": "username can not be blank",
        "invalid": "username must contain alphabet and special character",
        "required": "username required",
        "exists": "username already exist",
    },
    'email': {
        "blank": "Email can not be blank",
        "required": "Email required",
        "exists": "email already exist",
        "does_not_exists": "email does not exists"

    },
    'contact': {
        "blank": "contact can not be blank",
        "required": "contact required",
        "invalid": "invalid contact"
    },
    'password': {
        "blank": "password can not be blank",
        "invalid": "Password must contain uppercase, lowercase, digit and special character",
        "required": "password required",
        "do_not_match": "Passwords do not match"

    },
    'email_otp': {
        'required': 'Please enter OTP'
    },
    "invalid credentials": "Invalid Credentials",
    'token': 'Invalid token',

}

MAX_LENGTH = {
    'first_name': 30,
    'last_name': 30,
    'username': 16,
    'password': 16,
    'contact': 10
}

MIN_LENGTH = {
    'first_name': 3,
    'last_name': 3,
    'username': 8,
    'password': 8,
    'contact': 10,
}
