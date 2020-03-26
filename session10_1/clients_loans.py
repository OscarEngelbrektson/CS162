import sqlalchemy

from sqlalchemy import create_engine
engine = create_engine('sqlite:///:memory:', echo = True)
engine.connect()

from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

from sqlalchemy import Column, Integer, String, ForeignKey, Numeric
from sqlalchemy.orm import relationship, sessionmaker

class Client(Base):
    __tablename__ = 'clients'
    clientnumber = Column(Integer, ForeignKey('loans.clientnumber'), primary_key=True)
    firstname = Column(String)
    surname = Column(String)
    email = Column(String)
    phone = Column(String)

    def __repr__(self):
        return '<Client(clientnumber={0}, firstname={1}, surname={2},email={3}, phone={4})>'.format(self.clientnumber, self.firstname, self.surname, self.email, self.phone)

class Loan(Base):
    __tablename__ = 'loans'
    accountnumber = Column(Integer, primary_key=True)
    clientnumber = Column(Integer)
    startdate = Column(Integer)
    startmonth = Column(Integer)
    term = Column(Integer)
    remaining_term = Column(Integer)
    principaldebt = Column(Numeric)
    accountlimit = Column(Numeric)
    balance = Column(Numeric)
    status = Column(String)

    def __repr__(self):
        return '<Loan(accountnumber={0}, clientnumber={1}, startdate={2}, startmonth={3}, term={4}, remaining_term={5}, principaldebt={6}, accountlimit={7}, balance={8}, status={9})>'.format(self.accountnumber, self.clientnumber, self.startdate, self.startmonth, self.term, self.remaining_term, self.principaldebt, self.accountlimit, self.balance, self.status)

Base.metadata.create_all(engine)


#2. Write an Insert Statement
client_list = [Client(clientnumber=1, firstname='Carl', surname='Steln', email='carl.steln@gmail.com', phone='(512) 432-4321'),
                Client(clientnumber=2, firstname='Nils', surname='Schyffert', email='nils@aasd.com', phone='(615) 123-4355')]
loan_list = [Loan(accountnumber=1,clientnumber=1,startdate='2017-11-01 10:00:00', startmonth=201702, term=34, remaining_term=23, principaldebt=10000.00, accountlimit=15000.00, balance=10000.00, status='NORMAL'),
            Loan(accountnumber=2,clientnumber=2,startdate='2018-01-01 10:00:00', startmonth=201802, term=12, remaining_term=4, principaldebt=1000.00, accountlimit=1500.00, balance=1000.00, status='NORMAL')]

from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=engine)
session = Session()
session.add_all(client_list)
session.add_all(loan_list)
session.commit()

# 3. Write write an update query and a Select query
from sqlalchemy import update

#UPDATE: Person with account number 1 has now Paid off their debt.
session.query(Loan).filter(Loan.accountnumber==1).\
        update({Loan.status:"PAID OFF", Loan.principaldebt:0})

#Select: see that update went through
print(session.query(Loan).filter_by(accountnumber=1).all())