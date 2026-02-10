import json
from django.http import JsonResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from news.models import News
from users.auth.decorators import jwt_required
from media.models import Media


@method_decorator(csrf_exempt, name='dispatch')
@method_decorator(jwt_required, name='dispatch')
class NewsView(View):

    def post(self, request):
        try:
            data = json.loads(request.body)
            mediaId = data.get('MediaFiles')

            media = None
            if mediaId:
                media = Media.objects.get(id=mediaId)

            new = News.objects.create(
                Title = data['Title'],
                Summary = data['Summary'],
                NewsLink = data['NewsLink'],
                MediaFiles = media,
                Administrator_id=request.admin.id
            )

            return JsonResponse({"Message": "noticia criada com sucesso"})


        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

        except Media.DoesNotExist:
            return JsonResponse({"error": "Media não encontrada"}, status=404)

    def get(self, request):
        news = News.objects.all().values('Title','Summary','NewsLink')

        return  JsonResponse(list(news), safe=False)





