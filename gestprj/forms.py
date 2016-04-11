from django.forms import ModelForm, Textarea, TextInput, Select, EmailInput, NumberInput
from django import forms
from gestprj.models import TUsuarisXarxa
from gestprj.models import TCategoriaPrj
from gestprj.models import Projectes
from gestprj.models import CentresParticipants
from django.forms.extras.widgets import SelectDateWidget


class UsuariXarxaForm(forms.ModelForm):
    id_usuari_xarxa = forms.DecimalField()
    nom_xarxa = forms.CharField()

    class Meta:
        model = TUsuarisXarxa


class ProjectesForm(forms.ModelForm):  # hereda de la clase predefinida forms.ModelForm
    class Meta:
        model = Projectes
        fields = [
            'id_projecte',
            'codi_prj',
            'id_resp',
            'codi_oficial',
            'acronim',
            'titol',
            'resum',
            'serv_o_subven',
            'id_categoria',  # o id_categoria???
            'convocatoria',
            'resolucio',
            'data_inici_prj',
            'data_fi_prj',
            'comentaris',
            'es_docum_web',
            'data_docum_web',
            'id_estat_prj',
            'es_coordinat',
        ]
        widgets = {
            'id_resp': Select(),
            'serv_o_subven': forms.RadioSelect(),
            'id_categoria': Select(),
            'id_estat_prj': Select(),
            'data_inici_prj': SelectDateWidget,
            'data_fi_prj': SelectDateWidget,
            'data_docum_web': SelectDateWidget,
            'es_coordinat': forms.CheckboxInput

        }

    class CentresParticipantsForm(forms.ModelForm):
        class Meta:
            model = CentresParticipants
            fields = [
                'id_centre_part'
            ]
            widgets = {
                'id_centre_part': Select()
            }
