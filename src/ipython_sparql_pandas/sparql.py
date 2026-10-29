# -*- coding: utf-8 -*-

from IPython.core.magic import register_cell_magic, needs_local_scope
from IPython.core.magic_arguments import argument, magic_arguments, parse_argstring
from SPARQLWrapper import SPARQLWrapper, JSON
from IPython.core.display import display_javascript, Javascript
from rdflib import URIRef, Literal
import pandas as pd


@register_cell_magic
@needs_local_scope
@magic_arguments()
@argument("endpoint", help="SPARQL endpoint or RDFlib variable")
@argument("--save", "-s", help="Save result into variable")
@argument("--quiet", "-q", action="store_true", help="Don't output anything")
@argument("--params", "-p", help="Use parameter dict in percentage-formatted variables")
def sparql(line, cell, local_ns=None):
    args = parse_argstring(sparql, line)
    if args.params:
        cell = cell % local_ns[args.params]

    sparql_endpoint = args.endpoint

    if args.endpoint in local_ns:
        g = local_ns[args.endpoint]
        results = g.query(cell)
        if results.bindings:
            df = pd.DataFrame(results.bindings)
            df = df[df.columns[::-1]]
            df.columns = [str(c) for c in df.columns]
        elif None != results.askAnswer:
            df = pd.DataFrame([[results.askAnswer]], columns="ASK")
        else:
            df = results.graph
    else:
        client = SPARQLWrapper(sparql_endpoint)
        client.setReturnFormat(JSON)

        client.setQuery(cell)
        results = client.query().convert()
        df = df_results(results)

    if args.save:
        local_ns[args.save] = df

    if not args.quiet:
        return df


def convert_node(obj):
    if obj["type"] == "uri":
        return URIRef(obj["value"])
    if obj["type"] == "typed-literal" or "literal":
        if "datatype" in obj:
            dt = URIRef(obj["datatype"])
            return Literal(obj["value"], datatype=dt)
        elif "xsd:lang" in obj:
            lang = obj["xsd:lang"]
            return Literal(obj["value"], lang=lang)
        else:
            return Literal(obj["value"])

    raise Exception(f'Invalid RDF node type {obj["type"]}')


def df_results(result):

    if "boolean" in result:
        df = pd.DataFrame([[result["boolean"]]], columns="ASK")
    else:
        df = pd.DataFrame(result["results"]["bindings"])
        df.applymap(convert_node)

    return df


def load_ipython_extension(ipython):
    pass
