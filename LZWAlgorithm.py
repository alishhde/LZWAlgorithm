# Seyedali Shohadaalhosseini
from itertools import chain

import matplotlib.pyplot
from matplotlib import image as mpimg
from numpy import array


def main():
    print("Welcome!")
    data_Symbols, img_pixels_matrix = ReadFromInput()
    print("We're initialing the table base on your input image...")
    initTable = initTheTableWithAllLen1Symbols(data_Symbols)
    print("Initialization finished!")
    print("We're Encoding the input image...")
    outputCode, dictTable = LZWEncoding(initTable, img_pixels_matrix)
    print("Encoding finished..")
    print("We're decoding the coded image..")
    decodedMatrix = LZWDecoding(dictTable, outputCode)
    message = showTheDecodedData(decodedMatrix)
    print(message)
    # output Checker
    # print("\nThis is main Code: \n", len(img_pixels_matrix[2]))
    # print("\nThis is decoded Matrix\n", len(decodedMatrix[2]))
    # print("\nThis is main Code: \n", img_pixels_matrix[2])
    # print("\nThis is decoded Matrix\n", decodedMatrix[2])


def ReadFromInput(imagePath='D:\Teachers\DR  M. Rostaee\Multimedia\Exercises\HW1\img0-gray.jpg'):
    img_pixels_matrix = mpimg.imread(imagePath)
    data_Symbols = list(set(chain(*img_pixels_matrix)))  # here we have flattened our list
    return data_Symbols, img_pixels_matrix


def LZWEncoding(dictTable, data, image=True):
    generatedCode = list()
    global coder_counter
    data = data.tolist()
    if image:
        # LineController = 0
        for eachLine in data:
            tempCodeList = list()
            flag1 = False
            flag2 = False
            EOFLine_Flag = False
            symbolToSearch = ""
            line2 = 0
            for eachSymbolIndex in range(len(eachLine)):
                if flag1:
                    try:
                        before = symbolToSearch
                        symbolToSearch = symbolToSearch + "-" + "{}".format(eachLine[eachSymbolIndex+1])
                    except IndexError:
                        pass
                    flag1 = False
                    flag2 = True
                else:
                    try:
                        symbolToSearch = "{}".format(eachLine[eachSymbolIndex]) + "-" + "{}".format(eachLine[eachSymbolIndex+1])
                    except IndexError:
                        symbolToSearch = "{}".format(eachLine[eachSymbolIndex])
                        pass
                dictKeys = list(dictTable.keys())
                if symbolToSearch in dictKeys:
                    if eachSymbolIndex == len(eachLine) - 1:
                        EOFLine_Flag = True
                    else:
                        flag1 = True
                    continue
                else:
                    flag1 = False
                    coder_counter += 1
                    dictTable[symbolToSearch] = coder_counter
                    if flag2:
                        tempCodeList.append(dictTable["{}".format(before)])
                        flag2 = False
                    else:
                        tempCodeList.append(dictTable["{}".format(eachLine[eachSymbolIndex])])
                line2 += 1
                if line2 == 299:
                    break
            if EOFLine_Flag:
                tempCodeList.append(dictTable["{}".format(symbolToSearch)])
            generatedCode.append(tempCodeList)

            # print(LineController)
            # if LineController == 100:
            #     break
            # LineController += 1
    return generatedCode, dictTable


def LZWDecoding(dictTable, outputCode):
    decodedMatrix = []
    for eachLineOfCode in outputCode:
        tempDecode = list()
        for eachCode in eachLineOfCode:
            # Find the symbol from the dictTable
            allCodeIn = list(dictTable.values())
            allCodeKeyIn = list(dictTable.keys())
            findThisCodeIndex = allCodeIn.index(eachCode)
            ThisCodeKeyIs = allCodeKeyIn[findThisCodeIndex]
            codesToAdd = ThisCodeKeyIs.split("-")
            for code in codesToAdd:
                tempDecode.append(int(code))
        decodedMatrix.append(tempDecode)
    return decodedMatrix


def showTheDecodedData(dataToShow):
    # First we convert it to the array
    dataArray = array(dataToShow)
    print(dataArray)
    matplotlib.pyplot.imshow(dataArray, cmap='gray')
    matplotlib.pyplot.imsave("LZW Image.jpg", dataArray, cmap='gray')
    matplotlib.pyplot.show()
    return "Your image has been saved successfully"


# Table initialization
def initTheTableWithAllLen1Symbols(inputData):
    """
    :param inputData: our input data
    :return: returns the table with all strings length one
    """
    global coder_counter
    dataDict = dict()  # dataDict = {symbol:Code}
    for code in range(len(inputData)):
        dataDict["{}".format(inputData[code])] = code
        coder_counter = code
    return dataDict


if __name__ == '__main__':
    coder_counter = 0
    main()
