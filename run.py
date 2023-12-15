import gspread
from google.oauth2.service_account import Credentials
from pprint import pprint

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('love_sandwiches')

def get_sales_data():
    """
    Get sales figures in put from user
    Run a while loop to collect a valid string of data from a user
    via the terminal, which must be a string of 6 numbers, separated
    by commas. The loop repeatedly request data, until it valid!
    """
    while True: #The loop repeatedly request data, until it valid!
        print('Please enter sales data from the last market.')
        print('Data should be six numbers, separated with commas.')
        print('Example: 10,20,3,40,50,60\n')
    
        data_str = input("Enter your data here: ")
    
        sales_data = data_str.split(",")

        if validate_data(sales_data):
            print("Data is valid!")
            break
    
    return sales_data

def validate_data(values):
    """
    inside the try,converts all strings values into integers.
    Raise valueError if strings cannot be converted into int,
    or if there aren't exactly 6 values.
    """
    try:
        [int(value) for value in values]
        if len(values) != 6:
            raise ValueError(
                f"Exactly 6 values required, you provided {len(values)}"
            )
    except ValueError as e:
        """
        The {e} here is from except ValueError as e is a
        variable that was assigned a value from the
        the raise [ValueError] to print all together in case input 
        occur error
        """
        print(f"Invalid data: {e}, please try again.\n")
        return False
    
    return True

   #updating our sales worksheet

def update_sales_worksheet(data):
    """
    update sales worksheet, add new role with the list data provided.
    """
    print("Updating sales worksheet....\n")
    sale_worksheet = SHEET.worksheet('sales')
    sale_worksheet.append_row(data)
    print('Sales worksheet updated successfully.\n')

def calculate_surplus_data(sales_row):
    """
    Compare sales with stock and calculate the surplus for each item type.

    The surplus is defined as the sales figure subtracted from the stock:
    - Positive surplus indicates waste
    - Negative surplus indicates extra made when stock was sold out.
    """
    print("Calculating surplus data...\n")
    stock = SHEET.worksheet("stock").get_all_values()
    #print out the last role from the list worksheet
    stock_row = stock[-1]
    print(stock_row)

def main():
    """
    Run all program functions
    """
    data = get_sales_data()
    sales_data = [int(num) for num in data]
    update_sales_worksheet(sales_data)
    calculate_surplus_data(sales_data)


print("Welcome to Love Sand-wiches Data Automation")
main()
