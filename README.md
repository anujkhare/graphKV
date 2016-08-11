We follow the broad database model of DGraph, but in a simplified
manner, and implemented from scratch in Python, with very little robustness
and flexibility.

Because we don't need to run very complex queries, I would like to build a
simple parser and engine to execute the queries.

We will work off a schema which defines all the entities and their attributes.
This rigidity in the allowed data format will allow us to do semantic text
completion and construct queries easily.

# Design
## Why reinvent the wheel? What is the objective?
Just for fun, and as an excercise!
There are some good options, like Neo4j, DGraph, etc. that are available, but I
am not familiar with them. This project is only for fun and to learn python.
This is not meant to be robust, or even reusable at the moment. Although
I it seems easy to just reuse this for a different dataset, it is not the
objective.
I also wanted to see how minimally and efficiently I can achieve the kind
of queries I want to process..
The idea is to write quick code that works well for this specific case, and not
a general or (largely) scalable implementation.

# 
## UID list
Every single value, be it a literal value or an entity must be hashed
to an unique UID, and the mapping list will be stored in a single map.
Inside the database, only UIDs will be used to represent values, and
hence this mapping is important to store!

Whenever a value is encountered, it is hashed
UIDs follow the basic schema:
`entity-type:name`

For instance:
`company:foo.baz`
`person:bar.sur`

# Schema
In JSON, with the view that it might be useful for the js website as well.

## Entities and attributes
Entities define all the possible `types` of node in our database.
Each `instance` of an `entity` will contain an alphanumeric `val` which will be
converted to the internally used `uid`. The attributes will be defined in a
strongly typed manner between a fixed pair of entities.

We define anything that we would like to run queries from as an entity, and
constant values like date to literals.


This makes this particular application very simple, but is not a scalable
design, as defining such a schema can get very unwieldy for larger databases.

Each attribute can further have data stored (edge values).

Eg:
- `company` and `person` are entities
- the attribute `founded by` will be defined as `company -> person`.

## 
We will (might) scrape using multiple servers, but will use only a single Redis
server instance, on one computer, which will be accessed by all the scrapers.

# Experiments with other OSS

I looked at various OSS solutions *briefly* for different parts required.


## Dgraph
Open source graph database implementation. They do not implement intersection
yet, so ruled out.

## Tinkerpop integration / Gremlin queries
Too much work for this simple application.

## Neo4j et al
I just decided to do this on my own by now!
