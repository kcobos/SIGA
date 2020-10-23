import firebase_admin
from firebase_admin import credentials
from firebase_admin import messaging

class Notificacion():
    def __init__(self):
        cred = credentials.Certificate("")
        self.app = firebase_admin.initialize_app(cred)

    def notificar(self, tokens):
        # print(firebase_admin.get_app())
        # print(tokens)
        # print("===============")
        for token in tokens:
            print(token)
            # See documentation on defining a message payload.
            message = messaging.Message(
                data={
                    "title": "El aparcamiento ha sido ocupado",
                    "message": "El aparcamiento donde se dirige ha sido ocupado"
                },
                token=token,
            )

            # Send a message to the device corresponding to the provided
            # registration token.
            response = messaging.send(message)
            # Response is a message ID string.
            # print('Successfully sent message:', response)

            firebase_admin.delete_app(self.app)
