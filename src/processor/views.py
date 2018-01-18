from django.views.generic import ListView

from .models import Doi


class DoisView(ListView):

    model = Doi
    template_name = 'dois.html'
    context_object_name = 'dois'

    def get_queryset(self):
        return self.model.objects.filter(
            last_upload__user=self.request.user
        )
