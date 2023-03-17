from django import forms


class FormNameInput(forms.HiddenInput):
    """Used by MultipleFormMixin to determine current form when POST request has sent"""
    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context['widget']['name'] = 'form_name'
        return context
