import jwt
from django.conf import settings
from django.http import JsonResponse
from functools import wraps
from users.models import Admin
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError


def jwt_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        auth_header = request.headers.get("Authorization")

        if not auth_header:
            return JsonResponse({"error": "Token não fornecido"}, status=401)

        if not auth_header.startswith("Bearer "):
            return JsonResponse({"error": "Formato do token inválido"}, status=401)

        token = auth_header.split(" ")[1]

        try:
            payload = jwt.decode(
                token,
                settings.SECRET_KEY,
                algorithms=["HS256"]
            )

            admin = Admin.objects.get(id=payload["admin_id"])
            request.admin = admin

        except ExpiredSignatureError:
            return JsonResponse({"error": "Token expirado"}, status=401)
        except (InvalidTokenError, Admin.DoesNotExist):
            return JsonResponse({"error": "Token inválido"}, status=401)

        return view_func(request, *args, **kwargs)

    return wrapper
