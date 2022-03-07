from django.shortcuts import render, redirect
from googletrans import Translator
import googletrans

# Create your views here.
def index(request):
    context = {'ndict': googletrans.LANGUAGES}
    if request.method == 'POST':
        translator = Translator()
        text = request.POST.get('bf')
        fr = request.POST.get('fr')
        to = request.POST.get('to')
        if text:
            inter = translator.translate(text, src=fr, dest=to)
            context.update({
                'bf': text,
                'fr': fr,
                'to': to,
                'af': inter.text
            })
    return render(request, 'trans/index.html', context)