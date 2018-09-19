#!/usr/bin/python
# -*- coding: utf-8 -*-
# -*- mode: python -*-


"""Webotron: Deploy websites with AWS.

Webotron automates the process of deploying static websites
- Configure AWS S3 Buckets
  - Create them
  - Set them up for static website hosting
  - Deploy local files to them
- Configure DNS with AWS Route 53
- Configure a Content Delivery Network and SSL with AWS CloudFront
"""


import boto3
import click		# click.pocoo.org


# added "webotron." to make the script packable
from webotron.bucket import BucketManager
from webotron.domain import DomainManager
from webotron.certificate import CertificateManager
from webotron.cdn import DistributionManager
from webotron.ec2 import EC2Manager
from webotron.ecs import ECSManager
from webotron import util

SESSION = None
BUCKET_MANAGER = None
DOMAIN_MANAGER = None
CERT_MANAGER = None
DIST_MANAGER = None
EC2_MANAGER = None
ECS_MANAGER = None

str_sep = "-" * 80


@click.group()
@click.option('--profile', default=None,
              help='Use a given AWS profile.')
@click.option('--region', default='us-east-1',
              help='Use a given AWS region. Default=us-east-1')
def cli(profile, region):
    """Webotron deploys websites do AWS."""
    global SESSION, BUCKET_MANAGER, DOMAIN_MANAGER, CERT_MANAGER, \
        DIST_MANAGER, EC2_MANAGER, ECS_MANAGER
    session_cfg = {}
    if profile:
        session_cfg['profile_name'] = profile

    if region:
        session_cfg['region_name'] = region


# using **<variable> python expands it as a parameter=content
    SESSION = boto3.Session(**session_cfg)
    BUCKET_MANAGER = BucketManager(SESSION)
    DOMAIN_MANAGER = DomainManager(SESSION)
    CERT_MANAGER = CertificateManager(SESSION)
    DIST_MANAGER = DistributionManager(SESSION)
    EC2_MANAGER = EC2Manager(SESSION)
    ECS_MANAGER = ECSManager(SESSION)


@cli.command('list-buckets')
def list_buckets():
    """List all s3 buckets."""
    for bucket in BUCKET_MANAGER.all_buckets():
        print(bucket)


@cli.command('list-bucket-objects')
@click.argument('bucket')
def list_bucket_objects(bucket):
    """List objects available in the bucket."""
    for obj in BUCKET_MANAGER.all_objects(bucket).all():
        print(obj)


@cli.command('setup-bucket')
@click.argument('bucket')
def setup_bucket(bucket):
    """Create and configure S3 bucket."""
    s3_bucket = BUCKET_MANAGER.init_bucket(bucket)
    BUCKET_MANAGER.set_policy(s3_bucket)
    BUCKET_MANAGER.configure_website(s3_bucket)


@cli.command('sync')
@click.argument('pathname', type=click.Path(exists=True))
@click.argument('bucket')
def sync(pathname, bucket):
    """Sync contents of PATHNAME to BUCKET."""
    BUCKET_MANAGER.sync(pathname, bucket)
    print(BUCKET_MANAGER.get_bucket_url(BUCKET_MANAGER.s3.Bucket(bucket)))


@cli.command('setup-domain')
@click.argument('domain')
def setup_domain(domain):
    """Configure DOMAIN to point to BUCKET."""
    bucket = BUCKET_MANAGER.get_bucket(domain)

    zone = DOMAIN_MANAGER.find_hosted_zone(domain) \
        or DOMAIN_MANAGER.create_hosted_zone(domain)

    endpoint = util.get_endpoint(BUCKET_MANAGER.get_region_name(bucket))
    a_record = DOMAIN_MANAGER.create_s3_domain_record(zone, domain, endpoint)
    print("Domain configure: http://{}".format(domain))
    print("A record created: {}".format(a_record))


@cli.command('find-cert')
@click.argument('domain')
def find_cert(domain):
    """Find a certificate for <DOMAIN>."""
    print(CERT_MANAGER.find_matching_cert(domain))


