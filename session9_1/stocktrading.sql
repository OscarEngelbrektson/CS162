.mode column
.headers on
PRAGMA foreign_keys = ON;

CREATE TABLE Companies (
    CompanyID INTEGER PRIMARY KEY,
    CompanyName TEXT,
    Shares INTEGER
);

CREATE TABLE Desks (
    DeskID INTEGER PRIMARY KEY,
    DeskName TEXT,
    Shares INTEGER
);

CREATE TABLE StartingPoint (
    StockID INTEGER PRIMARY KEY,
    DeskID INTEGER,
    CompanyID INTEGER,
    Quantity INTEGER,
    FOREIGN KEY (DeskID) REFERENCES Desks(DeskID),
    FOREIGN KEY (CompanyID) REFERENCES Companies(CompanyID)
);

CREATE TABLE Orders (
    OrderID INTEGER PRIMARY KEY,
    DeskID INTEGER,
    CompanyID INTEGER,
    OrderType TEXT,
    Quantity INTEGER,
    Price INTEGER,
    Status TEXT,
    FilledBy INTEGER,
    FOREIGN KEY (DeskID) REFERENCES Desks(DeskID),
    FOREIGN KEY (CompanyID) REFERENCES Companies(CompanyID)
    FOREIGN KEY (FilledBy) REFERENCES Companies(CompanyID)
);

CREATE TABLE Summary (
    CompanyID INTEGER,
    NumOrdersPlaced INTEGER,
    NumOrdersFilled INTEGER,
    NumShares INTEGER,
    NumDollars NUMERIC,
    FOREIGN KEY (CompanyID) REFERENCES Companies(CompanyID)
);

INSERT INTO Orders VALUES (1, 1, 1, "Buy", 1, 1, "Open", "None") --Order placed

/*Now write a transaction that updates the portfolios for both the selling company and the buying company.*/
BEGIN TRANSACTION;
UPDATE  Orders SET  Status="Complete", FilledBy=2 WHERE OrderID == 1; --Order filled
UPDATE Summary SET NumOrdersPlaced = NumOrdersPlaced+1, NumShares=NumShares+1, NumDollars=NumDollars+1 WHERE CompanyID=1
UPDATE Summary SET NumOrdersPlaced = NumOrdersFilled+1, NumShares=NumShares+1, NumDollars=NumDollars+1 WHERE CompanyID=2
END TRANSACTION;

/*What would happen if the statements were not wrapped in a transaction, and everything went smoothly? 
What would happen if the set of updates were interrupted halfway through?*/

/*Wrapping statements in transactions ensures that if a set of updates are interrupted before every update is complete, 
none of the updates go through. Thus, I think problems from not wrapping statements in a transaction 
would only arise if a set of updates were interupted halfway through. If they were not wrapped, we could for example
have it shown that the same shares are held by different desks, if the buy part of the update went through without the sell part going through. 
This is obviously problematic, making transaction wrapping well worth it..*/



