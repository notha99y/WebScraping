'''
Pymongo Tutorial

Reference video: https://www.youtube.com/watch?v=GSL8JpyAjsE&list=LLpNVCNE9cYqVrjb2O8bZUGg&index=2&t=0s
'''

from pymongo import MongoClient  # import a MongoClient class

if __name__ == '__main__':
    client = MongoClient()  # because local machine you dont need to supply an ipaddress

    db = client.test_database  # create a database

    people = db.people  # create a collection (like tables in SQL)
    # no schema in mongodb, so you dont need to decide what is the columns

    # creating data
    people.insert({'name': 'Mike', 'food': 'cheese'})
    people.insert({'name': 'John', 'food': 'ham', 'location': 'UK'})
    people.insert({'name': 'Michelle', 'food': 'cheese'})

    # querying data
    print("Insert and Find Test")
    peeps = people.find()
    for person in peeps:
        print(person)

    print("Find with Dic test")
    peeps = people.find({'food': 'cheese'})
    for person in peeps:
        print(person)

    # querying data with regex
    # query people with name Mi or mi
    print("Find with regex test")
    peeps = people.find({'name': {'$regex': '.*[Mm]i.*'}})
    for person in peeps:
        print(person)

    # updating data
    print("Update record test")
    person = people.find_one({'food': 'ham'})
    person['food'] = 'eggs'
    people.save(person)

    for person in people.find({'food': 'eggs'}):
        print(person)

    # clearing out the data
    print("Removing records")
    for person in people.find():
        people.remove(person)

    # dropping database
    print("Dropping database")
    client.drop_database('test_database')
