from __future__ import print_function
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2 import service_account
from flask import Flask, request
from flask_restful import Resource, Api
import math

from functions.getTotalPricefunction import getTotalPrice
from functions.getAdvancefunction import getAdvance
from functions.getWeightChargefunction import getWeightCharge
from functions.getDeliveryChargefunction import getDeliveryCharge
from functions.getContactNumberfunction import getContactNumber
from functions.getAddressfunction import getAddress
from functions.getProductsfunction import getProducts

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# The ID and range of a sample spreadsheet.
# Take as user input?
SAMPLE_SPREADSHEET_ID = '1xl0OP_IhryWg4eXU5F8K6GoFVDKe0gpdNo5u13WjLlI'
SAMPLE_RANGE_NAME = 'Sheet1!A1:Z1000'

# just need to redefine this
SERVICE_ACCOUNT_FILE = 'cherie-notebook-cred.json'
credentials = None

credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)

service = build('sheets', 'v4', credentials=credentials)
sheet = service.spreadsheets()


def createSheet(sheetTitle):

    request = []
    request.append({'addSheet': {
        'properties': {
            'title': sheetTitle
        }
    }})
    response = sheet.batchUpdate(spreadsheetId=SAMPLE_SPREADSHEET_ID, body={
                                 'requests': request}).execute()


def getSheetID():
    metadata = sheet.get(spreadsheetId=SAMPLE_SPREADSHEET_ID).execute()
    sheetInfo = metadata.get("sheets")
    for sheeet in sheetInfo:
        if (sheeet.get("properties").get("title") == "Invoices"):
            return sheeet.get("properties").get("sheetId")
    # create worksheet named Invoices if not yet available
    createSheet("Invoices")
    metadata = sheet.get(spreadsheetId=SAMPLE_SPREADSHEET_ID).execute()
    sheetInfo = metadata.get("sheets")
    for sheeet in sheetInfo:
        if (sheeet.get("properties").get("title") == "Invoices"):
            return sheeet.get("properties").get("sheetId")

# Mergy boi for one table
# RowIndex += innerloopvar * 8
# ColumnIndex += outerloopvar * 5


def mergyboi(totallength, sheetId):
    requests = []
    for i in range(2):
        for j in range(math.ceil(totallength/2)):
            # C1-D2
            requests.append({'mergeCells': {
                'mergeType': 'MERGE_ALL',
                'range': {
                    'sheetId': sheetId,
                    'startColumnIndex': 2 + i*5,
                    'startRowIndex': 0 + j*8,
                    'endColumnIndex': 4 + i*5,
                    'endRowIndex': 2 + j*8
                }
            }})
            # A3-B3
            requests.append({'mergeCells': {
                'mergeType': 'MERGE_ALL',
                'range': {
                    'sheetId': sheetId,
                    'startColumnIndex': 0 + i*5,
                    'startRowIndex': 2 + j*8,
                    'endColumnIndex': 2 + i*5,
                    'endRowIndex': 3 + j*8
                }
            }})
            # A4-B5
            requests.append({'mergeCells': {
                'mergeType': 'MERGE_ALL',
                'range': {
                    'sheetId': sheetId,
                    'startColumnIndex': 0 + i*5,
                    'startRowIndex': 3 + j*8,
                    'endColumnIndex': 2 + i*5,
                    'endRowIndex': 5 + j*8
                }
            }})
            # A6-B6
            requests.append({'mergeCells': {
                'mergeType': 'MERGE_ALL',
                'range': {
                    'sheetId': sheetId,
                    'startColumnIndex': 0 + i*5,
                    'startRowIndex': 5 + j*8,
                    'endColumnIndex': 2 + i*5,
                    'endRowIndex': 6 + j*8
                }
            }})
            # A7-B7
            requests.append({'mergeCells': {
                'mergeType': 'MERGE_ALL',
                'range': {
                    'sheetId': sheetId,
                    'startColumnIndex': 0 + i*5,
                    'startRowIndex': 6 + j*8,
                    'endColumnIndex': 2 + i*5,
                    'endRowIndex': 7 + j*8
                }
            }})
            # C6-C7
            requests.append({'mergeCells': {
                'mergeType': 'MERGE_ALL',
                'range': {
                    'sheetId': sheetId,
                    'startColumnIndex': 2 + i*5,
                    'startRowIndex': 5 + j*8,
                    'endColumnIndex': 3 + i*5,
                    'endRowIndex': 7 + j*8
                }
            }})
            # D6-D7
            requests.append({'mergeCells': {
                'mergeType': 'MERGE_ALL',
                'range': {
                    'sheetId': sheetId,
                    'startColumnIndex': 3 + i*5,
                    'startRowIndex': 5 + j*8,
                    'endColumnIndex': 4 + i*5,
                    'endRowIndex': 7 + j*8
                }
            }})
    response = sheet.batchUpdate(spreadsheetId=SAMPLE_SPREADSHEET_ID, body={
                                 'requests': requests}).execute()


