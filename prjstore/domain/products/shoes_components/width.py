from contracts import contract


class Width:
    """
>>> width = Width(name='Wide', short_name='EE')
>>> width
Wide
>>> width.short_name
'EE'
    """

    def __init__(self, name: str, short_name: str) -> None:
        self.name: str = name
        self.short_name: str = short_name

    ###############################################################################################
    # name
    def __get_name(self) -> str:
        return self.__name

    @contract(name=str)
    def __set_name(self, name: str) -> None:
        self.__name = name

    name = property(__get_name, __set_name)

    ###############################################################################################
    # short_name
    def __get_short_name(self) -> str:
        return self.__short_name

    @contract(short_name=str)
    def __set_short_name(self, short_name: str) -> None:
        self.__short_name = short_name

    short_name = property(__get_short_name, __set_short_name)

    ###############################################################################################
    def __repr__(self) -> str:
        return self.name
