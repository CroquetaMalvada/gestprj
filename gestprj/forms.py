from django import forms

class UsuariXarxaForm(forms.Form):
    id_usuari_xarxa = forms.DecimalField()
    nom_xarxa = forms.CharField()
