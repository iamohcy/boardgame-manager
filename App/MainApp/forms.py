from registration.forms import RegistrationFormUniqueEmail
from django import forms
from users.models import Profile
from datetime import datetime
from crispy_forms.helper import FormHelper

START_YEAR = 1940
class BgRegistrationForm(RegistrationFormUniqueEmail):
    this_year = datetime.today().year
    BIRTH_YEAR_CHOICES = [x for x in range(this_year, START_YEAR-1, -1)]

    first_name = forms.CharField(widget=forms.TextInput())
    last_name = forms.CharField(widget=forms.TextInput())
    date_of_birth = forms.DateField(input_formats=['%d/%m/%Y'],
                        # widget=forms.TextInput(
                        #     attrs={'type': 'date'}
                        # )
                        widget=forms.SelectDateWidget(
                            empty_label=("Choose Year", "Choose Month", "Choose Day"),
                            years=BIRTH_YEAR_CHOICES,
                        ),
                    )    #
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        # self.helper.form_id = 'id-myModelForm'
        # self.helper.form_class = 'form-horizontal'
        # self.helper.form_action = 'my_model_form_url'
        # self.helper.form_error_title = 'Form Errors'
        # self.helper.help_text_inline = True
