from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic import View
from .forms import SubjectFormset, CreatorFormset, DoiForm
from django.shortcuts import render, redirect
import xml.etree.ElementTree as ET

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
            
            def dict_to_xml(d):
                xml_resource = ET.Element('resource')

                xml_identifier = ET.SubElement(xml_resource, 'identifier')
                xml_identifier.text = d['identifier']
                xml_identifier.attrib['identifierType'] = 'DOI'

                xml_titles = ET.SubElement(xml_resource, 'titles')
                xml_title = ET.SubElement(xml_titles, 'title')
                xml_title.text = d['title']

                xml_publisher = ET.SubElement(xml_resource, 'publisher')
                xml_publisher.text = d['publisher']

                xml_publication_year = ET.SubElement(xml_resource, 'publicationYear')
                xml_publication_year.text = d['publication_year']

                xml_resource_type = ET.SubElement(xml_resource, 'resourceType')
                xml_resource_type.text = d['resource_type']

                xml_subjects = ET.SubElement(xml_resource, 'subjects')
                for subject in d['subjects']:
                    xml_subject = ET.SubElement(xml_subjects, 'subject')
                    xml_subject.text = subject

                xml_creators = ET.SubElement(xml_resource, 'creators')
                for creator in d['creators']:
                    xml_creator = ET.SubElement(xml_creators, 'creator')
                    xml_creator_name = ET.SubElement(xml_creator, 'creatorName')
                    xml_creator_name.text = creator['familyname'] + ', ' + creator['givenname']
                    xml_creator_name.attrib['nameType'] = 'Personal'
                    xml_creator_given_name = ET.SubElement(xml_creator, 'givenName')
                    xml_creator_given_name.text = creator['givenname']
                    xml_creator_family_name = ET.SubElement(xml_creator, 'familyName')
                    xml_creator_family_name.text = creator['familyname']
                    xml_creator_affiliation = ET.SubElement(xml_creator, 'affiliation')
                    xml_creator_affiliation.text = creator['affiliation']

                return ET.tostring(xml_resource)

            e = dict_to_xml(metadata)
            print (e)

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

   


