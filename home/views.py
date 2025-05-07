'''
View for the home app
History:
(forgot to add history until recently)
Feb 21 2024 - Made the form actually work
'''

from django.shortcuts import render, HttpResponse, reverse, redirect, HttpResponseRedirect

from .forms import ScrapCodeForm


# based on: https://stackoverflow.com/questions/59255243/how-to-route-to-a-url-based-on-data-entered-in-django-form
# actually no, https://docs.djangoproject.com/en/5.0/topics/forms/ is way more helpful

def home(request):
    '''
    The homepage
    '''
    # if this is a POST request we need to process the form data
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = ScrapCodeForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            data = form.cleaned_data['scrapcode'] # this is the data from the form
            # redirect to the page for uploading to the scrapbook corresponding to the entered code
            return HttpResponseRedirect(f"/Scrapbook_project/{data}/")

    # if a GET (or any other method), create a blank form
    else:
        form = ScrapCodeForm()

    return render(request, "home/homepage.html", {'form' : form})