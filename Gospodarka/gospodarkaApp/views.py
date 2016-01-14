from django.shortcuts import render

# Create your views here.
from operator import attrgetter
from Gospodarka.gospodarkaApp.models import Object, Address
from Gospodarka.gospodarkaApp.forms import *
from django.template import Context, loader, RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.db.models import Q
@ensure_csrf_cookie


def index(request):
    if (request.user.is_authenticated()):
        print("Youre logged in")
        print(request.user.username)
    else:
        print("Youre not logged in")

    context = RequestContext(request)
    is_manager = request.user.groups.filter(name='Manager').exists()
    return render_to_response("index.html", { 'is_manager' : is_manager }, context)

def register(request):
    context = RequestContext(request)

    registered = False

    if request.method == 'POST':
        user_form    = UserForm(data=request.POST)
        usr_form     = UsrForm(data=request.POST)
        address_form = AddressForm(data=request.POST)

        if user_form.is_valid() and usr_form.is_valid() and address_form.is_valid():
            user = user_form.save(commit=False)

            user.set_password(user.password)
            user.save()

            address = address_form.save()

            usr = usr_form.save(commit=False)
            usr.user = user
            usr.address = address

            usr.save()

            group = Group.objects.get(name="Oridinary")
            if group:
                user.group.add(groups.id)
                user.save()

            registered = True

        else:
            print (user_form.errors, usr_form.errors, address_form.errors)

    else:
        user_form = UserForm()
        usr_form = UsrForm()
        address_form = AddressForm()

    return render_to_response(
            'register.html',
            {'user_form': user_form, 'usr_form': usr_form, 'address_form' : address_form, 'registered': registered}
            , context)

def user_login(request):
    context = RequestContext(request)

    if (request.user.is_authenticated()):
        print("Youre logged in")
        print(request.user.username)
    else:
        print("Youre not logged in")
    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':
        # Gather the usedrname and password provided by the user.
        # This information is obtained from the login form.
        username = request.POST['username']
        password = request.POST['password']

        # Use Django's machinery to attempt to see if the username/password
        # combination is valid - a User object is returned if it is.
        user = authenticate(username=username, password=password)

        # If we have a User object, the details are correct.
        # If None (Python's way of representing the absence of a value), no user
        # with matching credentials was found.
        if user:
            # Is the account active? It could have been disabled.
            if user.is_active:
                # If the account is valid and active, we can log the user in.
                # We'll send the user back to the homepage.
                login(request, user)
                return HttpResponseRedirect('/gospodarkaApp/')
            else:
                # An inactive account was used - no logging in!
                return HttpResponse("Your account is disabled.")
        else:
            # Bad login details were provided. So we can't log the user in.
            print ("Invalid login details: {0}, {1}".format(username, password))
            return HttpResponse("Invalid login details supplied.")

    # The request is not a HTTP POST, so display the login form.
    # This scenario would most likely be a HTTP GET.
    else:
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
        return render_to_response('login.html', {}, context)

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/gospodarkaApp/')

@login_required
def edit_profile(request):
    context = RequestContext(request)
    
    changed = False
    usr     = Usr.objects.get(user=request.user)

    if request.method == 'POST':
        email_form   = EmailForm(  data=request.POST)
        usr_form     = UsrForm(    data=request.POST)
        address_form = AddressForm(data=request.POST)

        if email_form.is_valid() and usr_form.is_valid() and address_form.is_valid():
            email = email_form.save(commit = False)
            request.user.email = email.email
            request.user.save()

            adr = address_form.save(commit = False)
            adr.id = usr.address.id
            adr.save()

            new_usr = usr_form.save(commit = False)
            new_usr.address = adr
            new_usr.user = request.user
            new_usr.id = usr.id
            new_usr.save()

            changed = True

        else:
            print (email_form.errors, usr_form.errors, address_form.errors)
    else:
        email_form   = EmailForm(  instance = request.user)
        usr_form     = UsrForm(    instance = usr)
        address_form = AddressForm(instance = usr.address)

    return render_to_response('edit_profile.html'
            , {'email_form' : email_form, 'usr_form' : usr_form, 'address_form' : address_form,
                'changed': changed,}, context)

def objects(request, user=None):
    context = RequestContext(request)

    is_manager = request.user.groups.filter(name='Manager').exists()

    if user==None:
        objects = Object.objects
    else:
        usrobjects = Usrobject.objects.filter(usr=user)
        query = Q()
        for usrobject in usrobjects:
            query = query | Q(id=usrobject.object.id)
        objects = Object.objects.filter(query)
    objects = objects.order_by('address__city')
    context_dict = {'objects': objects, 'is_manager': is_manager}

    return render_to_response('objects.html', context_dict, context)

@login_required
def add_object(request):
    context = RequestContext(request)

    created = False

    if request.method == 'POST':
        address_form = AddressForm(data=request.POST)
        object_form = ObjectForm(data=request.POST)

        if address_form.is_valid() and object_form.is_valid():
            adr = address_form.save()
            obj = object_form.save(commit=False)
            obj.address = adr
            obj.save()
            usr = Usr.objects.get(user=request.user)
            usrobject = Usrobject(usr=usr, object=obj)
            usrobject.save()

            created = True

        else:
            print (address_form.errors, object_form.errors)
    else:
        object_form  = ObjectForm()
        address_form = AddressForm()

    return render_to_response('add_object.html'
            , {'object_form' : object_form, 'address_form' : address_form, 'created': created}
            , context)

@login_required
def user_objects(request):
    return objects(request, Usr.objects.get(user=request.user))

def object(request, object_id):
    context = RequestContext(request)

    object = Object.objects.get(id=object_id)

    is_manager = request.user.is_authenticated()
    if is_manager:
        usr = Usr.objects.get(user=request.user)
        usrobject = Usrobject.objects.filter(usr=usr, object=object)
        if usrobject:
            is_manager = True
        else:
            print("ERROR: object without management")

    return render_to_response('object.html', {'object' : object, 'is_manager' : is_manager}, context)

def edit_object(request, object_id):
    context = RequestContext(request)
    
    changed = False
    object = Object.objects.get(id=object_id)

    if request.method == 'POST':
        address_form = AddressForm(data=request.POST)
        object_form  = ObjectForm( data=request.POST)

        if address_form.is_valid() and object_form.is_valid():
            adr = address_form.save(commit = False)
            adr.id = object.address.id
            adr.save()
            obj = object_form.save(commit = False)
            obj.id = object_id
            obj.address = adr
            obj.save()

            changed = True

        else:
            print (address_form.errors, object_form.errors)
    else:
        object_form  = ObjectForm( instance = object)
        address_form = AddressForm(instance = object.address)

    return render_to_response('edit_object.html'
            , {'object_form' : object_form, 'address_form' : address_form, 'changed': changed,
                'object_id' :object_id }, context)

def eventsTable(request):
    context = RequestContext(request)

    events = Event.objects.order_by('name')
    context_dict = {'events': events}

    return render_to_response('events.html', context_dict, context)

@login_required
def orders(request):
    context = RequestContext(request)

    orders = Ordr.objects.filter(usr__user=request.user)
    context_dict = {'orders' : orders}

    return render_to_response('orders.html', context_dict, context)
