from rest_framework import status, decorators
from rest_framework.response import Response
from ..serializers import URLSerializer


@decorators.api_view(["POST"])
# @decorators.throttle_classes()
def CreateUrl (request) : 
    try :
        serializer = URLSerializer(data=request.data)
        if serializer.is_valid() : 
            serializer.start()
            return Response({
                'message' : "Process completed successfully"
            },status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    except Exception as error :
        return Response({
            'message' : f'an error accoured : {error}'
        },status=status.HTTP_400_BAD_REQUEST)