import jwt
import json
from django.contrib.auth.hashers import make_password
import datetime
from django.conf import settings
from django.views import View
from django.http import JsonResponse
from django.contrib.auth.hashers import check_password
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from .models import Admin


@method_decorator(csrf_exempt, name='dispatch')
class RegisterView(View):
    def post(self, request):

        if not request.body:
            return JsonResponse({"error": "Body vazio"}, status=400)

        try:
            data = json.loads(request.body.decode('utf-8'))
        except json.JSONDecodeError:
            return JsonResponse({"error": "JSON inválido"}, status=400)

        required_fields = ['name', 'email', 'password']
        for field in required_fields:
            if not data.get(field):
                return JsonResponse(
                    {"error": f"Campo '{field}' é obrigatório"},
                    status=400
                )

        email = data['email']

        if Admin.objects.filter(email=email).exists():
            return JsonResponse({"error": "Email já registrado"}, status=400)

        Admin.objects.create(
            name=data['name'],
            email=email,
            password=make_password(data['password'])
        )

        return JsonResponse({"message": "Admin criado com sucesso"}, status=201)


@method_decorator(csrf_exempt, name='dispatch')
class LoginView(View):
    def post(self, request):
        data = json.loads(request.body)
        email = data.get('email')
        password = data.get('password')

        try:

            admin = Admin.objects.get(email=email)


            if check_password(password, admin.password):
                payload = {
                    'admin_id': admin.id,
                    'name': admin.name,
                    'email': admin.email,
                    'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24),
                    'iat': datetime.datetime.utcnow()
                }


                token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')

                return JsonResponse({'token': token}, status=200)

            return JsonResponse({'error': 'Senha incorreta'}, status=401)

        except Admin.DoesNotExist:
            return JsonResponse({'error': 'Administrador não encontrado'}, status=404)