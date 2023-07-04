from django.http import HttpResponse 
from django.shortcuts import render
from markdown2 import markdown

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def RenderPage(request, Page):
    
    
    
    if Page in util.list_entries() :
        return render(request, "encyclopedia/Page.html", {
            "Name" : Page ,
            "Content": markdown(util.get_entry(Page))
        })
        
    else :
        return render(request, "encyclopedia/Page404.html", {
            "Name" : Page
        })
    

def search(request):
    if request.method == "POST":
        q = request.POST['q']
        
        RelatedEntries = []
        
        for entry in util.list_entries():
            if q.lower() == entry.lower():
                return RenderPage(request, entry)
            
            elif q.lower() in entry.lower():
                RelatedEntries.append(entry)
        
        return render(request, "encyclopedia/RelatedEntries.html", {
            "entries": RelatedEntries
        })
        
def new(request):
    if request.method == "GET":
        return render(request, "encyclopedia/NewPage.html", {
            "title" : "",
            "content" : "",
            "endpoint" : "new",
            "error" : ""
        })

    elif request.method == "POST":
        title = request.POST['title']
        content = request.POST['md-content']
        
        for entry in util.list_entries():
            if title.lower() == entry.lower():
                return render(request, "encyclopedia/NewPage.html", {
                    "title" : title,
                    "content" : content,
                    "endpoint" : "new",
                    "Url" : "/wiki/"+title+"/edit/",
                    "error" : "<div id='error_box'>An Entry with the Same Name already exists...</div>"
                })
        
        util.save_entry(title, content)
        return RenderPage(request, title)
        
    
def editPage(request, Page):
    return render(request, "encyclopedia/NewPage.html", {
        "title" : Page,
        "content" : util.get_entry(Page),
        "endpoint" : "edit",
        "error" : ""
    })
    
def edit(request):
    if request.method == "POST":
        title = request.POST['title']
        content = request.POST['md-content']
        util.save_entry(title, content)
        return RenderPage(request, title)
