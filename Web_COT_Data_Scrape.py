from lxml import html
import requests
from datetime import datetime, timedelta
import numpy as np
import pandas as pd


"""
A class that generates an excel full of scraped data
"""
class Web_COT_Data_Scrape():


    #fin in the link
    dict_data1 = {
        #Currencies
        'AUSTRALIAN DOLLAR': '232741', 'BRITISH POUND STERLING': '096742', 'CANADIAN DOLLAR': '090741',
        'EURO FX': '099741', 'JAPANESE YEN': '097741', 'SWISS FRANC': '092741', 'U.S. DOLLAR INDEX': '098662',
        'MEXICAN PESO': '095741', 'NEW ZEALAND DOLLAR': '112741', 'BITCOIN': '133741',

        #Stock Indexes
        'S&P 500 STOCK INDEX': '13874%2B', 'NASDAQ-100 STOCK INDEX (MINI)': '209742', 'DOW JONES INDUSTRIAL AVG- x $5': '124603',
        'RUSSELL 2000 MINI INDEX FUTURE': '239742', 'E-MINI S&P 400 STOCK INDEX': '33874A', 'E-MINI S&P 500 STOCK INDEX': '13874A',

        #Treasuries and Rates
        '30-DAY FEDERAL FUNDS': '045601', '3-MONTH EURODOLLARS': '132741', '2-YEAR U.S. TREASURY NOTES': '042601',
        '5-YEAR U.S. TREASURY NOTES': '044601', '10-YEAR U.S. TREASURY NOTES': '043602',
    }

    #disagg in the link
    dict_data2 = {
        #Energies
        'CRUDE OIL, LIGHT SWEET':'067651', 'GASOLINE BLENDSTOCK (RBOB)': '111659',
        '#2 HEATING OIL, NY HARBOR-ULSD': '022651', 'NATURAL GAS': '023651',

        #Grains
        'Corn': '002602', 'SOYBEANS': '005602', 'SOYBEAN OIL': '007601', 'SOYBEAN MEAL': '026603', 'WHEAT-SRW': '001602',
        'WHEAT-HRW': '001612', 'WHEAT-HRSpring': '001626', 'OATS': '004603', 'ROUGH RICE': '039601',

        #Livestock
        'LIVE CATTLE': '057642', 'FEEDER CATTLE': '061641', 'LEAN HOGS': '054642',

        #Metals
        'GOLD': '088691', 'SILVER': '084691', 'COPPER-GRADE #1': '085692', 'PALLADIUM': '075651', 'PLATINUM': '076651',

        #Softs
        'COCOA': '073732', 'COTTON NO. 2': '033661', 'COFFEE C': '083731', 'SUGAR NO. 11': '080732',
        'FRZN CONCENTRATED ORANGE JUICE': '040701', 'RANDOM LENGTH LUMBER': '058643'
                       }


    """
    The initiator function
    name: name of the data we want to scrape
    year: the year we want to scrape the data from
    """
    def __init__(self, name,year):
        self.year = year
        self.name = name

        #the ticket of a name
        self.ticket = ""
        #the option is either "fin" or "disagg" in the links
        self.link_key = ""

        #get the ticket by the name we got from the user
        data1 = self.dict_data1.keys()
        data2 = self.dict_data2.keys()
        for i in data1:
            if(self.name == i):
                self.ticket = self.dict_data1.get(i)
                self.link_key = "fin"
                break
        if(self.ticket == ""):
            for i in data2:
                if (self.name == i):
                    self.ticket = self.dict_data2.get(i)
                    self.link_key = "disagg"
                    break

        if (self.ticket == ""):
            print("Wrong name")

        data = self.get_all_data()
        self.write_excel(data)


    """
    A function that scrapes data from a site by date
    """
    def web_scrape(self, date):

        url_legacy_futures = "https://www.tradingster.com/cot/legacy-futures/"+str(self.ticket)+"/"+str(date)
        response_legacy_futures = requests.get(url_legacy_futures)
        content_legacy_futures = response_legacy_futures.content
        parsed_content_legacy_futures = html.fromstring(content_legacy_futures)

        #There are cases when there is no Tuesday so I go to a Monday, thats the only second option
        if(parsed_content_legacy_futures.xpath('/ html / head / title/text()')[0] == '500 Internal Server Error'):
            #we change the date so we dont need to check the 2nd time in the futures
            date = datetime.strptime(date, '%Y-%m-%d') + timedelta(days=-1)
            date = date.strftime("%Y-%m-%d")
            url_legacy_futures = "https://www.tradingster.com/cot/legacy-futures/" + str(self.ticket) + "/" + str(date)
            response_legacy_futures = requests.get(url_legacy_futures)
            content_legacy_futures = response_legacy_futures.content
            parsed_content_legacy_futures = html.fromstring(content_legacy_futures)
            #If there is no Monday too to scrape, the year still hasn't ended.
            if (parsed_content_legacy_futures.xpath('/ html / head / title/text()')[0] == '500 Internal Server Error'):
                return None

        Long_Non_Commercial = parsed_content_legacy_futures.xpath('/html/body/div[1]/div/div/div[3]/div[2]/table/tbody/tr[2]/td[1]/text()')[0].replace(',', '')
        Long_Non_Commercial_Change = \
            parsed_content_legacy_futures.xpath(
                '/html/body/div[1]/div/div/div[3]/div[2]/table/tbody/tr[4]/td[1]/span/text()')[0].replace(',', '')
        Long_Non_Commercial_Percent = parsed_content_legacy_futures.xpath('/html/body/div[1]/div/div/div[3]/div[2]/table/tbody/tr[6]/td[1]/text()')[0]
        Short_Non_Commercial = parsed_content_legacy_futures.xpath('/html/body/div[1]/div/div/div[3]/div[2]/table/tbody/tr[2]/td[2]/text()')[0].replace(',', '')
        Short_Non_Commercial_Change = \
        parsed_content_legacy_futures.xpath('/html/body/div[1]/div/div/div[3]/div[2]/table/tbody/tr[4]/td[2]/span/text()')[0].replace(',', '')
        Short_Non_Commercial_Percent = parsed_content_legacy_futures.xpath('/html/body/div[1]/div/div/div[3]/div[2]/table/tbody/tr[6]/td[2]/text()')[0]

        Long_Commercial = parsed_content_legacy_futures.xpath('/html/body/div[1]/div/div/div[3]/div[2]/table/tbody/tr[2]/td[4]/text()')[0].replace(',', '')
        Long_Commercial_Change = \
        parsed_content_legacy_futures.xpath('/html/body/div[1]/div/div/div[3]/div[2]/table/tbody/tr[4]/td[4]/span/text()')[0].replace(',', '')
        Long_Commercial_Percent = parsed_content_legacy_futures.xpath('/html/body/div[1]/div/div/div[3]/div[2]/table/tbody/tr[6]/td[4]/text()')[0]
        Short_Commercial = parsed_content_legacy_futures.xpath('/html/body/div[1]/div/div/div[3]/div[2]/table/tbody/tr[2]/td[5]/text()')[0].replace(',', '')
        Short_Commercial_Change = \
        parsed_content_legacy_futures.xpath('/html/body/div[1]/div/div/div[3]/div[2]/table/tbody/tr[4]/td[5]/span/text()')[0].replace(',', '')
        Short_Commercial_Percent = parsed_content_legacy_futures.xpath('/html/body/div[1]/div/div/div[3]/div[2]/table/tbody/tr[6]/td[5]/text()')[0]


        #again we use the link_key because we have 2 types of links
        url_futures = "https://www.tradingster.com/cot/futures/"+self.link_key+"/"+str(self.ticket)+"/"+str(date)
        response_futures = requests.get(url_futures)
        content_futures = response_futures.content
        parsed_content_futures = html.fromstring(content_futures)


        Long_Leveraged_Funds = parsed_content_futures.xpath('/html/body/div[1]/div/div/div[3]/div[2]/table/tbody/tr[3]/td[2]/text()')[0].replace(',', '')
        Long_Leveraged_Funds_Change = \
        parsed_content_futures.xpath('/html/body/div[1]/div/div/div[3]/div[2]/table/tbody/tr[3]/td[2]/span/text()')[0].replace(',', '')
        Long_Leveraged_Funds_Percent = parsed_content_futures.xpath('/html/body/div[1]/div/div/div[3]/div[2]/table/tbody/tr[3]/td[3]/text()')[0]
        Short_Leveraged_Funds = parsed_content_futures.xpath('/html/body/div[1]/div/div/div[3]/div[2]/table/tbody/tr[3]/td[5]/text()')[0].replace(',', '')
        Short_Leveraged_Change = \
        parsed_content_futures.xpath('/html/body/div[1]/div/div/div[3]/div[2]/table/tbody/tr[3]/td[5]/span/text()')[0].replace(',', '')
        Short_Leveraged_Funds_Percent = parsed_content_futures.xpath('/html/body/div[1]/div/div/div[3]/div[2]/table/tbody/tr[3]/td[6]/text()')[0]


        data = [date, int(Long_Non_Commercial)+int(Short_Non_Commercial), int(Long_Non_Commercial) - int(Short_Non_Commercial), 0,
                Long_Non_Commercial, Long_Non_Commercial_Change, Long_Non_Commercial_Percent, 0,
                Short_Non_Commercial, Short_Non_Commercial_Change, Short_Non_Commercial_Percent, 0,

                "LINE",

                int(Long_Leveraged_Funds) + int(Short_Leveraged_Funds), int(Long_Leveraged_Funds) - int(Short_Leveraged_Funds), 0,
                Long_Leveraged_Funds, Long_Leveraged_Funds_Change, Long_Leveraged_Funds_Percent, 0,
                Short_Leveraged_Funds, Short_Leveraged_Change, Short_Leveraged_Funds_Percent, 0,

                "LINE",

                int(Long_Commercial) + int(Short_Commercial), int(Long_Commercial) - int(Short_Commercial), 0,
                Long_Commercial, Long_Commercial_Change, Long_Commercial_Percent, 0,
                Short_Commercial, Short_Commercial_Change, Short_Commercial_Percent, 0,
                ]

        return data


    """
    A functions that return a DataFrame of all the data we scraped and manipulated
    """
    def get_all_data(self):
        #List of all Tuesday's in a year
        list_of_dates = self.alltuesdays(self.year)

        #generate the Dataframe 0 rows, 36 columns
        df = pd.DataFrame(columns=np.arange(36))

        #A loop that goes through all dates and scrapes the data of the same date
        for date in list_of_dates:
            data = self.web_scrape(date)
            #If the data is None, doesn't exist, It means the year hasn't ended yet and we no longer need to scrape
            if(data == None):
                print("end data")
                break

            #Manipulating the data with the week before(2 weeks sum), the first row cant be manipulated,
            #there is no row before.
            if(len(df) > 0):

                last_data = df.loc[len(df) - 1]

                data[3] = int(data[2]) - int(last_data[2])
                data[7] = int(data[5]) + int(last_data[5])
                data[11] = int(data[9]) + int(last_data[9])

                data[15] = int(data[14]) - int(last_data[14])
                data[19] = int(data[17]) + int(last_data[17])
                data[23] = int(data[21]) + int(last_data[21])

                data[27] = int(data[26]) - int(last_data[26])
                data[31] = int(data[29]) + int(last_data[29])
                data[35] = int(data[33]) + int(last_data[33])

            print(data)
            #putting the data in the right row
            df.loc[len(df)] = data

        #reverse the dataframe
        df = df.loc[::-1]

        return df


    """
    A function that generates an excel file with all the data that we scraped
    dataFrame: A Data Frame object of data
    """
    def write_excel(self, dataFrame):

        writer = pd.ExcelWriter('COT_REPORT.xlsx', engine='openpyxl')
        dataFrame.to_excel(writer, sheet_name='COT_REPORT', index=False, startrow=6, header=False)
        writer.close()



    """
    A function that returns a list of all the dates of tuesday in the same year. Example, 2022-21-12
    year: A parameter for a year. Example, 2023
    """
    def alltuesdays(self, year):
        return pd.date_range(start=str(year), end=str(year + 1),
                freq='W-TUE').strftime('%Y-%m-%d').tolist()



