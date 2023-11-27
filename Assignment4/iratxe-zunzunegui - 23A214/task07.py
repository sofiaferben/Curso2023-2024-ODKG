# -*- coding: utf-8 -*-
"""Task07.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1MeKeX_vxdfCNRKdJGRxtiSqcT3gi2MaU

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
ns = Namespace("http://somewhere#")

##RDFlib
print("RDFlib result:")

def subclasses_livingthing(g, class_name, list):
    for s, p, o in g.triples((None, RDFS.subClassOf, class_name)):
        list.append(s)
        list = subclasses_livingthing(g, s, list)
    return list

list_q1 = []
list_q1 = subclasses_livingthing(g, ns.LivingThing, list_q1)
for element in list_q1:
  print(element)

##SPARQL
from rdflib.plugins.sparql import prepareQuery

q1 = prepareQuery('''
  SELECT DISTINCT ?s
  WHERE {
    ?s rdfs:subClassOf+ ns:LivingThing.
  }
  ''',
  initNs = { "rdfs": RDFS, "ns":ns}
)
# Visualize the results
print("SPARQL result:")
for r in g.query(q1):
  print(r.s)

"""**TASK 7.2: List all individuals of "Person" with RDFLib and SPARQL (remember the subClasses)**

"""

# TO DO

##RDFlib
print("RDFlib result:")

def subclasses_person(g, class_name, list):
    for s, p, o in g.triples((None, RDF.type, class_name)):
        list.append(s)
    for s, p, o in g.triples((None, RDFS.subClassOf, class_name)):
        list = subclasses_person(g, s, list)
    return list

list_q2 = []
list_q2 = subclasses_person(g, ns.Person, list_q2)
for element in list_q2:
    print(element)

##SPARQL
print("SPARQL result:")
q2 = prepareQuery('''
  SELECT ?s
  WHERE {
    {?s rdf:type ns:Person.} UNION{
    ?class rdfs:subclassOf* ns:Person.
    ?s rdf:type ?class.}
  }
  ''',
  initNs = { "rdf": RDF, "ns":ns, "rdfs":RDFS}
)
# Visualize the results
for r in g.query(q2):
  print(r.s)

"""**TASK 7.3: List all individuals of "Person" or "Animal" and all their properties including their class with RDFLib and SPARQL. You do not need to list the individuals of the subclasses of person**

"""

# TO DO

##RDFlib
print("RDFlib result:")
for s, p, o in g.triples((None, RDF.type, ns.Person)):
    for s1, p1, o1 in g.triples((s, None, None)):
      print(p1, o1)

for s, p, o in g.triples((None, RDF.type, ns.Animal)):
    for s1, p1, o1 in g.triples((s, None, None)):
      print(p1, o1)

##SPARQL
print("SPARQL result:")
q3 = prepareQuery('''
  SELECT ?p ?o
  WHERE {
    {?s rdf:type ns:Person.
    ?s ?p ?o.} UNION{
    ?s  rdf:type ns:Animal.
    ?s ?p ?o.}
  }
  ''',
  initNs = { "rdf": RDF, "ns":ns}
)

# Visualize the results
for r in g.query(q3):
  print(r.p, r.o)

"""**TASK 7.4:  List the name of the persons who know Rocky**"""

# TO DO

##RDFlib

VCARD = Namespace("http://www.w3.org/2001/vcard-rdf/3.0/")
FOAF = Namespace("http://xmlns.com/foaf/0.1/")
from rdflib import XSD

print("RDFLib result:")
for s, p, o in g.triples((None, RDF.type, ns.Person)):
    for s1, p1, o1 in g.triples((s, FOAF.knows, ns.RockySmith)):
      for s2, p2, o2 in g.triples((s1, VCARD.Given, None)):
        print(o2)

##SPARQL
print("SPARQL result:")

q4 = prepareQuery('''
  SELECT ?Given WHERE {
    ?s rdf:type ns:Person.
    ?s foaf:knows ?Rocky .
    ?Rocky vcard:FN ?RockyFullName.
    ?s vcard:Given ?Given.
  }
  ''',
  initNs={"foaf": FOAF, "vcard": VCARD,"ns": ns, "rdf": RDF, "xsd":XSD}
)

# Visualize the results

for r in g.query(q4, initBindings = {'?RockyFullName' : Literal('Rocky Smith', datatype=XSD.string)}):
  print(r.Given)

"""**Task 7.5: List the entities who know at least two other entities in the graph**"""

# TO DO

##RDFlib
print("RDFlib result:")
entity_counts = {}
for s, p, o in g.triples((None, FOAF.knows, None)):
  if s != o:
    if s in entity_counts:
      entity_counts[s] += 1
    else:
      entity_counts[s] = 1 #add the entity to the dictionary

# Visualize the results
for i in range(0,len(entity_counts)):
  entity=list(entity_counts.keys())[i]
  count=list(entity_counts.values())[i]
  if count >= 2:
    print(entity)

##SPARQL
print("SPARQL result:")
q5 = prepareQuery('''
 SELECT ?entity
 WHERE {
  ?entity foaf:knows ?knownEntity.
 }
 GROUP BY ?entity
 HAVING (count(?knownEntity) >= 2)
  ''',
  initNs = { "foaf": FOAF}
)

# Visualize the results

for r in g.query(q5):
  print(r.entity)

