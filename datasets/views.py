from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic import View
from .forms import SubjectFormset, CreatorFormset, DoiForm
from django.shortcuts import render, redirect
import xml.etree.ElementTree as ET
from .dict_to_xml import dict_to_xml
import mds.http.post as posttodoi

from doi_site.settings import DATACITE_TEST_URL, DATACITE_URL


class Mint(View):
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    # pylint: disable=no-self-use
    def get(self, request):
        template_name = 'create_normal.html'
        heading_message = 'Formset Demo'
        doiform = DoiForm(request.GET or None)
        formset1 = SubjectFormset(request.GET or None, prefix='form1')
        formset2 = CreatorFormset(request.GET or None, prefix='form2')
        return render(request, template_name, {
        'form': doiform,
        'formset1': formset1,
        'formset2': formset2,
        'heading': heading_message,
    })

    def post(self, request):
        doiform = DoiForm(request.POST or None)
        formset1 = SubjectFormset(request.POST or None, prefix='form1')
        formset2 = CreatorFormset(request.POST or None, prefix='form2')
        template_name = 'create_normal.html'
        heading_message = 'Formset Demo'
        if formset1.is_valid() and formset2.is_valid() and doiform.is_valid():
            metadata = doiform.cleaned_data
            metadata["subjects"] = [ x["subject"] for x in formset1.cleaned_data ]
            metadata["creators"] = formset2.cleaned_data
            print(metadata)
            e = dict_to_xml(metadata)
            print (e)
        response = posttodoi._post(DATACITE_URL + "/metadata/", e.encode(), { "Content-Type": "application/xml;charset=UTF-8" }, method="POST")
        if(response == 200):
            print("DOI site was called successfully!")
        else:
            print("DOI site was called successfully!")
        return render(request, template_name, {
        'form': doiform,
        'formset1': formset1,
        'formset2': formset2,
        'heading': heading_message,
    })

def _is_test_url():
    if DATACITE_URL == DATACITE_TEST_URL:
        return True
    return False

   


