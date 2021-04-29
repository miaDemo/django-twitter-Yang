from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth import (
    logout as django_logout,
    login as django_login,
    authenticate as django_authenticate,
)
from accounts.api.serializers import (
    UserSerializer,
    LoginSerializer,
    SignupSerializer
)


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


class AccountViewSet(viewsets.ViewSet):
    '''
    选择不使用framework已经定义好的viewset，个人选择
    老师选择的是自己定义behavior而不是使用framework已经定义好的, viewsets.ViewSet里面为空行为
    '''

    # serializer_class = UserSerializer # post action 的时候会使用我们创建的表单进行post
    # serializer_class = LoginSerializer  # 因为login的时候我们希望输入的是用户和密码而不是用户和邮箱
    serializer_class = SignupSerializer # 实现注册功能的时候，表单不一样

    @action(methods=['Get'], detail=False)
    def login_status(self, request):
        '''
        datail=true: http://localhost/api/accounts/login_status/ -> http://localhost/api/accounts/1/login_status/
        framework将accounts作为主资源目录，主资源目录下的叫做action(/api/accounts/login_status/)，严格上说这个写法不符合framework的规范，
        因为只允许增删查改。但是因为我们可以使用viewset，增加了自由度，可以让我们自己定义一个动作，需要annotation来表明
        访问localhost时候发现没有将我们这个新的方法list上去，这个是expected的，因为没有实现list的function
        :return: 根据需求我们需要返回一个hashset，please check https://www.lintcode.com/problem/2153/?_from=ladder&fromId=194
        '''

        data = {'has_logged_in': request.user.is_authenticated}
        if request.user.is_authenticated:
            data['user'] = UserSerializer(request.user).data
        return Response(data)

    @action(methods=['POST'], detail=False)
    def logout(self, request):
        '''
        完成登出这个动作，点击表单中的post
        '''
        django_logout(request)
        return Response({'success': True})

    @action(methods=['POST'], detail=False)
    def login(self, request):
        '''
        实现登陆，我们需要更改serializer，用于验证用户的输入
        '''
        # request中获取用户的用户名和密码
        # 不可以直接这个样子写request.data['username']，因为我们不确定是否存在，所以需要定义serializer
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({
                'success': False,
                'message': "Please check input.",
                'errors': serializer.errors
            }, status=400)

        # validation ok, login
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        # 登陆失败的原因：1 用户不存在 2 用户密码不匹配
        # debug, print query to console
        # queryset = User.objects.filter(username=username)
        # print(queryset.query)
        if not User.objects.filter(username=username).exists():
            return Response({
                'success': False,
                'message': "User does not exist.",
            }, status=400)

        user = django_authenticate(username=username, password=password) # authenticate之后的user才是我们可以用于login的
        if not user or user.is_anonymous:
            return Response({
                'success': False,
                'message': "Username and password does not match.",
            }, status=400)

        # 如果没有任何问题的话，实现login
        django_login(request, user)
        return Response({
            'success': True,
            'user': UserSerializer(user).data,
        })

    @action(methods=['POST'], detail=False)
    def signup(self, request):
        serializer = SignupSerializer(data=request.data) # 不指定data的话，默认的第一个参数是instance
        if not serializer.is_valid():
            return Response({
                "success": False,
                "message": "Please check input.",
                "errors": serializer.errors,
            }, status=400)

        user = serializer.save()

        django_login(request, user)
        return Response({
            'success': True,
            'user': UserSerializer(user).data,
        }, status=201) # 201指的创建数据成果，有时候会懒，直接用200


