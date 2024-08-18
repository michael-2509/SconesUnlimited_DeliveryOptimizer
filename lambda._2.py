ENDPOINT = "image-classification-2024-08-15-16-32-11-611"  

def lambda_handler(event, context):

    # Decode the image data from the event
    image = base64.b64decode(event["image_data"])  # TODO: Ensure "image_data" is the correct key

    # Instantiate a Predictor
    predictor = Predictor(
        endpoint_name=ENDPOINT,  # Use the endpoint name you specified above
        sagemaker_session=boto3.Session().client('sagemaker')
    )

    # For this model, the IdentitySerializer needs to be "image/png"
    predictor.serializer = IdentitySerializer("image/png")
    
    # Make a prediction
    inferences = predictor.predict(image)
    
    # We return the data back to the Step Function    
    event["inferences"] = inferences.decode('utf-8')
    return {
        'statusCode': 200,
        'body': json.dumps(event)
    }