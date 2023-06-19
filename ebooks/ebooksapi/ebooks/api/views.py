import cv2

from django.http import StreamingHttpResponse
from rest_framework import generics, mixins
from rest_framework import permissions
from rest_framework.validators import ValidationError


from ebooks.models import Ebook, Review
from ebooks.api.serializers import EbookSerializer, ReviewSerializer
from ebooks.api.permissions import IsAdminUserOrReadOnly, IsReviewAuthorOrReadOnly
from ebooks.api.paginations import SmallSetPagination

class EbookListCreateApiView(generics.ListCreateAPIView):
    queryset = Ebook.objects.all().order_by('id') # -id: reverse the order
    serializer_class = EbookSerializer
    permission_classes = [IsAdminUserOrReadOnly]
    pagination_class = SmallSetPagination
    
    
class EbookDetailApiView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Ebook.objects.all()
    serializer_class = EbookSerializer
    permission_classes = [IsAdminUserOrReadOnly]
    
    
class ReviewCreateApiView(generics.CreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def perform_create(self, serializer):
        ebook_pk = self.kwargs.get("ebook_pk")
        ebook = generics.get_object_or_404(Ebook, pk=ebook_pk)
        review_author = self.request.user
        
        review_queryset = Review.objects.filter(ebook=ebook, 
                                                review_author=review_author)
        if review_queryset.exists():
            raise ValidationError("You have already review this book!")
        serializer.save(ebook=ebook, review_author = review_author)
        
    
class ReviewDetailApiView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsReviewAuthorOrReadOnly]
    
    # def perform_update(self, serializer):
    #     return super().perform_update(serializer)
    

# class EbookListCreateApiView(mixins.ListModelMixin,
#                             mixins.CreateModelMixin, 
#                             generics.GenericAPIView):
#     queryset = Ebook.objects.all()
#     serializer_class = EbookSerializer
    
#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)
    
#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)

# class EbookDetailApiView(mixins.RetrieveModelMixin,
#                             mixins.UpdateModelMixin, 
#                             mixins.DestroyModelMixin,
#                             generics.GenericAPIView):
#     queryset = Ebook.objects.all()
#     serializer_class = EbookSerializer
    
#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)
    
#     def put(self, request, *args, **kwargs):
#         return self.update(request, *args, **kwargs)
    
#     def delete(self, request, *args, **kwargs):
#         return self.destroy(request, *args, **kwargs)
