from flask import Flask, render_template, request, flash, send_file
from dotenv import load_dotenv
from wtforms import StringField, Form
from wtforms.validators import InputRequired
import mysql.connector
import io
import os
import csv

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Ensure this is set to a secure key

# Define the form class
class MyForm(Form):
    sample_name = StringField('Sample Name', [InputRequired()], render_kw={"placeholder": "Specify the net-id of the Sample", "style": "width: 300px;"})

def fetch_entries_from_database(search_term):
    db = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS"),
        database=os.getenv("DB_NAME"),
        port=int(os.getenv("DB_PORT"))  
    )


    cursor = db.cursor()
    query = "SELECT name, alias, description FROM Sample WHERE alias LIKE %s"
    
    cursor.execute(query, (search_term,))
    results = cursor.fetchall()  
    cursor.close()
    db.close()
    
    return results

def generate_csv(results):
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['Sample ID', 'Sample Name', 'Description'])
    for name, alias, description in results:
        writer.writerow([name, alias, description])
    output.seek(0)
    return output

@app.route('/', methods=['GET', 'POST'])
def submit():
    form = MyForm(request.form)
    results = None
    if request.method == 'POST':
        if form.validate():
            search_term = f"{form.sample_name.data}%"
            
            # Fetch entries from database
            results = fetch_entries_from_database(search_term)
            
            if not results:
                flash(f"No entries found for Net-id '{form.sample_name.data}'")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    flash(f'{error}')
    
    return render_template('index.html', form=form, results=results)


@app.route('/download_csv')
def download_csv():
    search_term = request.args.get('search_term', '')

    if not search_term:
        return "No search term provided", 400

    results = fetch_entries_from_database(f"{search_term}%")
    csv_file = generate_csv(results)

    # Generate dynamic filename
    filename = f"{search_term}.csv"

    return send_file(
        io.BytesIO(csv_file.getvalue().encode('utf-8')),
        as_attachment=True,
        download_name=filename,
        mimetype="text/csv"
    )

if __name__ == '__main__':
    app.run(debug=True)

