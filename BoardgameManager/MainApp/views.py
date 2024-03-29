from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse

from registration.backends.default.views import RegistrationView
from .forms import BgRegistrationForm

from django.contrib.auth.models import User
from users.models import Profile
from games.models import Collection
from users.forms import LinkBggForm

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
        new_collection = Collection.objects.create(user=new_user)

        # new_user.save()
        # new_collection.save()
        # new_profile.save()
        return new_user

def index(request):
    if request.user.is_authenticated:
        link_bgg_form = LinkBggForm()
        #.all() so it's iterable
        # user_collection = request.user.collection.boardgames.all()
        # filtered_user_collection = user_collection.filter(boardgame__is_expansion=False).order_by('boardgame__name')
        # context = {'link_bgg_form': link_bgg_form, 'user_collection': filtered_user_collection}
        context = {'link_bgg_form': link_bgg_form, 'username':request.user.username, 'is_own_collection':True}
        return render(request, 'MainApp/main.html', context)
    else:
        context={}
        return render(request, 'MainApp/index.html', context)

def user_page(request, username):
    link_bgg_form = LinkBggForm()
    context = {'is_own_collection':False, 'username':username}
    return render(request, 'MainApp/main.html', context)

def login(request):
    context = {noNavBar: True}
    return render(request, 'MainApp/login.html', context)
