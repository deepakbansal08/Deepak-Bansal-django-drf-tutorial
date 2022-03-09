from rest_framework import serializers
from django.db.models import Count, Max
from django.contrib.postgres.aggregates import ArrayAgg
from projects.models import Project
from users.models import CustomUser


class ProjectMemberCreateSerializer(serializers.Serializer):
    user_ids = serializers.ListField(
        child=serializers.IntegerField(), required=True, write_only=True)

    def validate(self, data):
        if not 'project_id' in self.context["request"].query_params:
            raise serializers.ValidationError(
                'Project id must be provided in query params')

        project_id = self.context["request"].query_params["project_id"]
        user_ids = data['user_ids']
        result = {}

        # filter users that do not exist
        users = CustomUser.objects.filter(
            pk__in=user_ids).aggregate(ids=ArrayAgg('id'))

        def usersDoNotExistFilter(user_id):
            if not user_id in users['ids']:
                result[user_id] = 'User does not exist'
                return False
            return True

        user_ids_iterator = filter(usersDoNotExistFilter, user_ids)
        user_ids = list(user_ids_iterator)

        # filter user_ids already included in project
        usersAlreadyInProject = CustomUser.objects.filter(
            pk__in=user_ids, projects__id__exact=project_id).aggregate(ids=ArrayAgg('id'))

        def usersAlreadyInProjectFilter(user_id):
            if user_id in usersAlreadyInProject['ids']:
                result[user_id] = 'User is already a Member'
                return False
            return True

        user_ids_iterator = filter(usersAlreadyInProjectFilter, user_ids)
        user_ids = list(user_ids_iterator)

        # filter user_ids involved in two projects
        usersInTwoOrMoreProjects = CustomUser.objects.filter(pk__in=user_ids).annotate(
            num_projects=Count('projects')).filter(num_projects__gte=2).aggregate(ids=ArrayAgg('id'))

        def usersInTwoOrMoreProjectsFilter(user_id):
            if user_id in usersInTwoOrMoreProjects['ids']:
                result[user_id] = 'Cannot add as User is a member in two projects'
                return False
            return True

        user_ids_iterator = filter(usersInTwoOrMoreProjectsFilter, user_ids)
        user_ids = list(user_ids_iterator)

        # find number of members and maximum members in a project
        project = Project.objects.filter(id=project_id).aggregate(
            members=Count('members'), max_members=Max('max_members'))

        # project limit exceeded
        numberOfUsersThatCanBeAdded = project['max_members'] - \
            project['members']
        for user_id in user_ids[numberOfUsersThatCanBeAdded:]:
            result[user_id] = 'Cannot add as project reached maximum members limit'

        # Successfully added members
        Project.objects.get(id=project_id).members.add(
            *user_ids[:numberOfUsersThatCanBeAdded])
        for user_id in user_ids[:numberOfUsersThatCanBeAdded]:
            result[user_id] = 'Member added Successfully'

        return {'logs': result}


class ProjectMemberDestroySerializer(serializers.Serializer):
    user_ids = serializers.ListField(
        child=serializers.IntegerField(), required=True, write_only=True)

    def validate(self, data):
        if not 'project_id' in self.context:
            raise serializers.ValidationError(
                'Project id is not present')

        project_id = self.context["project_id"]
        user_ids = data['user_ids']
        result = {}

        # filter users that do not exist
        users = CustomUser.objects.filter(
            pk__in=user_ids).aggregate(ids=ArrayAgg('id'))

        def usersDoNotExistFilter(user_id):
            if not user_id in users['ids']:
                result[user_id] = 'User does not exist'
                return False
            return True

        user_ids_iterator = filter(usersDoNotExistFilter, user_ids)
        user_ids = list(user_ids_iterator)

        # users not present in project
        usersNotPresentInProject = CustomUser.objects.filter(pk__in=user_ids).exclude(
            projects__id__exact=project_id).aggregate(ids=ArrayAgg('id'))

        def usersNotPresentInProjectFilter(user_id):
            if user_id in usersNotPresentInProject['ids']:
                result[user_id] = 'User is not a Member of the Project'
                return False
            return True

        user_ids_iterator = filter(
            usersNotPresentInProjectFilter, user_ids)
        user_ids = list(user_ids_iterator)

        # users deleted successfully
        Project.objects.get(id=project_id).members.remove(*user_ids)
        for user_id in user_ids:
            result[user_id] = 'Member removed Successfully'
        pass

        return {'logs': result}
