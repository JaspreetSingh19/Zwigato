EMAIL_SITE_TITLE = "Zwigato"
INFO_EMAIL = "info@zwigato.org"
SUPPORT_PHONE = "6027774030"


EMAIL_DATA_SET = {
    'signup': {
        'subject': "Welcome to "+EMAIL_SITE_TITLE+"!",
        'body': {
            1: "Thank you for signing up !",
        },
        'notes': {
            1: "Here is your OTP",
            2: "If you have any issues with the verification process, please contact us at",
            'links': {'label': INFO_EMAIL, 'href_link': 'mailto:'+INFO_EMAIL},

        }
    },

}
