from pydantic import BaseModel

from prjstore.db.schemas.sale_line_item import SaleLineItem


class EditSLIPrice(BaseModel):
    old_sli: SaleLineItem
    new_sli: SaleLineItem