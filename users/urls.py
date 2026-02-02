from django.urls import path
from .views import RegisterView , LoginView

urlpatterns = [
    # Rota para criar um novo Admin
    path("register/", RegisterView.as_view(), name="register"),

    # Rota para o login manual que você vai criar
    path("login/", LoginView.as_view(), name="login"),

    # Nota: TokenRefreshView é do SimpleJWT.
    # Se você fizer na mão, precisará criar sua própria lógica de refresh ou removê-la.
]