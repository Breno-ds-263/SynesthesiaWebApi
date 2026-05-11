import json

from django.http import JsonResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from media.models import Media
from article.models import Articles
from users.auth.decorators import jwt_required


@method_decorator(csrf_exempt, name='dispatch')
class ArticlesView(View):

    @method_decorator(jwt_required)
    def post(self, request):
        try:
            data = json.loads(request.body)

            mediaId = data.get('MediaFiles')

            media = None

            if mediaId:
                media = Media.objects.get(id=mediaId)


            article = Articles.objects.create(
                Title = data['Title'],
                Summary = data['Summary'],
                Tag = data['Tag'],
                Event = data['Event'],
                Year = data['Year'],
                MediaFiles=media,
                ArticleLink=data.get('ArticleLink'),
                Administrator_id=request.admin.id
            )

            return JsonResponse({"Message": "Artigo criado com sucesso"}, status=201)

        except Media.DoesNotExist:
            return JsonResponse({"message": "Media não encontrada"}, status=404)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)


    def get(self, request):
        try:
            articlesList = Articles.objects.all()

            data = []



            for article in articlesList:
                media_data = None

                if article.MediaFiles:
                    media_data = {
                        "id": article.MediaFiles.id,
                        "FileName": article.MediaFiles.FileName,
                        "Path": article.MediaFiles.Path,
                        "TypeFile": article.MediaFiles.TypeFile,
                        "SizeBytes": article.MediaFiles.SizeBytes,
                        "CreateAt": article.MediaFiles.CreateAt,
                    }

                data.append({
                    "id": article.id,
                    "Title": article.Title,
                    "Summary": article.Summary,
                    "Tag": article.Tag,
                    "Event": article.Event,
                    "Year": article.Year,
                    "MediaFiles": media_data,
                    "ArticleLink": article.ArticleLink
                })

            return JsonResponse(data, safe=False, status=200)


        except Exception as e:
            return JsonResponse({"Error": str(e)}, status=400)

    @method_decorator(jwt_required)
    def delete(self, request, id):
        try:
            article = Articles.objects.get(id=id)

            file = article.MediaFiles

            article.delete()

            if file:
                file.delete()

            return JsonResponse({"Message": "Evento apagado com sucesso"}, status=200)

        except Articles.DoesNotExist:
            return JsonResponse({"error": "Evento não encontrada"}, status=404)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)