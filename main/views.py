from django.http import HttpResponse
from django.shortcuts import render

from random import choice

from .constants import MAIN_PAGE_CITATIONS


# Create your views here.
def main(request):
    rnd_citation = choice(MAIN_PAGE_CITATIONS)
    return render(request, 'main/index.html', {'citation': rnd_citation})
