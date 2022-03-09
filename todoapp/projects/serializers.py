from rest_framework import serializers
from django.db.models import Count, F, Max
from django.contrib.postgres.aggregates import ArrayAgg
from projects.models import Project, ProjectMember
from users.models import CustomUser

class ProjectMemberSerializer(serializers.Serializer):
    user_ids = serializers.ListField(child=serializers.IntegerField(), required=True, write_only=True)

    def validate(self, data):
        if self.context["project_id"] is None:
            raise serializers.ValidationError('Project id must be provided in query params')

        project_id = self.context["project_id"]
        user_ids = data['user_ids']
        result = {}

        # filter users that do not exist
        users = CustomUser.objects.filter(pk__in=user_ids).aggregate(ids=ArrayAgg('id'))
        def usersDoNotExistFilter(user_id):
            if not user_id in users['ids']:
                result[user_id] = 'User does not exist'
                return False
            return True

        user_ids_iterator = filter(usersDoNotExistFilter, user_ids)
        user_ids = list(user_ids_iterator)

        # filter user_ids already included in projects
        usersAlreadyInProject = CustomUser.objects.filter(pk__in=user_ids, projects__id__exact=project_id).aggregate(ids=ArrayAgg('id'))
        
        def usersAlreadyInProjectFilter(user_id):
            if user_id in usersAlreadyInProject['ids']:
                result[user_id] = 'User is already a Member'
                return False
            return True

        user_ids_iterator = filter(usersAlreadyInProjectFilter, user_ids)
        user_ids = list(user_ids_iterator)

        # filter user_ids involved in two projects
        usersIn2orMoreProjects = CustomUser.objects.filter(pk__in=user_ids).annotate(num_projects=Count('projects')).filter(num_projects__gte=2).aggregate(ids=ArrayAgg('id'))

        def usersIn2orMoreProjectsFilter(user_id):
            if user_id in usersIn2orMoreProjects['ids']:
                result[user_id] = 'Cannot add as User is a member in two projects'
                return False
            return True

        user_ids_iterator = filter(usersIn2orMoreProjectsFilter, user_ids)
        user_ids = list(user_ids_iterator)

        # project limit exceeded
        project = Project.objects.filter(id=project_id).aggregate(members=Count('members'), max_members=Max('max_members'))

        numberOfUsersThatCanBeAdded = project['max_members'] - project['members']
        for user_id in user_ids[numberOfUsersThatCanBeAdded:]:
            result[user_id] = 'Cannot add as project reached maximum members limit'

        # Successfully added members
        Project.objects.get(id=project_id).members.add(*user_ids[:numberOfUsersThatCanBeAdded])
        for user_id in user_ids[:numberOfUsersThatCanBeAdded]:
            result[user_id] = 'Member added Successfully'

        return { 'logs' : result }
