from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import permissions
from accounts.api.serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    提供一个api用于读取用户的内容：
        /api/user/1: 可以访问到第一个用户
    ModelViewSets: https://www.django-rest-framework.org/api-guide/viewsets/#modelviewset
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

