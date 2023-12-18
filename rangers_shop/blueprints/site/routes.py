from flask import Blueprint, render_template, flash, request, redirect

#internal import 
from rangers_shop.models import Product, db , Customer, Order
from rangers_shop.forms import ProductForm


site = Blueprint('site',__name__, template_folder='site_templates')


@site.route('/')
def shop():

    allproducts = Product.query.all()
    allcustomers = Customer.query.all() # ADD THIS
    allorders = Order.query.all() # ADD THIS

    product_count = len(allproducts)

    shop_stats = {
        'products' : len(allproducts), 
        'sales' : sum([order.order_total for order in allorders]),  #[ 27.99, 83.25, 50.99 ] sum them bad boys up
        'customers' : len(allcustomers)
    }


    return render_template('shop.html', shop=allproducts,product_count = product_count, stats=shop_stats)

@site.route('/shop/create',methods=['POST','GET'])
def create():

    create_form = ProductForm()

    if request.method=='POST' and create_form.validate_on_submit():

        name = create_form.name.data
        image = create_form.image.data
        description = create_form.description.data
        price = create_form.price.data
        playtime = create_form.playtime.data
        quantity = create_form.quantity.data

        product = Product(name, quantity, price, playtime, image, description)

        db.session.add(product)
        db.session.commit()

        flash(f"You have successfully created product {name}", category='success')
        return redirect('/')
    
    elif request.method == 'POST':
        flash("We were unable to process your request", category='warning')
        return redirect('/shop/create')
    

    return render_template('createproduct.html', form=create_form )


@site.route('/shop/update/<id>', methods=['GET', 'POST']) #<parameter> this is how pass parameters to our routes 
def update(id):

    #lets grab our specific product we want to update
    product = Product.query.get(id) #this should only ever bring back 1 item/object
    updateform = ProductForm()

    if request.method == 'POST' and updateform.validate_on_submit():

        product.name = updateform.name.data 
        product.image = updateform.image.data 
        product.description = updateform.description.data 
        product.price = updateform.price.data 
        product.quantity = updateform.quantity.data 

        #commit our changes
        db.session.commit()

        flash(f"You have successfully updated product {product.name}", category='success')
        return redirect('/')
    
    elif request.method == 'POST':
        flash("We were unable to process your request", category='warning')
        return redirect('/')
    
    return render_template('updateform.html', form=updateform, product=product )

@site.route('/shop/delete/<id>')
def delete(id):
    product = Product.query.get(id)

    db.session.delete(product)
    db.session.commit()

    return redirect('/')