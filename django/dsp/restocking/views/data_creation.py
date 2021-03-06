"""
Views surrounding the creation of test data for the project

These functions are not 'forbidden' and can be ran multiple times!
"""

import random
import datetime

from django.shortcuts import HttpResponse

from restocking.models import Order, OrderItem, Product, User, Transaction, TransactionItem, RestockingList, RestockingListItem

from restocking.processing import RestockingListProcessing

def create_order_3000(request):
    """
    Create an order of 3000 items

    In practice, an order of 3000 is not likely, but this is to simply test how
    the worst case scenario works.
    """
    products = list(Product.objects.all())
    order_items = []
    order = Order(delivery_date='2019-01-02', order_delivered=True, order_processed=True)
    order.save()

    for i in range(3000):
        rnd = random.randrange(0, len(products))
        order_items.append(OrderItem(
            quantity=random.randint(1, 4),
            product=products[rnd],
            order=order,
        ))
        products.pop(rnd)

    for item in order_items:
        item.save()

    return HttpResponse('Done')

def create_transaction(request, quantity):
    """
    Create x number of transactions

    Adapted from test.
    """
    

    products = list(Product.objects.all())
    transaction_items = []
    transactions = []
    limit = quantity

    for i in range(quantity):
        transaction = Transaction(user=User.objects.get(id=1))
        transaction.save()
        transactions.append(transaction)
        rnd_number_products = random.randint(1, 3)
        for j in range(rnd_number_products):
            products = list(Product.objects.filter(floor_quantity__gt=0))
            rnd_quantity = 1
            rnd_product = random.randrange(0, len(products))
            products[rnd_product].floor_quantity -= rnd_quantity
            products[rnd_product].save()
            transaction_items.append(TransactionItem(
                quantity=rnd_quantity,
                product=products[rnd_product],
                transaction=transaction,
            ))
            limit -= rnd_quantity
            if limit <= 0:
                break
        if limit <= 0:
            break


    for item in transaction_items:
        item.save()

    return HttpResponse('Done')

def generate_restocking_list(request):
    RestockingListProcessing().create_restocking_list()
    
    return HttpResponse('Done')