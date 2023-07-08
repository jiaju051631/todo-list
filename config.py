# Environment variables
OAUTHLIB_RELAX_TOKEN_SCOPE = "1"
OAUTHLIB_INSECURE_TRANSPORT = "0"

# Flask configurations
DEBUG = False
SECRET_KEY = "thisisaveryspecialsecretkey"
SQLALCHEMY_DATABASE_URI = "sqlite:///data.sqlite"

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


# Unit testing
## Test database
SQLALCHEMY_TEST_DATABASE_URI = "sqlite:///test.sqlite"

## Test data
VALID_ACCESS_TOKEN = "test-access-token"
INVALID_ACCESS_TOKEN = "invalid-access-token"
TEST_USER_NAME = "test_GH_000"
TEST_OAUTH_PROVIDER = "github"
TEST_OAUTH_PROVIDER_USER_ID = "000"
TEST_TASK_NAME = "Test TODO item 1"
