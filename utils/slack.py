import requests, json

SLACK_TOKEN = "##############"
slack_post_uri = "https://slack.com/api/chat.postMessage"
headers = {"Authorization": "Bearer " + SLACK_TOKEN}
channel = "#jooda_error_log"


def slack_post_message(church_name: str, title: str, body: str, error: str):
    attachment = [
        {
            "title": "[🤢 교회 푸시 알림 에러 발생 🤮]",
            "text": f"⛪︎  {church_name}",
            "fields": [
                {
                    "title": "푸시 알림 제목",
                    "value": title,
                },
                {
                    "title": "푸시 알림 내용",
                    "value": body,
                },
            ],
            "fallback": "교회 푸시 알림 에러 발생, 무슨 일인지 알아볼까요?",
            "color": "#5400DD",
            "attachment_type": "default",
            "actions": [
                {
                    "name": "confirm_error_log",
                    "text": "에러 로그 확인",
                    "type": "button",
                    "url": f"https://s3.console.aws.amazon.com/s3/buckets/jooda-push-api?prefix=error_logs/&region=ap-northeast-2",
                },
            ],
        }
    ]
    requests.post(
        slack_post_uri,
        headers=headers,
        data={
            "channel": channel,
            "text": f"❗️[error_message] :{error}",
            "attachments": json.dumps(attachment),
        },
    )


def check_ip(host):
    requests.post(
        slack_post_uri,
        headers=headers,
        data={"channel": "#jooda_error_log", "text": f"❗️[error_message] :{host}"},
    )