def formatInvoice(totallength, sheetId):
    requests = []
    for i in range(2):
        for j in range(math.ceil(totallength/2)):
            # A1 text bold, italic, fontSize
            requests.append({'repeatCell': {
                'range': {
                    'sheetId': sheetId,
                    'startColumnIndex': 0 + i*5,
                    'startRowIndex':  0 + j*8,
                    'endColumnIndex': 1 + i*5,
                    'endRowIndex': 1 + j*8
                },
                'cell': {
                    'userEnteredFormat': {
                        'textFormat': {'bold': True, 'fontSize': 20, 'italic': True}
                    }
                },
                'fields': 'userEnteredFormat(textFormat)'
            }})

            # A2 text bold
            requests.append({'repeatCell': {
                'range': {
                    'sheetId': sheetId,
                    'startColumnIndex': 0 + i*5,
                    'startRowIndex':  1 + j*8,
                    'endColumnIndex': 1 + i*5,
                    'endRowIndex': 2 + j*8
                },
                'cell': {
                    'userEnteredFormat': {
                        'textFormat': {'bold': True, }
                    }
                },
                'fields': 'userEnteredFormat(textFormat)'
            }})

            # C1-D2 text bold, fontSize and alignment
            requests.append({'repeatCell': {
                'range': {
                    'sheetId': sheetId,
                    'startColumnIndex': 2 + i*5,
                    'startRowIndex':  0 + j*8,
                    'endColumnIndex': 4 + i*5,
                    'endRowIndex': 2 + j*8
                },
                'cell': {
                    'userEnteredFormat': {
                        'textFormat': {'bold': True, 'fontSize': 20, },
                        'verticalAlignment': 'BOTTOM',
                        'horizontalAlignment': 'CENTER'
                    }
                },
                'fields': 'userEnteredFormat(textFormat, verticalAlignment, horizontalAlignment)'
            }})

            # A3-D3 text bold
            requests.append({'repeatCell': {
                'range': {
                    'sheetId': sheetId,
                    'startColumnIndex': 0 + i*5,
                    'startRowIndex':  2 + j*8,
                    'endColumnIndex': 4 + i*5,
                    'endRowIndex': 3 + j*8
                },
                'cell': {
                    'userEnteredFormat': {
                        'textFormat': {'bold': True, }
                    }
                },
                'fields': 'userEnteredFormat(textFormat)'
            }})

            # C6-D7 text bold
            requests.append({'repeatCell': {
                'range': {
                    'sheetId': sheetId,
                    'startColumnIndex': 2 + i*5,
                    'startRowIndex': 5 + j*8,
                    'endColumnIndex': 4 + i*5,
                    'endRowIndex': 7 + j*8
                },
                'cell': {
                    'userEnteredFormat': {
                        'textFormat': {'bold': True, }
                    }
                },
                'fields': 'userEnteredFormat(textFormat)'
            }})

            # A1 row height
            requests.append({'updateDimensionProperties': {
                'range': {
                    'sheetId': sheetId,
                    'dimension': 'ROWS',
                    'startIndex': 0 + j*8,
                    'endIndex': 1 + j*8
                },
                'properties': {'pixelSize': 38},
                'fields': 'pixelSize'
            }})

            # C-D column width
            requests.append({'updateDimensionProperties': {
                'range': {
                    'sheetId': sheetId,
                    'dimension': 'COLUMNS',
                    'startIndex': 2 + i*5,
                    'endIndex': 4 + i*5
                },
                'properties': {'pixelSize': 70},
                'fields': 'pixelSize'
            }})

            # A4-A5 row height and width
            requests.append({'updateDimensionProperties': {
                'range': {
                    'sheetId': sheetId,
                    'dimension': 'ROWS',
                    'startIndex': 3 + j*8,
                    'endIndex': 5 + j*8
                },
                'properties': {'pixelSize': 50},
                'fields': 'pixelSize'
            }})
            requests.append({'updateDimensionProperties': {
                'range': {
                    'sheetId': sheetId,
                    'dimension': 'COLUMNS',
                    'startIndex': 0 + i*5,
                    'endIndex': 2 + i*5
                },
                'properties': {'pixelSize': 115},
                'fields': 'pixelSize'
            }})

            # A4-A5 text wrap and alignment
            requests.append({'repeatCell': {
                'range': {
                    "sheetId": sheetId,
                    "startRowIndex": 3 + j*8,
                    "endRowIndex": 5 + j*8,
                    "startColumnIndex": 0 + i*5,
                    "endColumnIndex": 2 + i*5
                },
                'cell': {
                    'userEnteredFormat': {
                        'wrapStrategy': 'WRAP',
                        'verticalAlignment': 'TOP'
                    }
                },
                'fields': 'userEnteredFormat(wrapStrategy, padding, verticalAlignment)'
            }})

            # C3 Border
            requests.append({'repeatCell': {
                'range': {
                    'sheetId': sheetId,
                    'startColumnIndex': 2 + i*5,
                    'startRowIndex': 2 + j*8,
                    'endColumnIndex': 3 + i*5,
                    'endRowIndex': 3 + j*8
                },
                'cell': {
                    'userEnteredFormat': {
                        'borders': {
                            'top': {
                                'color': {'red': 0, 'green': 0, 'blue': 0},
                                'style': 'SOLID'
                            },
                            'left': {
                                'color': {'red': 0, 'green': 0, 'blue': 0},
                                'style': 'SOLID'
                            }
                        }
                    }
                },
                'fields': 'userEnteredFormat(borders)'
            }})

            # D3 Border
            requests.append({'repeatCell': {
                'range': {
                    'sheetId': sheetId,
                    'startColumnIndex': 3 + i*5,
                    'startRowIndex': 2 + j*8,
                    'endColumnIndex': 4 + i*5,
                    'endRowIndex': 3 + j*8
                },
                'cell': {
                    'userEnteredFormat': {
                        'borders': {
                            'top': {
                                'color': {'red': 0, 'green': 0, 'blue': 0},
                                'style': 'SOLID'
                            },
                            'right': {
                                'color': {'red': 0, 'green': 0, 'blue': 0},
                                'style': 'SOLID'
                            }
                        }
                    }
                },
                'fields': 'userEnteredFormat(borders)'
            }})

            # C4-C5 Border
            requests.append({'repeatCell': {
                'range': {
                    'sheetId': sheetId,
                    'startColumnIndex': 2 + i*5,
                    'startRowIndex': 3 + j*8,
                    'endColumnIndex': 3 + i*5,
                    'endRowIndex': 5 + j*8
                },
                'cell': {
                    'userEnteredFormat': {
                        'borders': {
                            'left': {
                                'color': {'red': 0, 'green': 0, 'blue': 0},
                                'style': 'SOLID'
                            }
                        }
                    }
                },
                'fields': 'userEnteredFormat(borders)'
            }})

            # D4-D5 Border
            requests.append({'repeatCell': {
                'range': {
                    'sheetId': sheetId,
                    'startColumnIndex': 3 + i*5,
                    'startRowIndex': 3 + j*8,
                    'endColumnIndex': 4 + i*5,
                    'endRowIndex': 5 + j*8
                },
                'cell': {
                    'userEnteredFormat': {
                        'borders': {
                            'right': {
                                'color': {'red': 0, 'green': 0, 'blue': 0},
                                'style': 'SOLID'
                            }
                        }
                    }
                },
                'fields': 'userEnteredFormat(borders)'
            }})

            # C6-C7 Border
            requests.append({'repeatCell': {
                'range': {
                    'sheetId': sheetId,
                    'startColumnIndex': 2 + i*5,
                    'startRowIndex': 5 + j*8,
                    'endColumnIndex': 3 + i*5,
                    'endRowIndex': 7 + j*8
                },
                'cell': {
                    'userEnteredFormat': {
                        'borders': {
                            'bottom': {
                                'color': {'red': 0, 'green': 0, 'blue': 0},
                                'style': 'SOLID'
                            },
                            'left': {
                                'color': {'red': 0, 'green': 0, 'blue': 0},
                                'style': 'SOLID'
                            }
                        }
                    }
                },
                'fields': 'userEnteredFormat(borders)'
            }})

            # D6-D7 Border
            requests.append({'repeatCell': {
                'range': {
                    'sheetId': sheetId,
                    'startColumnIndex': 3 + i*5,
                    'startRowIndex': 5 + j*8,
                    'endColumnIndex': 4 + i*5,
                    'endRowIndex': 7 + j*8
                },
                'cell': {
                    'userEnteredFormat': {
                        'borders': {
                            'bottom': {
                                'color': {'red': 0, 'green': 0, 'blue': 0},
                                'style': 'SOLID'
                            },
                            'right': {
                                'color': {'red': 0, 'green': 0, 'blue': 0},
                                'style': 'SOLID'
                            }
                        }
                    }
                },
                'fields': 'userEnteredFormat(borders)'
            }})

            # A7-B7 Border
            requests.append({'repeatCell': {
                'range': {
                    'sheetId': sheetId,
                    'startColumnIndex': 0 + i*5,
                    'startRowIndex': 6 + j*8,
                    'endColumnIndex': 2 + i*5,
                    'endRowIndex': 7 + j*8
                },
                'cell': {
                    'userEnteredFormat': {
                        'borders': {
                            'top': {
                                'color': {'red': 0, 'green': 0, 'blue': 0},
                                'style': 'SOLID'
                            },
                            'left': {
                                'color': {'red': 0, 'green': 0, 'blue': 0},
                                'style': 'SOLID'
                            },
                            'right': {
                                'color': {'red': 0, 'green': 0, 'blue': 0},
                                'style': 'SOLID'
                            },
                            'bottom': {
                                'color': {'red': 0, 'green': 0, 'blue': 0},
                                'style': 'SOLID'
                            }
                        }
                    }
                },
                'fields': 'userEnteredFormat(borders)'
            }})

    # E width
    requests.append({'updateDimensionProperties': {
        'range': {
            'sheetId': sheetId,
            'dimension': 'COLUMNS',
            'startIndex': 4,
            'endIndex': 5
        },
        'properties': {'pixelSize': 50},
        'fields': 'pixelSize'
    }})
    response = sheet.batchUpdate(spreadsheetId=SAMPLE_SPREADSHEET_ID, body={
                                 'requests': requests}).execute()


