from django.shortcuts import render
from markdown2 import Markdown
import markdown
from . import util
import random


def convert_md_to_html(title):
    content=util.get_entry(title)
    markdowner=markdown.Markdown()
    if content == None:
        return None
    else:
        return markdowner.convert(content)

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries() 
    })
def entry(request,title):
    html_content = convert_md_to_html(title)
    if html_content == None:
        return render(request, "encyclopedia/error.html",{
                    "message": "This entry does not extist"})
    else:
        return render(request, "encyclopedia/entry.html",{
                "title": title,
                "content" : html_content})

def search(request):
    if request.method == "POST":
        entry_search = request.POST['q']
        html_content = convert_md_to_html(entry_search)
        if html_content is not None:
            return render(request, "encyclopedia/entry.html",{
                "title": entry_search,
                "content" : html_content})
        else:
            allEntries = util.list_entries()
            recomendation = []
            for entry in allEntries:
                if entry_search.lower() in entry.lower():
                    recomendation.append(entry)
            return render(request, "encyclopedia/search.html",{
                "recomendation": recomendation
            })
    

def new_page(request):
    if request.method == "GET":
        return render(request,"encyclopedia/new_page.html")
    else:
        title = request.POST['title']
        content= request.POST['content']
        titleExist = util.get_entry(title)
        if titleExist is not None:
            return render(request, "encyclopedia/error.html",{
                "message": "entry page already exists"
            })
        else:
            util.save_entry(title, content)
            html_content = convert_md_to_html(title)
            return render(request, "encyclopedia/entry.html",{
                "title":title,
                "content": html_content
            })
def edit(request):
    if request.method=="POST":
        title = request.POST['entry_title']
        content= util.get_entry(title)
        return render(request, "encyclopedia/edit.html",{
            "title":title,
            "content":content
        })
    
def save_edit(request):
    if request.method == 'POST':
        title = request.POST['title']
        content= request.POST['content']
        util.save_entry(title,content)
        html_content = convert_md_to_html(title)
        return render(request, "encyclopedia/entry.html",{
            "title":title,
            "content": html_content})
    # ...
    #title = request.POST.get('title')  # Retrieve the entered title from the form
    #context = {'title': title}
    #return render(request, 'your_template.html', context)

def rand(request):
    allEntries = util.list_entries()
    rand_entries = random.choice(allEntries)
    html_content = convert_md_to_html(rand_entries)
    return render(request, "encyclopedia/entry.html",{
        "title": rand_entries,
        "content":html_content
    })