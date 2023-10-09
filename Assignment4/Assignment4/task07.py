# -*- coding: utf-8 -*-
"""Task07.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Hk_jENDVvQOpQgHS4TcBxjnFpUQ2lhUI

**Task 07: Querying RDF(s)**
"""

!pip install rdflib
github_storage = "https://raw.githubusercontent.com/FacultadInformatica-LinkedData/Curso2023-2024/master/Assignment4/course_materials"

"""First let's read the RDF file"""

from rdflib import Graph, Namespace, Literal
from rdflib.namespace import RDF, RDFS
g = Graph()
g.namespace_manager.bind('ns', Namespace("http://somewhere#"), override=False)
g.namespace_manager.bind('vcard', Namespace("http://www.w3.org/2001/vcard-rdf/3.0#"), override=False)
g.parse(github_storage+"/rdf/example6.rdf", format="xml")

"""**TASK 7.1: List all subclasses of "LivingThing" with RDFLib and SPARQL**"""

# TO DO
from rdflib.plugins.sparql import prepareQuery

q1 = prepareQuery('''
  SELECT ?Subject WHERE {
    ?Subject RDFS:subClassOf ?LivingThing.
  }
  ''',
  initNs = { "RDFS": RDFS}
)

# Visualize the results
for r in g.query(q1):
  print(r.Subject)

"""**TASK 7.2: List all individuals of "Person" with RDFLib and SPARQL (remember the subClasses)**

"""

# TO DO
from rdflib.plugins.sparql import prepareQuery
ns = Namespace("http://somewhere#")

q2 = prepareQuery('''
   SELECT  ?Subject ?Individual  WHERE {
    ?Subject RDFS:subClassOf* ns:Person.
  ?Individual RDF:type ?Subject.
  }
  ''',
  initNs = { "RDFS": RDFS,
            "RDF": RDF,
             "ns":ns}
)
#Visualize the results

for r in g.query(q2):
  print(r.Individual)

"""**TASK 7.3: List all individuals of "Person" or "Animal" and all their properties including their class with RDFLib and SPARQL. You do not need to list the individuals of the subclasses of person**

"""

# TO DO
q3 = prepareQuery('''
  SELECT  ?Individual ?Property WHERE {
    ?Individual ?Property ?value
    {
    ?Subject RDFS:subClassOf ns:Person.
  ?Individual RDF:type ?Subject.
  }  UNION
  {
    ?Subject RDFS:subClassOf* ns:Animal.
  ?Individual RDF:type ?Subject.
  }}
  ''',
  initNs = { "RDFS": RDFS,
            "RDF": RDF,
             "ns":ns}
)

#Visualize the results
for r in g.query(q3):
  print(r.Individual, r.Property)

"""**TASK 7.4:  List the name of the persons who know Rocky**"""

# TO DO
from rdflib.plugins.sparql import prepareQuery

FOAF = Namespace("http://xmlns.com/foaf/0.1/")
vcard = Namespace("http://www.w3.org/2001/vcard-rdf/3.0/")

q4 = prepareQuery('''
  SELECT ?Subject ?Name WHERE {
    ?Subject FOAF:knows ?RockySmith.
    ?Subject vcard:Given ?Name.
  }
  ''',
  initNs = { "FOAF": FOAF, "vcard": vcard}
)
#Visualize the results
for r in g.query(q4):
  print(r.Name)

"""**Task 7.5: List the entities who know at least two other entities in the graph**"""

for s, p, o in g:
  print(s,p,o)

# TO DO
from rdflib.plugins.sparql import prepareQuery

FOAF = Namespace("http://xmlns.com/foaf/0.1/")
ns = Namespace("http://somewhere#")

q5 = prepareQuery('''
   SELECT ?Subject (COUNT(?known) AS ?count)
  WHERE {
  ?Subject foaf:knows ?known.
  }
  GROUP BY ?Subject
  HAVING (COUNT(?known) >= 2)
  ''',
  initNs = {"foaf":FOAF}
)

#Visualize the results
for r in g.query(q5):
  print(r.Subject)