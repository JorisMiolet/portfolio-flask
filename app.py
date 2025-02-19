import csv
from flask import Flask, render_template, url_for, request, redirect
import pandas as pd
from sqlalchemy import create_engine, text
import mysql.connector
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential

app = Flask(__name__)

credential = DefaultAzureCredential()
client = SecretClient(vault_url="https://portfoliojomikeyvault.vault.azure.net/", credential=credential)

host='oege.ie.hva.nl'
database='zmioulej'
user='mioulej'
password = client.get_secret("database-password")

connection = mysql.connector.connect(
    host=host,
    database=database,
    user=user,
    password=password
)

connectionString = client.get_secret("connection-string")

# if connection.is_connected():
#     db_info = connection.get_server_info()
#     print("Connected to MySQL Server version", db_info)

engine = create_engine(connectionString.value)


# df = pd.read_sql(text("SELECT * FROM Interests"), con=engine.connect())

# print(df.head())
@app.route('/personal-interests')
@app.route('/personal-interests.html')
def personal_interest():
    try:
        with engine.connect() as conn:
            query = text("SELECT * FROM Interests")
            result = conn.execute(query)
            interests = [dict(row) for row in result.mappings()]  # Converts rows to dictionaries
            print(interests)
            return render_template('personal-interests.html', interests=interests)
    except Exception as e:
        print(f"Database error: {e}")
        return render_template('index.html')
        interests = []  # Return empty list in case of error

@app.route('/')
def homepage():
    return render_template('index.html')


@app.route('/<string:page_name>')
def html_page(page_name):
    return render_template(page_name, debug=True)


# def write_to_file(data):
#     with open('database.txt', mode='a') as database:
#         email = data['email']
#         subject = data['subject']
#         message = data['message']
#         file = database.write(f'\n{email},{subject},{message}')


def write_to_csv(data):
    with open('database.csv', 'a', newline='') as csvfile:
        email = data['email']
        subject = data['subject']
        message = data['message']
        writer = csv.writer(csvfile)
        writer.writerow([email, subject, message])


@app.route('/submit_form', methods=['GET', 'POST'])
def submit_form():
    if request.method == 'POST':
        data = request.form.to_dict()
        write_to_csv(data)
        return redirect('/thankyou.html')
    else:
        return 'Something went wrong!'
