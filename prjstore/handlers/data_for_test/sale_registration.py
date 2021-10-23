from prjstore.domain.item import Item
from prjstore.domain.place_of_sale import PlaceOfSale
from prjstore.domain.product_catalog import ProductCatalog
from prjstore.domain.product_factory import ProductFactory
from prjstore.domain.products.shoes import Shoes
from prjstore.domain.seller import Seller
from util.money import Money

pc = ProductCatalog()
pc.set_product(ProductFactory.create(prod_id='04', name='sim prod', price=Money(25)))
pc.set_product(ProductFactory.create(prod_id='02', name='battery', price=Money(25)))

pc.set_product(ProductFactory.create(
    product_type='shoes', prod_id='03', name='nike air force', price=Money(900), color='red', size=43,
    length_of_insole=28
))
pc.set_product(ProductFactory.create(
    product_type='shoes', prod_id='01', name='nike Jordan', price=Money(750), color='red', size=43,
    length_of_insole=28.5
))
pc.set_product(ProductFactory.create(
    product_type='shoes', prod_id='05', name='nike air force мех', price=Money(1200), color='red', size=42,
    length_of_insole=27, width=Shoes.widths['Medium']
))
pc.set_product(pc['05'].copy('06'))
pc['06'].color = 'white'
pc.set_product(pc['05'].copy('07'))
pc['07'].size = 44
pc['07'].length_of_insole = 28.5
pc.set_product(pc['05'].copy('08'))
pc['08'].width = Shoes.widths['Wide']
items = {
    5: Item(id=5, product=pc['04'], buy_price=Money(40)),
    2: Item(id=2, product=pc['02'], buy_price=Money(50.5), qty=2),
    3: Item(id=3, product=pc['03'], buy_price=Money(50.5), qty=2),
    4: Item(id=4, product=pc['03'], buy_price=Money(55.5), qty=2),
    1: Item(id=1, product=pc['01'], buy_price=Money(55.5)),
    6: Item(id=6, product=pc['05'], buy_price=Money(55.5)),
    7: Item(id=7, product=pc['06'], buy_price=Money(55.5)),
    8: Item(id=8, product=pc['07'], buy_price=Money(55.5)),
    9: Item(id=9, product=pc['08'], buy_price=Money(55.5)),
}


def put_test_data(handler):
    handler._store.pc = pc
    handler._store.items = items
    handler._store.sellers = {1: Seller(1, 'Igor'), 2: Seller(2, 'Anna'), 3: Seller(3, 'Sasha')}
    places_of_sale = {1: PlaceOfSale(1, 'Интернет'), 2: PlaceOfSale(2, 'Бокс 47'),
                      3: PlaceOfSale(3, 'Магазин 1-й этаж'), 4: PlaceOfSale(4, 'Магазин 2-й этаж')}
    handler._store.places_of_sale = places_of_sale
