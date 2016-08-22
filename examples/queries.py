from graphdb.redis.query import GraphQueryRedis

q1 = GraphQueryRedis()
q2 = GraphQueryRedis()

# Chained queries: You can chain the queries. NOTE: fetch returns the final
# set, and can not be used further for chaining.
print('\n... CHAINED: Companies founded by sachinb')
print(q1.clear().add_values('sachinb').get_attr('found company').fetch())

# Copmanies founded by alumni of IITG
print('\n...Companies founded by alumni of IITG')
q1.clear()
q1.add_values('indian-institute-of-technology-guwahati')
q1.get_attr('alumni')
q1.get_attr('found company')

# But there are different abbreviations for locations and colleges
# iit-guwahati-3 is another. We will deal with such things later, for now:
q2.clear()
q2.add_values('indian-institute-of-technology-guwahati')
q2.get_attr('alumni')
q2.get_attr('found company')
q1.union(q2)
print(q1.fetch())

# INTERSECTIONS
# employees of X who worked at Y
print('\n...Employees of flipkart who worked at amazon')
q1.clear()
q1.add_values('flipkart')
q1.get_attr('current employees')
q2.add_values('amazon')
q2.get_attr('past employees')
q1.intersection(q2)
print(q1.fetch())

# companies founded by ex-employees of Y
print('\n...Companies founded by ex-employees of amazon')
q1.clear()
q1.add_values('amazon')
q1.get_attr('past employees')
q1.get_attr('found company')
print(q1.fetch())


def filter_func(s): return s.get_attr('funding rounds').count() >= 2
# FILTERING RESULTS
# Filtering based on size of results
print('\n... Founded by ex amazons, which have at least 2 funding rounds')
q1.clear()
q1.add_values('amazon')
q1.get_attr('past employees')
q1.get_attr('found company')
q1.filter_by_func(filter_func)
print(q1.fetch())

# Filter based on values in attributes.
# NOTE: Redis returns binary strings, so be sure to use b'string' for comparing
print('\n... Past employees of amazon skilled at "angular-js"')
q1.clear().add_values('amazon').get_attr('past employees')
q1.filter_by_func(lambda s: b'angular-js' in s.get_attr('skills').fetch())
print(q1.fetch())

# SCAN QUERIES
# We keep an index of each entity in the database, making such `scan` type
# queries easier.
# Filter first, then make some more queries. WARNING: LARGE QUERY!
print('\n... Number of companies by first time founders (LARGE QUERY)')
q1.at_uids('person')
q1.filter_by_func(lambda s: s.get_attr('found company').count() == 1)
q1.get_attr('found company')
print(q1.count())


def num_companies(uid):
    s = GraphQueryRedis(uid)
    s.get_attr('alumni').get_attr('found company')
    return s.count()
# COUNT QUERIES - DIY!
print('\n... Number of companies by college (Top 20) (LARGE QUERY)')
num_company_by_college = []
q1.at_uids('college')
num_company_by_college = [(key, count)
                          for key, count in ((key, num_companies(key))
                                             for key in q1.fetch())
                          if count > 0]
num_company_by_college.sort(key=lambda x: x[1], reverse=True)
print(num_company_by_college[:20])

# TODO
# startups with founders from the same college
