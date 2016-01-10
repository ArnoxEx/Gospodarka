from django.shortcuts import render

# Create your views here.
from Gospodarka.gospodarkaApp.models import Object, Address
from Gospodarka.gospodarkaApp.forms import *
from django.template import Context, loader, RequestContext
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.views.decorators.csrf import ensure_csrf_cookie
@ensure_csrf_cookie



def index(request):
    object_list = Object.objects.filter(address__city__exact = 'Wroclaw').order_by('address_id')
    tmpl = loader.get_template("index.html")
    cont = Context({'Object': object_list})
    return HttpResponse(tmpl.render(cont))

def afterLogin(request):
    if request.method == 'POST':
        c = {}
        c.update(csrf(request))
        return render_to_response("afterLogin.html", c)

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

