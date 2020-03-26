import sqlalchemy

from sqlalchemy import create_engine
engine = create_engine('sqlite:///:memory:', echo = True)
engine.connect()

from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

from sqlalchemy import Column, Integer, String, ForeignKey, Numeric
from sqlalchemy.orm import relationship, sessionmaker

#Recreate tables
class Product(Base):
    __tablename__ = 'products'
    ProductID = Column(Integer, primary_key=True)
    Title = Column(String)
    Description = Column(String)
    Price = Column(Numeric)
    Cost = Column(Numeric)

class Orders(Base):
    __tablename__ = 'orders'
    OrderID = Column(Integer, primary_key=True)
    CustomerID = Column(Integer, ForeignKey("customers.CustomerID"))
    DateOrdered = Column(String)
    MonthOrdered = Column(Integer)

class OrderItems(Base):
    __tablename__ = 'orderItems'
    OrderID = Column(Integer, ForeignKey("orders.OrderID"), primary_key=True)
    ProductID = Column(Integer, ForeignKey("products.ProductID"))
    Quantity = Column(Integer)

class Warehouse(Base):
    __tablename__ = 'warehouse'
    WarehouseID = Column(Integer, primary_key=True)
    WarehouseName = Column(String)
    AddressLine1 = Column(String)
    AddressLine2 = Column(String)
    AddressLine3 = Column(String)

class Inventory(Base):
    __tablename__ = 'inventory'
    RowID = Column(Integer, ForeignKey("warehouse.WarehouseID"), primary_key=True)
    WarehouseID = Column(Integer, ForeignKey("warehouse.WarehouseID"))
    ProductID = Column(Integer, ForeignKey("products.ProductID"))
    Quantity = Column(Integer)
    Quantity = Column(String)

class Supplier(Base):
    __tablename__ = 'supplier'
    SupplierID = Column(Integer, primary_key=True)
    SupplierName = Column(String)
    AddressLine1 = Column(String)
    AddressLine2 = Column(String)
    AddressLine3 = Column(String)
    PhoneNumber = Column(String)
    Email = Column(String)


class SupplierProduct(Base):
    __tablename__ = 'supplierProduct'
    SupplierID = Column(Integer, ForeignKey("supplier.SupplierID"), primary_key=True)
    ProductID = Column(Integer, ForeignKey("products.ProductID"))
    DaysLeadTime = Column(Integer)
    Cost = Column(Numeric)

class SupplierOrders(Base):
    __tablename__ = 'supplierOrders'
    SupplierOrderID = Column(Integer, primary_key=True)
    SupplierID = Column(Integer, ForeignKey("supplier.SupplierID"))
    ProductID = Column(Integer, ForeignKey("products.ProductID"))
    WarehouseID = Column(Integer, ForeignKey("warehouse.WarehouseID"))
    Quantity = Column(Integer)
    Status = Column(String)
    DateOrdered = Column(String)
    DateDue = Column(String)

class Customer(Base):
    __tablename__ = 'customers'
    CustomerID = Column(Integer, primary_key=True)
    FirstName = Column(String)
    Surname = Column(String)
    AddressLine1 = Column(String)
    AddressLine2 = Column(String)
    AddressLine3 = Column(String)
    PhoneNumber = Column(String)
    Email = Column(String)

Base.metadata.create_all(engine)

#Insert data
product_list = [Product(ProductID=3001, Title="Widget",Description="", Price=1, Cost=1),
                Product(ProductID=3001, Title="Wodget",Description="", Price=1, Cost=1)]

order_list = [Orders(OrderID=1000, CustomerID=2000, DateOrdered="2025-01-01 10:00:00", MonthOrdered=202501)]

orderItems_list = [OrderItems(OrderID=1000, ProductID=3001, Quantity=1),
                    OrderItems(OrderID=1000, ProductID=3001, Quantity=1)]

