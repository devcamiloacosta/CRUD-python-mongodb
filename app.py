from email.mime import message
from flask import Flask, render_template, request, Response, jsonify, redirect, url_for
import db as dbase 
from product import Product


dbb = dbase.conectionDb()

app = Flask(__name__)


#rutas
@app.route('/')

def home():
  return render_template('index.html')

@app.route('/products', methods=['POST'])
def add_product():
    products = dbb['products']
    name = request.form['name']
    price = request.form['price']
    quantity = request.form['quantity']

    if name and price and quantity:
      product = Product(name, price, quantity)
      products.insert_one(product.dbCollection())
      response = jsonify({
        'name': name,
        'price': price,
        'quantity': quantity
      })
      return redirect(url_for('home'))
    else:
      return notFound()

#Metodo de eliminar
@app.route('/delete/<string:product_name>')
def delete(product_name):
  pass

@app.errorhandler(404)
def notFound(error=None):
  message = {
    'message': 'No encontrado' + request.url,
    'status': '404 Not Found'
  }
  response = jsonify(message)
  response.status_code = 404
  return response


if __name__ == '__main__':
  app.run(debug=True, port=4000)