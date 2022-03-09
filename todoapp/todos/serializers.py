from rest_framework import serializers

from todos.models import Todo

# Add your serializer(s) here


class TodoSerializer(serializers.ModelSerializer):
    todo = serializers.CharField(source='name')
    todo_id = serializers.PrimaryKeyRelatedField(source='id', read_only=True)

    class Meta:
        model = Todo
        fields = ['todo_id', 'done', 'todo', 'date_created']
        read_only_fields = ['date_created']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super(TodoSerializer, self).create(validated_data)


class UserSerializer(serializers.Serializer):
    email = serializers.EmailField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()


class fetch_all_todo_list_with_user_details_serializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    status = serializers.SerializerMethodField(method_name='convert_status')
    created_at = serializers.SerializerMethodField(
        method_name='convert_created_at')
    creator = UserSerializer(source="user")

    def convert_status(self, instance):
        if instance.done == True:
            return "Done"
        else:
            return "To Do"

    def convert_created_at(self, instance):
        datetime = instance.date_created.strftime("%l:%M %p, %d %b, %Y")
        return f"0{datetime[1:]}"


class fetch_users_todo_stats_serializer(serializers.Serializer):
    id = serializers.IntegerField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.EmailField()
    completed_count = serializers.IntegerField()
    pending_count = serializers.IntegerField()


class fetch_five_users_with_max_pending_todos_serializer(serializers.Serializer):
    id = serializers.IntegerField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.EmailField()
    pending_count = serializers.IntegerField()


class fetch_users_with_n_pending_todos_serializer(serializers.Serializer):
    id = serializers.IntegerField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.EmailField()
    pending_count = serializers.IntegerField()


class project_report_serializer(serializers.Serializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.EmailField()
    pending_count = serializers.IntegerField()
    completed_count = serializers.IntegerField()


class fetch_project_wise_report_serializer(serializers.Serializer):
    project_title = serializers.CharField(source="name")
    report = project_report_serializer(many=True, source="members")


class fetch_user_wise_project_status_serializer(serializers.Serializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.EmailField()
    to_do_projects = serializers.ListField()
    completed_projects = serializers.ListField()
    in_progress_projects = serializers.ListField()
