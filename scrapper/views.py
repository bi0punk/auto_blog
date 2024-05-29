import requests
from django.shortcuts import render
from django import forms

class URLForm(forms.Form):
    url = forms.URLField(label='URL', max_length=200)

def check_url(request):
    code = None
    if request.method == 'POST':
        form = URLForm(request.POST)
        if form.is_valid():
            url = form.cleaned_data['url']
            try:
                response = requests.get(url)
                code = response.status_code
            except requests.exceptions.RequestException as e:
                code = str(e)
    else:
        form = URLForm()
    return render(request, 'webtester/check_url.html', {'form': form, 'code': code})
