from rest_framework import authentication, exceptions
import jwt
from jwt import exceptions as jwt_exceptions

from .models import Seller


class JWTTokenAuthentication(authentication.BaseAuthentication):
    """
    JWT Token Authentication

    Clients should authenticate by passing the JWT token in the "Authorization"
    HTTP header, prepended with the string "Bearer ". For example:

    """
    keyword = 'Bearer'

    def authenticate(self, request):
        auth = authentication.get_authorization_header(request).split()

        if not auth or auth[0].lower() != self.keyword.lower().encode():
            msg = 'Invalid token header. No credentials provided.'
            raise exceptions.AuthenticationFailed(msg)

        if len(auth) == 1:
            msg = 'Invalid token header. No credentials provided.'
            raise exceptions.AuthenticationFailed(msg)
        elif len(auth) > 2:
            msg = 'Invalid token header. Token string should not contain spaces.'
            raise exceptions.AuthenticationFailed(msg)

        return self.authenticate_credentials(auth[1])


    def authenticate_credentials(self, key):

        jwt_secret = "abcdefgh"

        try:
            decoded_token = jwt.decode(key, jwt_secret, algorithms=["HS256"])["_id"]

        except jwt_exceptions.DecodeError:
            msg = 'Invalid JWT token header. Malformed JWT Token.'
            raise exceptions.AuthenticationFailed(msg)
        except jwt_exceptions.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed('Token already expired.')

        current_seller = Seller.objects.filter(phone_number=decoded_token).first()
        if current_seller is None:
            raise exceptions.AuthenticationFailed(
                'Invalid JWT token header. Seller doesn\'t have the correct permission to proceed.')

        return (current_seller, key)
