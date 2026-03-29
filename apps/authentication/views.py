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

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError

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


# Add this new view at the bottom of views.py
class LogoutView(APIView):
    """
    Logout by blacklisting the refresh token.
    After this the refresh token cannot be used to get new access tokens.
    User is effectively logged out even though JWT is stateless.
    """
    permission_classes = [IsAuthenticated]
    # Only logged-in users can logout — makes sense!

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh_token")
            # Client must send their refresh token in request body
            # We need it to blacklist it

            if not refresh_token:
                return Response({
                    "success": False,
                    "errors": {"detail": "Refresh token is required"}
                }, status=status.HTTP_400_BAD_REQUEST)

            token = RefreshToken(refresh_token)
            # Create a RefreshToken object from the string

            token.blacklist()
            # Add this token to the blacklist table in PostgreSQL
            # Now this token can NEVER be used again — even if not expired

            return Response({
                "success": True,
                "message": "Logged out successfully"
            }, status=status.HTTP_200_OK)

        except TokenError:
            # TokenError happens if token is already blacklisted or invalid
            return Response({
                "success": False,
                "errors": {"detail": "Token is invalid or already blacklisted"}
            }, status=status.HTTP_400_BAD_REQUEST)