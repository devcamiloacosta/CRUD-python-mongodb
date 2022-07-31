from crypt import methods
from email.mime import message
from itertools import product
from urllib import response
from flask import Flask, render_template, request, Response, jsonify, redirect, url_for
import db as dbase 
from product import Product


dbb = dbase.conectionDb()

app = Flask(__name__)


#rutas
@app.route('/')

def home():
  products = dbb['products']
  productsReceived = products.find()
  return render_template('index.html', products = productsReceived)

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
  products = dbb['products']
  products.delete_one({
    'name': product_name
  })
  return redirect(url_for('home'))

#Metodo de modificacion
@app.route('/edit/<string:product_name>', methods=['POST'])
def edit(id, product_name):
  products = dbb['products']
  name = request.form['name']
  price = request.form['price']
  quantity = request.form['quantity']

  if name and price and quantity:
    products.update_one({'id': id}, {'$set': {'name': name, 'price': price, 'quantity': quantity}})
    response = jsonify({'message': 'Producto' + product_name + 'actualizado exitosamente'})
    return redirect(url_for('home'))
  else:
    return notFound()

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