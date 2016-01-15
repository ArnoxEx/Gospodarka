from django.shortcuts import render

# Create your views here.
from operator import attrgetter
from datetime import timedelta
from datetime import datetime
import hashlib, random
from django.core.mail import send_mail
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
            # user.is_active = False
            user.save()

            address = address_form.save()

            usr = usr_form.save(commit=False)
            usr.user = user
            usr.address = address

            # salt = hashlib.sha1(str(random.random()).encode('utf-8')).hexdigest()[:5]
            # activation_key = hashlib.sha1((salt+user.email).encode('utf-8')).hexdigest()
            # key_expires = datetime.now() + timedelta(2)
            # usr.activation_key = activation_key
            # usr.key_expires = key_expires

            usr.save()

            group = Group.objects.filter(name="Oridinary")
            if group:
                user.groups.add(group[0].id)
                user.save()

            # email_subject = 'Account confirmation'
            # email_body = "Hey %s, thanks for signing up. To activate your account, click this link within \
            # 48hours http://127.0.0.1:8000/gospodarkaApp/confirm/%s" % (user.username, activation_key)

            # send_mail(email_subject, email_body, 'dobreWydarzenie@gospodarkaApp.com',
            #     [user.email], fail_silently=False)

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
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/gospodarkaApp/')
            else:
                return HttpResponse("Your account is disabled.")
        else:
            print ("Invalid login details: {0}, {1}".format(username, password))
            return HttpResponse("Invalid login details supplied.")

    else:
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

    is_manager = request.user.groups.filter(name='Manager').exists()

    return render_to_response('edit_profile.html'
            , {'email_form' : email_form, 'usr_form' : usr_form, 'address_form' : address_form,
                'changed': changed, 'is_manager' : is_manager}, context)

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

    is_manager = request.user.groups.filter(name='Manager').exists()
    return render_to_response('add_object.html'
            , {'object_form' : object_form, 'address_form' : address_form, 'created': created, 'is_manager' : is_manager}
            , context)

@login_required
def user_objects(request):
    return objects(request, Usr.objects.get(user=request.user))

def object(request, object_id):
    context = RequestContext(request)

    object = Object.objects.get(id=object_id)

    is_manager = False
    if request.user.is_authenticated():
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

    is_manager = request.user.groups.filter(name='Manager').exists()
    return render_to_response('edit_object.html'
            , {'object_form' : object_form, 'address_form' : address_form, 'changed': changed,
                'object_id' :object_id, 'is_manager' : is_manager}, context)

@login_required
def remove_object(request, object_id):
    context = RequestContext(request)

    object = Object.objects.get(id=object_id)

    is_manager = False
    if request.user.is_authenticated():
        usr = Usr.objects.get(user=request.user)
        usrobject = Usrobject.objects.filter(usr=usr, object=object)
        if usrobject:
            is_manager = True
            object.delete()
        else:
            print("ERROR: object without management")

    return render_to_response('remove_object.html', {'is_manager' : is_manager,} , context)

def eventsTable(request):
    context = RequestContext(request)

    is_manager = request.user.groups.filter(name='Manager').exists()
    events = Event.objects.order_by('name')
    context_dict = {'events': events, 'is_manager' : is_manager}

    return render_to_response('events.html', context_dict, context)

def event(request, event_id):
    context = RequestContext(request)

    event = Event.objects.get(id=event_id)

    is_manager = False
    if request.user.is_authenticated():
        usr = Usr.objects.get(user=request.user)
        usrobject = Usrobject.objects.filter(usr=usr, object=event.place)
        if usrobject:
            is_manager = True
        else:
            print("ERROR: object without management")

    ticket_number = event.max_tickets
    orders = Ordr.objects.filter(event=event)
    for order in orders:
        ticket_number = ticket_number - order.numb

    return render_to_response('event.html',
        {'event' : event, 'ticket_number' : ticket_number, 'is_manager' : is_manager}, context)

