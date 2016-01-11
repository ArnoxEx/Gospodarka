from django.shortcuts import render

# Create your views here.
from Gospodarka.gospodarkaApp.models import Object, Address
from Gospodarka.gospodarkaApp.forms import *
from django.template import Context, loader, RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
@ensure_csrf_cookie


def index(request):
    if (request.user.is_authenticated()):
        print("Youre logged in")
        print(request.user.username)
    else:
        print("Youre not logged in")

    context = RequestContext(request)

    # object_list = Object.objects.filter(address__city__exact = 'Wroclaw').order_by('address_id')
    # tmpl = loader.get_template("index.html")
    # cont = Context({'Object': object_list})
    return render_to_response("index.html", {}, context)

def register(request):
    context = RequestContext(request)

    # A boolean value for telling the template whether the registration was successful.
    # Set to False initially. Code changes value to True when registration succeeds.
    registered = False

    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        # Note that we make use of both UserForm and UserProfileForm.
        user_form    = UserForm(data=request.POST)
        usr_form     = UsrForm(data=request.POST)
        address_form = AddressForm(data=request.POST)

        # If all forms are valid...
        if user_form.is_valid() and usr_form.is_valid() and address_form.is_valid():
            # Save the user's form data to the database.
            user = user_form.save()

            # Now we hash the password with the set_password method.
            # Once hashed, we can update the user object.
            user.set_password(user.password)
            user.save()

            # Now we insert address data to database
            address = address_form.save()

            # Now sort out the Usr instance.
            # Since we need to set the user attribute ourselves, we set commit=False.
            # This delays saving the model until we're ready to avoid integrity problems.
            usr = usr_form.save(commit=False)
            usr.user = user
            usr.address = address

            # Now we save the Usr model instance.
            usr.save()

            # Update our variable to tell the template registration was successful.
            registered = True

        # Invalid form or forms - mistakes or something else?
        # Print problems to the terminal.
        # They'll also be shown to the user.
        else:
            print (user_form.errors, usr_form.errors, address_form.errors)

    # Not a HTTP POST, so we render our form using two ModelForm instances.
    # These forms will be blank, ready for user input.
    else:
        user_form = UserForm()
        usr_form = UsrForm()
        address_form = AddressForm()

    # Render the template depending on the context.
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
