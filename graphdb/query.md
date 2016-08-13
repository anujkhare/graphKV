# Query language
## Goals
Examples of queries I want to run:
TODO
- which college has the most startups
- who has the most (listed) startup attempts

TODO
- college-wise startup founders table

TODO
- people who have *common* skills (not exactly same)
- people who are living in the same city
- companies in the same domain

- employees of X who worked at Y
- companies founded by ex-employees of Y
- people who have X,Y,Z skills
- startups founded by alumni of IITG
- startups with n founders
- startups with x rounds of investment
- startups with founders from the same college
- startups with first time founders
- first time founders
- startups with VCs from xyz

## GraphQL
A neat language for querying, but I could not find any obvious way to implement
queries with intersections (assume a valid schema for the queries):

### OK: get companies started by alumni of iit guwahati
```
{
  me(_xid_: college.iit.guwahati) {
    alumni {
      name
      companies_founded
    }
  }
}
```

### FAIL: employees of X who worked at Y
You can get both the lists separately, but how do I write a query to get their
intersection?
```
{
  me(_xid_: company.X) {
    employees({past_employers: {Y}}) {
      name
    }
  }
}
```
We use a context to filter based on attributes of a given node.
This kind of filtering allows us to implement intersection style queries.

### People who worked at X and Y
```
{
  me(_xid_: company.X) {
    past_employees({past_employers: {Y}}) {
      name
    }
  }
}
```

I read [here](http://react-etc.net/entry/graph-query-languages-graphql-opencypher-gremlin-and-sparql)
that graphql is not really meant to be the SQL for graph databases, and so it
probably does not fit this use case.
*Someone help here?*


## Internal query rep
Loosely inspired by Gremlin.
Have a class Query which can execute them.
Each query object will hold a list of uids of a particular type at any given
time.
The results can only be entity lists, and not attributes. For instance, you can
get `list of people who did X`, but Not `name and age of people of who did X`.
We can filter the final result by attributes to achieve such a result, but it
is not possible within the query.
There are certain methods to modify that list:

Query.byId(name, type)
Query.attr(attr)
Query.intersection(*queries)
Query.union(*queries)

## Redis specific
In Redis, the queries do NOT fetch the data to the client, rather they create a
separate storage named `result1` for `query1` and so on.. A call to `fetch` is
required to get the results to the client. This is done so that intermediate
results do not need to be fetched, saving time!
There are some exceptions to this.

Example (follow the list):
### Companies founded by Anuj
```
 -> byId('person:anuj') ---> ['anuj']
 -> attr('companies_founded') ---> ['flipkart', 'amazon']
 -> fetch()
```

### Copmanies founded by alumni of IITG
```
 -> byId('college.iit.guwahati')  ---> ['iit.guwahati']
 -> attr('alumni')                ---> ['anuj', 'abc', 'azb', 'arx']
 -> attr('companies_founded')     ---> ['blah', 'blqq', 'qq']
 -> fetch()
```

## Intersections
### employees of X who worked at Y
```
q1:
 -> byId('company.X')
 -> attr('employees')

q2:
 -> byId('company.Y')
 -> attr('past_employees')

q3:
 -> intersection([q1, q2])
 -> fetch()
```

### companies founded by ex-employees of Y
```
  -> byId('company.Y')
  -> attr('past_employees')
  -> attr('companies_founded')
  -> fetch()
```

## Scan queries
We keep an index of each entity in the database, making such `scan` type
queries easier.
### founders of all startups
```
 -> byId('startups')
 -> attr('founders')
 -> fetch()
```

## Count queries 
TODO
### Number of founders by college
```
 -> byId('college')
 -> attr('alumni')
```

## Filtering based on size of results
### startups with n founders
NOTE: We can query the cardinality of the sets
```
 -> byId('startups')
 -> filter_attr_size('founders', labmda size: size > n)
 -> fetch()
```

### startups with x rounds of investment
```
 -> byId('startups')
 -> filter_attr_size('funding', lambda size: size == x)
 -> fetch()
```

### startups by first time founders
NOTE: if the attribute is not found, the particular result is automatically
excluded. Hence, only people who have founded some company will be selected.
```
 -> byId('people')
 -> filter_attr_size('companies_founded', lambda size: size < 1)
 -> attr('companies_founded')
 -> fetch()
```

TODO
### startups with founders from the same college
```
```
TODO
## General filters on attributes
In this case the results are fetched back to the client. These types of
queries are not very efficient!
### people who have X,Y,Z skills
```

```
