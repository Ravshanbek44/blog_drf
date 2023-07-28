from .serializers import BlogListSerializer, BlogSerializer
from rest_framework import generics
from .models import Blog


class BlogListAPIView(generics.ListAPIView):
    serializer_class = BlogListSerializer

    def get_queryset(self):
        queryset = Blog.objects.all()
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(title__icontains=search)
        return queryset


class BlogGetByIdAPIView(generics.RetrieveAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogListSerializer
    lookup_field = 'pk'


class BlogCreateAPIView(generics.CreateAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer


class BlogUpdateAPIView(generics.UpdateAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    lookup_field = 'pk'


class BlogDestroyAPIView(generics.DestroyAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    lookup_field = 'pk'
