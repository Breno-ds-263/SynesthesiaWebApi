from django.forms import Media
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
import json
from django.views.decorators.csrf import csrf_exempt
from cards.models import Card
from users.auth.decorators import jwt_required
from media.models import Media

@method_decorator(csrf_exempt, name='dispatch')
class CardView(View):

    @method_decorator(jwt_required)
    def post(self, request):
        try:
            data = json.loads(request.body)
            mediaId = data.get('MediaFiles')

            media = None
            if mediaId:
                media = Media.objects.get(id=mediaId)

            card = Card.objects.create(
                Name=data['Name'],
                EducationLevel=data['EducationLevel'],
                Role=data['Role'],
                MediaFiles=media,
                Administrator_id=request.admin.id
            )
            return JsonResponse({"Message": "Card criado com sucesso"}, status=201)

        except Media.DoesNotExist:
            return JsonResponse({"error": "Media não encontrada"}, status=404)

        except Exception as e:
            return JsonResponse({"Error": str(e)}, status=400)



    def get(self,request):
        try:
            cards = Card.objects.all()

            data=[]

            for card in cards:
                mediaData = None

                if card.MediaFiles:
                    mediaData= {
                    "id": card.MediaFiles.id,
                    "FileName": card.MediaFiles.FileName,
                    "Path": card.MediaFiles.Path,
                    "TypeFile": card.MediaFiles.TypeFile,
                    "SizeBytes": card.MediaFiles.SizeBytes,
                    "CreateAt": card.MediaFiles.CreateAt
                }

                data.append({
                    "id": card.id,
                    "Name": card.Name,
                    "EducationLevel": card.EducationLevel,
                    "Role": card.Role,
                    "CreateAt": card.CreateAt,
                    "MediaFiles": mediaData
                })

            return JsonResponse(data, safe=False, status=200)

        except Exception as e:
            return JsonResponse({"Error": str(e)}, status=500)

    @method_decorator(jwt_required)
    def delete(self,request, id):
        try:
            card = Card.objects.get(id=id)

            file = card.MediaFiles

            card.delete()

            if file:
                file.delete()

            return JsonResponse({"Message": "card apagado com sucesso"}, status=200)

        except Card.DoesNotExist:
            return JsonResponse({"error": "Card não encontrada"}, status=404)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
