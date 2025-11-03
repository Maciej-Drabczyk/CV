from django.shortcuts import render
from django import forms
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse
from random import choice
from markdown2 import Markdown

from . import util

def convertMarkdown(title):
    # Returns Markdown content by entry title
    content = util.get_entry(title)
    if content == None:
        return None
    else:
        markdowner = Markdown()
        return markdowner.convert(content)

class SearchForm(forms.Form):
    search = forms.CharField(label="")

class CreateForm(forms.Form):
    title = forms.CharField(label="Title")
    content = forms.CharField(widget=forms.Textarea())

class EditForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea())

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "form": SearchForm()
    })

def entry(request, title=""):
    if title == "":
        return render(request, "encyclopedia/entry.html", {
            "title": None,
            "content": None,
            "form": SearchForm()
        })
    markdowner = Markdown()
    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "content": convertMarkdown(title),
        "form": SearchForm()
    })

def search(request):
    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            return render(request, "encyclopedia/search.html", {
                "title": form.cleaned_data["search"],
                "entries": util.list_entries,
                "form": SearchForm()
            })
    return render(request, "encyclopedia/search.html", {
        "title": "",
        "entries": util.list_entries,
        "form": SearchForm()
    })

def create_new(request):
    # Check request method and form
    if request.method == "POST":
        form = CreateForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            for entry in util.list_entries():
                if title.lower() == entry.lower():
                    return render(request, "encyclopedia/create_new.html", {
                        "form": SearchForm(),
                        "createForm": form,
                        "error": True
                    })
                
            # Add entry
            util.save_entry(title, form.cleaned_data["content"])
            return HttpResponseRedirect(reverse("page") + title)
    return render(request, "encyclopedia/create_new.html", {
        "form": SearchForm(),
        "createForm": CreateForm(),
        "error": False
    })

def edit(request, title=""):
    if request.method == "POST":
        form = EditForm(request.POST)
        if form.is_valid():
            util.save_entry(title, form.cleaned_data["content"])
            return HttpResponseRedirect(reverse("page") + title)
    markdowner = Markdown()
    return render(request, "encyclopedia/edit.html", {
        "title": title,
        "content": util.get_entry(title),
        "form_edit": EditForm()
    })

def random(request):
    x = choice(util.list_entries())
    return HttpResponseRedirect(reverse("page") + x)
