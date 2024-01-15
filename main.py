
from Web_COT_Data_Scrape import Web_COT_Data_Scrape
from Asset import Asset

if __name__ == "__main__":
    list_of_asset = []
    while(True):
        print("Enter Name: (or type 'F' to finish)")
        name = str(input()).rstrip()
        if(name == 'F'):
            break
        else:
            list_of_asset.append(Asset(name))

    print("Enter year:")
    year = int(input())

    print("Last week (0) OR All year (1) ? ")
    time = int(input())

    Web_COT_Data_Scrape(list_of_asset, year, time)

