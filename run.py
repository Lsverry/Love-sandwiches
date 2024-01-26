import gspread
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT= gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('love_sandwiches')

def get_sales_data():
    """
    Get sales figures input from the user
    """
    while True:

        print("Please enter sales data from the last market.")
        print("Data should be six numbers, separated by commas.")
        print("Example: 10, 20, 30, 40, 50, 60\n")

        
        data_str = input("Enter your data here:\n")
        
        sales_data = data_str.split(",")
        

        if validate_data(sales_data):
            print("Data is valid")
            break
    
    return sales_data


def validate_data(values):
    """
    Inside the try, converts all string values into integers
    Raises ValueError if strings cannot be converted into int.
    or if there aren't exactly 6 values
    """

    try:
        values = [int(x) for x in values]
        if len(values) != 6:
            raise ValueError(f"Exactly 6 values required, you provided {len(values)}")
    except ValueError as e:
        print(f"Invalid data: {e}, please try again.\n")
        return False
    
    return True


def update_worksheet(data, worksheet):
    """
    Recieves a list of integers to be inserted into a worksheet
    """
    print(f"Updating {worksheet} worksheet....\n")

    worksheet_to_update = SHEET.worksheet(worksheet)
    worksheet_to_update.append_row(data) 
    print(f"{worksheet} worksheet updated successfully\n")


def calculte_surplus_data(sales_row):
    """
    Compare sales with stock and calculate the surplus for each item type
    """
    print("Calculating surplus data\n")
    stock = SHEET.worksheet("stock").get_all_values()
    stock_row = stock[-1]
    stock_row = [int(x) for x in stock_row]
    
    surplus_data = []
    for stock, sales in zip(stock_row, sales_row):
        surplus = stock - sales
        surplus_data.append(surplus)
    return surplus_data


def get_last_5_entries_sales():
    """
    Collects columns of data from sales worksheet
    """
    sales = SHEET.worksheet("sales")

    colums = []
    for column in range(1,7):
        column = sales.col_values(column)
        colums.append(column[-5:])
    return colums

def calculate_stock_data(data):
    """
    Calculate the average stock for each item type, adding 10%
    """
    print("Calculating stock data...\n")
    new_stock_data = []
    for column in data:
        int_column = [int(num) for num in column]
        average = sum(int_column) / len(int_column)
        stock_num = average * 1.1
        new_stock_data.append(round(stock_num))

    return new_stock_data
def main():
    """
    Run all program functions
    """
    data = get_sales_data()
    sales_data = [int(num) for num in data]
    update_worksheet(sales_data,"sales")
    new_surplus_data = calculte_surplus_data(sales_data)
    update_worksheet(new_surplus_data,"surplus")
    sales_columns = get_last_5_entries_sales()
    stock_data = calculate_stock_data(sales_columns)
    update_worksheet(stock_data,"stock")

main()

