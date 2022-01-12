from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic import View
from .forms import SubjectFormset, CreatorFormset, DoiForm
from django.shortcuts import render, redirect


from doi_site.settings import DATACITE_TEST_URL, DATACITE_URL


class Mint(View):
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    # pylint: disable=no-self-use
    def get(self, request):
        template_name = 'create_normal.html'
        heading_message = 'Formset Demo'
        form = DoiForm(request.GET or None)
        formset1 = SubjectFormset(request.GET or None, prefix='form1')
        formset2 = CreatorFormset(request.GET or None, prefix='form2')
        return render(request, template_name, {
        'form': form,
        'formset1': formset1,
        'formset2': formset2,
        'heading': heading_message,
    })

    def post(self, request):
        formset1 = SubjectFormset(request.POST, prefix='form1')
        formset2 = CreatorFormset(request.POST, prefix='form2')
        template_name = 'create_normal.html'
        heading_message = 'Formset Demo'
        if formset1.is_valid() and formset2.is_valid():
            for form in formset1:
                # extract name from each form and save
                name = form.cleaned_data.get('name')
                print(name)
            for form in formset2:
                # extract name from each form and save
                creator = form.cleaned_data.get('creator')
                print(creator)
        return render(request, template_name, {
        'formset1': formset1,
        'formset2': formset2,
        'heading': heading_message,
    })
def _is_test_url():
    if DATACITE_URL == DATACITE_TEST_URL:
        return True
    return False

   


