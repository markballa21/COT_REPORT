from lxml import html
import requests
from datetime import datetime, timedelta
import numpy as np
import pandas as pd
from Excel import Excel


"""
A class that generates an excel full of scraped data
""" 
class Web_COT_Data_Scrape():


    """
    The initiator function
    name: list of asset names of the data we want to scrape
    year: the year we want to scrape the data from
    """
    def __init__(self, list_of_asset, year, time):
        self.year = year
        self.list_of_asset = list_of_asset
        self.time = time

        #number of columns in excel
        self.column_num = 13

        for asset in self.list_of_asset:
            data = self.get_all_data(asset)
            Excel(asset.name, data)


    """
    A function that scrapes data from a site by date
    """
    def web_scrape(self, date, link_key, ticket):

        url_legacy_futures = "https://www.tradingster.com/cot/legacy-futures/"+str(ticket)+"/"+str(date)
        parsed_content_legacy_futures = self.parse_web(url_legacy_futures)

        #There are cases when there is no Tuesday so I go to a Monday, thats the only second option
        if(parsed_content_legacy_futures.xpath('/ html / head / title/text()')[0] == '500 Internal Server Error'):
            #we change the date so we dont need to check the 2nd time in the futures
            date = datetime.strptime(date, '%Y-%m-%d') + timedelta(days=-1)
            date = date.strftime("%Y-%m-%d")
            url_legacy_futures = "https://www.tradingster.com/cot/legacy-futures/" + str(ticket) + "/" + str(date)
            parsed_content_legacy_futures = self.parse_web(url_legacy_futures)
            #If there is no Monday too to scrape, the year still hasn't ended.
            if (parsed_content_legacy_futures.xpath('/ html / head / title/text()')[0] == '500 Internal Server Error'):
                return None

        Long_Non_Commercial = parsed_content_legacy_futures.xpath('/html/body/div[1]/div/div/div[3]/div[2]/table/tbody/tr[2]/td[1]/text()')[0].replace(',', '')
        Long_Non_Commercial_Percent = parsed_content_legacy_futures.xpath('/html/body/div[1]/div/div/div[3]/div[2]/table/tbody/tr[6]/td[1]/text()')[0]
        Short_Non_Commercial = parsed_content_legacy_futures.xpath('/html/body/div[1]/div/div/div[3]/div[2]/table/tbody/tr[2]/td[2]/text()')[0].replace(',', '')
        Short_Non_Commercial_Percent = parsed_content_legacy_futures.xpath('/html/body/div[1]/div/div/div[3]/div[2]/table/tbody/tr[6]/td[2]/text()')[0]

        Long_Commercial = parsed_content_legacy_futures.xpath('/html/body/div[1]/div/div/div[3]/div[2]/table/tbody/tr[2]/td[4]/text()')[0].replace(',', '')
        Long_Commercial_Percent = parsed_content_legacy_futures.xpath('/html/body/div[1]/div/div/div[3]/div[2]/table/tbody/tr[6]/td[4]/text()')[0]
        Short_Commercial = parsed_content_legacy_futures.xpath('/html/body/div[1]/div/div/div[3]/div[2]/table/tbody/tr[2]/td[5]/text()')[0].replace(',', '')
        Short_Commercial_Percent = parsed_content_legacy_futures.xpath('/html/body/div[1]/div/div/div[3]/div[2]/table/tbody/tr[6]/td[5]/text()')[0]


        #again we use the link_key because we have 2 types of links
        url_futures = "https://www.tradingster.com/cot/futures/"+link_key+"/"+str(ticket)+"/"+str(date)
        parsed_content_futures = self.parse_web(url_futures)


        Long_Leveraged_Funds = parsed_content_futures.xpath('/html/body/div[1]/div/div/div[3]/div[2]/table/tbody/tr[3]/td[2]/text()')[0].replace(',', '')
        Long_Leveraged_Funds_Percent = parsed_content_futures.xpath('/html/body/div[1]/div/div/div[3]/div[2]/table/tbody/tr[3]/td[3]/text()')[0]
        Short_Leveraged_Funds = parsed_content_futures.xpath('/html/body/div[1]/div/div/div[3]/div[2]/table/tbody/tr[3]/td[5]/text()')[0].replace(',', '')
        Short_Leveraged_Funds_Percent = parsed_content_futures.xpath('/html/body/div[1]/div/div/div[3]/div[2]/table/tbody/tr[3]/td[6]/text()')[0]

        data = [date, Long_Non_Commercial, Long_Non_Commercial_Percent,
                Short_Non_Commercial, Short_Non_Commercial_Percent,

                Long_Leveraged_Funds, Long_Leveraged_Funds_Percent,
                Short_Leveraged_Funds, Short_Leveraged_Funds_Percent,

                Long_Commercial, Long_Commercial_Percent,
                Short_Commercial, Short_Commercial_Percent,

        ]
        print(data)
        return data

    def parse_web(self, url):
        response = requests.get(url)
        content = response.content
        parsed_content = html.fromstring(content)
        return parsed_content

    """
    A functions that return a DataFrame of all the data we scraped and manipulated
    """
    def get_all_data(self, asset):
        #asset_data
        link_key = asset.link_key
        ticket = asset.ticket

        #List of all Tuesday's in a year
        if(self.time == 1):
            list_of_dates = self.alltuesdays(self.year)
        elif(self.time == 0):
            day = datetime.today().weekday()
            #2 for wednesday, 3 for thursday
            if(day == 2 or day == 3):
                today = datetime.today() - timedelta(days=7)
            else:
                today = datetime.today() 
            offset = (today.weekday() - 1) % 7
            last_tuesday = (today - timedelta(days=offset)).strftime('%Y-%m-%d')
            list_of_dates = [last_tuesday]
        else:
            print("Something Went wrong with the dates")
            list_of_dates = []

        #generate the Dataframe 0 rows, X columns
        df = pd.DataFrame(columns=np.arange(self.column_num))

        #A loop that goes through all dates and scrapes the data of the same date
        for date in list_of_dates:
            data = self.web_scrape(date, link_key, ticket)
            #If the data is None, doesn't exist, It means the year hasn't ended yet and we no longer need to scrape
            if(data == None):
                print("end data")
                break

            #putting the data in the right row
            df.loc[len(df)] = data

        #reverse the dataframe
        df = df.loc[::-1]

        return df


    """
    A function that returns a list of all the dates of tuesday in the same year. Example, 2022-21-12
    year: A parameter for a year. Example, 2023
    """
    def alltuesdays(self, year):
        return pd.date_range(start=str(year), end=str(year + 1),
                freq='W-TUE').strftime('%Y-%m-%d').tolist()
