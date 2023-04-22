import json
import os
import boto3

STATE_MACHINE_ARN = os.environ['STATE_MACHINE_ARN']
DEFAULT_TARGET_EMAIL = os.environ['DEFAULT_TARGET_EMAIL']
DEFAULT_SOURCE_EMAIL = os.environ['DEFAULT_SOURCE_EMAIL']
DEFAULT_TARGET_NUMBER = os.environ['DEFAULT_TARGET_NUMBER']
DEFAULT_SOURCE_NUMBER = os.environ['DEFAULT_SOURCE_NUMBER']
sf_client = boto3.client('stepfunctions')

def start_step_function_execution(message_id, sf_input):
    # Execute Step Function for CodeBuild
    try:
        sf_response = sf_client.start_execution(
            stateMachineArn=STATE_MACHINE_ARN,
            name="Notification-" + message_id,
            input=json.dumps(sf_input),
        )
        print(sf_response)
    except Exception as e:
        print(e)

def handler(event, context):
    body = json.loads(event['Records'][0]['body'])
    '''
    {
        "status": String()
        "message": String()
        "channels": Array(String)
    }
    '''
    status = body['data']['status']
    message = body['data']['message']
    channels = body['data']['channels']
    message_id = event['Records'][0]['messageId']

    sf_input = {
        status: status,
        message: message,
        channels: channels,
        message_id: message_id
    }
    start_step_function_execution(message_id, sf_input)

    # TODOS: Build the Step Function State Machine JSON file
    # TODOS: Test the Step Function Execution

    return {}