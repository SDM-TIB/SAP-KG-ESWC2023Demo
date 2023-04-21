import json
import operator
import itertools
import pandas as pd
from SPARQLWrapper import SPARQLWrapper, JSON
import time

KGDBpedia = 'https://dbpedia.org/sparql'
KGWikidata = 'https://query.wikidata.org/sparql'


def current_milli_time():
    return round(time.time() * 1000)


#Cardinality based on triple Wikidata
def query_generationWikidata(non_onco_drugs, endpoint):
    query_select_clause = "SELECT (COUNT(?p) as ?count)"
    query_where_clause = """WHERE { ?s ?p ?o. """


    query_where_clause = query_where_clause + """FILTER (?p IN( """ + non_onco_drugs + ")) ."""

    query_where_clause = query_where_clause[:-1] + "}"
    sparqlQuery = query_select_clause + " " + query_where_clause
    print(sparqlQuery)

    sparql = SPARQLWrapper(endpoint)
    sparql.setQuery(sparqlQuery)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    data = results["results"]["bindings"]
    print(int(data[0]["count"]["value"]))
    

    return int(data[0]["count"]["value"])


#Cardinality based on triple Wikidata
def query_generationWikidata2(onco_drugs, endpoint):
    query_select_clause = "SELECT (COUNT(?p) as ?count)"
    query_where_clause = """WHERE { ?s ?p ?o. """

    query_where_clause = query_where_clause + """FILTER (?p IN( """ + onco_drugs + ")) ."""

    query_where_clause = query_where_clause[:-1] + "}"
    sparqlQuery = query_select_clause + " " + query_where_clause
    print(sparqlQuery)

    sparql = SPARQLWrapper(endpoint)
    sparql.setQuery(sparqlQuery)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    data = results["results"]["bindings"]
    print(int(data[0]["count"]["value"]))
    

    return int(data[0]["count"]["value"])




def computeMetricOverlap(onco_drugs, non_onco_drugs, endpoint):
    #input_cui = onco_drugs + non_onco_drugs
    random_id = str(current_milli_time())
    # with open(input_file, "r") as input_file_descriptor:
        # input_data = json.load(input_file_descriptor)
    countWikidata = query_generationWikidata(onco_drugs, endpoint)
    countWikidata2 = query_generationWikidata2(non_onco_drugs, endpoint)    
    metric = round(float(min(countWikidata2, countWikidata) / max(countWikidata2, countWikidata)) * 100, 2)
    print("Percentage of Total Overlap-Synonym:", metric)
    return metric

def load_data(file):
    onco_drugs = file["Input"]["IndependentVariables"]["WikidataPredicate2"]
    non_onco_drugs = file["Input"]["IndependentVariables"]["WikidataPredicate"]

    return computeMetricOverlap(onco_drugs, non_onco_drugs, 'https://query.wikidata.org/sparql')

# if __name__ == '__main__':
#     res = computeMetricOverlap("inputfilePredicateIntra.json")