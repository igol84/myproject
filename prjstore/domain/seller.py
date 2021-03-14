from contracts import contract

class Seller:
    '''
>>> seller = Seller('Igor')
>>> seller
<Seller: name=Igor>
>>> seller.name = 'Anna'
>>> seller.name
'Anna'
    '''
    def __init__(self, name):
        self.name = name

    def get_name(self):
        return self._name

    @contract(name=str)
    def set_name(self, name):
        self._name = name

    name = property(get_name, set_name)

    def __repr__(self):
        return f'<{self.__class__.__name__}: name={self.name}>'