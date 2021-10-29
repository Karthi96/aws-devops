import json
import time
import urllib.request
import urllib.request

import boto3
import botocore
from jose import jwk, jwt
from jose.utils import base64url_decode

from src.register.exceptions import UserFoundException

USER_POOL_ID = "User pool id"
TEMPORARY_PASSWORD = "Demo@12345"
CLIENT_ID = "client id"
KEYS_URL = 'https://cognito-idp.{}.amazonaws.com/{}/.well-known/jwks.json'.format("ap-south-1", USER_POOL_ID)

client = boto3.client('cognito-idp', region_name='ap-south-1')


class CognitoRepository:

    def create_user_in_cognito(self, user_payload):
        user_attributes = [
            {"Name": "custom:first_name", "Value": user_payload.get("first_name", "default name")},
            {"Name": "custom:last_name", "Value": user_payload.get("last_name", "default name")},
            {"Name": "email_verified", "Value": "true"},
            {"Name": "custom:full_name", "Value": user_payload.get("full_name", "default name")},
            {"Name": "email", "Value": user_payload.get("email_id", "default name")}
        ]
        try:
            response = client.admin_create_user(
                UserPoolId=USER_POOL_ID,
                Username=user_payload.get("email_id"),
                UserAttributes=user_attributes,
                DesiredDeliveryMediums=['EMAIL'],
                TemporaryPassword=TEMPORARY_PASSWORD
            )
        except botocore.exceptions.ClientError as err:
            if err.response['Error']['Code'] == 'UsernameExistsException':
                raise UserFoundException()
            else:
                raise err

        if response["ResponseMetadata"]["HTTPStatusCode"] != 200:
            raise Exception(f"Failed to create user in cognito for the payload={user_payload}")

    def admin_set_user_password(self, username):
        try:
            response = client.admin_set_user_password(
                UserPoolId=USER_POOL_ID,
                Username=username,
                Password=TEMPORARY_PASSWORD,
                Permanent=True
            )
        except botocore.exceptions.ClientError as err:
            raise err

        if response["ResponseMetadata"]["HTTPStatusCode"] != 200:
            raise Exception(f"Failed to set the password for username={username}")

    def user_login(self, username):
        response = client.admin_initiate_auth(
            UserPoolId=USER_POOL_ID,
            ClientId=CLIENT_ID,
            AuthFlow='ADMIN_NO_SRP_AUTH',
            AuthParameters={
                'USERNAME': username,
                'PASSWORD': TEMPORARY_PASSWORD
            }
        )
        if response["ResponseMetadata"]["HTTPStatusCode"] != 200:
            raise Exception(f"Failed to login username={username}")

        return response

    def verify_token(self, token):
        with urllib.request.urlopen(KEYS_URL) as f:
            response = f.read()
        keys = json.loads(response.decode('utf-8'))['keys']

        headers = jwt.get_unverified_headers(token)
        kid = headers['kid']
        key_index = -1
        for i in range(len(keys)):
            if kid == keys[i]['kid']:
                key_index = i
                break
        if key_index == -1:
            print('Public key not found in jwks.json')
            return False

        public_key = jwk.construct(keys[key_index])
        message, encoded_signature = str(token).rsplit('.', 1)
        # decode the signature
        decoded_signature = base64url_decode(encoded_signature.encode('utf-8'))
        # verify the signature
        if not public_key.verify(message.encode("utf8"), decoded_signature):
            print('Signature verification failed')
            return False
        print('Signature successfully verified')

        claims = jwt.get_unverified_claims(token)
        if time.time() > claims['exp']:
            print('Token is expired')
            return False
        if claims['aud'] != CLIENT_ID:
            print('Token was not issued for this audience')
            return False

        return True
