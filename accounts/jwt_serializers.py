from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer
)


class MyTokenObtainPairSerializer(
    TokenObtainPairSerializer
):

    def validate(self, attrs):

        data = super().validate(attrs)

        data["accessToken"] = data.pop("access")
        data["refreshToken"] = data.pop("refresh")

        data["user"] = {
            "id": self.user.id,
            "username": self.user.username,
            "email": self.user.email,
            "role": self.user.role,
        }

        return data