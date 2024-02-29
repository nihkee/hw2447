# import flask & sql
from flask import Flask, render_template, request, redirect, url_for
import sqlite3 
  
app = Flask(__name__) 
  
# render index.html as our homepage
@app.route('/') 
@app.route('/home') 
def index(): 
    return render_template('index.html') 
  
# create a database file 
connect = sqlite3.connect('database.db') 
# create a players table with 2 text type, 1 int type if it doesnt exist yet
connect.execute( 
    'CREATE TABLE IF NOT EXISTS PLAYERS (name TEXT, idNum TEXT, points INTEGER)') 
  
# route for create user  
@app.route('/create', methods=['GET', 'POST']) 
def create(): 
    # retrieve data from form
    if request.method == 'POST': 
        name = request.form['name'] 
        idNum = request.form['idNum'] 
        points = request.form['points'] 
    # insert into database table
        with sqlite3.connect("database.db") as users: 
            cursor = users.cursor() 
            cursor.execute("INSERT INTO PLAYERS (name,idNum,points) VALUES (?,?,?)", 
                           (name, idNum, points)) 
            users.commit() 
        return render_template("index.html") 
    # render create.html
    else: 
        return render_template('create.html') 
  
 # route for view users
@app.route('/view') 
def view(): 
    # connect to db
    connect = sqlite3.connect('database.db') 
    cursor = connect.cursor() 
    cursor.execute('SELECT * FROM PLAYERS') 
    # fetch & return data to be rendered
    data = cursor.fetchall() 
    return render_template("view.html", data=data) 

# route for search user
@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        # retrieve name for search query
        search_query = request.form['search_query']
        # connect to db
        connect = sqlite3.connect('database.db')
        cursor = connect.cursor()
        # use SQL query to search for user based on name or idNum
        cursor.execute("SELECT * FROM PLAYERS WHERE name LIKE ? OR idNum = ?", (search_query, search_query))
        # fetch & return results as data
        data = cursor.fetchall()
        return render_template("searchResults.html", data=data, search_query=search_query)
    else:
        # render search form
        return render_template('search.html')

# route for update user
@app.route('/update', methods=['GET', 'POST'])
def update():
    if request.method == 'POST':
        # retrieve old name and new info
        oldName = request.form['oldName']
        newName = request.form['name']
        idNum = request.form['idNum']
        points = request.form['points']
        # use SQL query to update values based on player's old name
        with sqlite3.connect("database.db") as users:
            cursor = users.cursor()
            cursor.execute("UPDATE PLAYERS SET name=?, idNum=?, points=? WHERE name=?", (newName, idNum, points, oldName))
            users.commit()
        # render new table
        return redirect(url_for('view'))
    else:
        # render update page
        return render_template('update.html')

# route for delete user
@app.route('/delete', methods=['GET', 'POST'])
def delete():
    if request.method == 'POST':
        # uses name from form
        name = request.form['name']
        # uses SQL DELETE to remove from db table
        with sqlite3.connect("database.db") as users:
            cursor = users.cursor()
            cursor.execute("DELETE FROM PLAYERS WHERE name=?", (name,))
            users.commit()
        # render new table
        return redirect(url_for('view'))
    else:
        # render delete page
        return render_template('delete.html')
        
# debugging
if __name__ == '__main__': 
    app.run(debug=True) 