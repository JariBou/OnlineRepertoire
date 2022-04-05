import sqlite3


class Link:

    def __init__(self, filename):
        self.filename = filename
        self.type = ''   # SUCESS/ERROR/EXISTS....
        self.msg = ''   # Returned MSG

    def getNames(self):
        response = self.execute("SELECT Name FROM person")
        names = []
        for e in response:
            names.append(e[0])
        if names:
            self.type = "SUCCESS"
        self.type = "ERROR"
        return names

    def getNumbersList(self):
        response = self.execute("SELECT Number FROM numbers")
        numbers = []
        for e in response:
            numbers.append(e[0])
        if numbers:
            self.type = "SUCCESS"
        self.type = "ERROR"
        return numbers


    def getPersonFromNumber(self, number: str):
        ans = self.execute(f"SELECT Name FROM person, numbers WHERE Holder_Id=person.Id AND Number='{number}'")
        try:
            return ans[0][0]
        except IndexError:
            return "NONE"

    def insertPerson(self, name: str, number: str):

        namesList = self.getNames()
        numbersList = self.getNumbersList()
        if name in namesList:
            self.type, self.msg = f"EXISTS", f"Name {name} already defined"
        elif number in numbersList:
            self.type, self.msg = "NUMBER", f"Number '{number}' already assigned to {self.getPersonFromNumber(number)}"
        else:
            self.execute(f"INSERT INTO person (Id, Name) VALUES (Null, '{name}')")
            holder_id = self.execute(f"SELECT Id FROM person WHERE Name='{name.capitalize()}'")
            self.execute(f"INSERT INTO numbers (Id, Number, Holder_Id) VALUES (Null, '{number}', {holder_id[0][0]})")
            self.type, self.msg = "SUCCESS", f"Successfully added {name} with number {number}"

    def insertNumber(self, name: str, num: str):
        numbersList = self.getNumbersList()
        if num in numbersList:
            self.type, self.msg = "EXISTS", f"{num} already assigned to {self.getPersonFromNumber(num)}"
        else:
            holder_id = self.execute(f"SELECT Id FROM person WHERE Name='{name.capitalize()}'")
            self.execute(f"INSERT INTO numbers (Id, Number, Holder_Id) VALUES (Null, '{num}', {holder_id[0][0]})")
            self.type, self.msg = "SUCCESS", f"Successfully added number '{num}' to {name}"

    def getIdFromName(self, name: str):
        ans = self.execute(f"SELECT Id, Name FROM person WHERE Name='{name.capitalize()}'")
        return ans

    def getNumbersFrom(self, name: str):
        try:
            Id = self.getIdFromName(name)[0][0]
        except IndexError:
            return "NONE"
        response = self.execute(f"SELECT Number FROM numbers WHERE Holder_Id={Id}")

        numbers = []
        for e in response:
            numbers.append(e[0])
        return numbers if numbers else [f"No Numbers assigned to {name}!"]

    def removeNumber(self, number: str):
        person = self.getPersonFromNumber(number)
        self.execute(f"DELETE FROM numbers WHERE numbers.Number='{number}'")

    def removePerson(self, name: str):
        holder_id = self.execute(f"SELECT Id FROM person WHERE Name='{name.capitalize()}'")
        self.execute(f"DELETE FROM person WHERE person.Name='{name.capitalize()}'")
        self.execute(f"DELETE FROM numbers WHERE numbers.Holder_ID={holder_id[0][0]}")
        self.type, self.msg = "SUCCESS", f"Successfully removed '{name}' from database"

    def execute(self, command: str):
        conn = sqlite3.connect(self.filename)
        cur = conn.cursor()
        cur.execute(command)
        conn.commit()
        ans = cur.fetchall()
        cur.close()
        conn.close()
        return ans
