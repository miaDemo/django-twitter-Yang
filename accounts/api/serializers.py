from django.contrib.auth.models import User, Group
from rest_framework import serializers

class UserSerializer(serializers.HyperlinkedModelSerializer):
    '''
    HyperlinkedModelSerializer: 网页显示的时候url可以点击进去具体的用户
    ModelSerializer: 返回用户的id：1，2，3
    当修改代码之后，可以发现vagrant会自动重启
    '''
    class Meta:
        model = User
        fields = ('url', 'username', 'email')