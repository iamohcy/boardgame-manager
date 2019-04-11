import time

# Create your views here.
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.shortcuts import redirect

from rest_framework.renderers import JSONRenderer

# BGG Imports
from boardgamegeek import BGGClient
from boardgamegeek.exceptions import BGGItemNotFoundError

from users.forms import LinkBggForm
from .serializers import CollectionSerializer, BoardGameMechanicSerializer

# Models
from django.contrib.auth.models import User
from .models import BoardGame, BoardGameCategory, BoardGameMechanic, \
                         BoardGameStatistics, BoardGameFamily, BoardGameRank, Collection
        # log.info("boardgame id      : {}".format(self.id))
        # log.info("boardgame name    : {}".format(self.name))
        # log.info("number of plays   : {}".format(self.numplays))
        # log.info("last modified     : {}".format(self.lastmodified))
        # log.info("rating            : {}".format(self.rating))
        # log.info("own               : {}".format(self.owned))
        # log.info("preordered        : {}".format(self.preordered))
        # log.info("previously owned  : {}".format(self.prev_owned))
        # log.info("want              : {}".format(self.want))
        # log.info("want to buy       : {}".format(self.want_to_buy))
        # log.info("want to play      : {}".format(self.want_to_play))
        # log.info("wishlist          : {}".format(self.wishlist))
        # log.info("wishlist priority : {}".format(self.wishlist_priority))
        # log.info("for trade         : {}".format(self.for_trade))
        # log.info("comment           : {}".format(self.comment))

GLOBAL_bggApi = BGGClient()

# args:
#   request: HTTP Request object
#   collection: BGG collection of user
def getCollection(request, username):

    try:
        # user = bgg.user(form.cleaned_data['bgg_username'])
        collection = GLOBAL_bggApi.collection(username)
        user = GLOBAL_bggApi.user(username)
    except BGGItemNotFoundError:
        response = JsonResponse({'Error': 'User not found!'})
        return response

    # set bgg_username of user_profile
    user_profile = request.user.profile
    user_profile.bgg_username = username
    user_profile.save()

    # processUser(request, user)
    list_of_games = processCollection(request, collection)

    return list_of_games


# # args:
# #   user: BGG user object containing his rankings, and etc.
# def processUser(request, bgg_user):
#     user = request.user

#     return 0

# args:
#   collection: BGG collection of user
def processCollection(request, bgg_collection):
    user = request.user

    user_collection_set = user.collection.boardgames
    all_games = []

    new_game_ids = []
    valid_game_ids = []
    # bgg_c_game = game object from a collection, contains less details than
    # game which is an entire bgg board game object (e.g. contains image links, etc.)
    for bgg_c_game in bgg_collection.items:
        bgg_id = bgg_c_game.id
        # print("Trying to find bgg_id: " + str(bgg_id)) # DEBUG
        game_valid = False

        # Step 1 - Get or create board game object
        try:
            # Board game already in database
            ddb_boardgame = BoardGame.objects.get(pk=bgg_id)
            # print("It exists!! bgg_id: " + str(bgg_id)) # DEBUG
            valid_game_ids.append(bgg_id)
            # TODO UPDATE!! - Ranks, Ratings, etc.
        except:
            # Add game to list of games (by id) that we want to get from boardgamegeek
            new_game_ids.append(bgg_id)

    # Step 1b - Create BoardGame objects if they don't already exist
    if new_game_ids:
        print("Grabbing list of %d games from BGG..." % (len(new_game_ids)))
        start_time = time.process_time()
        print(new_game_ids)
        bgg_new_games = GLOBAL_bggApi.game_list(new_game_ids)
        print(bgg_new_games)
        print(len(bgg_new_games))

        end_time = time.process_time()
        print ("Games grabbed from BGG API in %f s" % (end_time-start_time))

        # Step 1c - Create BoardGame objects in DDB database
        for bgg_game in bgg_new_games:
            # We don't want to classify accessories as games
            # Make sure user actually owns the game before adding to collection
            if (not bgg_game.accessory) and (bgg_c_game.owned):
                print("Does not exist! Creating board game %s!" % (bgg_game.name))
                ddb_boardgame = BoardGame.objects.create_boardgame(bgg_game)
                valid_game_ids.append(bgg_game.id)

    # Step 2 - Update or create collection board game object
    for bgg_c_game in bgg_collection.items:
        bgg_id = bgg_c_game.id
        if (bgg_c_game.id in valid_game_ids):
            # This is different from board game object which is one per game
            # For this, every user has a collection board game object per game
            # in his/her collection
            all_games.append(bgg_c_game.name)
            try:
                # Board game already in database
                # uc = User Collection
                ddb_c_game = user_collection_set.get(boardgame__bgg_id=bgg_id)

                # Update ratings and num plays!
                ddb_c_game.num_plays = bgg_c_game.numplays
                ddb_c_game.rating = bgg_c_game.rating
                ddb_c_game.save()
            except:
                ddb_boardgame = BoardGame.objects.get(pk=bgg_id)
                ddb_c_game = user_collection_set.create(boardgame=ddb_boardgame,
                                                        num_plays=bgg_c_game.numplays,
                                                        rating=bgg_c_game.rating)

    return all_games

@login_required
def link_bgg(request):
    if request.method == 'POST': # If the form has been submitted...

        form = LinkBggForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data
            print(form.cleaned_data['bgg_username'])
            try:
                list_of_games = getCollection(request, form.cleaned_data['bgg_username'])
                response = JsonResponse({'bgg_username': form.cleaned_data['bgg_username'],
                                         'games': list_of_games})
                return response

            except BGGItemNotFoundError:
                return JsonResponse({'Error': 'User not found!'})
        else:
            return JsonResponse({'Error': 'invalid form!'})

        # return redirect('/')
        # return response
    else:
        return HttpResponse("Invalid non POST call to link_bgg!")

# @login_required
def get_user_collection(request):
    if request.method == 'GET': # If the form has been submitted...
        user_collection = request.user.collection
        serializer = CollectionSerializer(user_collection)
        json_str = JSONRenderer().render(serializer.data)

        return HttpResponse(json_str, content_type='application/json')
        # return redirect('/')
        # return response
    else:
        return HttpResponse("Invalid non GET call to get_user_collection!")

# @login_required
def get_boardgame_metadata(request):
    if request.method == 'GET': # If the form has been submitted...
        mechanics = BoardGameMechanic.objects.all()
        serializer = BoardGameMechanicSerializer(mechanics, many=True)
        json_data = {"mechanics": serializer.data};
        json_str = JSONRenderer().render(json_data)

        return HttpResponse(json_str, content_type='application/json')
        # return redirect('/')
        # return response
    else:
        return HttpResponse("Invalid non GET call to get_boardgame_metadata!")

# @login_required
def get_user_collection(request, username):
    if request.method == 'GET':
        user = User.objects.get(username=username)
        user_collection = user.collection
        serializer = CollectionSerializer(user_collection)
        json_str = JSONRenderer().render(serializer.data)

        return HttpResponse(json_str, content_type='application/json')
        # return redirect('/')
        # return response
    else:
        return HttpResponse("Invalid non GET call to get_user_collection!")
