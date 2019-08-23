import os

class Config():
    # clef de protection obtenue avec :
    # import secret
    # secrets.token_hex(16)
    SECRET_KEY = 'e3d382beb72006c1b138754e940145d7'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'

    TOASTR_TIMEOUT = 2000
    TOASTR_EXTENDED_TIMEOUT = 0
    TOASTR_POSITION_CLASS = 'toast-bottom-center'

    ## config Mail
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    #MAIL_USENAME = os.environ.get('EMAIL_USER')
    #MAIL_USENAME = os.environ.get('EMAIL_USER')

    MAIL_USERNAME = 'valent1lefranc@gmail.om'
    MAIL_PASSWORD = ''

    ### UPLOAD CONFIG ###############
    UPLOAD_FOLDER = 'C:/Users/Vlefranc/'
    ALLOWED_EXTENSIONS = set(['txt', 'csv'])
    UPLOAD_FOLDER = UPLOAD_FOLDER
