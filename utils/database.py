from boto3.dynamodb.conditions import Key, Attr
from utils.settings import dynamodb
from re import sub

push_table = dynamodb.Table("push")
DOMAIN_LIST = ["church"]


class Database:
    def __init__(self, table_name: str):
        self.table = dynamodb.Table(table_name)

    def bulk_insert(
        self,
        accounts: str,
        domain: str,
        title: str,
        body: str,
        type: str,
        id: str,
        content: str,
        stage: str,
        created_at: str,
        church_id: str,
    ):
        item = {
            "type": type,
            "title": title,
            "body": body,
            "id": id,
            "content": content,
        }

        with self.table.batch_writer() as batch:
            for index, account in enumerate(accounts):
                batch.put_item(
                    Item={
                        "account_id": account,
                        "church_id": church_id,
                        "created_at": created_at + str(index),
                        "domain": domain,
                        "stage": stage,
                        "data": item,
                    }
                )

    def filter(
        self,
        stage: str,
        account_id: str,
        domain: str,
        created_at: str,
    ):
        params = {
            "KeyConditionExpression": Key("account_id").eq(sub("-", "", account_id))
            & Key("created_at").lt(created_at),
            "FilterExpression": Attr("stage").eq(stage),
            "ScanIndexForward": False,
            "Limit": 50,
        }
        if domain in DOMAIN_LIST:
            params["FilterExpression"] = Attr("stage").eq(stage) & Attr("domain").eq(
                domain
            )

        response = self.table.query(**params)
        return response["Items"]
