# encoding: utf-8

"""
Initializes lxml parser and makes available a handful of functions that wrap
its typical uses.
"""

from __future__ import absolute_import

from lxml import etree, objectify

from pptx.oxml.ns import NamespacePrefixedTag


# oxml-specific constants
XSD_TRUE = '1'


# configure objectified XML parser
_fallback_lookup = objectify.ObjectifyElementClassLookup()
_element_class_lookup = etree.ElementNamespaceClassLookup(_fallback_lookup)
oxml_parser = etree.XMLParser(remove_blank_text=True)
oxml_parser.set_element_class_lookup(_element_class_lookup)


def oxml_fromstring(text):
    """``etree.fromstring()`` replacement that uses oxml parser"""
    return objectify.fromstring(text, oxml_parser)


def oxml_parse(source):
    """``etree.parse()`` replacement that uses oxml parser"""
    return objectify.parse(source, oxml_parser)


def oxml_tostring(elm, encoding=None, pretty_print=False, standalone=None):
    # if xsi parameter is not set to False, PowerPoint won't load without a
    # repair step; deannotate removes some original xsi:type tags in core.xml
    # if this parameter is left out (or set to True)
    objectify.deannotate(elm, xsi=False, cleanup_namespaces=False)
    xml = etree.tostring(
        elm, encoding=encoding, pretty_print=pretty_print,
        standalone=standalone
    )
    return xml


def register_custom_element_class(nsptag_str, cls):
    """
    Register the lxml custom element class *cls* with the parser to be used
    for XML elements with tag matching *nsptag_str*.
    """
    nsptag = NamespacePrefixedTag(nsptag_str)
    namespace = _element_class_lookup.get_namespace(nsptag.nsuri)
    namespace[nsptag.local_part] = cls