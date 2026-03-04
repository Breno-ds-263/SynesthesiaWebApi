from django.http import JsonResponse
from django.shortcuts import render
import json

from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from users.auth.decorators import jwt_required
from video.models import Video

@method_decorator(csrf_exempt, name='dispatch')
class VideoView(View):

    @method_decorator(jwt_required)
    def post(self, request):
        try:
            data = json.loads(request.body)

            video = Video.objects.create(
                Title=data['Title'],
                VideoUrl=data['VideoUrl'],
                Administrator_id=request.admin.id
            )

            return JsonResponse({"Message": "Video adicionado com sucesso"}, status=200)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)


