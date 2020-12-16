from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse
from django import forms

import markdown2
import random

from . import util


# to create form to create new pages
class CreateForm(forms.Form):
    title_page = forms.CharField()
    content = forms.CharField(widget=forms.Textarea)

# to create form to edit pages
class EditForm(forms.Form):
    #title_edit = forms.CharField()
    cont_edit = forms.CharField(widget=forms.Textarea)

# home page
def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

# view to show the content of the entry
def detail(request, title):
    return render(request, "encyclopedia/title.html", {
        "contenu": markdown2.markdown(util.get_entry(title)), "title": title
    })

# view to show the page user searches for or the list of results
def search(request):
    query = request.GET.get('q')
    entries = util.list_entries()
    for title in entries:
        if query == title:
            r = detail(request,title)
            break
        elif query in title:
            r =  render(request, "encyclopedia/search.html", { "entries": entries, "query": query})
            break
        #else:
         #   return HttpResponse ("Entry not found")
    
    return r

# view to create new pages
def new(request):
    if request.method == "POST":
        form = CreateForm(request.POST)
        if form.is_valid():
            title_page = form.cleaned_data["title_page"]
            content = form.cleaned_data["content"]
            if (title_page in util.list_entries()):
                    return HttpResponse ("Error File already exists")
            else:    
                util.save_entry(title_page, content)
                r = detail(request, title_page)
                return r
            
        else:
            return render(request, "encyclopedia/new.html", {
                "form": form
            })

    
    else:
        return render(request, "encyclopedia/new.html" , {
                "form": CreateForm()
        })

# view to edit the particular page
def edit(request, title):

    if request.method == "POST":
        form = EditForm(request.POST)
        if form.is_valid():
            #title_edit = form.cleaned_data["title_edit"]
            cont_edit = form.cleaned_data["cont_edit"]
            # saving the new content   
            util.save_entry(title, cont_edit)
            r = detail(request, title)
            return r
            
        else:
            return render(request, "encyclopedia/edit.html" , {
            "form": EditForm(initial={"cont_edit": util.get_entry(title)}), "title": title
        })
    else:
        return render(request, "encyclopedia/edit.html" , {
            "form": EditForm(initial={"cont_edit": util.get_entry(title)}), "title": title
        })

# view to display random page in the encyclopedia
def rando(request):
    entries = util.list_entries()
    entry_choice = random.choice(entries)
    r = detail(request, entry_choice)
    return r