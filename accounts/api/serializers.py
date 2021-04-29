from django.contrib.auth.models import User
from rest_framework import serializers, exceptions

'''
Serializer作用：
- 将queryset与model实例等进行序列化，转化成json格式，返回给用户(api接口)。
- 将post与patch/put的上来的数据进行验证。
- 对post与patch/put数据进行处理。
'''


class UserSerializer(serializers.ModelSerializer):
    '''
    HyperlinkedModelSerializer: 网页显示的时候url可以点击进去具体的用户
    ModelSerializer: 返回用户的id：1，2，3
    当修改代码之后，可以发现vagrant会自动重启
    '''
    class Meta:
        model = User
        # 省去每隔字段再写一个field
        fields = ('username', 'email')

class LoginSerializer(serializers.Serializer):
    '''
    检测用户名和密码是否有
    '''
    username = serializers.CharField()
    password = serializers.CharField()

class SignupSerializer(serializers.ModelSerializer):
    '''
    ModelSerializer: 最后我们调用save的时候可以成功的把user创建出来
    '''
    username = serializers.CharField(max_length=20, min_length=6)
    password = serializers.CharField(max_length=20, min_length=6)
    email = serializers.EmailField()

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    # 调用is_valid的时候会被调用
    def validate(self, data):
        # 用户名和邮箱存储的时候我们存小写的，大小写不敏感
        # User.objects.filter(username__iexact=data['username'].lower()).exists()，效率很低
        if User.objects.filter(username=data['username'].lower()).exists():
            raise exceptions.ValidationError({
                'message': 'This username has been occupied.'
            })
        if User.objects.filter(email=data['email'].lower()).exists():
            raise exceptions.ValidationError({
                'message': 'This email address has been occupied.'
            })
        return data

    def create(self, validated_data):
        username = validated_data['username'].lower()
        email = validated_data['email'].lower()
        password = validated_data['password']

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
        )
        # User.object.create(username=username, ...): 不行，因为我们传进来的密码是明文，我们需要转化成密文，这个django帮忙做了
        return user



