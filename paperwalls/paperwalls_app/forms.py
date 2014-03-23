from paperwalls_app.models import Album,Categoria,Imagen
from django import forms

from selectable import forms as sforms



from paperwalls_app.lookups import AlbumLookup,CategoriaLookup,ImagenLookup


from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Hidden



class BuscadorAlbumForm(forms.Form):
    album = sforms.AutoCompleteSelectField(
        lookup_class=AlbumLookup,
        label='Buscar :',
        required=False
    )
    def __init__(self, *args, **kwargs):
        super(BuscadorAlbumForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'get'
        self.helper.form_class='form-horizontal'
        self.helper.label_class='col-lg-2'
        self.helper.field_class='col-lg-8'

class BuscadorCategoriaForm(forms.Form):
    categoria = sforms.AutoCompleteSelectField(
        lookup_class=CategoriaLookup,
        label='Buscar :',
        required=False
    )
    def __init__(self, *args, **kwargs):
        super(BuscadorCategoriaForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'get'
        self.helper.form_class='form-horizontal'
        self.helper.label_class='col-lg-2'
        self.helper.field_class='col-lg-8'

class BuscadorImagenForm(forms.Form):
    imagen = sforms.AutoCompleteSelectField(
        lookup_class=ImagenLookup,
        label='Buscar :',
        required=False
    )
    def __init__(self, *args, **kwargs):
        super(BuscadorImagenForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'get'
        self.helper.form_class='form-horizontal'
        self.helper.label_class='col-lg-2'
        self.helper.field_class='col-lg-8'





class AlbumForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AlbumForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_id = 'album'
        self.helper.form_method = 'post'
        self.helper.form_class='form-horizontal'
        self.helper.add_input(Submit('submit-album', 'Crear'))
        self.helper.add_input(Hidden('input-confirma-borrar','False'))
        self.helper.label_class='col-lg-2'
        self.helper.field_class='col-lg-8'

    class Meta:
        model = Album
        exclude = ['creador']



class ImagenForm(forms.ModelForm):
    
    class Meta:
        model = Imagen        
        exclude = ['width','height','user']
    
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


from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
class ExtendedUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 
                  'email', "first_name", 'last_name' )

class UserEditForm(ExtendedUserCreationForm):
    class Meta:
        model = User
        exclude = ('username', 'password1', 'password2')