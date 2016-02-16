from __future__ import division, print_function

from django.shortcuts import render
from django.views import generic

import forms
import models

try:
    DEFAULT_DOCUMENTS_TO_SHOW = models.Setting.objects.get(pk='DEFAULT_DOCUMENTS_TO_SHOW').value
    DEFAULT_NODES_TO_SHOW = models.Setting.objects.get(pk='DEFAULT_NODES_TO_SHOW').value
except:
    pass


class IndexView(generic.View):

    def get(self, request):
        return render(request, 'hypothesize_app/index.html')


class DocumentSearchView(generic.ListView):

    template_name = 'hypothesize_app/document_search.html'
    context_object_name = 'documents'

    def get_context_data(self, **kwargs):
        """We'll use this to bulk up later maybe."""
        context = super(DocumentSearchView, self).get_context_data(**kwargs)
        return context

    def get_queryset(self):
        return models.Document.objects.order_by('-last_viewed')


class DocumentDetailView(generic.DetailView):
    """
    Automatically look for template "document_detail.html".
    To change this, change the template_name class variable.
    """
    model = models.Document


def document_change(request, document_id):
    pass


def document_add(request):
    pass


class NodeSearchView(generic.ListView):

    template_name = 'hypothesize_app/node_search.html'
    context_object_name = 'nodes'

    def get_context_data(self, **kwargs):
        """We'll use this to bulk up later maybe."""
        context = super(NodeSearchView, self).get_context_data(**kwargs)
        return context

    def get_queryset(self):
        return models.Node.objects.order_by('-last_viewed')


class NodeDetailView(generic.DetailView):
    """
    Automatically look for template "node_detail.html".
    To change this, change the template_name class variable.
    """
    model = models.Node


class NodeChangeView(generic.UpdateView):

    template_name_suffix = '_change'
    form_class = forms.NodeForm

    def get_object(self):
        return models.Node.objects.get(pk=self.kwargs['pk'])


def node_add(request):
    pass