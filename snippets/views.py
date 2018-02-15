from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from snippets.models import Snippet
from snippets.serializers import SnippetSerializer, UserSerializer
from rest_framework import generics
from django.contrib.auth.models import User
from rest_framework import permissions
from snippets.permissions import IsOwnerOrReadOnly
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import renderers
from rest_framework import viewsets
from rest_framework.decorators import detail_route
"""
@csrf_exempt
def snippet_list(request):
    
    if request.method == 'GET':
        snippets = Snippet.objects.all()
        serializer = SnippetSerializer(snippets, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = SnippetSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

@csrf_exempt
def snippet_detail(request, pk):
    
    try:
        snippet = Snippet.objects.get(pk=pk)
    except Snippet.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = SnippetSerializer(snippet)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = SnippetSerializer(snippet, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        snippet.delete()
        return HttpResponse(status=204)


# HttpResponse or JsonResponse can be returned by server 

"""

'''
@api_view(['GET', 'POST'])
def snippet_list(request):
    if request.method == 'GET':
        snippets = Snippet.objects.all()
        serializer = SnippetSerializer(snippets, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = SnippetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def snippet_detail(request, pk):
    
    try:
        snippet = Snippet.objects.get(pk=pk)
    except Snippet.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = SnippetSerializer(snippet)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = SnippetSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

#we're no longer explicitly tying our requests or responses to a given content type. request.data can handle incoming json requests, but it can also handle other formats like request for HTML etc,...Response renders content type as of the content type of the request.
# we can also add optional suffixes in URl patterns to refer to a specific format
'''

'''



#using generic class based views
class SnippetList(generics.ListCreateAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)#will ensure that authenticated requests get read-write access, and unauthenticated requests get read-only access.


    def perform_create(self, serializer):  #associating snippets with users
         serializer.save(owner=self.request.user)

class SnippetDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,#snippet objectlevelpermissions
                      IsOwnerOrReadOnly,)
    
class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

@api_view(['GET']) #creating endpoint for the entry to our api
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'snippets': reverse('snippet-list', request=request, format=format)
    })

    


class SnippetHighlight(generics.GenericAPIView):# view for representing highlighted snippets
    queryset = Snippet.objects.all()
    renderer_classes = (renderers.StaticHTMLRenderer,)# HTML repr of highlighted snippets

    def get(self, request, *args, **kwargs):
        snippet = self.get_object()
        return Response(snippet.highlighted)


 '''
@api_view(['GET']) #creating endpoint for the entry to our api
def api_root(request, format=None):
     return Response({
         'users': reverse('user-list', request=request, format=format),
         'snippets': reverse('snippet-list', request=request, format=format)
     })

     
class UserViewSet(viewsets.ReadOnlyModelViewSet):#provide the default 'read-only' operations.
     """
     This viewset automatically provides `list` and `detail` actions.
     """
     queryset = User.objects.all()
     serializer_class = UserSerializer

class SnippetViewSet(viewsets.ModelViewSet):# get complete set of default read and write operations for the views in this viewset
     """
     This viewset automatically provides `list`, `create`, `retrieve`,
     `update` and `destroy` actions.

     Additionally we also provide an extra `highlight` action.
     """
     queryset = Snippet.objects.all()
     serializer_class = SnippetSerializer
     permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                           IsOwnerOrReadOnly,)
     @detail_route(renderer_classes=[renderers.StaticHTMLRenderer])
     def highlight(self, request, *args, **kwargs):
         snippet = self.get_object()
         return Response(snippet.highlighted)

     def perform_create(self, serializer):
             serializer.save(owner=self.request.user)

    