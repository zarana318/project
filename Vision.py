import base64
import argparse
from picamera import PiCamera
from time import sleep
import pyttsx
from googleapiclient.discovery import build
from oauth2client.client import GoogleCredentials


def cam():
    camera=PiCamera()
    camera.capture('/home/pi/Desktop/project_pi/img.jpg')

def voice(label):
    engine=pyttsx.init()
    engine.say("Lables found"+label)
    engine.runAndWait()


def main(photo):

    credentials=GoogleCredentials.get_application_default()
    service=build("vision","v1",credentials=credentials)

    cam()

    with open(photo,"rb") as image:
        image_content=base64.b64encode(image.read())
        service_request = service.images().annotate(body={
                'requests': [{
                    'image': {
                        'content': image_content.decode('UTF-8')
                    },
                    'features': [{
                        'type': 'LABEL_DETECTION',
                        'maxResults': 1
                    }]
                }]
            })
        response = service_request.execute()
        label= response['responses'][0]['labelAnnotations'][0]['description']
        print('Found label: %s for %s' % (label, photo))
        voice(label)

        

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('image_file', help='The image you\'d like to label.')
    args = parser.parse_args()
    main(args.image_file)

