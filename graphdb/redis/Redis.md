# Use case
No bulk loading! No bulk reading!
For very specific use case of getting the data from a scraper, and reading via
queries in a NL like manner.

# No duplicate names allowed!
If two people / colleges / companies have the same name, they are considered to
be the same!

## Internal structure: Redis
We will store all hash maps in a key-value store, utilising the Redis
database.
I need a DB system since I plan to use multiple scrapers and parsers
distributed across machines, but a single database instance.
I don't expect the database to be very big, since I am only looking at
~1500 companies and associated entitites. So using a RAM based model makes
sense to me, for the speed gains.

## Why NoSQL?
A company may have arbitrary number of employees, founders and so on. Similarly
for college alumni, person skills, etc. Such a situtation in SQL tables can get
really unweildy with junction tables, and difficult to query.

## Redis database structure
This is my first time working with Redis, or any NoSql database as such!
The size of my dataset is tiny, and queries might be slightly complex, so having
everything on RAM is really great!

For larger datasets, I might move to MongoDB or other suitable key-value /
document stores.

## Datastructures to use:
overall it will be one large Key-Value store,

`uid -> < hash of attributes >`

The hash of attributes will hash:
`attribute_name -> < set of values of particular type > `

In cases where an ordering is required, we use an `ordered set` instead. An
example of such a situtation is in the attribute `alumni` of `college`, since we
would like the alumni to be sorted by the year of graduation.

`attribute_name -> < set of values of particular type > `

### On back-links
Whenever you add an attribute, the reverse link gets added as well. For
instance, adding the triple:
`x -> alumnus of -> [A, B]`

will automatically add the following:
`x.colleges + -> [A, B]
 A.alumni + -> [x]
 B.alumni + -> [x]
`

To achieve this, you need to define the schema, wherein you define all the
entities, their attributes, and 

### sorted set vs hash by year to set
sorted set with key as year: insertion in O(logN), and extraction by
year in O(1).
hash: key year, to set of people. insertion in O(1) and extraction O(1).

If we only want lists of people by year, hash sounds better.

#### What about range queries?
1995 < year < 2001
Ordered set: O(1) search
Hash: O(keys) scan required over keys, and then merge the resulting sets
O(Nlog(N))

#### Answer
Overall ordered sets make more sense to me.