warehouse_list = [Warehouse(WarehouseID=4001, WarehouseName="ABC Warehouse", AddressLine1="1374 Elkview Drive", AddressLine2="Fort Lauderdale", AddressLine3="FL 33301"),
                Warehouse(WarehouseID=4002, WarehouseName="XYZ Warehouse", AddressLine1="1576 Walnut Street", AddressLine2="Jackson", AddressLine3="MS 39211")]

inventory_list = [Inventory(WarehouseID=4001, ProductID=3001, Quantity=3),
                Inventory(WarehouseID=4001, ProductID=3002, Quantity=1),
                Inventory(WarehouseID=4002, ProductID=3001, Quantity=1),
                Inventory(WarehouseID=4002, ProductID=3002, Quantity=4)]

supplier_list = [Supplier(SupplierID=5001, SupplierName="Widge Suppliers Ltd", AddressLine1="3316 Whitetail Lane", AddressLine2="Irving", AddressLine3="TX 75039", PhoneNumber="479-357-6159", Email="TimothyCSilva@widge.com"),
                Supplier(SupplierID=5002, SupplierName="Wodge Suppliers Ltd", AddressLine1="3316 Whitetail Lane", AddressLine2="Irving", AddressLine3="TX 75039", PhoneNumber="479-357-6159", Email="TimothyCSilva@widge.com")]

supplierProduct_list = [SupplierProduct(SupplierID=5001, ProductID=3001, DaysLeadTime=3, Cost=1),
                        SupplierProduct(SupplierID=5001, ProductID=3002, DaysLeadTime=20, Cost=1),
                        SupplierProduct(SupplierID=5002, ProductID=3001, DaysLeadTime=20, Cost=10),
                        SupplierProduct(SupplierID=5002, ProductID=3002, DaysLeadTime=3, Cost=1123)]

supplierOrder_list = [SupplierOrders(SupplierOrderID=6001, SupplierID=5001, ProductID=3001, WarehouseID=4001, Quantity=99, Status="Ordered", DateOrdered="2025-01-15", DateDue="2025-01-21"),
                        SupplierOrders(SupplierOrderID=6002, SupplierID=5001, ProductID=3001, WarehouseID=4002, Quantity=99, Status="Delivered", DateOrdered="2025-01-16", DateDue="2025-01-23")]

customer_list = [Customer(CustomerID=2000, FirstName="Gertrud", Surname="Karr", AddressLine1="3316 Whitetail Lane", AddressLine2="Irving", AddressLine3="TX 75039", PhoneNumber="479-357-6159", Email="TimothyCSilva@widge.com"),
                Customer(CustomerID=2001, FirstName="Clara", Surname="Tang", AddressLine1="3316 Whitetail Lane", AddressLine2="Irving", AddressLine3="TX 75039", PhoneNumber="479-357-6159", Email="TimothyCSilva@widge.com")]
from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=engine)
session = Session()
session.add_all(product_list)
session.add_all(order_list)
session.add_all(orderItems_list)
session.add_all(warehouse_list)
session.add_all(inventory_list)
session.add_all(supplier_list)
session.add_all(supplierProduct_list)
session.add_all(supplierOrder_list)
session.add_all(customer_list)
session.commit()

#Replicate queries

#/*Write a transaction for a delivery from the Widge supplier which has just arrived at the ABC warehouse and unloaded 99 new Widgets.*/
session.query(Inventory).filter(Inventory.WarehouseID==4001 and Inventory.ProductID==3001).\
        update({Inventory.Quantity:Inventory.Quantity+99})
#Select: see that update went through
print(session.query(Inventory).filter_by(Inventory.WarehouseID==4001 and Inventory.ProductID==3001).all())

# Write a transaction for a Customer order of 500 Wodgets
new_transaction = [Orders(OrderID=1001, CustomerID=2000, DateOrdered="2025-01-01 10:00:00", MonthOrdered=202501),
                    OrderItems(OrderID=1000, ProductID=3001, Quantity=500),
                    SupplierOrders(SupplierOrderID=6003, SupplierID=5002, ProductID=3002, WarehouseID=4001, Quantity=500, Status="Ordered", DateOrdered="2025-01-15", DateDue="2025-01-21")]
session.add_all(new_transaction)