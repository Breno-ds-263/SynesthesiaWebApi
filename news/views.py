import json
from operator import attrgetter

from django.http import JsonResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from news.models import News
from users.auth.decorators import jwt_required
from media.models import Media


@method_decorator(csrf_exempt, name='dispatch')
class NewsView(View):

    @method_decorator(jwt_required)
    def post(self, request):
        try:
            data = json.loads(request.body)
            mediaId = data.get('MediaFiles')

            media = None
            if mediaId:
                media = Media.objects.get(id=mediaId)

            new = News.objects.create(
                Title=data['Title'],
                Summary=data['Summary'],
                NewsLink=data['NewsLink'],
                MediaFiles=media,
                Administrator_id=request.admin.id
            )

            return JsonResponse({"Message": "noticia criada com sucesso"}, status=201)

        except Media.DoesNotExist:
            return JsonResponse({"error": "Media não encontrada"}, status=404)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    def get(self, request):
        news_list = News.objects.all().order_by("-CreateAt")
        data = []

        for news in news_list:
            media_data = None

            if news.MediaFiles:
                media_data = {
                    "id": news.MediaFiles.id,
                    "FileName": news.MediaFiles.FileName,
                    "Path": news.MediaFiles.Path,
                    "TypeFile": news.MediaFiles.TypeFile,
                    "SizeBytes": news.MediaFiles.SizeBytes,
                    "CreateAt": news.MediaFiles.CreateAt
                }

            data.append({
                "id": news.id,
                "Title": news.Title,
                "Summary": news.Summary,
                "NewsLink": news.NewsLink,
                "CreateAt": news.CreateAt,
                "MediaFiles": media_data
            })

        return JsonResponse(data, safe=False, status=200)

    @method_decorator(jwt_required)
    def patch(self, request, id):
        try:
            # 1. Busca a notícia existente pelo ID recebido na URL
            news = News.objects.get(id=id)
            data = json.loads(request.body)

            # 2. Atualiza os campos de texto apenas se eles foram enviados no JSON
            if 'Title' in data:
                news.Title = data['Title']
            if 'Summary' in data:
                news.Summary = data['Summary']
            if 'NewsLink' in data:
                news.NewsLink = data['NewsLink']

            # 3. Lógica para atualizar a Mídia (MediaFiles)
            if 'MediaFiles' in data:
                media_id = data['MediaFiles']
                if media_id is None:
                    news.MediaFiles = None  # Remove a mídia associada se mandarem null
                else:
                    media = Media.objects.get(id=media_id)
                    news.MediaFiles = media

            # 4. Salva as alterações no banco de dados
            news.save()

            return JsonResponse({"Message": "Notícia atualizada com sucesso"}, status=200)

        except News.DoesNotExist:
            return JsonResponse({"error": "Notícia não encontrada"}, status=404)

        except Media.DoesNotExist:
            return JsonResponse({"error": "Mídia informada não encontrada"}, status=404)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    @method_decorator(jwt_required)
    def delete(self, request, id):
        try:
            new = News.objects.get(id=id)
            file = new.MediaFiles

            new.delete()

            if file:
                file.delete()

            return JsonResponse({"Message": "Notícia e mídia associada excluídas com sucesso"}, status=200)

        except News.DoesNotExist:
            return JsonResponse({"error": "Notícia não encontrada"}, status=404)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)