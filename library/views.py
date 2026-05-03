from rest_framework import generics, viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils.timezone import now
from .models import *
from .serializers import *
from .permissions import *

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    filterset_fields = ['author', 'genres']
    search_fields = ['title']
    ordering_fields = ['title']

    def get_serializer_class(self):
        if self.action in ['create', 'update']:
            return BookCreateSerializer
        return BookSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'destroy']:
            return [IsLibrarian()]
        return []

class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

    def get_permissions(self):
        if self.action == 'create':
            return [IsLibrarian()]
        return []

class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer

    def get_permissions(self):
        if self.action == 'create':
            return [IsLibrarian()]
        return []

class BorrowViewSet(viewsets.ModelViewSet):
    queryset = BorrowRequest.objects.all()
    serializer_class = BorrowRequestSerializer

    def get_queryset(self):
        return BorrowRequest.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['patch'], permission_classes=[IsLibrarian])
    def approve(self, request, pk=None):
        obj = self.get_object()
        obj.status = 'APPROVED'
        obj.approved_at = now()
        obj.save()
        return Response({'status': 'approved'})

    @action(detail=True, methods=['patch'], permission_classes=[IsLibrarian])
    def reject(self, request, pk=None):
        obj = self.get_object()
        obj.status = 'REJECTED'
        obj.save()
        return Response({'status': 'rejected'})

    @action(detail=True, methods=['patch'])
    def return_book(self, request, pk=None):
        obj = self.get_object()
        obj.status = 'RETURNED'
        obj.returned_at = now()
        obj.save()
        return Response({'status': 'returned'})

class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_queryset(self):
        return BookReview.objects.filter(book_id=self.kwargs['book_id'])

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, book_id=self.kwargs['book_id'])