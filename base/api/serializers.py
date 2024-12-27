from rest_framework.serializers import ModelSerializer # type: ignore
from base.models import Room, Topic, User

class RoomSerializer(ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'

class TopicSerializer(ModelSerializer):
    class Meta:
        model = Topic
        fields = '__all__'

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'name', 'bio', 'avatar']