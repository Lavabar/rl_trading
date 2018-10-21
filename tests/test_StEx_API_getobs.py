import sys
sys.path.append("../")

from TradeAPI import TestApp

if __name__ == '__main__':

    app = TestApp("127.0.0.1", 7497, 1)

    ## lets get positions
    positions_list = app.get_current_positions()
    print(positions_list)

    ## get the account name from the position
    ## normally you would know your account name
    accountName = positions_list[1][0]

    ## and accounting information
    accounting_values = app.get_accounting_values(accountName)
    print(accounting_values)

    for i in range(len(accounting_values)):
        if accounting_values[i][0] == 'CashBalance':
            print("CashBalance = [" + str(i) + "]")
        elif accounting_values[i][0] == 'NetLiquidation':
            print("NetLiquidation = [" + str(i) + "]")

    ## these values are cached
    ## if we ask again in more than 5 minutes it will update everything
    accounting_updates = app.get_accounting_updates(accountName)
    print(accounting_updates)

app.disconnect()