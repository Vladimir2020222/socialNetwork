import inspect
from functools import partialmethod
from typing import Union

from django import forms
from django.core.exceptions import PermissionDenied, ImproperlyConfigured
from django.forms import BaseForm, ModelForm, Form
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic.base import ContextMixin

from feed.forms import FormNameInput
from feed.models import Post

__all__ = ['VerifyAuthorMixin', 'MultiFromMixin']


class VerifyAuthorMixin:
    def _verify_author(self):
        user = self.request.user
        if user != Post.objects.get(pk=self.kwargs.get('pk')).author and not user.has_perm('feed.change_post'):
            return PermissionDenied()

    def dispatch(self, request, *args, **kwargs):
        self._verify_author()
        super().dispatch(request, *args, **kwargs)


class DefaultMethods:
    def _get_attr(self, form_name, attr_name):
        for conf in self.forms:
            if conf['form_name'] == form_name:
                return conf[attr_name]

    _get_attr.necessary_in_process = True

    def get_initial(self, form_name):
        return self._get_attr(form_name, 'initial').copy()

    def get_prefix(self, form_name):
        return self._get_attr(form_name, 'prefix')

    def get_form_class(self, form_name):
        return self._get_attr(form_name, 'form_class')

    def get_form(self, form_name):
        kwargs = self.form_method(form_name, 'get_form_kwargs')()
        form: BaseForm = self.form_method(form_name, 'get_form_class')()(**kwargs)

        form.fields[self.form_name_html_field_name] = forms.CharField(required=False, widget=FormNameInput(
            attrs={
                'value': form_name,
            }))

        return form

    def get_form_kwargs(self, form_name):
        kwargs = {
            'initial': self.form_method(form_name, 'get_initial')(),
            'prefix': self.form_method(form_name, 'get_prefix')()
        }

        if self.request.method in ('POST', 'PUT') and \
                self.request.POST.get(self.form_name_html_field_name) == form_name:
            kwargs.update(
                {
                    'data': self.request.POST,
                    'files': self.request.FILES
                }

            )
        return kwargs

    def get_success_url(self, form_name):
        success_url = self._get_attr(form_name, 'success_url')
        if success_url is None:
            raise ImproperlyConfigured(
                "No URL to redirect to in config number %s. Provide a success_url"
                "or set it to 'empty' to return HttpResponse(''). It may be useful"
                "when using ajax."
            )
        if success_url == 'empty':
            success_url = reverse('empty_page')
        return str(success_url)

    def form_valid(self, form, form_name):
        return HttpResponseRedirect(self.form_method(form_name, 'get_success_url'))

    def form_invalid(self, form, form_name):
        return self.render_to_response(self.get_context_data(form=form))


class MultiFormMixinMeta(type):
    def __new__(mcs, name, bases, attrs):
        if IsMultiFromMixin in bases:
            return super().__new__(mcs, name, bases, attrs)

        attrs['forms'] = mcs.normalize_forms(attrs['forms'])

        class FormMethodsBase:  # methods from DefaultMethods will be added to this class. It will be added to the
            pass  # end of bases. It is used to let call super().<form_name>_<method_name>()

        necessary_in_process_method_names = {}
        form_names = [f_conf['form_name'] for f_conf in attrs['forms']]

        for default_method_name, method in inspect.getmembers(
                DefaultMethods, predicate=inspect.isfunction
        ):
            necessary_in_process = getattr(method, 'necessary_in_process', None)    # is method used by DefaultMethods
            if necessary_in_process:
                necessary_in_process_method_names[default_method_name] = default_method_name
            if not default_method_name.startswith('_'):
                for form_name in form_names:
                    method_name = f'{form_name}_{default_method_name}'
                    partial_method = partialmethod(method, form_name=form_name)

                    setattr(FormMethodsBase, method_name, partial_method)
            elif necessary_in_process:
                setattr(FormMethodsBase, default_method_name, method)

        bases = bases + (FormMethodsBase,)

        new_class = super().__new__(mcs, name, bases, attrs)

        # verifying that child class doesn't override methods that is used by MethodsBase
        for necessary_method_name in necessary_in_process_method_names:
            cls_method = getattr(new_class, necessary_method_name)
            if not hasattr(cls_method, 'necessary_in_process'):
                raise ImproperlyConfigured(
                    'class %s overrides %s method that is necessary for automatic generation'
                    'methods for form processes' % (name, necessary_method_name)
                )

        return new_class

    @staticmethod
    def normalize_forms(forms_conf):
        normalized_forms = []
        used_names = set()
        for form_config in forms_conf:
            if 'form_class' not in form_config:
                raise ImproperlyConfigured(
                    'form_clas is missed in form configuration number %s' % (forms_conf.index(form_config),))
            if 'form_name' not in form_config:
                raise ImproperlyConfigured(
                    'form_name is missed in form configuration number %s' % (forms_conf.index(form_config),))
            if form_config['form_name'] in used_names:
                raise ImproperlyConfigured()

            used_names.add(form_config['form_name'])

            normalized_form_config = {'initial': {}, 'prefix': None, 'success_url': None, 'include_to_context': True}

            normalized_form_config.update(form_config)
            normalized_forms.append(normalized_form_config)

        used_prefixes = set()

        for prefix in [f_conf['prefix'] for f_conf in normalized_forms]:
            if prefix is None:
                prefix = ''
            if prefix in used_prefixes:
                if prefix == '':
                    msg = "You cant have two unset prefixes in one forms config"
                else:
                    msg = "You cant set two and more identical prefixes in one forms config"
                return ImproperlyConfigured(msg)
        return normalized_forms


class IsMultiFromMixin:
    pass


class MultiFromMixin(IsMultiFromMixin, ContextMixin, metaclass=MultiFormMixinMeta):
    """
    MultiFormMixin lets define more than one form class for one view. forms attribute must be a list of
    dicts form configurations. Form configurations must contain two required keys form_class,
    form_name and success_url four optional keys initial, include_to_context (bool) and prefix, that must be unique.
    Methods for forms must be named as <form_name>_<method_name> where method_name is one of
    methods FormMixin class. Not provided methods will be automatically generated with
    Automatically generated methods will have implementation as FromMixin methods.
    If form can be used with ajax, and you don't need to return response, you can set success_url to
    'empty', in this case response will be HttpResponse(''). get_context_data adds
    form_name: self.<form_name>_get_form() pairs.
    """

    forms: list[dict] = []

    form_name_html_field_name = 'form_name'

    def get_form(self, request) -> tuple[Union[ModelForm, Form], str]:
        if request.method not in ("POST", "PUT"):
            raise TypeError('get_form() method should be used only with POST requests')
        form_name = request.POST.get(self.form_name_html_field_name)
        form = self.form_method(form_name, 'get_form')()
        return form, form_name

    def form_method(self, form_name, method_name):
        return getattr(self, f'{form_name}_{method_name}')

    def get_context_data(self, **kwargs):
        for form_conf in self.forms:
            if form_conf['include_to_context']:
                get_form = getattr(self, f'{form_conf["form_name"]}_get_form')
                kwargs[form_conf['form_name']] = get_form()
        return kwargs

    def post(self, request, *args, **kwargs):
        form, form_name = self.get_form(request)
        if form.is_valid():
            return self.form_method(form_name, 'form_valid')(form)
        return self.form_method(form_name, 'form_invalid')(form)
