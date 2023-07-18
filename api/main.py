from mangum import Mangum
from fastapi import FastAPI, Request
from pydantic import BaseModel

from firebase_admin import messaging

from datetime import datetime

from utils.slack import slack_post_message, check_ip
from utils.upload_error import upload_error_notification_to_s3
from utils.database import Database

app = FastAPI()
handler = Mangum(app=app)


class Notification(BaseModel):
    tokens: list
    accounts: list
    title: str
    body: str
    content: str
    type: str
    id: str
    stage: str
    church_id: str


@app.get("/api/")
async def list(
    stage: str,
    account_id: str,
    created_at: str = str(datetime.today()),
    domain: str = None,
):
    push_table = Database("push")
    payload = {
        "push_notification_list": push_table.filter(
            stage, account_id, domain, created_at
        )
    }
    return {"success": True, "payload": payload}


@app.post("/api/churchs/")
async def create(notification: Notification):
    date_now = str(datetime.today())
    try:
        push_table = Database("push")

        message = messaging.MulticastMessage(
            notification=messaging.Notification(
                title=notification.title,
                body=notification.body,
            ),
            tokens=notification.tokens,
            data={
                "domain": "church",
                "type": notification.type,
                "id": notification.id,
                "content": notification.content,
                "created_at": date_now,
                "church_id": notification.church_id,
            },
        )
        messaging.send_multicast(message)
        push_table.bulk_insert(
            accounts=notification.accounts,
            domain="church",
            title=notification.title,
            body=notification.body,
            type=notification.type,
            id=notification.id,
            content=notification.content,
            stage=notification.stage,
            created_at=date_now,
            church_id=notification.church_id,
        )
        return {"success": True}
    except Exception as error:
        slack_post_message(
            notification.title,
            notification.body,
            notification.content,
            error,
        )
        upload_error_notification_to_s3(
            notification.title,
            notification.body,
            notification.content,
            notification.tokens,
        )
        return {"success": False}
