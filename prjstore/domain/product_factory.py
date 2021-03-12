from prjstore.domain.products.simple_product import SimpleProduct
from prjstore.domain.products.shoes import Shoes


def product_factory(product_type='product', *args, **kwargs):
    products = {
        'product': SimpleProduct,
        'shoes': Shoes,
    }

    return products[product_type](*args, **kwargs)
