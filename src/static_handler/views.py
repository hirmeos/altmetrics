from django.http import Http404, HttpResponse
from django.utils.encoding import smart_str
from django.views.generic import View

import mimetypes

mimetypes.init()
mimetypes.add_type('text/css', '.css')
mimetypes.add_type('text/html', '.html')
mimetypes.add_type('text/javascript', '.js')

class StaticFileServeView(View):

    def get(self, request, path, *args, **kwargs):
        filename = path.split('/').pop()
        filepath = '/static_files/{path}'.format(path=path)

        try:
            with open(filepath, 'rb') as file_p:
                response = HttpResponse(
                    content=file_p,
                    content_type=mimetypes.guess_type(filepath)[0]
                ) 
                response['Content-Disposition'] = 'attachment; filename=%s' % smart_str(filename)

                return response
        except FileNotFoundError as e:
            raise Http404('{path} not found'.format(path=filepath))
