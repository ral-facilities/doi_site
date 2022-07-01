from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic import View
from .forms import SubjectFormset, RelatedIdentifierFormset, CreatorFormset, FunderFormset, DateFormset, DoiForm, AddUrlForm, UrlForm
from django.shortcuts import render, redirect
from .dict_to_xml import dict_to_xml
from mds.mds_api import MdsApi
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
        doiform = DoiForm(request.GET or None, domains=suffixlist) 
        subjectformset = SubjectFormset(request.GET or None, prefix='subjectform')
        dateformset = DateFormset(request.GET or None, prefix='dateform')
        relatedidentifierformset = RelatedIdentifierFormset(request.GET or None, prefix='relatedidentifierform')
        creatorformset = CreatorFormset(request.GET or None, prefix='creatorform')
        funderformset = FunderFormset(request.GET or None, prefix='funderform')
        for form in creatorformset:
            form.use_required_attribute = True
        return render(request, template_name, {
        'form': doiform,
        'subjectformset': subjectformset,
        'relatedidentifierformset': relatedidentifierformset,
        'creatorformset': creatorformset,
        'dateformset': dateformset,
        'funderformset' : funderformset,
        'doi_prefix': DOI_PREFIX,
        'suffixlist': suffixlist,
        'heading': heading_message,
        'is_testing' : _is_test_url()
    })

    def post(self, request):
        subjectformset = SubjectFormset(request.POST or None, prefix='subjectform')
        relatedidentifierformset = RelatedIdentifierFormset(request.POST or None, prefix='relatedidentifierform')
        creatorformset = CreatorFormset(request.POST or None, prefix='creatorform')
        dateformset = DateFormset(request.POST or None, prefix='dateform')
        funderformset = FunderFormset(request.POST or None, prefix='funderform')
        authorized_dois = []
        notAuthorised = False
        groups = request.user.groups.iterator()
        for group in groups:
            try:
                authorized_dois.append(group.groupprofile.doi_suffix)
            except ObjectDoesNotExist:
                pass
        suffixlist = authorized_dois
        doiform = DoiForm(request.POST or None, domains=suffixlist, request=request)
        for form in creatorformset:
            form.use_required_attribute = True
        for form in funderformset:
            form.use_required_attribute = True
        template_name = 'create_normal.html'
        heading_message = 'Formset Demo'
       
        if subjectformset.is_valid() and relatedidentifierformset.is_valid() and creatorformset.is_valid() and funderformset.is_valid() and dateformset.is_valid() and doiform.is_valid():
            mds_api = MdsApi(request) 
            metadata = doiform.cleaned_data
            canUseSuffix = helper.is_authorized(request, metadata['identifier'])
            if canUseSuffix:
                pass
            else:
                notAuthorised = True,
                return render(request, template_name, {
                'form': doiform,
                'subjectformset': subjectformset,
                'relatedidentifierformset': relatedidentifierformset,
                'creatorformset': creatorformset,
                'dateformset': dateformset,
                'funderformset' : funderformset,
                'doi_prefix': DOI_PREFIX,
                'heading': heading_message,
                'suffixlist': suffixlist,
                'notAuthorised': notAuthorised,
                'is_testing' : _is_test_url()
                })
            metadata["subjects"] = [x.get("subject") for x in subjectformset.cleaned_data if x.get('subject')]
            metadata["related_identifiers"] = [x for x in relatedidentifierformset.cleaned_data if x]
            metadata["creators"] = [x for x in creatorformset.cleaned_data if x]
            metadata["dates"] = [x for x in dateformset.cleaned_data if x]
            metadata["funders"] = [x for x in funderformset.cleaned_data if x]
            metadata['identifier'] = DOI_PREFIX + '/'+ metadata['identifier']
            doi = metadata['identifier'] 
            e = dict_to_xml(metadata)
            try:
                response = mds_api.put("/metadata/" + doi, e.encode(), headers={ "Content-Type": "application/xml;charset=UTF-8" })
                response.raise_for_status()
            except Exception as err:
                return render(request, template_name, {
                    'form': doiform,
                    'subjectformset': subjectformset,
                    'relatedidentifierformset': relatedidentifierformset,
                    'creatorformset': creatorformset,
                    'dateformset': dateformset,
                    'funderformset' : funderformset,
                    'doi_prefix': DOI_PREFIX,
                    'heading': heading_message,
                    'suffixlist': suffixlist,
                    'err': err,
                    'notAuthorised': notAuthorised,
                    'is_testing' : _is_test_url()
                    })
            else:
                pass 
        else:
            return render(request, template_name, {
            'form': doiform,
            'subjectformset': subjectformset,
            'relatedidentifierformset': relatedidentifierformset,
            'creatorformset': creatorformset,
            'dateformset': dateformset,
            'funderformset' : funderformset,
            'doi_prefix': DOI_PREFIX,
            'suffixlist': suffixlist,
            'heading': heading_message,
            'is_testing' : _is_test_url()
        })
        if(response.status_code == 201):
            return redirect('minturl', doi) 
        else:
            return render(request, template_name, {
            'form': doiform,
            'subjectformset': subjectformset,
            'relatedidentifierformset': relatedidentifierformset,
            'creatorformset': creatorformset,
            'dateformset': dateformset,
            'funderformset' : funderformset,
            'suffixlist': suffixlist,
            'doi_prefix': DOI_PREFIX,
            'heading': heading_message,
            'is_testing' : _is_test_url()
        })


