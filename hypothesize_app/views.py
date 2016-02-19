from __future__ import division, print_function

from django.core.urlresolvers import reverse_lazy
from django.views import generic

import forms
import models
import node_processing
import search


class Index(generic.TemplateView):

    template_name = 'hypothesize_app/index.html'


class DocumentSearch(generic.ListView):

    template_name = 'hypothesize_app/document_search.html'
    context_object_name = 'documents'

    def get_context_data(self, **kwargs):
        """We'll use this to bulk up later maybe."""
        context = super(DocumentSearch, self).get_context_data(**kwargs)
        context['document_search_form'] = forms.DocumentSearchForm(self.request.GET)
        return context

    def get_queryset(self):
        return search.document_query(self.request.GET.get('query', ''))


class DocumentDetail(generic.DetailView):
    """
    Automatically look for template "document_detail.html".
    To change this, change the template_name class variable.
    """
    model = models.Document


class DocumentChange(generic.UpdateView):
    """
    Update the contents of a document.
    """
    template_name = 'hypothesize_app/document_form.html'
    form_class = forms.DocumentForm

    def get_object(self):
        return models.Document.objects.get(pk=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        # get baseline context variables
        context = super(DocumentChange, self).get_context_data(**kwargs)
        # add in tab complete options
        context['document_pk_list'] = [str(pk) for pk in models.Document.objects.values_list('id', flat=True)]
        return context


class DocumentCreate(generic.CreateView):
    """
    Add a new document.
    """
    template_name = 'hypothesize_app/document_form.html'
    form_class = forms.DocumentForm

    def get_context_data(self, **kwargs):
        # get baseline context variables
        context = super(DocumentCreate, self).get_context_data(**kwargs)
        # add in tab complete options
        context['document_pk_list'] = [str(pk) for pk in models.Document.objects.values_list('id', flat=True)]
        return context


class DocumentDelete(generic.DeleteView):
    """
    Delete a document.
    """

    model = models.Document
    success_url = reverse_lazy('hypothesize_app:document_search')


class NodeSearch(generic.ListView):

    template_name = 'hypothesize_app/node_search.html'
    context_object_name = 'nodes'

    def get_context_data(self, **kwargs):
        """We'll use this to bulk up later maybe."""
        context = super(NodeSearch, self).get_context_data(**kwargs)
        context['node_search_form'] = forms.NodeSearchForm(self.request.GET)
        return context

    def get_queryset(self):
        return search.node_query(self.request.GET.get('query', ''))


class NodeDetail(generic.DetailView):
    """
    Automatically look for template "node_detail.html".
    To change this, change the template_name class variable.
    """
    model = models.Node


class NodeChange(generic.UpdateView):

    template_name = 'hypothesize_app/node_form.html'
    form_class = forms.NodeForm

    def get_object(self):
        return models.Node.objects.get(pk=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        # get baseline context variables
        context = super(NodeChange, self).get_context_data(**kwargs)
        # add in tab complete options
        context['tab_complete_options'] = node_processing.make_tab_complete_options(
            document_model=models.Document, node_model=models.Node,
        )
        return context


class NodeCreate(generic.CreateView):

    template_name = 'hypothesize_app/node_form.html'
    form_class = forms.NodeForm

    def get_context_data(self, **kwargs):
        # get baseline context variables
        context = super(NodeCreate, self).get_context_data(**kwargs)
        # add in tab complete options
        context['tab_complete_options'] = node_processing.make_tab_complete_options(
            document_model=models.Document, node_model=models.Node,
        )
        return context


class NodeDelete(generic.DeleteView):

    model = models.Node
    success_url = reverse_lazy('hypothesize_app:node_search')