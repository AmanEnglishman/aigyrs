from rest_framework.generics import ListAPIView

from .serializers import PostSerializers
from .models import Post


class PostListAPIView(ListAPIView):
    serializer_class = PostSerializers
    queryset = Post.object.all()
