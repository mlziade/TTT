from django.shortcuts import render
from django.views import View
from .forms import TextForm

class HomeView(View):
    template_name = 'home.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
    
class TextView(View):
    template_name = 'text.html'

    def get(self, request, *args, **kwargs):

        # Create form
        form = TextForm()

        return render(request, self.template_name, {'form': form})
    
    def post(self, request, *args, **kwargs):
        # Create form with POST data
        form = TextForm(request.POST)

        if form.is_valid():
            # Process the data in form.cleaned_data
            text = form.cleaned_data['text']
            
            #TODO: Process text

            return render(request, self.template_name, {'form': form, 'text': text})

        return render(request, self.template_name, {'form': form})