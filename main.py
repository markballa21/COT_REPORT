
from Web_COT_Data_Scrape import Web_COT_Data_Scrape


if __name__ == "__main__":
    print("Enter Name:")
    name = str(input())
    print("Enter start year:")
    year = int(input())
    Web_COT_Data_Scrape(name, year)

