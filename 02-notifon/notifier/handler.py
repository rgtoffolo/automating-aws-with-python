import os

from botocore.vendored import requests

def autoscaling_post_to_slack(event, context):
    slack_webhook_url = os.environ['SLACK_WEBHOOK_URL']

    slack_message = "From {source} at {detail[StartTime]}: {detail[Description]}".format(**event)
    data = { "text": slack_message }
    requests.post(slack_webhook_url, json=data)

    return


def ec2state_post_to_slack(event, context):
    slack_webhook_url = os.environ['SLACK_WEBHOOK_URL']

    slack_message = "From {account}/{source}/{region} --> {detail-type}: {detail[instance-id]}/{detail[state]}".format(**event)

    data = { "text": slack_message }

    requests.post(slack_webhook_url, json=data)

    #print(event)
    #print(slack_message)

    return
