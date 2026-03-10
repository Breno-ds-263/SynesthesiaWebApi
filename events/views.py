import json

from django.http import JsonResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from events.models import Events
from media.models import Media
from users.auth.decorators import jwt_required


@method_decorator(csrf_exempt, name='dispatch')
class EventsView(View):

    @method_decorator(jwt_required)
    def post(self, request):
        try:
            data = json.loads(request.body)
            mediaid = data.get('MediaFiles')

            media = None

            if mediaid:
                media = Media.objects.get(id = mediaid)

            event = Events.objects.create(
                Title=data['Title'],
                summary=data['summary'],
                MediaFiles=media,
                Administrator_id=request.admin.id
            )

            return JsonResponse({"Message": "noticia criada com sucesso"}, status=201)


        except Media.DoesNotExist:
            return JsonResponse({"error": "Media não encontrada"}, status=404)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)


    def get(self, request):
        try:
            eventsList = Events.objects.all()

            data = []

            for event in eventsList:
                mediaData = None

                if event.MediaFiles:
                    mediaData = {
                        "id": event.MediaFiles.id,
                        "FileName": event.MediaFiles.FileName,
                        "Path": event.MediaFiles.Path,
                        "TypeFile": event.MediaFiles.TypeFile,
                        "SizeBytes": event.MediaFiles.SizeBytes,
                        "CreateAt": event.MediaFiles.CreateAt
                    }

                data.append({
                    "id": event.id,
                    "Title": event.Title,
                    "summary": event.summary,
                    "CreateAt": event.CreateAt,
                    "MediaFiles": mediaData
                })

            return JsonResponse(data, safe=False, status=200)

        except Media.DoesNotExist:
            return JsonResponse({"error": "Media não encontrada"}, status=404)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    @method_decorator(jwt_required)
    def delete(self,request,id):
        try:
            events = Events.objects.get(id=id)

            file = events.MediaFiles

            events.delete()

            if file:
                file.delete()

            return JsonResponse({"Message": "Evento apagado com sucesso"}, status=200)

        except Events.DoesNotExist:
            return JsonResponse({"error": "Evento não encontrada"}, status=404)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)





