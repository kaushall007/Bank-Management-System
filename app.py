# app.py

from flask import Flask, jsonify, render_template, request, redirect, url_for
import csv
import os
import random
import time
import sys
import pathlib
import pickle

app = Flask(__name__)

class Account:
    def __init__(self):
        self.phoneNo = 0
        self.accNo = 0
        self.name = 'none'
        self.deposit = 0
        self.type = ''
        self.adrs = 'none'
        self.pin = ''
        self.last_login=time.ctime()

    def createAccount(self):
        print("\n\n")
        self.phoneNo = request.form.get("phoneNo")
        self.name = request.form.get("name")
        self.adrs = request.form.get("address")
        self.type = request.form.get("account_type")
        self.pin = request.form.get("pin")
        if (self.type.upper() == 'S' or self.type.upper() == 'C') and len(str(self.pin)) == 4:
            self.deposit = int(request.form.get("initial_amount"))
            self.accNo = random.randint(4211111111, 4222222222)
            print("\nLOADING")
            animation = ["....................."]
            for i in range(len(animation)):
                time.sleep(1)
                sys.stdout.write("." + animation[i % len(animation)])
                sys.stdout.flush()
            self.deposit += 100
            print("\n\nYOUR ACCOUNT NUMBER IS", self.accNo)
            self.writeAccountToCSV()
            return "Account created successfully! Your account number is {}".format(self.accNo)
            
        else:
            return "Invalid account type or PIN length should be 4."

    def writeAccountToCSV(self):
        with open('accounts.csv', mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([self.accNo,self.pin,self.name, self.phoneNo, self.adrs, self.type, self.deposit])

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/new_customer')
def new_customer():
    return render_template('new_customer.html')

@app.route('/create_account', methods=['POST'])
def create_account():
    account = Account()
    message = account.createAccount()
    return message

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/authenticate', methods=['POST'])
def authenticate():
    accNo = request.form.get("accNo")
    pin = request.form.get("pin")
    accounts = readAccountsFromCSV()
    for account in accounts:
        if account.accNo == accNo and account.pin == pin:
            # Redirect to dashboard with account information
            return redirect(url_for('dashboard', accNo=accNo))
    return "Login failed. Please check your account number and PIN."

@app.route('/dashboard/<accNo>')
def dashboard(accNo):
    account = getAccountByAccNo(accNo)
    if account:
        name = account.name
        deposit = account.deposit
        last_login = account.last_login
        # Pass the fetched data to the template
        return render_template('dashboard.html', name=name, accNo=accNo, balance=deposit, last_login=last_login)
    else:
        return "Account not found"

def getAccountByAccNo(accNo):
    # You need to implement this function to fetch account information from your data source (e.g., CSV file)
    accounts = readAccountsFromCSV()
    for account in accounts:
        if account.accNo == accNo:
            return account
    return None

#dashboard features functions
@app.route('/deposit_funds', methods=['GET', 'POST'])
def deposit_funds():
    if request.method == 'POST':
        
        amount = int(request.form.get('amount'))
        account = Account()  
        account.deposit += amount  
        return redirect(url_for('dashboard'))  
    return render_template('deposit_funds.html')  


@app.route('/withdraw_funds', methods=['GET', 'POST'])
def withdraw_funds():
    if request.method == 'POST':
        # Get the amount to withdraw from the form
        amount = int(request.form.get('amount'))

        account = Account()  
        account.deposit -= amount 

        # Redirect to the dashboard after withdrawing funds
        return redirect(url_for('dashboard'))

    # If it's a GET request, render the withdraw funds form
    return render_template('withdraw_fund.html')



@app.route('/check_balance', methods=['GET', 'POST'])
def check_balance():
    if request.method == 'POST':
        accNo = request.form.get("accNo")
        pin = request.form.get("pin")
        accounts = readAccountsFromCSV()
        for account in accounts:
            if account.accNo == accNo and account.pin == pin:
                return render_template('check_balance.html', balance=account.deposit)
        return render_template('check_balance.html', error_message="Invalid username or password.")
    else:
        return render_template('check_balance.html')

def readAccountsFromCSV():
    accounts = []
    file_path = 'accounts.csv'
    if os.path.exists(file_path):
        with open(file_path, mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) == 7:
                    account = Account()
                    account.accNo, account.pin, account.name, account.phoneNo, account.adrs, account.type, account.deposit = row
                    accounts.append(account)
                else:
                    print(f"Invalid row: {row}")
    return accounts

if __name__ == '__main__':
    app.run(debug=True)
