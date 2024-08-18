import json
import base64
import boto3


runtime= boto3.client('runtime.sagemaker')

# Fill this in with the name of your deployed model
ENDPOINT = "image-classification-2024-08-15-16-32-11-611"

def lambda_handler(event, context):

    # Decode the image data
    image = base64.b64decode(event['body']['image_data'])

    response = runtime.invoke_endpoint(EndpointName=ENDPOINT, ContentType='image/png', Body=image)

    # Make a prediction and deserialize:
    inferences = json.loads(response['Body'].read().decode('utf-8'))
    
    # We return the data back to the Step Function    
    event["inferences"] = inferences
    return {
        'statusCode': 200,
        'body': json.dumps(event)
    }