from flask import Flask, render_template, request
import requests
import xml.etree.ElementTree as ET

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/handle_data', methods=['POST'])
def handle_data():
    amount = request.form['cur']
    return int(amount)


@app.route('/currency_from', methods=['POST'])
def currency_from():
    value = request.form['currencyfrom']
    return value


@app.route('/currency_to', methods=['POST'])
def currency_to():
    value = request.form['currencyto']
    return value


@app.route('/btn', methods=['POST'])
def btn():
    handle_data()
    currency_from()
    currency_to()
    makeRequest()


def getRequest():
    result = {
        'usd': 0,
        'eur': 0,
    }
    get_xml = requests.get('http://www.cbr.ru/scripts/XML_val.asp?d=0')
    structure = ET.fromstring(get_xml.content)

    usd = structure.find("./*[@ID='R01235']/Value")
    result['usd'] = usd.text.replace(',', '.')

    eur = structure.find("./*[@ID='R01239']/Value")
    result['eur'] = eur.text.replace(',', '.')

    return result


@app.route('/res', methods=['POST'])
def makeRequest():
    cf = currency_from()
    ct = currency_to()
    amount = handle_data()
    rate = getRequest()
    if cf == 'USD' and ct == 'RUB':
        result = amount * rate['usd']
        x_result = f"{result} {ct}"
    elif cf == 'EUR' and ct == 'RUB':
        result = amount * rate['eur']
        x_result = f"{result} {ct}"
    elif cf == 'USD' and ct == 'EUR':
        result = (amount * rate['usd']) / rate['eur']
        x_result = f"{result} {ct}"
    elif cf == 'EUR' and ct == 'USD':
        result = (amount * rate['eur']) / rate['usd']
        x_result = f"{result} {ct}"
    elif cf == 'RUB' and ct == 'USD':
        result = amount / rate['usd']
        x_result = f"{result} {ct}"
    elif cf == 'RUB' and ct == 'EUR':
        result = amount / rate['eur']
        x_result = f"{result} {ct}"
    else:
        result = amount
        x_result = f"{result} {ct}"
    return render_template('index.html', x_result=x_result)


app.run('127.0.0.1', port=8000, debug=True)
