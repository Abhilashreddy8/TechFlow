from rest_framework import status
# status = HTTP status codes in readable format
# status.HTTP_200_OK = 200, status.HTTP_400_BAD_REQUEST = 400 etc

from rest_framework.response import Response
# Response = DRF's way to send JSON back to client
# Always use this instead of Django's HttpResponse for APIs

from rest_framework.views import APIView
# APIView = base class for all our API views
# Handles GET, POST, PUT, DELETE methods

from rest_framework.permissions import IsAuthenticated, AllowAny
# IsAuthenticated = only logged-in users with valid JWT can access
# AllowAny = anyone can access — no login needed (for register/login)

from .serializers import RegisterSerializer, UserProfileSerializer


class RegisterView(APIView):
    # This handles POST /api/auth/register/
    # Anyone can register — no login needed
    permission_classes = [AllowAny]

    def post(self, request):
        # request.data = the JSON body sent by Postman/Frontend
        # Example: {"email": "abhi@gmail.com", "password": "Test@123"}

        serializer = RegisterSerializer(data=request.data)
        # Pass incoming data to serializer for validation

        if serializer.is_valid():
            # is_valid() runs all validations we defined
            # If everything is correct — returns True

            user = serializer.save()
            # Calls our create() method in serializer
            # Creates user in PostgreSQL with hashed password

            return Response({
                "message": "Account created successfully",
                "user": {
                    "id": str(user.id),
                    "email": user.email,
                    "full_name": user.full_name
                }
            }, status=status.HTTP_201_CREATED)
            # 201 = Created — standard response for successful resource creation
            # Never return password in response — not even hashed

        return Response(
            serializer.errors,          # returns exactly what went wrong
            status=status.HTTP_400_BAD_REQUEST
            # 400 = Bad Request — client sent invalid data
        )


class ProfileView(APIView):
    # This handles GET /api/auth/profile/
    # PROTECTED — only users with valid JWT token can access
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # request.user = the logged-in user Django found from JWT token
        # Django automatically decodes the token and loads the user for us

        serializer = UserProfileSerializer(request.user)
        # No data= here because we are READING not writing
        # We pass the user object directly

        return Response(
            serializer.data,        # converts User object → JSON
            status=status.HTTP_200_OK
        )