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


@method_decorator(csrf_exempt, name='dispatch')  # Necessário para APIs sem session
class RegisterView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            name = data.get('name')
            email = data.get('email')

            if Admin.objects.filter(name=name).exists():
                return JsonResponse({"Message": "Nome já existe!"}, status=400)

            if Admin.objects.filter(email=email).exists():
                return JsonResponse({"Message": "Email já registrado!"}, status=400)



            admin = Admin.objects.create(
                name=data['name'],
                email=data['email'],
                password=make_password(data['password'])  # Criptografa a senha
            )


            return JsonResponse({"message": "Admin criado com sucesso"}, status=201)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)


@method_decorator(csrf_exempt, name='dispatch')
class LoginView(View):
    def post(self, request):
        data = json.loads(request.body)
        username = data.get('name')
        password = data.get('password')

        try:
            # 1. Busca o Admin no seu banco limpo
            admin = Admin.objects.get(name=username)

            # 2. Verifica a senha (PBKDF2 vs Texto Plano)
            if check_password(password, admin.password):
                # 3. Cria o Payload (dados que vão dentro do token)
                payload = {
                    'admin_id': admin.id,
                    'name': admin.name,
                    'email': admin.email,
                    'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24),  # Expira em 24h
                    'iat': datetime.datetime.utcnow()
                }

                # 4. Assina o Token com sua SECRET_KEY do settings.py
                token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')

                return JsonResponse({'token': token}, status=200)

            return JsonResponse({'error': 'Senha incorreta'}, status=401)

        except Admin.DoesNotExist:
            return JsonResponse({'error': 'Administrador não encontrado'}, status=404)