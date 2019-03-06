"""
Contains very dangerous functions that are only meant to be run once.

The URLs for these functions should be disabled and only re-enabled if completely necessary
They are mainly here for reference.
"""

import os
import json
import random
from django.shortcuts import HttpResponse

from restocking.models import Product

def add_quantities(request):
    """
    Assigning random(ish) quantities to each product.
    """

    path = os.getcwd()
    with open(path + '\\restocking\\data\\initial_product_levels.json') as data_file:
        quantity_data = json.load(data_file)

    product_set = Product.objects.all()

    for product in product_set:
        if product.size in quantity_data['department'][product.department]['size_data']['common']:
            size_category = 'common'
        else:
            size_category = 'uncommon'

        if '.5' in str(product.size):
            size_half = 'half'
        else:
            size_half = 'whole'

        quantity = quantity_data['department'][product.department]['code'][product.product_code]['size'][size_category][size_half]
        product.stock_quantity = quantity + random.randint((round(quantity/2) * -1), (round(quantity/2)))
        product.save()

    return HttpResponse('Success')

def add_data(request):
    """
    Creates random data from a file
    
    This will delete all products from the database, so don't run this unless you need to.
    """

    Product.objects.all().delete()
    print('Products deleted.')

    _colour_pop_chance = 50
    _fitting_pop_chance = 75
    def randint_x(n_1, n_2):
        """Returns a random number within the given range (exclusive)"""
        return random.randint(n_1, n_2-1)

    path = os.getcwd()
    with open(path + '\\restocking\\data\\product_metadata.json') as data_file:
        product_md = json.load(data_file)

    name_list = []#list to prevent duplicate names
    for department in product_md:
        for code in product_md[department]['codes']:
            for shoe in range(product_md[department]['codes'][code]['quantity']):
                #Name
                duplicate = True
                while duplicate:
                    primary_name = product_md[department]['codes'][code]['names'][randint_x(0, len(product_md[department]['codes'][code]['names']))]
                    secondary_name = product_md[department]['secondary'][randint_x(0, len(product_md[department]['secondary']))]
                    name = primary_name+" "+secondary_name
                    if name not in name_list:
                        name_list.append(name)
                        duplicate = False
                #Size
                sizes = []
                if department == 'childrens':
                    for size in range(0, len(product_md[department]['codes'][code]['sizes'])):
                        sizes.append(product_md[department]['codes'][code]['sizes'][size])
                else:
                    for size in range(0, len(product_md[department]['codes'][code]['sizes']), random.randint(1, 2)):
                        sizes.append(product_md[department]['codes'][code]['sizes'][size])
                #Fitting
                fittings = list(product_md[department]['codes'][code]['fittings'])
                if department == 'childrens':
                    if product_md[department]['codes'][code]['type'] == 'shoe' and random.randint(0, 1) == 1:
                        fittings.pop()
                        fittings.pop()
                else:
                    for x in range(0, len(fittings)-1):
                        if random.randint(0, 100) <= _fitting_pop_chance:
                            fittings.pop()
                #Colour
                colours = list(product_md[department]['codes'][code]['colours'])
                for x in range(len(colours)-1):
                    if random.randint(0, 100) <= _colour_pop_chance:
                        colours.pop()
                #Price
                price = product_md[department]['codes'][code]['prices'][randint_x(0, len(product_md[department]['codes'][code]['prices']))]
                product_type = product_md[department]['codes'][code]['type']
                product_code = code
                department = department

                for size in sizes:
                    for fitting in fittings:
                        for colour in colours:
                            Product.objects.create(
                                name=name,
                                size=size,
                                fitting=fitting,
                                colour=colour,
                                price=price,
                                product_type=product_type,
                                product_code=product_code,
                                department=department
                            )
        print('created department products')


    return HttpResponse("DONE")

def add_floor_quantities(request):
    _pop_chance = 40

    path = os.getcwd()
    with open(path + '\\restocking\\data\\initial_shop_floor_levels.json') as data_file:
        quantity_data = json.load(data_file)

    product_set = Product.objects.all()

    for product in product_set:
        if product.size in quantity_data['department'][product.department]['size_data']['common']:
            size_category = 'common'
        else:
            size_category = 'uncommon'

        if '.5' in str(product.size):
            size_half = 'half'
        else:
            size_half = 'whole'

        quantity = quantity_data['department'][product.department]['code'][product.product_code]['size'][size_category][size_half]
        if random.randint(0, 100) <= _pop_chance:
            quantity += -1
        product.floor_quantity = quantity
        product.save()

    return HttpResponse("DONE")
