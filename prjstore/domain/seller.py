from contracts import contract


class Seller:
    """
>>> seller = Seller('Igor')
>>> seller
<Seller: name=Igor>
>>> seller.name = 'Anna'
>>> seller.name
'Anna'
    """

    def __init__(self, name: str):
        self.name: str = name

    ###############################################################################################
    # name
    def __get_name(self) -> str:
        return self.__name

    @contract(name=str)
    def __set_name(self, name: str) -> None:
        self.__name = name

    name = property(__get_name, __set_name)

    def __repr__(self):
        return f'<{self.__class__.__name__}: name={self.name}>'
