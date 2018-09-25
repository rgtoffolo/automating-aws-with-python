# -*- coding: utf-8 -*-

"""Classes for EC2 Instances."""


class EC2Manager:
    """Manage EC2 Instances."""

    def __init__(self, session):
        """Create a EC2Manager object."""
        self.session = session
        self.ec2 = self.session.resource('ec2')


    def list_instances(self):
        """List all existing instances in the default zone."""
        response = self.ec2.instances.all()
        return response

    def list_instances_by_tag(self, tag_key, tag_value):
        """List intances by tag Name:Value."""
        response = self.session.client('ec2').describe_instances(
            Filters=[
                {
                    'Name': 'tag:' + tag_key,
                    'Values': [
                        tag_value
                    ]
                },
                {
                    'Name': 'instance-state-name',
                    'Values': ['pending',
                               'running',
                               'shutting-down',
                               'stopping',
                               'stopped']  # not showing terminated instances

                }
            ]
        )
        return response
