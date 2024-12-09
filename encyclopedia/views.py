from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
import random
import markdown2

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry_page(request, entry_name):
    if util.get_entry(entry_name) is not None:
        html_entry = markdown2.markdown(util.get_entry(entry_name))
        return render(request, "encyclopedia/entry_content.html", {
            "entry": html_entry,
            "entry_name": entry_name
        })
    
    else:
        return render(request, "encyclopedia/error_page.html")
    
def search(request):
    
    # Capture user query
    if request.method == "GET":
        query = request.GET.get('q', '')
        
        # Exact query match
        entry_match_list = [entry for entry in util.list_entries() if query.lower() == entry.lower()]
        entry_match_string = "".join(entry_match_list)
        
        # Substring match
        substring_list = [entry for entry in util.list_entries() if query.lower() in entry.lower()]
        
        # Execute statement if there is an exact match
        if len(entry_match_list) == 1:
            html_entry = markdown2.markdown(util.get_entry(entry_match_string))
            return render(request, "encyclopedia/entry_content.html", {
            "entry": html_entry,
            "entry_name": entry_match_string
        })
        
        # Execute statement if there is a substring match
        elif len(substring_list) > 0:
            return render(request, "encyclopedia/search.html", {
                "search_result": substring_list,
                "query": query
            })
            
        # No results found
        else:
            return render(request, "encyclopedia/no_result.html")
        
def display_new_entry_form(request):
            return render(request, "encyclopedia/create_new.html")
        
def create_new_entry(request):
    
    if request.method == "POST":
        title = request.POST["entry_title"]
        content = request.POST["entry_content"]
        
        try:
            if util.check_entry(title):
                util.save_entry(title, content)
                return HttpResponseRedirect(reverse("encyclopedia:entry_page", args=(title,)))
        
            else:
                return render(request, "encyclopedia/already_exist.html")
            
        except:
            return render(request, "encyclopedia/invalid_entry.html")
        
def edit_display(request, entry_name):
     if util.get_entry(entry_name) is not None:
        return render(request, "encyclopedia/edit_entry.html", {
            "entry": util.get_entry(entry_name),
            "entry_name": entry_name
        })
    
     else:
        return render(request, "encyclopedia/error_page.html")
    
def edit_entry(request, entry_name):
    
    if request.method == "POST":
        content = request.POST["entry_content"]
        util.save_entry_old(entry_name, content)
        return HttpResponseRedirect(reverse("encyclopedia:entry_page", args=(entry_name,)))
    
def random_entry(request):
    randomized_list = random.sample(util.list_entries(), len(util.list_entries()))
    html_entry = markdown2.markdown(util.get_entry(randomized_list[0]))
    return render(request, "encyclopedia/entry_content.html", {
        "entry": html_entry,
        "entry_name": randomized_list[0]
    })