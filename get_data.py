'''
In this file we will get neccessary csv-data from Alpha Vantage service

example usage: python3 get_data.py -f TIME_SERIES_DAILY -F msft.csv -s MSFT

downloaded file will appear in given path with given name

'''

import requests
import csv
import argparse

# getting api key for alpha vantage from file
with open("AV_token.txt", "r") as f:
    api_key = f.readline()

functions = ["TIME_SERIES_INTRADAY", "TIME_SERIES_DAILY", 
    "TIME_SERIES_DAILY_ADJUSTED","TIME_SERIES_WEEKLY", 
    "TIME_SERIES_WEEKLY_ADJUSTED", "TIME_SERIES_MONTHLY", 
    "TIME_SERIES_MONTHLY_ADJUSTED"]

def get_bestmatch(res_list):
    max_score = max(res_list[:][1])
    idx = res_list[:][1].index(max_score)
    name = res_list[idx][0]

    return name

def checking_args(function, symbol):
    if not (function in functions):
        raise NameError

    # checking symbol through another request(search request)
    req = "https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords=" + \
                                symbol + "&apikey=" + api_key + "&datatype=csv"
    data = requests.get(req)
    reader = csv.reader(data.text.splitlines())
    
    # making list of possible symbols and their match scores
    res_list = []
    for row in reader:
        # skipping head of table
        if row[0] == "symbol":
            continue
        res_list.append((row[0], row[-1]))
    # in case symbol wasnt found we are taking symbol with best score
    if not (symbol in res_list[:][0]):
        name = get_bestmatch(res_list)
        print("Wrong symbol... Did you mean " + name + "? (yes | no)")
        confirm = input("Your answer is: ")
        if confirm == "yes":
            return name
        else:
            raise NameError
    else:
        return ""

if __name__ == "__main__":
    # parsing arguments through argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--foo', type=str, required=True, \
                    help='str fmt = \"TIME_SERIES_[your mode]\"')
    parser.add_argument('-p', '--path', type=str, required=True, \
                    help='just type the name of file wuth csv extension')
    parser.add_argument('-s', '--symbol', type=str, required=True, \
                    help='string code of company(example:\"MSFT\")')

    args = parser.parse_args()

    function = args.foo
    csv_file = args.path.split("/")[-1]
    symbol = args.symbol

    new_symbol = checking_args(function, symbol)
    if new_symbol != "":
        symbol = new_symbol
    save_path = args.path

    # making request
    if function == "TIME_SERIES_DAILY" or function == "TIME_SERIES_INTRADAY":
        req = "https://www.alphavantage.co/query?function=" + function + \
            "&symbol=" + symbol + "&apikey=" + api_key + "&datatype=csv&outputsize=full"
        if function == "TIME_SERIES_INTRADAY":
            req += "&interval=" + input("Choose interval(1 or 5): ") + "min"
    else:
        req = "https://www.alphavantage.co/query?function=" + function + \
            "&symbol=" + symbol + "&apikey=" + api_key + "&datatype=csv"
    print(req)
    data = requests.get(req)

    # reading response and writing to the file
    with open(save_path, 'w') as f: 
        writer = csv.writer(f) 
        reader = csv.reader(data.text.splitlines()) 

        for row in reader: 
            writer.writerow(row)