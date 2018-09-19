# -*- coding: utf-8 -*-

"""Classes for EC2 Instances."""


class EC2Manager:
    """Manage EC2 Instances."""

    def __init__(self, session):
        """Create a BucketManager object."""
        self.session = session
        self.ec2 = self.session.resource('ec2')

    def list_instances(self):
        """List all existing instances in the default zone."""
        response = self.ec2.instances.all()
        return response
