from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from apps.accounts.serializers.serializers import AccountSerializer
from apps.accounts.utils import create_or_get_user, find_user_in_website, generate_tokens_for_user


class GoogleLogin(TokenObtainPairView):
    permission_classes = (permissions.AllowAny,)

    @swagger_auto_schema(tags=['accounts'],
                         responses={201: AccountSerializer,
                                    400: "error code 4007 for not enough credentials",
                                    401: "error code 4006 for not submitted users & 4009 for wrong credentials"})
    def post(self, request, *args, **kwargs):

        user = create_or_get_user(user_data={**request.data, "password": request.data.get("email")},
                                  website=request.data.get("website"))

        access_token, refresh_token = generate_tokens_for_user(user)

        return Response({
            'user': AccountSerializer(user).data,
            'access': str(access_token),
            'refresh': str(refresh_token)
        }, status=status.HTTP_201_CREATED)
