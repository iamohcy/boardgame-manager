from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse

from registration.backends.default.views import RegistrationView
from .forms import BgRegistrationForm
from users.models import Profile
from django.shortcuts import render

class BgRegistrationView(RegistrationView):

    form_class = BgRegistrationForm

    def register(self, form_class):
        new_user = super().register(form_class)
        _first_name = form_class.cleaned_data['first_name']
        _last_name = form_class.cleaned_data['last_name']

        # # Save first and last name in user object too
        # new_user.first_name = first_name
        # new_user.last_name = last_name
        # new_user.save()

        _date_of_birth = form_class.cleaned_data['date_of_birth']

        new_profile = Profile.objects.create(user=new_user, first_name=_first_name,
                                             last_name=_last_name, date_of_birth=_date_of_birth)
        new_profile.save()
        return new_user

def index(request):
    context = {}
    return render(request, 'MainApp/index.html', context)
