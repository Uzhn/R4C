from django import forms
from .models import Robot
from .validators import validate_created


class RobotForm(forms.ModelForm):
    """Форма создания робота."""
    created = forms.DateTimeField(validators=[validate_created])

    class Meta:
        model = Robot
        fields = ['model', 'version', 'created']

    def save(self, commit=True):
        instance = super(RobotForm, self).save(commit=False)
        model = self.cleaned_data.get('model')
        version = self.cleaned_data.get('version')
        instance.serial = f'{model}-{version}'

        if commit:
            instance.save()
        return instance