def writeinvoice(invoices, sheetId):
    numInvoices = len(invoices)
    mergyboi(numInvoices, sheetId)
    data = []
    odd = 0
    even = 0
    for i in range(numInvoices):
        if i % 2 == 0:
            rangeMul = 'Invoices!A' + str(even*8+1)
            data.append({
                'range': rangeMul,
                'values': invoices[i]
            },)
            even += 1
        else:
            rangeMul = 'Invoices!F' + str(odd*8+1)
            data.append({
                'range': rangeMul,
                'values': invoices[i]
            },)
            odd += 1
    body = {
        'valueInputOption': "RAW",
        'data': data
    }
    invoicewrite = sheet.values().batchUpdate(
        spreadsheetId=SAMPLE_SPREADSHEET_ID, body=body).execute()
    formatInvoice(numInvoices, sheetId)


def generateInvoices(dataframe):
    invoices = []
    temp = dataframe[(dataframe['Order Status'] == 'Dispatch')]
    names = temp['Facebook Name'].unique()
    for name in names:
        finalDataframe = temp[(temp['Facebook Name'] == name)]
        invoices.append(makeInvoice(finalDataframe, name))
    writeinvoice(invoices, getSheetID())


def makeInvoice(dataframe, name):
    sum = getTotalPrice(dataframe)
    adv = getAdvance(dataframe)
    deliveryCharge = getDeliveryCharge(dataframe, sum, adv)
    contactNumber = getContactNumber(dataframe)
    address = getAddress(dataframe)

    invoiceData = []
    totalItems = "Number of items: "
    totalItems = totalItems + str(len(dataframe))

    invoiceData.append(["Chérie", "", "Invoice"])
    invoiceData.append(["Delivery to"])
    invoiceData.append([name, "", "Total Price", sum])
    invoiceData.append([address, "", "Delivery \nCharge", deliveryCharge])
    invoiceData.append(["", "", "Advance", adv])
    invoiceData.append(
        [contactNumber, "", "Total Due", sum-adv+deliveryCharge])
    invoiceData.append([totalItems])
    invoiceData.append(["------------------------------------------"])
    return invoiceData
