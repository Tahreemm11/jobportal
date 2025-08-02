from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .serializers import UserRegistrationSerializer, JobSeekerProfileSerializer, EmployerProfileSerializer
from .models import User, JobSeekerProfile, EmployerProfile
from rest_framework.permissions import IsAuthenticated

class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # Create appropriate profile based on role
        if user.role == 'job_seeker':
            JobSeekerProfile.objects.create(user=user)
        elif user.role == 'employer':
            EmployerProfile.objects.create(user=user)
        from .tasks import send_verification_email
        send_verification_email(user.id)
        
        return Response({
            "message": "User created successfully",
            "user_id": user.id,
            "role": user.role
        }, status=status.HTTP_201_CREATED)

class ProfileUpdateView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.user.role == 'job_seeker':
            return JobSeekerProfileSerializer
        return EmployerProfileSerializer

    def get_object(self):
        if self.request.user.role == 'job_seeker':
            return self.request.user.job_seeker_profile
        return self.request.user.employer_profile