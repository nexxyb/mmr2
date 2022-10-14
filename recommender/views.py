from django.shortcuts import render
from .models import *
from django.views import generic
from . import mmr3 
from recommender.forms import SearchForm
from django.http import HttpResponseRedirect

#Create your views here.

def index(request):
    """View function for home page of site.""" 
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form =  SearchForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            data= form.cleaned_data['movie']
            result= mmr3.get_movie([data])

    # if a GET (or any other method) we'll create a blank form
    else:
        form = SearchForm()
        result= mmr3.get_movie(form.data)
    
    context = {
        'result': result,
        'form':form
    }

    return render(request, 'recommender/index.html', context=context)

# class Index(generic.TemplateView):
#     template_name = 'recommender/index.html'
#     form = SearchForm()
    
#     def get_context_data(self, **kwargs):
#         context= super(Index, self).get_context_data(**kwargs)
#         form = SearchForm()
#         data= form.data
#         result= mmr3.get_movie([data])
#         context['result']= result
#         return context
    
#     def form_valid(self, form):
#         data= form.cleaned_data['movie']
#         result= mmr3.get_movie([data])
#         return super().form_valid(form)
        
    
class ReloadView(generic.TemplateView):
    template_name= 'recommender/index.html'
    
    
class ContactView(generic.FormView):
    template_name= 'recommender/contact.html'
    #form_class= 