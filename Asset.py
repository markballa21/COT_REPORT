


class Asset():

    # fin in the link
    dict_data1 = {
        # Currencies
        'AUSTRALIAN DOLLAR': '232741', 'BRITISH POUND STERLING': '096742', 'CANADIAN DOLLAR': '090741',
        'EURO FX': '099741', 'JAPANESE YEN': '097741', 'SWISS FRANC': '092741', 'U.S. DOLLAR INDEX': '098662',
        'MEXICAN PESO': '095741', 'NEW ZEALAND DOLLAR': '112741', 'BITCOIN': '133741',

        # Stock Indexes
        'S&P 500 STOCK INDEX': '13874%2B', 'NASDAQ-100 STOCK INDEX (MINI)': '209742',
        'DOW JONES INDUSTRIAL AVG- x $5': '124603',
        'RUSSELL 2000 MINI INDEX FUTURE': '239742', 'E-MINI S&P 400 STOCK INDEX': '33874A',
        'E-MINI S&P 500 STOCK INDEX': '13874A',

        # Treasuries and Rates
        '30-DAY FEDERAL FUNDS': '045601', '3-MONTH EURODOLLARS': '132741', '2-YEAR U.S. TREASURY NOTES': '042601',
        '5-YEAR U.S. TREASURY NOTES': '044601', '10-YEAR U.S. TREASURY NOTES': '043602',
    }

    # disagg in the link
    dict_data2 = {
        # Energies
        'CRUDE OIL, LIGHT SWEET': '067651', 'GASOLINE BLENDSTOCK (RBOB)': '111659',
        '#2 HEATING OIL, NY HARBOR-ULSD': '022651', 'NATURAL GAS': '023651',

        # Grains
        'CORN': '002602', 'SOYBEANS': '005602', 'SOYBEAN OIL': '007601', 'SOYBEAN MEAL': '026603',
        'WHEAT-SRW': '001602',
        'WHEAT-HRW': '001612', 'WHEAT-HRSpring': '001626', 'OATS': '004603', 'ROUGH RICE': '039601',

        # Livestock
        'LIVE CATTLE': '057642', 'FEEDER CATTLE': '061641', 'LEAN HOGS': '054642',

        # Metals
        'GOLD': '088691', 'SILVER': '084691', 'COPPER-GRADE #1': '085692', 'PALLADIUM': '075651', 'PLATINUM': '076651',

        # Softs
        'COCOA': '073732', 'COTTON NO. 2': '033661', 'COFFEE C': '083731', 'SUGAR NO. 11': '080732',
        'FRZN CONCENTRATED ORANGE JUICE': '040701', 'RANDOM LENGTH LUMBER': '058643'
    }

    def __init__(self, name):
        self.name = name
        self.ticket = ''
        self.link_key = ''

        if(self.name in self.dict_data1):
            self.ticket = self.dict_data1[name]
            self.link_key = 'fin'
        elif(self.name in self.dict_data2):
            self.ticket = self.dict_data2[name]
            self.link_key = 'disagg'
