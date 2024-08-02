from rest_framework import viewsets
from .models import File, Folder
from .serializers import FileSerializer, FolderSerializer, FileShareSerializer
from .permissions import IsOwner
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.contrib.auth.models import User
from django.db.models import Q




class FileViewSet(viewsets.ModelViewSet):
    queryset = File.objects.all()
    serializer_class = FileSerializer

    def get_queryset(self):
        user = self.request.user
        return File.objects.filter(Q(author=user) | Q(shared_with=user))

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_permissions(self):
        permission_classes = [IsAuthenticated]

        if self.action in ["create", "update", "destroy"]:
            permission_classes = [IsOwner]
        return [permission() for permission in permission_classes]
        
class FolderViewSet(viewsets.ModelViewSet):
    queryset = Folder.objects.all()
    serializer_class = FolderSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_permissions(self):
        permission_classes = [IsAuthenticated]
        if self.action in ["create", "partial_update", "destroy"]:
            permission_classes = [IsOwner]
        return [permission() for permission in permission_classes]

class FileShareAPIView(APIView):

    def post(self, request, *args, **kwargs):
        share_with_id = request.data.get('share_with')
        file_id = request.data.get('file')

        share_user = User.objects.filter(id=share_with_id).first()
        file = File.objects.filter(id=file_id).first()

        if not share_user or not file:
            return Response({"error": "User or file not found"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = FileShareSerializer(file, data={'shared_with': [share_user.id]}, partial=True)
        if serializer.is_valid():
            updated_file = serializer.save()
            return Response(FileSerializer(updated_file).data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
