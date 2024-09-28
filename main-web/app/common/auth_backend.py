from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed
from common.utils import is_access_token_blacklisted  # Import the utility function

class CustomJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        auth = super().authenticate(request)

        if not auth:
            return None

        user, token = auth
        # print(type(auth), '\n', auth,  '\n \n \n')
        # print(user)
        # print(token)

        # Check if the token is blacklisted using the utility function
        if is_access_token_blacklisted(token):
            raise AuthenticationFailed("This token has been blacklisted.", code=401)

        return auth
