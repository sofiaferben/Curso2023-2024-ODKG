# -*- coding: utf-8 -*-
"""Task09.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1csdjfwzOoJiOTwg3OhD3JXieW8AFsrrJ

**Task 09: Data linking**
"""

!pip install rdflib
github_storage = "https://raw.githubusercontent.com/FacultadInformatica-LinkedData/Curso2021-2022/master/Assignment4/course_materials/"

from rdflib import Graph, URIRef
from pprint import pprint
g1 = Graph()
g2 = Graph()
g3 = Graph()
g1.parse(github_storage+"rdf/data03.rdf", format="xml")
g2.parse(github_storage+"rdf/data04.rdf", format="xml")

"""Busca individuos en los dos grafos y enlázalos mediante la propiedad OWL:sameAs, inserta estas coincidencias en g3. Consideramos dos individuos iguales si tienen el mismo apodo y nombre de familia. Ten en cuenta que las URI no tienen por qué ser iguales para un mismo individuo en los dos grafos.

Find individuals in the two graphs and link them using the OWL:sameAs property, inserting these matches into g3. We consider two individuals equal if they have the same nickname and family name. Keep in mind that URIs do not have to be the same for the same individual in both graphs.
"""

# The solution to this task is assuming that we should filter by the properties "given" and "family" of the ontology
# As "Full Name" is not mentioned


# Create a dictionary to store persons and their IDs
persons_dict = {}

# Iterate over the graphs to fill the dictionary
for g, db_num in ((g1, "three"), (g2, "four")):

  # Find all elements from class Person
  persons_query = f"""SELECT DISTINCT ?x
  WHERE {{
    ?x <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://data.{db_num}.org#Person> .
    ?x ?y ?z .
    FILTER (?y != <http://www.w3.org/1999/02/22-rdf-syntax-ns#type>)
  }}"""

  # Once we have the elements, we can find their given and family names
  for r in g.query(persons_query):
    given_name_query = f"""SELECT DISTINCT ?given
      WHERE {{
        ?x <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://data.{db_num}.org#Person> .
        ?x ?y ?given .
        FILTER (?y != <http://www.w3.org/1999/02/22-rdf-syntax-ns#type>)
        FILTER (?x = <{r[0]}>) .
        FILTER (?y = <http://www.w3.org/2001/vcard-rdf/3.0#Given>) .
      }}"""

    family_name_query = f"""SELECT DISTINCT ?family
      WHERE {{
        ?x <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://data.{db_num}.org#Person> .
        ?x ?y ?family .
        FILTER (?y != <http://www.w3.org/1999/02/22-rdf-syntax-ns#type>)
        FILTER (?x = <{r[0]}>) .
        FILTER (?y = <http://www.w3.org/2001/vcard-rdf/3.0#Family>) .
      }}"""

    # Fill the dict by using the Given + Family names as key/id and the URI as value
    for given, family in zip(g.query(given_name_query), g.query(family_name_query)):
      ID = f"{given[0]} {family[0]}"
      if ID not in persons_dict.keys():
        persons_dict[ID] = []
      persons_dict[ID].append(r[0])

pprint(persons_dict)

# Add the matches to the graph g3
for ID, URIs in persons_dict.items():
  print(f"ID: {ID}")
  for URI in URIs:
    print(f"  URI: {URI}")

  if len(URIs) < 2:
    print("  This person is not in both databases")
    print("Skipping")
  else:
    owl_sameAs = URIRef("http://www.w3.org/2002/07/owl#sameAs")
    g3.add((URIs[0], owl_sameAs, URIs[1]))
    print(f"Added {URIs[0]} owl:sameAs {URIs[1]} to g3")

  print()

print("The matched persons are:")
for s, p, o in g3:
  print(s,p,o)