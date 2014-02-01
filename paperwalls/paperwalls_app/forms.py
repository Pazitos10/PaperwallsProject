from paperwalls_app.models import Album,Categoria,Imagen
from django import forms


from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit




class AlbumForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AlbumForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_id = 'album'
        self.helper.form_method = 'post'
        self.helper.form_class='form-horizontal'
        self.helper.add_input(Submit('submit-album', 'Crear'))
        self.helper.label_class='col-lg-2'
        self.helper.field_class='col-lg-8'

    class Meta:
        model = Album



class ImagenForm(forms.ModelForm):
    #Cambio campo Etiquetas original por uno customizado, luego analizo tags en la vista correspondiente
    Tags = forms.CharField(widget = forms.TextInput(attrs={'id':'id_tag','placeholder':'ingrese un tag y pulse enter'}))
    class Meta:
        model = Imagen        
        exclude = ['width','height','etiquetas','user']
    
    def __init__(self, *args, **kwargs):
        super(ImagenForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'imagen'
        self.helper.form_method = 'post'
        self.helper.form_class='form-horizontal'
        self.helper.add_input(Submit('submit-imagen', 'Guardar'))
        self.helper.label_class='col-lg-2'
        self.helper.field_class='col-lg-8'
              


class CategoriaForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CategoriaForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_id = 'categoria'
        self.helper.form_class='form-horizontal'
        self.helper.add_input(Submit('submit-categoria', 'Crear'))
        self.helper.label_class='col-lg-2'
        self.helper.field_class='col-lg-8'

    class Meta:
        model = Categoria        

