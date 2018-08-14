# automating-aws-with-python
Repository for Automating AWS with Python

## 01-webotron

Webotron is a script that will sync a local directory to an s3 bucket, and optionally configure Route 53 and cloudfront as well.

### Options

- --profile [profile_name]    - forces webotron to use a given "aws config profile"
- --region  [region_name]     - forces webotron to use a given "aws region" (Default=us-east-1)


### Features

Webotron currently has the following features:

- List bucket
- List contents of a bucket
- List CloudFront distributions for a given domain-name
- List EC2 instances (id, type, status, tag[Name])
- Create and set up bucket
- Sync directory tree to bucket
- Set AWS profile with --profile=profileName
- Configure route 53 domain
- Setup a CloudFront CDN and SSL


## 02-notifon

Notifon is a project to notify Slack users of changes to your AWS account using CloudWatch Events

### Features

Notifon currently has the following features:

- Notify your Slack account when a Auto-scaling event occurs on your Application Load Balance



## 03 - Videolyzer

Videolyzer is a project that uses an S3 upload events (MP4 files) to trigger a Lambda function that analyses the video using AWS-Rekognition

### features

Videolyzer currently has the following features:

- ...
