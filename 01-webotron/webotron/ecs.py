# -*- coding: utf-8 -*-

"""Classes for ECS clusters."""


class ECSManager:
    """Manage ECS Clusters."""

    def __init__(self, session):
        """Create a ECS object."""
        self.session = session
        self.ecs = self.session.client('ecs')


    def list_ecs_clusters(self):
        """List all existing clusters in a default zone."""
        response = self.ecs.list_clusters()
        return response


    def list_ecs_task_definitions(self):
        """List all existing ECS task definitions."""
        response = self.ecs.list_task_definitions()
        return response
