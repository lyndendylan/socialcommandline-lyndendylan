import oauthclient
import AuthController

class TwitterController(AuthController.AuthController):
    """Controller for handling Twitter Oauth"""

    __display_name = "Twitter"
    __request_token_url = "https://api.twitter.com/oauth/request_token"
    __authorize_url = "https://api.twitter.com/oauth/authenticate"
    __access_token_url = "https://api.twitter.com/oauth/access_token"
    __authenticate_url = "https://api.twitter.com/oauth/authenticate"
    __consumer_key = "MIEorUIGXR3Z4W4aUsv83hled"
    __consumer_secret = "GyEJT7eTiYTIWmyc2sNGnFXNv790DAhNe9CrxNYwoUm5yMMfN0"


    @classmethod
    def get_twitter_service(cls):
        twitter_service = oauthclient.models.OAuthService.get_by_key_name("twitter")
        if twitter_service is None:
            twitter_service                     = oauthclient.models.OAuthService(key_name="twitter")
            twitter_service.display_name        = cls.__display_name
            twitter_service.request_token_url   = cls.__request_token_url
            twitter_service.authorize_url       = cls.__authorize_url
            twitter_service.access_token_url    = cls.__access_token_url
            twitter_service.authenticate_url    = cls.__authenticate_url
            twitter_service.consumer_key        = cls.__consumer_key
            twitter_service.consumer_secret     = cls.__consumer_secret

            twitter_service.put()
        else:
            return oauthclient.models.OAuthService.get_by_key_name("twitter")



    

