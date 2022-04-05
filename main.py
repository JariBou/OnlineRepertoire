import sqlite3


from flask import Flask, render_template, request

from DataLinkClass import Link


app = Flask(__name__)

link = Link("PhoneNumbers.db")


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/resultat/', methods=['Post', 'Get'])
def result():
    type = request.args.get('type', default='add', type=str)
    result = request.form
    prevPageUrl = str(request.referrer)
    print(prevPageUrl)

    match type:

        case "add_new":
            name = result['nom'].capitalize()
            num = result['num']
            try:
                int(num)
            except TypeError:
                return render_template("resultat.html", typ="error", returnAllowed=True, prevUrl=prevPageUrl,  error_msg=f"ERROR, '{num}' is not a valid Number")
            except BaseException:
                namesList = link.getNames()
                if name in namesList:
                    return render_template("person_settings.html", name=name)
                else:
                    return render_template("resultat.html", typ="error", returnAllowed=True, prevUrl=prevPageUrl,
                                           error_msg=f"ERROR, '{num}' is not a valid Number")
            link.insertPerson(name, num)
            match link.type:
                case "EXISTS":
                    return render_template("person_settings.html", name=name)
                case "SUCCESS":
                    return render_template("resultat.html", returnAllowed=True, prevUrl=prevPageUrl, typ='add_new', nom=name, num=num, add_msg=link.msg)
                case "NUMBER":
                    return render_template("resultat.html", returnAllowed=True, prevUrl=prevPageUrl, typ='error', add_msg=link.msg)

        case "add":
            name = request.args.get('name', default='', type=str)
            num = result['num']
            try:
                int(num)
            except ValueError:
                return render_template("resultat.html", returnAllowed=True, prevUrl=prevPageUrl, typ="error", error_msg=f"ERROR, '{num}' is not a valid Number")
            link.insertNumber(name, num)
            if link.type == "EXISTS":
                return render_template("resultat.html", returnAllowed=True, prevUrl=prevPageUrl, typ="error", error_msg=link.msg)
            else:
                return render_template("resultat.html", typ="add", returnAllowed=True, prevUrl=prevPageUrl, add_msg=link.msg)

        case "search":
            typo = request.args.get('typo', default='name', type=str)
            print(result)
            if typo == "num":
                num = result['num']
                try:
                    int(num)
                except ValueError:
                    return render_template("resultat.html", typ="error", returnAllowed=True, prevUrl=prevPageUrl,
                                           error_msg=f"ERROR, '{num}' is not a valid Number")
                name = link.getPersonFromNumber(num)
                if name == "NONE":
                    return render_template("resultat.html", returnAllowed=True, typ="error", prevUrl=prevPageUrl,
                                           error_msg=f"The number '{num}' is not registered")
                return render_template("resultat.html", typ="search_num", returnAllowed=True, prevUrl=prevPageUrl, number=num, name=name)

            else:
                name = result['name'].capitalize()

                numbers = link.getNumbersFrom(name)
                if numbers == "NONE":
                    return render_template("resultat.html", returnAllowed=True, prevUrl=prevPageUrl, typ="error", error_msg=f"Name '{name}' is not registered")
                return render_template("resultat.html", typ="search_name", returnAllowed=True, prevUrl=prevPageUrl, numbers=numbers, name=name)

        case "remove":
            name = request.args.get('name', default='', type=str)
            link.removePerson(name)
            return render_template('resultat.html', typ='remove', msg=link.msg)

        case "remove_num":
            name = request.args.get('name', default='', type=str)
            numbersList = link.getNumbersFrom(name.capitalize())
            numbers_removed = 0
            for num in numbersList:
                if result.get(num, default='off') == 'on':
                    link.removeNumber(num)
                    numbers_removed += 1
            if len(numbersList) == numbers_removed:
                link.removePerson(name)
                return render_template('resultat.html', typ='remove', msg=link.msg)
            return render_template('resultat.html', typ='remove', returnAllowed=True, prevUrl=prevPageUrl, msg=f"Succesfully removed {numbers_removed} numbers from {name}")

        case "watch":
            name = request.args.get('name', default='', type=str)
            numbersList = link.getNumbersFrom(name.capitalize())
            return render_template('resultat.html', typ='watch', name=name, numbers=numbersList)


@app.route('/add_num/')
def add_num():
    type = request.args.get('new', default='add', type=str)
    name = request.args.get('name', default="", type=str)
    if type == 'yes':
        return render_template("add_num.html", new='yes')
    return render_template("add_num.html", new='no', name=name)


@app.route('/remove_numbers/', methods=['Post', 'Get'])
def remove_numbs():
    name = request.args.get('name', default="", type=str)
    numbersList = link.getNumbersFrom(name.capitalize())
    prevPageUrl = request.referrer
    return render_template('remove_numbers.html', prevUrl=prevPageUrl, name=name, numbers=numbersList)


@app.route('/search/')
def search_num():
    type = request.args.get('type', default='add', type=str)
    prevPageUrl = request.referrer
    if type == 'num':
        data = link.getNumbersList()
        searchName = "Number"
        searchVar = "num"
    else:
        data = link.getNames()
        searchName = "Name"
        searchVar = "name"
    if not data:
        return render_template('result.html', typo='error', returnAllowed=True, prevUrl=prevPageUrl, error_msg=f'No {searchName}s entered in Repertoire')
    return render_template("search.html", searchVar=searchVar, searchName=searchName, data=data)


@app.route('/search_person')
def search_person():
    return render_template("add_num.html")


@app.route('/search_num')
def search_nim():
    return render_template("add_num.html")


@app.route('/person_settings/')
def person_settings():
     name = request.args.get('name', default='', type=str)
     return render_template('person_settings.html', name=name)


@app.template_filter('getNums')
def getNums(s):
    return link.getNumbersFrom(s)


@app.route('/peak')
def peak():
    names = link.getNames()

    return render_template("peak.html", names=names)


conn = sqlite3.connect('PhoneNumbers.db')
cur = conn.cursor()

cur.execute("""CREATE TABLE IF NOT EXISTS person(
            Id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
            Name TEXT)""")
conn.commit()
cur.execute("""CREATE TABLE IF NOT EXISTS numbers(
            Id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
            Number TEXT, Holder_Id INTEGER)""")
conn.commit()

##TODO: Check on input if number can be converted to string


app.run(debug=True)
