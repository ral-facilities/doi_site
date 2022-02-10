from urllib.error import HTTPError
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic import View
from .forms import SubjectFormset, CreatorFormset, DoiForm, AddUrlForm, UrlForm
from django.shortcuts import render, redirect
import xml.etree.ElementTree as ET
from .dict_to_xml import dict_to_xml
import mds.http.post as postdoi
import mds.http.get as getdoi
from mds.MdsApi import MdsApi
from django.core.exceptions import ObjectDoesNotExist
from doi_site.settings import DATACITE_TEST_URL, DATACITE_URL, DOI_PREFIX
import mds.http.helper as helper


class Mint(View):
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    # pylint: disable=no-self-use
    def get(self, request):
        template_name = 'create_normal.html'
        heading_message = 'Formset Demo'
        authorized_dois = []
        groups = request.user.groups.iterator()
        for group in groups:
            try:
                authorized_dois.append(group.groupprofile.doi_suffix)
            except ObjectDoesNotExist:
                pass
        suffixlist = authorized_dois
        doiform = DoiForm(request.GET or None)
        formset1 = SubjectFormset(request.GET or None, prefix='form1')
        formset2 = CreatorFormset(request.GET or None, prefix='form2')
        for form in formset2:
            form.use_required_attribute = True
        return render(request, template_name, {
        'form': doiform,
        'formset1': formset1,
        'formset2': formset2,
        'doi_prefix': DOI_PREFIX,
        'suffixlist': suffixlist,
        'heading': heading_message,
    })

    def post(self, request):
        doiform = DoiForm(request.POST or None)
        formset1 = SubjectFormset(request.POST or None, prefix='form1')
        formset2 = CreatorFormset(request.POST or None, prefix='form2')
        authorized_dois = []
        notAuthorised = False
        groups = request.user.groups.iterator()
        for group in groups:
            try:
                authorized_dois.append(group.groupprofile.doi_suffix)
            except ObjectDoesNotExist:
                pass
        suffixlist = authorized_dois
        for form in formset2:
            form.use_required_attribute = True
        template_name = 'create_normal.html'
        heading_message = 'Formset Demo'
        if formset1.is_valid() and formset2.is_valid() and doiform.is_valid():
            mds_api = MdsApi(request) 
            metadata = doiform.cleaned_data
            canUseSuffix = helper.is_authorized(request, metadata['identifier'])
            if canUseSuffix:
                pass
            else:
                notAuthorised = True,
                return render(request, template_name, {
                'form': doiform,
                'formset1': formset1,
                'formset2': formset2,
                'doi_prefix': DOI_PREFIX,
                'heading': heading_message,
                'suffixlist': suffixlist,
                'notAuthorised': notAuthorised
                })
            metadata["subjects"] = [x.get("subject") for x in formset1.cleaned_data if x.get('subject')]
            metadata["creators"] = [x for x in formset2.cleaned_data if x]
            metadata['identifier'] = DOI_PREFIX + '/'+ metadata['identifier']
            doi = metadata['identifier'] 
            print(metadata)
            e = dict_to_xml(metadata)
            print (e)
            try:
                response = mds_api.put("/metadata/" + doi, e.encode(), headers={ "Content-Type": "application/xml;charset=UTF-8" })
                response.raise_for_status()
            except Exception as err:
                print(f'Other error occurred: {err}')
                return render(request, template_name, {
                    'form': doiform,
                    'formset1': formset1,
                    'formset2': formset2,
                    'doi_prefix': DOI_PREFIX,
                    'heading': heading_message,
                    'suffixlist': suffixlist,
                    'err': err,
                    'notAuthorised': notAuthorised
                    })
            else:
                print('Data site call was successful!') 
        else:
            return render(request, template_name, {
            'form': doiform,
            'formset1': formset1,
            'formset2': formset2,
            'doi_prefix': DOI_PREFIX,
            'heading': heading_message,
        })
        if(response.status_code == 201):
            print("DOI site was called successfully!")
            return redirect('minturl', doi) 
        else:
            print("DOI site was not called successfully!")
            return render(request, template_name, {
            'form': doiform,
            'formset1': formset1,
            'formset2': formset2,
            'doi_prefix': DOI_PREFIX,
            'heading': heading_message,
        })


class AddUrl(View):
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    template_name = 'add_url.html'
    def get(self, request, err=None):
        addurlform = AddUrlForm(request.GET or None)
        return render(request, self.template_name, {'form': addurlform})
class Url(View):
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    template_name = 'mint_url.html'

    def get(self, request, doi, err=None):
        mds_api = MdsApi(request)
        if doi.startswith(DOI_PREFIX + "/"):
            suffix = doi.removeprefix(DOI_PREFIX + "/")
            if not helper.is_authorized(request, suffix):
                err = "The doi suffix is not accepted"
        else:
            err = "The doi prefix is not accepted"
        if not err: 
            try:
                r = mds_api.get('/doi/' + doi)
                r.raise_for_status()
                url = r.text
            except Exception as newerr:
                print(f'Other error occurred: {newerr}')
                url = None
                urlform = UrlForm(request.GET or None, initial={'url':r.text})
                return render(request, self.template_name, {'form':urlform, 'doi':doi, 'url':url, 'err':newerr})
        r = mds_api.get('/doi/' + doi)
        url = r.text
        urlform = UrlForm(request.GET or None, initial={'url':r.text})
        return render(request, self.template_name, {'form':urlform, 'doi':doi, 'url':url, 'err':err})
        
    def post(self, request, doi):
        mds_api = MdsApi(request) 
        url_form= UrlForm(request.POST or None)
        if url_form.is_valid():
            url = url_form.cleaned_data['url']

        body = 'doi='+doi+'\n'+'url='+url
        try: 
            r = mds_api.put('/doi/' + doi, data=body.encode(), headers={ "Content-Type": "text/plain;charset=UTF-8" })
            r.raise_for_status()
        except Exception as err:
                print(f'Other error occurred: {err}')
                return self.get(request, doi, err)
        return self.get(request, doi, err=None)


def _is_test_url():
    if DATACITE_URL == DATACITE_TEST_URL:
        return True
    return False

   


