from rest_framework.decorators import api_view # type: ignore
from rest_framework.response import Response # type: ignore
from rest_framework import status # type: ignore
from base.models import Room, Topic, User # type: ignore
from .serializers import RoomSerializer, TopicSerializer, UserSerializer # type: ignore

@api_view(['GET'])
def getRoutes(request):
    routes = [
        'GET /api',
        'GET /api/rooms',
        'GET /api/rooms/:id',
        'GET /api/topics',
        'GET /api/topics/:id',
        'GET /api/users',
        'GET /api/users/:id'
    ]
    return Response(routes)

@api_view(['GET', 'POST'])
def getRooms(request):
    if request.method == 'GET':
        rooms = Room.objects.all()
        serializer = RoomSerializer(rooms, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = RoomSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE']) 
def getRoom(request, pk):
    try:
        room = Room.objects.get(id=pk)
    except Room.DoesNotExist:
        return Response({'error': 'Room not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = RoomSerializer(room)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = RoomSerializer(room, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        room.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
def getTopics(request):
    topics = Topic.objects.all()
    serializer = TopicSerializer(topics, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getTopic(request, pk):
    try:
        topic = Topic.objects.get(id=pk)
        serializer = TopicSerializer(topic)
        return Response(serializer.data)
    except Topic.DoesNotExist:
        return Response({'error': 'Topic not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def getUsers(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getUser(request, pk):
    try:
        user = User.objects.get(id=pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)