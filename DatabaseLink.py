import json
import sqlite3

# conn = sqlite3.connect('PhoneNumbers.db')
# cur = conn.cursor()
#
#
# cur.execute("""CREATE TABLE IF NOT EXISTS person(
#             Id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
#             Name TEXT)""")
# conn.commit()
# cur.execute("""CREATE TABLE IF NOT EXISTS numbers(
#             Id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
#             Number INTEGER, holder_id INTEGER)""")
# conn.commit()

##TODO: Check on input if number can be converted to string, Maybe use a list on person to avoid complications


def getIdFromName(name: str):
    conn = sqlite3.connect('PhoneNumbers.db')
    cur = conn.cursor()
    cur.execute(f"SELECT Id, Name FROM person WHERE Name='{name.capitalize()}'")
    conn.commit()
    ans = cur.fetchall()
    conn.close()
    return ans


def getNames():
    conn = sqlite3.connect('PhoneNumbers.db')
    cur = conn.cursor()
    cur.execute("SELECT Name FROM person")
    conn.commit()
    response = cur.fetchall()
    names = []
    for e in response:
        names.append(e[0])
    conn.close()
    return names if names else ["No Persons!"]


def getNumbersList():
    conn = sqlite3.connect('PhoneNumbers.db')
    cur = conn.cursor()
    cur.execute("SELECT Number FROM numbers")
    conn.commit()
    response = cur.fetchall()
    numbers = []
    for e in response:
        numbers.append(e[0])
    conn.close()
    return numbers if numbers else ["No Numbers!"]


def getPersonFromNumber(number: int):
    conn = sqlite3.connect('PhoneNumbers.db')
    cur = conn.cursor()
    cur.execute(f"SELECT Name FROM person, numbers WHERE Holder_Id=person.Id AND Number={number}")
    try:
        ans = cur.fetchall()[0][0]
    except IndexError:
        ans = "NONE"
    conn.close()
    return ans


def insertPerson(name: str, number: int):
    conn = sqlite3.connect('PhoneNumbers.db')
    cur = conn.cursor()

    namesList = getNames()
    if name in namesList:
        conn.close()
        return f"EXISTS", f"Name {name} already defined"

    numbersList = getNumbersList()
    if number in numbersList:
        conn.close()
        return "NUMBER", f"{number} already assigned to {getPersonFromNumber(number)}"

    cur.execute(f"INSERT INTO person (Id, Name) VALUES (Null, '{name}')")
    conn.commit()
    cur.execute(f"SELECT Id FROM person WHERE Name='{name.capitalize()}'")
    conn.commit()
    holder_id = cur.fetchall()
    cur.execute(f"INSERT INTO numbers (Id, Number, Holder_Id) VALUES (Null, {number}, {holder_id[0][0]})")
    conn.commit()
    conn.close()
    return "SUCCESS", f"Successfully added {name} with number {number}"


def insertNumber(name: str, num: int):
    conn = sqlite3.connect('PhoneNumbers.db')
    cur = conn.cursor()

    numbersList = getNumbersList()
    if num in numbersList:
        conn.close()
        return "EXISTS", f"{num} already assigned to {getPersonFromNumber(num)}"

    cur.execute(f"SELECT Id FROM person WHERE Name='{name.capitalize()}'")
    conn.commit()
    holder_id = cur.fetchall()
    cur.execute(f"INSERT INTO numbers (Id, Number, Holder_Id) VALUES (Null, {num}, {holder_id[0][0]})")
    conn.commit()
    conn.close()
    return "SUCCESS", f"Successfully added number '{num}' to {name}"


def getJSON():
    conn = sqlite3.connect('PhoneNumbers.db')
    cur = conn.cursor()
    # cur.execute(f"SELECT p.Id, p.Name, n.Number FROM persons as p RIGHT OUTER JOIN numbers as n ON p.Id = n.Holder_Id ORDER BY p.Id, n.Holder_Id FOR JSON AUTO")
    cur.execute(f"SELECT p.Id, p.Name, n.Number FROM person as p, numbers as n WHERE Holder_Id=p.Id")
    ans = cur.fetchall()
    conn.close()
    return ans


# cur.execute("INSERT INTO person (Id, Name) VALUES (Null, 'James')")
# conn.commit()
# print(getIdFromName("James"))

def add_data(**kwargs):
    values = list(kwargs.values())
    keys = list(kwargs.keys())
    #cur.execute("INSERT")


def getNumbersFrom(name: str):
    conn = sqlite3.connect('PhoneNumbers.db')
    cur = conn.cursor()
    try:
        Id = getIdFromName(name)[0][0]
    except IndexError:
        return "NONE"
    cur.execute(f"SELECT Number FROM numbers WHERE Holder_Id={Id}")
    conn.commit()

    response = cur.fetchall()
    numbers = []
    for e in response:
        numbers.append(e[0])
    conn.close()
    return numbers if numbers else ["No Numbers!"]


def removePerson(name: str):
    conn = sqlite3.connect('PhoneNumbers.db')
    cur = conn.cursor()

    cur.execute(f"SELECT Id FROM person WHERE Name='{name.capitalize()}'")
    conn.commit()
    holder_id = cur.fetchall()

    cur.execute(f"DELETE FROM person WHERE person.Name='{name.capitalize()}'")
    conn.commit()
    cur.execute(f"DELETE FROM numbers WHERE numbers.Holder_ID={holder_id[0][0]}")
    conn.commit()
    return f"Successfully removed '{name}' from database"