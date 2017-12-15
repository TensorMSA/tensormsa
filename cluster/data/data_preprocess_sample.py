import pandas as pd


def data_preprocess_by_file(train ):

    train['AS1'] ,train['AS2'] = train['A1'].str.split(' ').str
    train = train.drop(train.loc[train['AS1'] == '`'].index)
    train['AS2' ] =train['AS2'].astype(int)
    train['A2'] = train['A2'].map( {'3X1': 0, '2Y1': 1, '2X1': 2, '1X1': 3, '3Y1': 4, '4X1': 5} ).astype(int)
    train['A3'] = train['A3'].map( {'K': 0, 'P': 1} ).astype(int)
    train['A4'] = train['A4'].fillna('W')
    train['A4'] = train['A4'].map( {'Q': 0, 'G': 1, 'K': 2, 'C': 3 ,'M': 4, 'L': 5, 'W': 6, 'A': 7,
                                    'R': 8, 'X': 9, 'B': 10, 'E': 11 ,'6': 12, '7': 13, 'P': 14, 'O': 15,
                                    'H': 16, '8': 17, '9': 18, 'N': 19 ,'5': 20, 'I': 21, '2': 22, '3': 23 ,'V': 24, 'Z': 25 } ).astype(int)
    train['A5'] = train['A5'].map( {'H3': 0, 'H5': 1, 'H2': 2, 'H1': 3 } ).astype(int)
    train['A6'] = train['A6'].map( {'Y': 0, 'N': 1} ).astype(int)
    train['A7'] = train['A7'].map( {'Y': 0, 'N': 1} ).astype(int)
    train['A8'] = train['A8'].fillna('Z')
    train['A8'] = train['A8'].map( {'Z': 0, 'B': 1, 'A': 2, 'E': 3} ).astype(int)
    train['A9'] = train['A9'].fillna('Z')
    train['A9'] = train['A9'].map( {'Z': 0, 'KAN_3_ROLL': 1, 'POH_2_ROLL': 2, 'POH_1_ROLL': 3 ,'KAN_2_ROLL' :4, 'KAN_1_ROLL' :5
         ,'KAN_4_ROLL' :6} ).astype(int)

    from sklearn import preprocessing
    le = preprocessing.LabelEncoder()
    A12_Classes = ['EN-DD', 'API_MID', 'SAE10', 'GENERAL', 'PHT_L', 'PHT_H', 'API_HI', 'JS-STKT590', 'PHT_M', 'UPCG', 'JS-SM4', 'JS-SG', 'EN-S', 'JS-SPFH5', 'PHY_L', 'JS-STK', 'SP-A3', 'POSH', 'POSEIDON500', 'SPECIFICATION_CD_ETC', 'ATOS', 'PHY_M', 'UPCQ', 'JS-SAPH', 'YPHC-NS', 'ECOGI', 'PHH100', 'UPEG', 'HPDQ', 'MP', 'SAE15B40T', 'A1011', 'PK', 'API-B', 'PHC0', 'A36', 'POSP_L', 'A715', 'RSCZMZBBZZ', 'HA', 'RBBZZZZZZZ', 'GBAZZZFCZZ', 'JS-STKM', 'POSP_M', 'TP-MRT', 'PHH800', 'NPS400', 'HICARBON', 'API-K55', 'UPPO270', 'POSA10', 'PS410', 'POSP_H', 'RBSZZZZZZZ', 'A178-D', 'AHSS', 'VAA1', 'JS-SNCM220']
    le.fit(A12_Classes)
    train['A12'] = le.transform(train['A12'])
    train['A13'] = train['A13'].fillna('Z')
    train['A13'] = train['A13'].map( {'Z': 0, 'HIGH_TENSILE': 1, 'LOAD_SIZE': 2 } ).astype(int)
    train['A14'] = train['A14'].fillna('Z')
    train['A14'] = train['A14'].map( {'Z': 0, 'N': 1, 'Q': 2, 'Y': 2 , 'R': 2 , 'L': 2 , 'F': 2 , 'K': 2  } ).astype(int)

    train['A16'] = train['A16'].map( {'Y': 0, 'N': 1 } ).astype(int)
    train['A17'] = train['A17'].map( {'H': 0, 'K': 1 ,'XXX': 2, 'R': 3, 'L': 4, '6': 5, 'D': 6, '3': 7, '5': 8,  '7': 9} ).astype(int)
    train['A18'] = train['A18'].map( {'FINAL': 0, 'REQUIRED': 1 ,'OCCURED': 2 } ).astype(int)



    train.head()
    train.dtypes
    train.columns

    return train

