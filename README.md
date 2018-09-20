# automating-aws-with-python
Repository for Automating AWS with Python

## 01-webotron

Webotron is a script that has a list of features that can be used to interact with your AWS resources.


### Options

- -p, --profile [profile_name]    - forces webotron to use a given "aws config profile"
- -r, --region  [region_name]     - forces webotron to use a given "aws region" (Default=us-east-1)
- -c, --clear                     - clear terminal screen before returning the script results


### Features

Webotron currently has the following features:

S3
- List bucket
- List contents of a bucket
- Create and set up bucket
- Sync directory tree to bucket

CloudFront / Route53
- List CloudFront distributions for a given domain-name
- Setup a CloudFront CDN and SSL
- Configure route 53 domain

EC2
- List EC2 instances (id, type, status, tag[Name])
- List EC2 instances filtering by tag (key/value)

ECS/ECR
- List ECS clusters ARNs
- List ECS task definitions/versions
- List ECR repositories
- List ECR repository details (from a given repository name)



## 02-notifon

Notifon is a project to notify Slack users of changes to your AWS account using CloudWatch Events

### Features

Notifon currently has the following features:

- Notify your Slack account when:

  - an Auto-scaling event occurs on your Application Load Balance
  - an EC2-instance change its state


## 03 - Videolyzer

Videolyzer is a project that uses an S3 upload events (MP4 files) to trigger a Lambda function that analyses the video using AWS-Rekognition

### features

Videolyzer currently has the following features:

- Using an S3 event Videolyzer calls AWS-Rekognition and return a list of tags with there are in the video. After processing the video, the completion is notified via SNS topic and saved in DynamoDB.
