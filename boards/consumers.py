import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync


class BoardUpdateConsumer(WebsocketConsumer):
    def connect(self):
        self.user = self.scope["user"]
        self.board = int(self.scope["url_route"]["kwargs"]["board"])

        self.GROUP_NAME = f"board-update-{self.board}"
        print(f"THE THINGS GROUP ON CONNECTION: {self.GROUP_NAME}")
        async_to_sync(self.channel_layer.group_add)(self.GROUP_NAME, self.channel_name)
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.GROUP_NAME, self.channel_name
        )

    def instance_created(self, event):
        self.send(
            text_data=json.dumps(
                {
                    "type": "created",
                    "id": event["id"],
                    "x": event["x"],
                    "y": event["y"],
                    "w": event["w"],
                    "h": event["h"],
                    "content": event["content"],
                }
            )
        )

    def instance_updated(self, event):
        print("INSTANCE WAS UPDATED PROPERLY")
        self.send(
            text_data=json.dumps(
                {
                    "type": "updated",
                    "id": event["id"],
                    "x": event["x"],
                    "y": event["y"],
                    "w": event["w"],
                    "h": event["h"],
                    "content": event["content"],
                }
            )
        )
