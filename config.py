# Environment variables
OAUTHLIB_RELAX_TOKEN_SCOPE = "1"
OAUTHLIB_INSECURE_TRANSPORT = "0"

# Flask configurations
DEBUG = True
SECRET_KEY = "thisisaveryspecialsecretkey"
SQLALCHEMY_DATABASE_URI   = "sqlite:///data.sqlite"

# OAuth configurations
GOOGLE_OAUTH_CLIENT_ID = "150745538866-ao8g94450vjmo4nfg03vbucuv7hjmkqd.apps.googleusercontent.com"
GOOGLE_OAUTH_CLIENT_SECRET = "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"
GITHUB_OAUTH_CLIENT_ID = "d7a57bc22d0405993c51"
GITHUB_OAUTH_CLIENT_SECRET = "4af5c6817d84994520f7ef6c871e32d5586f2959"
FACEBOOK_OAUTH_CLIENT_ID = "955707712312608"
FACEBOOK_OAUTH_CLIENT_SECRET = "96c5c5660e7df0a22a165c690fbd554c"

# SSL files
SSL_CERT = "ssl/cert.pem"
SSL_KEY = "ssl/key.pem" 