import json

from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from media.models import Media
from materials.models import  Materials
from users.auth.decorators import jwt_required


@method_decorator(csrf_exempt, name='dispatch')
class MaterialsView(View):

    @method_decorator(jwt_required)
    def post(self,request):
        try:
            data = json.loads(request.body)
            mediaId = data.get('MediaFiles')

            media = None

            if mediaId:
                media = Media.objects.get(id=mediaId)


            materials = Materials.objects.create(
                Title=data['Title'],
                Summary=data['Summary'],
                MaterialsLink=data['MaterialsLink'],
                MediaFiles=media,
                Administrator_id=request.admin.id
            )

            return JsonResponse({"message": "Material criado com sucesso"}, status=201)

        except Media.DoesNotExist:
            return  JsonResponse({"message:": "Media não exisente"}, status=404)

        except Exception as e:
            return JsonResponse ({"error": str(e)}, status=400)


    def get(self,request):
        materialsList = Materials.objects.select_related('MediaFiles').all()

        data = []

        for materials in materialsList:
            media_data = None

            if materials.MediaFiles:
                media_data = {
                    "id": materials.MediaFiles.id,
                    "FileName": materials.MediaFiles.FileName,
                    "Path": materials.MediaFiles.Path,
                    "TypeFile": materials.MediaFiles.TypeFile,
                    "SizeBytes": materials.MediaFiles.SizeBytes,
                    "CreateAt": materials.MediaFiles.CreateAt,
                }

            data.append({
                "id": materials.id,
                "Title": materials.Title,
                "Summary": materials.Summary,
                "NewsLink": materials.MaterialsLink,
                "MediaFiles": media_data
            })

        return JsonResponse(data, safe=False, status=200)

    @method_decorator(jwt_required)
    def delete(self,request,id):
        try:

            materials = Materials.objects.get(id=id)

            file = materials.MediaFiles

            materials.delete()

            if file:
                file.delete()

            return JsonResponse({"Message": "Material apagado com sucesso"}, status=200)

        except Materials.DoesNotExist:
            return JsonResponse({"Message": "Material não encontrado"}, status=404)

        except Exception as e:
            return JsonResponse({"Error": str(e)}, status = 400)








