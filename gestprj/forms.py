from django.forms import ModelForm, Textarea, TextInput, Select, EmailInput, NumberInput
from django import forms
from gestprj.models import TUsuarisXarxa
from gestprj.models import TCategoriaPrj
from gestprj.models import Projectes
from gestprj.models import CentresParticipants
from gestprj.models import TCategoriaPrj
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
          'id_resp',
          'codi_prj',
          'codi_oficial',
          'titol',
          'acronim',
          'resum',
          'comentaris',
          'data_inici_prj',
          'data_fi_prj',
          'id_categoria',
          'serv_o_subven',
          'canon_oficial',
          'percen_canon_creaf',
          'percen_iva',
          'es_docum_web',
          'data_docum_web',
          'id_estat_prj',
          'es_coordinat',
          'id_usuari_extern',
          'convocatoria',
          'resolucio',
          'es_coordinat',
        ]
        widgets = {
            'es_coordinat': forms.HiddenInput(),
            'es_docum_web': forms.HiddenInput(),
            # 'codi_prj': forms.TextInput(attrs={'disabled':'True'}),
            # 'id_resp': Select(),
            'serv_o_subven': forms.RadioSelect(choices=[(1,'Servei'),(2,'Subvencio')],attrs={'class':'servsubv','checked':True}),
            # 'id_categoria': Select(),
            # 'id_categoria': forms.ChoiceField(choices=[(cat.id_categoria,cat.desc_categoria) for cat in TCategoriaPrj.objects.all()]),
            # 'id_estat_projecte': Select(),
            # 'data_inici_prj': SelectDateWidget,
            # 'data_fi_prj': SelectDateWidget,
            # 'data_docum_web': SelectDateWidget,

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
