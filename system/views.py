from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

# Create your views here.
class DefaultAPIView(APIView):
    authentication_classes = TokenAuthentication,
    permission_classes     = IsAuthenticated,