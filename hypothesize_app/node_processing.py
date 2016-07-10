from __future__ import division, print_function, unicode_literals
import os
import re

from django.conf import settings
from django.core.urlresolvers import NoReverseMatch
from django.core.urlresolvers import reverse
import markdown

DOCUMENT_LINK_PATTERN = r'\[\[(.*?)\]\]'
NODE_LINK_PATTERN = r'\(\((.*?)\)\)'
DOCUMENT_LINK_PATTERN_FULL = r'\[\[.*?\]\]'
NODE_LINK_PATTERN_FULL = r'\(\(.*?\)\)'


def make_node_save_directory(path):
    """
    Make a new directory for saving nodes in.
    :param path: path to directory
    """

    if not os.path.exists(path):

        os.makedirs(path)


def update_text_file(node):
    """
    Update the text file corresponding to an updated node.
    :param node: node instance
    """

    node_save_directory = settings.NODE_SAVE_DIRECTORY

    make_node_save_directory(node_save_directory)

    path = os.path.join(node_save_directory, node.id)

    if not os.path.exists(os.path.dirname(path)):

        os.makedirs(os.path.dirname(path))

    with open('{}.md'.format(path), 'w') as f:

        f.write(node.text)

    return True


def extract_linked_objects(text, document_model, node_model):
    """
    Extract all of the linked objects from a node's text.
    :param text: text
    :param document_model: models.Document
    :param node_model: models.Node
    :return: linked documents list, linked nodes list
    """

    # extract documents

    document_links = re.findall(DOCUMENT_LINK_PATTERN, text)
    document_ids = [link.split('|')[0].strip() for link in document_links]

    documents = [document_model.objects.filter(id=document_id).first() for document_id in document_ids]
    documents = [document for document in documents if document is not None]

    # extract node links

    node_links = re.findall(NODE_LINK_PATTERN, text)
    node_ids = [link.split('|')[0].strip() for link in node_links]

    nodes = [node_model.objects.filter(id=node_id).first() for node_id in node_ids]
    nodes = [node for node in nodes if node is not None]

    return documents, nodes


def bind_linked_objects(node, document_model, node_model):
    """
    Bind all of the documents and nodes that a node links to itself in the database.

    :param node: node
    :param document_model: models.Document
    :param node_model: models.Node
    """

    documents, nodes = extract_linked_objects(node.text, document_model, node_model)

    node.documents.clear()
    node.documents.add(*documents)

    node.nodes.clear()
    node.nodes.add(*nodes)


def document_link_to_html(match):
    """
    Convert document link pattern to html.
    :param match: regular expression match
    :return: html for link to document
    """

    fragments = match.group()[2:-2].split('|', 1)

    document_id = fragments[0]

    if len(fragments) == 1:

        text_to_display = fragments[0]

    elif len(fragments) == 2:

        text_to_display = fragments[1]

    try:

        url = reverse('hypothesize_app:document_detail', args=(document_id.strip(),))

    except NoReverseMatch:

        url = '#'

    html = '<a href="{}" class="internal-link" data-linkpk="document-{}">{}</a>'.format(
        url, document_id, text_to_display)

    return html


def node_link_to_html(match):
    """
    Convert node link pattern to html.
    :param match: regular expression match
    :return:
    """

    fragments = match.group()[2:-2].split('|', 1)

    node_id = fragments[0]

    if len(fragments) == 1:

        text_to_display = fragments[0]

    elif len(fragments) == 2:

        text_to_display = fragments[1]

    try:

        url = reverse('hypothesize_app:node_detail', args=(node_id.strip(),))

    except NoReverseMatch:

        url = '#'

    html = '<a href="{}" class="internal-link" data-linkpk="node-{}">{}</a>'.format(
        url, node_id, text_to_display)

    return html


def text_to_md(text):
    """
    Convert node text to markdown, parsing all of the links.
    :param text: node text
    :return node markdown
    """

    # replace document links and node links in text with markdown

    temp = re.compile(DOCUMENT_LINK_PATTERN_FULL).sub(document_link_to_html, text)

    md = re.compile(NODE_LINK_PATTERN_FULL).sub(node_link_to_html, temp)

    return md


def text_to_html(text):
    """Convert node text to html."""

    # convert internal links to html

    md = text_to_md(text)
    html = markdown.markdown(md)

    return html


def make_tab_complete_options(document_model, node_model):
    """
    Generate a list of things that can be tab completed.
    :param document_model: models.Document,
    :param node_model: models.Node
    :return list of strings for tab completion
    """

    document_strings = [str(doc_id) for doc_id in document_model.objects.values_list('id', flat=True)]
    node_strings = [str(node_id) for node_id in node_model.objects.values_list('id', flat=True)]

    return document_strings + node_strings