import os
from django.conf import settings
from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from users.auth.decorators import jwt_required
from .models import Media

@method_decorator(csrf_exempt, name='dispatch')
@method_decorator(jwt_required, name='dispatch')
class MediaView(View):

    def post(self, request):
        if 'file' not in request.FILES:
            return JsonResponse({"error": "Arquivo não enviado"}, status=400)

        file = request.FILES['file']

        existingMedia = Media.objects.filter(FileName=file.name).first()

        if existingMedia:
            return JsonResponse({"message":"Arquivo já existe no banco de dados",
                "id": existingMedia.id,
                "fileName": existingMedia.FileName,
                "path": existingMedia.Path
            }, status=200)

        folder = 'uploads/images'
        physical_path = os.path.join(settings.MEDIA_ROOT, folder)
        os.makedirs(physical_path, exist_ok=True)

        file_path = os.path.join(physical_path, file.name)

        with open(file_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)

        media = Media.objects.create(
            FileName=file.name,
            Path=f"/media/{file.name}",
            TypeFile=file.content_type,
            SizeBytes=file.size,
            administrator_id= request.admin.id
        )


        return JsonResponse({
            "id": media.id,
            "fileName": media.FileName,
            "path": media.Path
        }, status=201)

    def get(self, request):
        medias = Media.objects.all().values('id','FileName', 'Path')

        return JsonResponse(list(medias), safe=False)

    def delete(self, request, id):
        try:
            media = Media.objects.get(id=id)

            physical_path = os.path.join(
                settings.BASE_DIR,
                media.Path.lstrip("/")
            )

            if os.path.exists(physical_path):
                os.remove(physical_path)

            media.delete()



            return JsonResponse(
                {"message": "Arquivo removido com sucesso"},
                status=200
            )

        except Media.DoesNotExist:
            return JsonResponse(
                {"error": "Arquivo não encontrado"},
                status=404
            )


