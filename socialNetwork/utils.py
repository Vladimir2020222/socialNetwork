from django.conf import settings
from django.forms.renderers import get_default_renderer
from django.forms.utils import RenderableMixin
from django.utils.module_loading import import_string


class RequestRenderableMixin(RenderableMixin):
    renderer = get_default_renderer()

    def render(self, template_name=None, context=None, renderer=None, request=None):
        if request is None:
            raise ValueError('request token is necessary to render instances of %s, '
                             'may be you should use render_with_request template filter' %
                             (self.__class__.__qualname__, ))
        if context is None:
            context = self.get_context()
            context = self.extend_context_with_request(context, request)
        return super().render(template_name, context, renderer)

    @classmethod
    def extend_context_with_request(cls, context, request):
        context = context.copy()
        for processor in settings.TEMPLATES[0]['OPTIONS']['context_processors']:
            processor = import_string(processor)
            context.update(processor(request))
        return context
