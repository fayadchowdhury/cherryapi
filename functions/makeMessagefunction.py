from functions.getTotalPricefunction import getTotalPrice
from functions.getAdvancefunction import getAdvance
from functions.getWeightChargefunction import getWeightCharge
from functions.getDeliveryChargefunction import getDeliveryCharge
from functions.getContactNumberfunction import getContactNumber
from functions.getAddressfunction import getAddress
from functions.getProductsfunction import getProducts

import re

def makeMessage(dataframe, name):
    sum = getTotalPrice(dataframe)
    adv = getAdvance(dataframe)
    wc = getWeightCharge(dataframe)
    deliveryCharge = getDeliveryCharge(dataframe, sum, adv)
    deliveryArea = ""
    if (deliveryCharge > 100):
        deliveryArea = "130 or 160 Outside Dhaka"
    else:
        deliveryArea = "100 Inside Dhaka"
    contactNumber = getContactNumber(dataframe)
    address = getAddress(dataframe)

    message = name + "\n"
    message = getProducts(dataframe, message)
    message += "\nTotal - " + str(sum) + " BDT\n"
    weirdFlag = False
    for val in dataframe['WC']:
      if (val != ''):
        if ( re.search('[a-zA-Z]+', val) == None ):
          continue
        else:
          weirdFlag = True
    if ( weirdFlag == True ):
        due = sum - adv
      else:
        due = sum - adv + wc

      if ( weirdFlag == False and wc > 0 ):
        message+="Weight charge - " + str(wc) + " BDT\n"

      message+="Advanced - " + str(adv) + " BDT\n"
      if ( weirdFlag == True ):
        message += "Due = " + str(due) + " BDT + Delivery Charge (" +  deliveryArea + ") + Weight Charge (According to the list above)\n"
      else:
        message += "Due = " + str(due) + " BDT + Delivery Charge (" +  deliveryArea + ")\n"
      message += "\nDelivery Details:\n"
      message+="Contact Number: " + contactNumber + "\n"
      message+="Address: " + address + "\n"
      message += "\n"
    return message