from dooby.fields import *
from dooby.model import Base

class Partner(Base):
    __tablename__ = "partners"
    id = KeyField()
    name = StringField()
    type = StringField()
    director = StringField()
    phone = StringField()
    rating = IntegerField()

    sales = RefTo("Sale", "partner")

    @property
    def total_sales(self):
        return sum(sale.total_price for sale in self.sales)

    @property
    def discount(self):
        ts = self.total_sales
        if ts < 10000:
            return 0
        elif ts < 50000:
            return 5
        elif ts < 300000:
            return 10
        else:
            return 15


class Product(Base):
    __tablename__ = "products"
    id = KeyField()
    name = StringField()
    category = StringField()
    price = FloatField()

    sales = RefTo("Sale", "product")


class Sale(Base):
    __tablename__ = "sales"
    id = KeyField()
    partner_id = ExternalKey("partners.id")
    product_id = ExternalKey("products.id")
    quantity = IntegerField()
    date = DateTimeField()

    partner = RefTo("Partner", "sales")
    product = RefTo("Product", "sales")

    @property
    def total_price(self):
        return (self.product.price if self.product else 0.0) * self.quantity
