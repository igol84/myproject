import datetime

from prjstore.domain.item import Item
from prjstore.domain.place_of_sale import PlaceOfSale
from prjstore.domain.product_catalog import ProductCatalog
from prjstore.domain.product_factory import ProductFactory
from prjstore.domain.products.shoes import Shoes
from prjstore.domain.seller import Seller
from prjstore.domain.store import Store
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

pc.set_product(pc['03'].copy('09'))
pc['09'].size = 44
pc['09'].length_of_insole = 28.5
pc['09'].price = Money(1200)
pc.set_product(pc['09'].copy('10'))
pc['10'].size = 42
pc['10'].length_of_insole = 27.5

items = {
    5: Item(id=5, product=pc['04'], buy_price=Money(40), date_buy=datetime.date(2021, 12, 30)),
    2: Item(id=2, product=pc['02'], buy_price=Money(50.5), qty=112, date_buy=datetime.date(2022, 1, 4)),
    3: Item(id=3, product=pc['03'], buy_price=Money(50.5), qty=2, date_buy=datetime.date(2022, 2, 5)),
    4: Item(id=4, product=pc['03'], buy_price=Money(55.5), qty=2, date_buy=datetime.date(2022, 2, 6)),
    1: Item(id=1, product=pc['01'], buy_price=Money(55.5), date_buy=datetime.date(2022, 2, 7)),
    6: Item(id=6, product=pc['05'], buy_price=Money(55.5), date_buy=datetime.date(2022, 2, 12)),
    7: Item(id=7, product=pc['06'], buy_price=Money(55.5), date_buy=datetime.date(2022, 2, 22)),
    8: Item(id=8, product=pc['07'], buy_price=Money(55.5), date_buy=datetime.date(2022, 2, 24)),
    9: Item(id=9, product=pc['08'], buy_price=Money(55.5), date_buy=datetime.date(2022, 3, 1)),
    10: Item(id=10, product=pc['09'], buy_price=Money(55.5), date_buy=datetime.date(2022, 3, 5)),
    11: Item(id=11, product=pc['10'], buy_price=Money(55.5), date_buy=datetime.date(2022, 3, 24)),
}


def put_test_data(handler):
    handler.__store.pc = pc
    handler.__store.items = items
    handler.__store.sellers = {1: Seller(1, 'Igor'), 2: Seller(2, 'Anna'), 3: Seller(3, 'Sasha')}
    places_of_sale = {1: PlaceOfSale(1, 'Интернет'), 2: PlaceOfSale(2, 'Бокс 47'),
                      3: PlaceOfSale(3, 'Магазин 1-й этаж'), 4: PlaceOfSale(4, 'Магазин 2-й этаж')}
    handler.__store.places_of_sale = places_of_sale


def put_test_data_to_store(store):
    store.pc = pc
    store.items = items
    store.sellers = {1: Seller(1, 'Igor'), 2: Seller(2, 'Anna'), 3: Seller(3, 'Sasha')}
    places_of_sale = {1: PlaceOfSale(1, 'Интернет'), 2: PlaceOfSale(2, 'Бокс 47'),
                      3: PlaceOfSale(3, 'Магазин 1-й этаж'), 4: PlaceOfSale(4, 'Магазин 2-й этаж')}
    store.places_of_sale = places_of_sale

if __name__ == '__main__':
    store = Store(id=1, name='test')
    put_test_data_to_store(store)
    items: dict[int: Item] = store.items
    for item in items.values():
        if item.product.product_type=='shoes':
            print(item.product.width.short_name)