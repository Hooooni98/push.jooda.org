import csv, os, requests
from datetime import datetime
from utils.settings import S3_CLIENT


def upload_error_notification_to_s3(
    church_name: str, title: str, body: str, tokens: list
):
    file = "/tmp/error_notifications.csv"
    w = open(f"{file}", "w", encoding="utf-8")
    wr = csv.writer(w)

    wr.writerow(["교회 명", church_name])
    wr.writerow(["제목", title])
    wr.writerow(["내용", body])
    wr.writerow(["", ""])
    wr.writerow(["", ""])
    wr.writerow(["index", "fcm_token"])
    for index, token in enumerate(tokens):
        wr.writerow([index + 1, token])

    w.close()

    upload_path = f"error_logs/{str(datetime.now())[:19]}.csv"

    S3_CLIENT.upload_file(file, "jooda-push-api", upload_path)

    if os.path.exists(file) and os.path.isfile(file):
        os.remove(file)
