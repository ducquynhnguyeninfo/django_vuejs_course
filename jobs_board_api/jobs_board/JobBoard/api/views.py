from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import get_object_or_404

from JobBoard.models import JobOffer
from JobBoard.api.serializers import JobOfferSerializer


class JobOfferListView(APIView):
    def get(self, request):
        jobs = JobOffer.objects.all()
        serializers = JobOfferSerializer(jobs, many=True,)
        
        return Response(serializers.data)
    
    def post(self, request):
        serializer = JobOfferSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class JobOfferDetailView(APIView):
    
    def get_object(self, pk) -> JobOffer:
        job = get_object_or_404(JobOffer, pk=pk)
        return job
    
    def get(self, request, pk) -> JobOffer:
        job = self.get_object(pk=pk)
        serializer = JobOfferSerializer(data=job)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
       
       
    def update(self, request, pk) -> JobOffer:
        job = self.get_object(pk=pk)
        serializer = JobOfferSerializer(job, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK) 
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
    
    def delete(self, request, pk) -> JobOffer:
        job = self.get_object(pk=pk)
        job.delete()
        return Response(status=status.HTTP_204_NO_CONTENT) 
    
    