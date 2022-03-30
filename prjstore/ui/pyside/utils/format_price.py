from typing import Union


def format_price(value: Union[int, float]) -> str:
    if type(value) == float and value % 1 == 0:
        value = f'{int(value):,}'
    else:
        value = f'{value:,.2f}'
    return value


if __name__ == '__main__':
    assert format_price(5.0) == '5'
    assert format_price(5.2) == '5.20'
