from src.register.exceptions import UserNotFoundException
from src.register.repository.cognito_repository import CognitoRepository
from src.register.repository.dynamo_repository import DynamoRepository


class UserService:
    def __init__(self):
        self.cognito_repo = CognitoRepository()
        self.dynamo_repo = DynamoRepository()

    def create_user(self, user_payload):
        self.cognito_repo.create_user_in_cognito(user_payload=user_payload)
        self.cognito_repo.admin_set_user_password(username=user_payload.get("email_id"))
        self.dynamo_repo.create_user_in_dynamo(user_payload=user_payload)

    def user_login(self, username):
        check_email_presence = self.dynamo_repo.check_user_email(user_email=username)
        if check_email_presence:
            return self.cognito_repo.user_login(username=username)
        else:
            raise UserNotFoundException()

    def write_data(self, token, payload):
        self.cognito_repo.verify_token(token)
        self.dynamo_repo.write_data_in_dynamo(payload=payload)
        return "Successfully Updated"