def add_event(request, object_id):
    context = RequestContext(request)

    created = False

    if request.method == 'POST':
        event_form = EventForm(data=request.POST)

        if event_form.is_valid():
            event  = event_form.save(commit=False)
            object = Object.objects.get(id=object_id)
            event.place = object
            event.save()

            created = True

        else:
            print (event_form.errors)
    else:
        event_form = EventForm()

    is_manager = request.user.groups.filter(name='Manager').exists()
    return render_to_response('add_event.html'
            , {'event_form' : event_form, 'object_id' : object_id, 'created' : created, 'is_manager' : is_manager} , context)

def edit_event(request, event_id):
    context = RequestContext(request)

    changed = False
    event = Event.objects.get(id=event_id)

    if request.method == 'POST':
        event_form = EventForm(data=request.POST)

        if event_form.is_valid():
            new_event = event_form.save(commit = False)
            new_event.id = event.id
            new_event.place = event.place
            new_event.save()

            changed = True

        else:
            print (event_form.errors)
    else:
        event_form = EventForm(instance=event)

    is_manager = request.user.groups.filter(name='Manager').exists()
    return render_to_response('edit_event.html'
            , {'event_form' : event_form, 'event_id' : event_id, 'changed': changed, 'is_manager' : is_manager} , context)

@login_required
def remove_event(request, event_id):
    context = RequestContext(request)

    event = Event.objects.get(id=event_id)

    is_manager = False
    if request.user.is_authenticated():
        usr = Usr.objects.get(user=request.user)
        usrobject = Usrobject.objects.filter(usr=usr, object=event.place)
        if usrobject:
            is_manager = True
            event.delete()
        else:
            print("ERROR: object without management")

    return render_to_response('remove_event.html'
            , {'is_manager' : is_manager,} , context)

@login_required
def orders(request):
    context = RequestContext(request)

    is_manager = request.user.groups.filter(name='Manager').exists()
    orders = Ordr.objects.filter(usr__user=request.user)
    context_dict = {'orders' : orders, 'is_manager' : is_manager}

    return render_to_response('orders.html', context_dict, context)

def otherOrders(request):
    user = Usr.objects.get(user=request.user)
    context = RequestContext(request)
    objectsIds = Usrobject.objects.filter(usr=user).values_list('object')
    events=Event.objects.filter(place__in=objectsIds).values_list('id')
    orders = Ordr.objects.filter(event__in=events)
    is_manager = request.user.groups.filter(name='Manager').exists()
    context_dict = {'otherOrders' : orders, 'is_manager' : is_manager}

    return render_to_response('otherOrders.html', context_dict, context)

@login_required
def add_order(request, event_id):
    context = RequestContext(request)

    created = False
    too_much = False
    too_little = False
    price = 0

    if request.method == 'POST':
        order_form = OrderForm(data=request.POST)

        if order_form.is_valid():
            order = order_form.save(commit=False)
            if order.numb < 1:
                too_little = True
            else:
                event = Event.objects.get(id=event_id)
                ticket_number = event.max_tickets
                orders = Ordr.objects.filter(event=event)
                for ordr in orders:
                    ticket_number = ticket_number - ordr.numb
                    ordr.price = event.ticket_price*ordr.numb
                if order.numb > ticket_number:
                    too_much = True
                else:
                    usr = Usr.objects.get(user=request.user)
                    status = Status.objects.get(value='Created')

                    order.usr = usr
                    order.event = event
                    order.status = status
                    order.price = event.ticket_price*order.numb
                    price = order.price
                    order.save()

                    created = True

        else:
            print (order_form.errors)
    else:
        order_form = OrderForm()

    is_manager = request.user.groups.filter(name='Manager').exists()
    return render_to_response('add_order.html',
        {'order_form' : order_form, 'created': created, 'event_id' : event_id, 'price' : price,
        'too_much' : too_much, 'too_little' : too_little, 'is_manager' : is_manager}, context)
