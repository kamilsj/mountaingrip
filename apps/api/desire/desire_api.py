from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser


class Desire(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        data = {}
        suggestions = []
        
        if request.method == 'GET':
            q = request.GET['query']
            
            
            


            data = {
                'query': q,
                'suggestions': {
                    'value': 'value',
                    'data': 'data'
                }
            }

        return Response(data)
    

    def post(self, request):
        data = {}