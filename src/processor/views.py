from django.views.generic import ListView

from .models import Uri


class DoisView(ListView):

    model = Uri
    template_name = 'dois.html'
    context_object_name = 'dois'

    def get_queryset(self):
        return self.model.objects.filter(
            last_upload__user=self.request.user
        )