class AddUrl(View):
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    template_name = 'add_url.html'

    def get(self, request, err=None):
        addurlform = AddUrlForm(request.GET or None, initial={'add_url':DOI_PREFIX+'/'})
        return render(request, self.template_name, {'form': addurlform, 'is_testing' : _is_test_url()})

    def post(self, request, err=None):
        addurlform = AddUrlForm(request.POST or None)
        if addurlform.is_valid():
            url_dict = addurlform.cleaned_data
            mds_api = MdsApi(request)
            if url_dict['add_url'].startswith(DOI_PREFIX + "/"):
                suffix = url_dict['add_url'][len(DOI_PREFIX + "/"):]
                if not helper.is_authorized(request, suffix):
                    err = "You have no authorization for the current subdomain: " + suffix
                    addurlform = AddUrlForm(request.POST or None)
                    return render(request, self.template_name, {'form':addurlform, 'doi':url_dict['add_url'], 'err':err, 'is_testing' : _is_test_url()})
            else:
                err = "The doi prefix is not accepted"
                addurlform = AddUrlForm(request.POST or None)
                return render(request, self.template_name, {'form':addurlform, 'doi':url_dict['add_url'], 'err':err, 'is_testing' : _is_test_url()})
            if not err: 
                try:
                    r = mds_api.get('/doi/' + url_dict['add_url'])
                    r.raise_for_status()
                    url = r.text
                    path = 'mint/' + url_dict['add_url']
                    return redirect(path)
                except Exception as newerr:
                    addurlform = AddUrlForm(request.POST or None)
                    return render(request, self.template_name, {'form':addurlform, 'doi':url_dict['add_url'], 'newerr':newerr, 'is_testing' : _is_test_url()})
            else:
                addurlform = AddUrlForm(request.POST or None)
                return render(request, self.template_name, {'form':addurlform, 'doi':url_dict['add_url'], 'err':err, 'is_testing' : _is_test_url()})
        else:
          return render(request, self.template_name, {'form': addurlform, 'is_testing' : _is_test_url()}) 
 
class Url(View):
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    template_name = 'mint_url.html'

    def get(self, request, doi, err=None):
        mds_api = MdsApi(request)
        if doi.startswith(DOI_PREFIX + "/"):
            suffix = doi[len(DOI_PREFIX + "/"):]
            if not helper.is_authorized(request, suffix):
                err = "You have no authorization for the current subdomain: " + suffix
        else:
            err = "The doi prefix is not accepted"
        if not err: 
            try:
                r = mds_api.get('/doi/' + doi)
                r.raise_for_status()
                url = r.text
            except Exception as newerr:
                url = None
                urlform = UrlForm(request.GET or None, initial={'url':r.text})
                return render(request, self.template_name, {'form':urlform, 'doi':doi, 'url':url, 'err':newerr, 'is_testing' : _is_test_url()})
        r = mds_api.get('/doi/' + doi)
        url = r.text
        urlform = UrlForm(request.GET or None, initial={'url':r.text})
        return render(request, self.template_name, {'form':urlform, 'doi':doi, 'url':url, 'err':err, 'is_testing' : _is_test_url()})
        
    def post(self, request, doi):
        template_name = 'mint_url.html'
        mds_api = MdsApi(request) 
        url_form= UrlForm(request.POST or None)
        if url_form.is_valid():
            url = url_form.cleaned_data['url']
            body = 'doi='+doi+'\n'+'url='+url
            try: 
                r = mds_api.put('/doi/' + doi, data=body.encode(), headers={ "Content-Type": "text/plain;charset=UTF-8" })
                r.raise_for_status()
                return self.get(request, doi, err=None)
            except Exception as err:
                return self.get(request, doi, err)
        else:
            r = mds_api.get('/doi/' + doi)
            url = r.text
            return render(request, template_name, {'form':url_form, 'doi':doi, 'url':url, 'is_testing' : _is_test_url()})

def _is_test_url():
    if DATACITE_URL == DATACITE_TEST_URL:
        return True
    return False

   


