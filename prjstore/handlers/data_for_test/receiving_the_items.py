from prjstore.ui.pyside.receiving_the_items.schemas import ModelSizeShoes, ModelProductShow, ModelColorShoesShow


def get_test_data() -> list[ModelProductShow]:
    list_pd_prod = []
    sizes = {38: ModelSizeShoes(size=38, length=24.5, qty=5),
             39: ModelSizeShoes(size=39, length=25, qty=8),
             42: ModelSizeShoes(size=42, length=27.5, qty=1),
             43: ModelSizeShoes(size=43, length=28, qty=2)}
    shoes = ModelColorShoesShow(colors=['black'], width='EE', sizes=sizes)
    list_pd_prod.append(
        ModelProductShow(id=115, type='shoes', name='con chak h 70', price_sell=640.40, module=shoes))
    list_pd_prod.append(ModelProductShow(id=22, type='product', name='battery', price_sell=840))
    for n in range(23, 24):
        list_pd_prod.append(ModelProductShow(id=n, type='product', name=f'battery {n}', price_sell=840 + n))
    sizes = {36: ModelSizeShoes(size=36, length=23.5, qty=1),
             37: ModelSizeShoes(size=37, length=24, qty=2),
             38: ModelSizeShoes(size=38, length=24.5, qty=1),
             39: ModelSizeShoes(size=39, length=25, qty=2),
             41: ModelSizeShoes(size=41, length=26.5, qty=3)}
    shoes = ModelColorShoesShow(colors=['white', 'red'], sizes=sizes)
    list_pd_prod.append(ModelProductShow(id=254, type='shoes', name='con chak l 70', price_sell=420, module=shoes))

    sizes = {37: ModelSizeShoes(size=37, length=24, qty=1),
             38: ModelSizeShoes(size=38, length=24.5, qty=2),
             39: ModelSizeShoes(size=39, length=25, qty=1),
             40: ModelSizeShoes(size=40, length=25.5, qty=2)}
    shoes = ModelColorShoesShow(colors=['white', 'green'], sizes=sizes)
    list_pd_prod.append(ModelProductShow(id=258, type='shoes', name='con chak l 75', price_sell=425, module=shoes))
    return list_pd_prod
