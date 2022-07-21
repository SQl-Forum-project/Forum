import os
import requests


def send_mail(email, subject, body):
    headers = {
        'accept': 'application/json',
        'api-key': os.environ.get('EMAIL_API'),
        'content-type': 'application/json',
    }

    json_data = {
        'sender': {
            'name': 'SIES Forum',
            'email': 'salmanad5s3@gmail.com',
        },
        'to': [
            {
                'email': email,
                'name': 'SIES Forum',
            },
        ],
        'subject': subject,
        'htmlContent': body,
    }

    try:
        response = requests.post(
            'https://api.sendinblue.com/v3/smtp/email', headers=headers, json=json_data)
        print(response.text)
        return True

    except Exception as e:
        print(e)
        return False
