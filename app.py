from flask import Flask, render_template, request
import requests
import xml.etree.ElementTree as ET

app = Flask(__name__)


# @app.route('/handle_data', methods=['GET', 'POST'])
def handle_data():
    amount = request.form['cur']
    return int(amount)


# @app.route('/currency_from', methods=['GET', 'POST'])
def currency_from():
    value = request.form['currencyfrom']
    return str(value)


# @app.route('/currency_to', methods=['GET', 'POST'])
def currency_to():
    value = request.form['currencyto']
    return str(value)


def getRequest():
    result = {
        'usd': 0,
        'eur': 0,
    }
    get_xml = requests.get('http://www.cbr.ru/scripts/XML_daily.asp?')
    structure = ET.fromstring(get_xml.content)

    usd = structure.find("./*[@ID='R01235']/Value")
    result['usd'] = usd.text.replace(',', '.')
    eur = structure.find("./*[@ID='R01239']/Value")
    result['eur'] = eur.text.replace(',', '.')

    return result


@app.route('/', methods=['GET', 'POST'])
def index():
    x_result = ''
    if request.method == 'POST':
        cf = currency_from()
        ct = currency_to()
        amount = handle_data()
        rate = getRequest()
        if cf == 'USD' and ct == 'RUB':
            result = amount * float(rate['usd'])
            x_result = f"{result} {ct}"
        elif cf == 'EUR' and ct == 'RUB':
            result = amount * float(rate['eur'])
            x_result = f"{result} {ct}"
        elif cf == 'USD' and ct == 'EUR':
            result = (amount * float(rate['usd'])) / float(rate['eur'])
            x_result = f"{result} {ct}"
        elif cf == 'EUR' and ct == 'USD':
            result = (amount * float(rate['eur'])) / float(rate['usd'])
            x_result = f"{result} {ct}"
        elif cf == 'RUB' and ct == 'USD':
            result = amount / float(rate['usd'])
            x_result = f"{result} {ct}"
        elif cf == 'RUB' and ct == 'EUR':
            result = amount / float(rate['eur'])
            x_result = f"{result} {ct}"
        else:
            result = amount
            x_result = f"{result} {ct}"

    return render_template('index.html', x_result=x_result)


if __name__ == '__main__':
    app.run('127.0.0.1', port=8000, debug=True)
