from flask import Flask, redirect, url_for, request, Response, render_template
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Zero@123'
app.config['MYSQL_DB'] = 'assgnment4'

mysql = MySQL(app)

@app.route("/")
def home_page():
    return render_template('index.html')

@app.route("/bonds" , methods = ['GET' , 'POST'])
def bonds():
    if request.method == "POST":
        records = request.form
        bond = records['box']
        cur = mysql.connection.cursor()
        sql_query = "select * from file2 join file1 on file2.Bond_Number = file1.Bond_Number where file1.Bond_Number =  %s"
        cur.execute(sql_query, (bond, ))
        mysql.connection.commit()
        record = cur.fetchall()
        cur.close()
        return render_template('/bonds.html' , records=record)
    return render_template('/bonds.html')

@app.route("/companies" , methods=['GET' , 'POST'])
def companies():
    if request.method == "POST":
        if 'company' in request.form:
            company_name = request.form['company']
            cur = mysql.connection.cursor()
            sql_query = "select %s ,count(Bond_Number) from file1 where `Name of the Purchaser` =  %s"
            cur.execute(sql_query, (company_name, company_name))
            mysql.connection.commit()
            comp_record = cur.fetchall()
            cur.close()
            return render_template('/companies.html' , company_name=comp_record)
        elif 'party_company' in request.form:
            party_company_name = request.form['party_company']
            cur = mysql.connection.cursor()
            sql_query = "select distinct file2.`Name of the Political Party`, sum(file1.Denominations) from file2 join file1 on file2.Bond_Number = file1.Bond_Number where file1.`Name of the Purchaser` = %s GROUP BY file2.`Name of the Political Party`"
            cur.execute(sql_query, (party_company_name,))
            mysql.connection.commit()
            comp_record = cur.fetchall()
            cur.close()
            return render_template('/companies.html' , party_company_name=comp_record)
    return render_template('/companies.html')

@app.route("/parties" , methods=['GET' , 'POST'])
def parties(): 
    if request.method == "POST":
        if "party" in request.form:
            party_name = request.form['party']
            cur = mysql.connection.cursor()
            sql_query = "select %s ,count(Bond_Number) from file2 where `Name of the Political Party` =  %s"
            cur.execute(sql_query, (party_name, party_name))
            mysql.connection.commit()
            party_record = cur.fetchall()
            cur.close()
            return render_template('/parties.html' , party_name=party_record)
        elif "party_company" in request.form:
            parties_name = request.form['party_company']
            cur = mysql.connection.cursor()
            sql_query = "select distinct file1.`Name of the Purchaser`, sum(file2.Denominations) from file1 join file2 on file1.Bond_Number = file2.Bond_Number where file2.`Name of the Political Party` = %s GROUP BY file1.`Name of the Purchaser`"
            cur.execute(sql_query, (parties_name, ))
            mysql.connection.commit()
            party_record = cur.fetchall()
            cur.close()
            return render_template('/parties.html' , parties_name=party_record)
    return render_template('/parties.html')

if __name__ == "__main__":
    app.run(debug=True)





"select * from file2 join file1 on file2.Bond_Number = file1.Bond_Number where file1.`Name of the Purchaser` = %s GROUP BY file2.`Name of the Political Party`"