@cli.command('find-dist')
@click.argument('domain')
def find_dist(domain):
    """Find a distribution (CloudFront) for a <DOMAIN>."""
    print(DIST_MANAGER.find_matching_dist(domain))


@cli.command('setup-cdn')
@click.argument('domain')
@click.argument('bucket')
def setup_cdn(domain, bucket):
    """Set up CloudFront CDN for DOMAIN pointing to BUCKET."""
    dist = DIST_MANAGER.find_matching_dist(domain)

    if not dist:
        cert = CERT_MANAGER.find_matching_cert(domain)
        if not cert:  # SSL is not optional at this time
            print("Error: No matching cert found.")
            return

        dist = DIST_MANAGER.create_dist(domain, cert)
        print("Waiting for distribution deployment...")
        DIST_MANAGER.await_deploy(dist)

    zone = DOMAIN_MANAGER.find_hosted_zone(domain) \
        or DOMAIN_MANAGER.create_hosted_zone(domain)

    DOMAIN_MANAGER.create_cf_domain_record(zone, domain, dist['DomainName'])

    print("Domain configured: https://{}".format(domain))

    return


@cli.command('list-instances')
def list_instances():
    """List the EC2 instances for the current session."""
    print(str_sep)
    print("Listing EC2 instances form {} region.".format(SESSION.region_name))
    print("{:20s}{:15s}{:10s}{}".format("ID", "TYPE", "STATE", "NAME"))
    print(str_sep)

    for instance in EC2_MANAGER.list_instances():
        # get the instance name in the tags list
        name = next((item for item in instance.tags if item["Key"] == "Name"),
                    {'Key': 'Name', 'Value': 'None'})

        print("{:20s}{:15s}{:10s}{}".format(instance.id,
                                instance.instance_type,
                                instance.state['Name'],
                                name['Value']))

    print(str_sep)


@cli.command('list-ecs-clusters')
def list_ecs_clusters():
    """List ECS clusters for a given profile and region."""
    clusters = ECS_MANAGER.list_ecs_clusters()

    print(str_sep)

    if clusters:
        print("Listing clusters ARNs available in {}".format(SESSION.region_name.upper()))
        print(str_sep)
        for arn in clusters['clusterArns']:
            print(arn)

    print(str_sep)


@cli.command('list-ecs-task-definitions')
def list_ecs_task_definitions():
    """List ECS task definitions."""
    tasks = ECS_MANAGER.list_ecs_task_definitions()
    if tasks:
        print(str_sep)
        print("Listing task definitions available in {}".format(SESSION.region_name.upper()))
        print("{:50}{:20}".format('Task', 'Version'))
        print(str_sep)

        for task in tasks['taskDefinitionArns']:
            if len(task) > 0:
                task_name, version = task.rsplit("/", 1)[1].split(":")
                print("{:50}{:20}".format(task_name, version))


@cli.command('list-ecr-repositories')
def list_ecr_repositories():
    """List ECR repositories and URIs."""
    repositories = ECS_MANAGER.list_ecr_repositories()

    if repositories:
        print(str_sep)
        print("Listing repositories available in {}".format(SESSION.region_name.upper()))
        print("{:30}{:60}".format('NAME', 'URI'))
        print(str_sep)

        for rep in repositories['repositories']:
            print("{:30}{:60}".format(rep['repositoryName'], rep['repositoryUri']))


@cli.command('list-ecr-repository-details')
@click.argument('repository_name')
def list_ecr_repository_details(repository_name):
    """List ECR repository details from a given repository name."""
    rep_details = ECS_MANAGER.list_ecr_repository_details(repository_name)

    print(str_sep)
    print("Listing details from repository [{}] in {}".format(repository_name, SESSION.region_name.upper()))
    print("{:20}{:20}{:30}".format('REP NAME', 'IMAGE TAGS', 'PUSHED AT'))
    print(str_sep)

    for detail in rep_details['imageDetails']:
        for tag in detail['imageTags']:
            print("{:20}{:20}{:%Y-%m-%d %H:%M:%S}".format(detail['repositoryName'],
                                                          tag,
                                                          detail['imagePushedAt']))


if __name__ == '__main__':
    # print the arguments received
    # print(sys.argv)
    cli()
