import uuid
from datetime import datetime

import boto3
from botocore.exceptions import ClientError

TABLE_NAME = "registration"
dynamodb = boto3.resource('dynamodb', region_name='ap-south-1')
table = dynamodb.Table(TABLE_NAME)
write_table = dynamodb.Table("user_data")


class DynamoRepository:
    def __init__(self):
        pass

    def create_user_in_dynamo(self, user_payload):
        now = datetime.now()
        current_time = now.strftime("%m/%d/%Y, %H:%M:%S")
        response = table.put_item(
            Item={
                'first_name': user_payload.get("first_name", "default name"),
                'last_name': user_payload.get("last_name", "default name"),
                'user_email': user_payload.get("email_id"),
                'created_time': current_time,
                'last_logged_in': user_payload.get("last_logged_in", None),
                'status': user_payload.get("status", "Single")
            }
        )
        print(f"Registration successfull with details {response}")

    def check_user_email(self, user_email):
        try:
            response = table.get_item(Key={'user_email': user_email})
        except ClientError as e:
            print(e.response['Error']['Message'])
        else:
            return response.get('Item', None)

    def write_data_in_dynamo(self, payload):
        response = write_table.put_item(
            Item=payload
        )
        print(f"Written successfully with details {response}")

