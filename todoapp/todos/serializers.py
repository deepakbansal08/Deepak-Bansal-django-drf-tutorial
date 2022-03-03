from django.contrib.auth import get_user_model
from rest_framework import serializers


# Add your serializer(s) here

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


class fetch_users_with_n_pending_todos_serializer():
    id = serializers.IntegerField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.EmailField()
    pending_count = serializers.IntegerField()
