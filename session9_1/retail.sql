.mode column
.headers on
PRAGMA foreign_keys = ON;

CREATE TABLE Product (
    ProductID INTEGER PRIMARY KEY,
    Title TEXT,
    Description TEXT,
    Price NUMERIC(11, 2),
    Cost NUMERIC(11, 2)
);

CREATE TABLE Orders (
    OrderID INTEGER PRIMARY KEY,
    CustomerID INTEGER,
    DateOrdered DATETIME,
    MonthOrdered INTEGER,
    FOREIGN KEY (CustomerID) REFERENCES Customer(CustomerID)
);

CREATE TABLE OrderItems (
    OrderID INTEGER,
    ProductID INTEGER,
    Quantity INTEGER,
    FOREIGN KEY (OrderID) REFERENCES Orders(OrderID),
    FOREIGN KEY (ProductID) REFERENCES Product(ProductID)
);

CREATE TABLE Warehouse (
    WarehouseID INTEGER PRIMARY KEY,
    WarehouseName TEXT,
    AddressLine1 TEXT,
    AddressLine2 TEXT,
    AddressLine3 TEXT
);

CREATE TABLE Inventory (
    WarehouseID INTEGER,
    ProductID INTEGER,
    Quantity INTEGER,
    FOREIGN KEY (WarehouseID) REFERENCES Warehouse(WarehouseID),
    FOREIGN KEY (ProductID) REFERENCES Product(ProductID)
);

CREATE TABLE Supplier (
    SupplierID INTEGER PRIMARY KEY,
    SupplierName TEXT,
    AddressLine1 TEXT,
    AddressLine2 TEXT,
    AddressLine3 TEXT,
    PhoneNumber TEXT,
    Email TEXT
);
CREATE TABLE SupplierProduct(
    SupplierID INTEGER,
    ProductID INTEGER,
    DaysLeadTime INTEGER,
    Cost NUMERIC(11, 2),
    FOREIGN KEY (SupplierID) REFERENCES Supplier(SupplierID),
    FOREIGN KEY (ProductID) REFERENCES Product(ProductID)
);

CREATE TABLE SupplierOrders(
    SupplierOrderID INTEGER PRIMARY KEY,
    SupplierID INTEGER,
    ProductID INTEGER,
    WarehouseID INTEGER,
    Quantity INTEGER,
    Status TEXT,
    DateOrdered DATE,
    DateDue DATE,
    FOREIGN KEY (SupplierID) REFERENCES Supplier(SupplierID),
    FOREIGN KEY (ProductID) REFERENCES Product(ProductID),
    FOREIGN KEY (WarehouseID) REFERENCES Warehouse(WarehouseID)
);

CREATE TABLE Customer (
    CustomerID INTEGER PRIMARY KEY,
    FirstName TEXT,
    Surname TEXT,
    AddressLine1 TEXT,
    AddressLine2 TEXT,
    AddressLine3 TEXT,
    PhoneNumber TEXT,
    Email TEXT
);

INSERT INTO Product VALUES (3001, "Widget", "Widge all your worries away!", 99.95, 23.05);
INSERT INTO Product VALUES (3002, "Wodget", "Wodge all your worries away!", 199.95, 123.05);

INSERT INTO Orders VALUES (1000, 2000, "2025-01-01 10:00:00", 202501);
INSERT INTO OrderItems VALUES (1000, 3001, 1);
INSERT INTO OrderItems VALUES (1000, 3002, 2);

INSERT INTO Warehouse VALUES (4001, "ABC Warehouse", "1374 Elkview Drive", "Fort Lauderdale", "FL 33301");
INSERT INTO Warehouse VALUES (4002, "XYZ Warehouse", "1576 Walnut Street", "Jackson", "MS 39211");

INSERT INTO Inventory VALUES (4001,3001,3);
INSERT INTO Inventory VALUES (4001,3002,1);
INSERT INTO Inventory VALUES (4002,3001,1);
INSERT INTO Inventory VALUES (4002,3002,4);

INSERT INTO Supplier VALUES (5001, "Widge Suppliers Ltd", "3316 Whitetail Lane", "Irving", "TX 75039","479-357-6159", "TimothyCSilva@widge.com");
INSERT INTO Supplier VALUES (5002, "Wodge Suppliers PLC", "390 Clarksburg Park Road", "Scottsdale", "AZ 85256", "252-441-7555", "JohnAWilley@wodge.co.uk");

INSERT INTO SupplierProduct VALUES (5001, 3001, 3, 23.05);
INSERT INTO SupplierProduct VALUES (5001, 3002, 20, 999.99);
INSERT INTO SupplierProduct VALUES (5002, 3001, 20, 9999.99);
INSERT INTO SupplierProduct VALUES (5002, 3002, 5, 123.05);

INSERT INTO SupplierOrders VALUES (6001, 5001, 3001, 4001, 99, "ORDERED", "2025-01-15", "2025-01-21");
INSERT INTO SupplierOrders VALUES (6002, 5001, 3001, 4002, 99, "DELIVERED", "2025-01-16", "2025-01-23");

INSERT INTO Customer VALUES (2000, "Gertrud", "Karr", "1709 Woodridge Lane", "Memphis", "TN 38110", "559-309-6624", "gkarr@dayrep.com");
INSERT INTO Customer VALUES (2001, "Clara", "Tang", "500 Retreat Avenue", "York", "ME 03909", "312-367-6954", "clara_tang@armyspy.com");

/*Write a transaction for a delivery from the Widge supplier which has just arrived at the ABC warehouse and unloaded 99 new Widgets.*/
BEGIN TRANSACTION;
UPDATE Inventory SET Quantity = Quantity + 99 WHERE WarehouseID=4001 AND ProductID=3001;
SELECT Quantity FROM Inventory WHERE WarehouseID=4001 AND ProductID=3001;
END TRANSACTION;

/*Write a transaction for a Customer order of 500 Wodgets which places an order with the cheapest supplier.*/
BEGIN TRANSACTION;
INSERT INTO Orders VALUES (1001, 2000, "2025-01-01 10:00:00", 202501);
INSERT INTO OrderItems VALUES (1001, 3002, 500);
INSERT INTO SupplierOrders VALUES (6003, 5002, 3002, 500, "ORDERED", "2025-01-15", "2025-01-21")
END TRANSACTION;

/*What statements would be needed to update a customer's details to their new address, 
while still maintaining referential integrity? */
BEGIN TRANSACTION;
UPDATE Customer SET AddressLine1 = "...", AddressLine2 = "...", AddressLine3 = "..." WHERE CustomerID = 2000
END TRANSACTION;

/*What steps would we need to take to delete a product from the Product table, while still maintaining referential integrity? 
Put all of these statements together into a transaction. What collateral damage would be done if a product was deleted? 
(In practice, a product will almost never get deleted unless it has never been referenced in any other table.)
*/


/*Either update every transaction involding the product to reference e.g. some "deleted product" id instead, 
or remove the transactions*/
/*If we remove an item from the Product table, we would be unable to compute revenue 
from goods sold and costs from goods bought. That is, any transaction involving that product.*/
BEGIN TRANSACTION;
UPDATE Orders ...
--Probably you would only delete a product if it was not in inventory, i.e. quantity=0
DELETE FROM Inventory WHERE ProductID = 3001
DELETE FROM Product WHERE ProductID = 3001
END TRANSACTION;
