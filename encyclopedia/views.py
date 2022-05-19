from aiohttp import parse_content_disposition
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
import markdown2
from . import util
from random import randint


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    return render(request, "encyclopedia/entry.html", {
        "entry": markdown2.markdown(util.get_entry(title)),
        "title": title
    })

def create(request):
    if request.method == "POST":
        title = request.POST["title"]
        if util.get_entry(title) is not None:
            return render(request, "encyclopedia/create.html", {
                "key": True
            })
        content = request.POST["content"]
        util.save_entry(title, content)
        return HttpResponseRedirect(reverse("entry", kwargs={"title": title}))
    return render(request, "encyclopedia/create.html", {
        "key": False
    })

def search(request):
    query = request.POST["q"]
    if util.get_entry(query) is not None:
        return HttpResponseRedirect(reverse("entry", kwargs={"title": query}))
    else:
        entry_list = util.list_entries()
        entries = []
        for entry in entry_list:
            if entry.find(query) != -1:
                entries.append(entry)
        if len(entries) == 0:
            return render(request, "encyclopedia/search.html", {
                "key": False
            })
        else:
            return render(request, "encyclopedia/search.html", {
                "key": True,
                "entries": entries
            })


def random(request):
    entry_list = util.list_entries()
    index = randint(0, len(entry_list) - 1)
    return HttpResponseRedirect(reverse("entry", kwargs={"title": entry_list[index]}))

def edit(request, title):
    if request.method == "POST":
        util.save_entry(title, request.POST["content"])
        return HttpResponseRedirect(reverse("entry", kwargs={"title": title}))
    return render(request, "encyclopedia/edit.html", {
        "entry": util.get_entry(title),
        "title": title
    })