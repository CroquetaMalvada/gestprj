from django import forms
from gestprj.models import TUsuarisXarxa

class UsuariXarxaForm(forms.ModelForm):
    id_usuari_xarxa = forms.DecimalField()
    nom_xarxa = forms.CharField()
    class Meta:
        model = TUsuarisXarxa
