from flask import Flask, jsonify, render_template, request, redirect, url_for
import gspread
from oauth2client.service_account import ServiceAccountCredentials

app = Flask(__name__)

# Google Sheets authentication
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
client = gspread.authorize(creds)

# Specify the Google Sheet ID and worksheet name
sheet_id = '1G8lCA7YedFeHabnw2VCMEngk450k9KdaAYReiX2aHL8'
worksheet_name = 'Sheet1'

# Get the worksheet
worksheet = client.open_by_key(sheet_id).worksheet(worksheet_name)


@app.route('/')
def home():
    data = worksheet.get_all_values()[1:]
    return render_template('home.html', data=data)


# Add data
@app.route('/add', methods=['POST'])
def add():
    name = request.form['name']
    email = request.form['email']
    phone = request.form['phone']
    row = [name, email, phone]
    worksheet.append_row(row)
    return redirect(url_for('home'))



# delete data
@app.route('/data')
def get_data():
    data = worksheet.get_all_values()[1:]
    return jsonify(data)  # Return JSON data


@app.route('/delete/<int:index>', methods=['POST'])
def delete(index):
    worksheet.delete_row(index+1)
    return redirect(url_for('home'))




# Update code
@app.route('/data')
def get_dataa():
    data = worksheet.get_all_values()[1:]
    return render_template('data.html', data=data)


@app.route('/update', methods=['POST'])
def update_data():
    row_index = int(request.form['row_index'])
    name = request.form['name']
    email = request.form['email']
    phone = request.form['phone']
    new_row = [name, email, phone]
    worksheet.insert_row(new_row, index=row_index+1)
    worksheet.delete_row(row_index+2)   
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)
