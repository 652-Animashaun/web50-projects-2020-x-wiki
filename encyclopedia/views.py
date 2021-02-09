import secrets
import markdown2
from django.shortcuts import render
from django import forms
from django.urls import reverse
from django.http import HttpResponseRedirect

from . import util


class SearchForm(forms.Form):
    query = forms.CharField(label="search entry")
class EditEntryForm(forms.Form):
	title = forms.CharField(label="Title", max_length=20)
	content= forms.CharField(label="Body", widget=forms.Textarea, max_length=1000)

class NewPageForm(forms.Form):
	title = forms.CharField(label="Title", max_length=20)
	content= forms.CharField(label="Body", widget=forms.Textarea, max_length=1000)



def index(request):
	if request.method == "POST":
		form = SearchForm(request.POST)
		if form.is_valid():
			query = form.cleaned_data["query"].lower()

			print(query)
			low_list=[]
			for i in util.list_entries():
					i = i.strip().lower()
					low_list.append(i)
			

			if query in low_list:
				return HttpResponseRedirect(reverse("wiki:singlepage",
					kwargs={'title':query}))
				# return render(request, "encyclopedia/singlepage.html",{
				# 	"singleentry": util.get_entry(query)
				# 	})

			elif [k for k in low_list if query in k]:
				FiltList = [k for k in low_list if query in k]
				return render(request,"encyclopedia/results.html",{
					"entries": FiltList,
					"form": SearchForm(),
					"results": len(FiltList)
					})
				print(len(FiltList))

			else:
				return render(request, "encyclopedia/notfound.html")

	else:
		return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "form": SearchForm()

    })

    
def singlepage(request, title):
	if util.get_entry(title) is not None:
		entryMarkdown = markdown2.markdown(util.get_entry(title))
		return render(request, "encyclopedia/singlepage.html", {

		
		"singleentry": entryMarkdown,
		"title":title

		})
	else:
		return render(request, "encyclopedia/notfound.html")

def NewPage(request):

	if request.method=="POST":
		form=NewPageForm(request.POST)
		if form.is_valid():
			# topics=form.cleaned_data['topics']
			title=form.cleaned_data['title']
			content=form.cleaned_data['content']

			if title==util.get_entry(title):
				pass

			util.save_entry(title, content)

			return HttpResponseRedirect(reverse("wiki:singlepage",
					kwargs={'title':title}))



	return render(request, "encyclopedia/create.html", {
		"form":NewPageForm()
		})


def editEntry(request, title):
	
	if request.method=="POST":
		form = EditEntryForm(request.POST)
		if form.is_valid():
			title = form.cleaned_data["title"]
			content = form.cleaned_data["content"]
			util.save_entry(title, content)
			return HttpResponseRedirect(reverse("wiki:singlepage", 
				kwargs={'title':title}))
	else:
		if util.get_entry(title) is not None:
			data={"title": title, "content": util.get_entry(title)}
			return render(request, "encyclopedia/editentry.html",{
				"title":title,
				"form": EditEntryForm(data)
				})
		



def randomPage(request):
	title = secrets.choice(util.list_entries())
	entryMarkdown = markdown2.markdown(util.get_entry(title))

	print(title)
	return render(request, "encyclopedia/singlepage.html", {
		"singleentry": entryMarkdown,
		"title":title

		})




