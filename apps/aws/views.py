import boto3

from django.shortcuts import render


def text_detection(request):
    client = boto3.client('rekognition')
    bucket = 'photo-bucket-artur'
    photo = 'photo'

    response = client.detect_text(Image={'S3Object': {'Bucket': bucket, 'Name': photo}})

    text_detections = response['TextDetections']
    print('Detected text\n----------')
    for text in text_detections:
        print('Detected text:' + text['DetectedText'])
        print('Confidence: ' + "{:.2f}".format(text['Confidence']) + "%")
        print('Id: {}'.format(text['Id']))
        if 'ParentId' in text:
            print('Parent Id: {}'.format(text['ParentId']))
        print('Type:' + text['Type'])

    print("Text detected: " + str(len(text_detections)))
    return render(request, 'aws/detect-text.html')
