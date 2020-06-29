"""
Information Theory
by prof. reuven cohen
course assignment

student: Agai Maor
ID:     305544546

Intro:
this python file should be located with the dickens.txt file in the same folder to work
by running it, it will produce a compressed file (with a matching name)
and a decompressed file (for the compressed one obviously)

Abstract:
the algorithm used includes a LZ compression followed by parsing and a huffman coding algorithm
"""

import time
from queue import PriorityQueue


def compressedParser(compressedList):
    # parser method for the LZ compression output
    parsed = bytearray()
    for i in range(len(compressedList)):
        parsed += int(compressedList[i]).to_bytes(3, 'big')
    return parsed


def deparsser(parsedlist):
    # deparser method to the LZ decompression method
    b = [byte for byte in bytearray(parsedlist)]
    b = [b[i:i + 3] for i in range(0, len(b), 3)]
    outlist = []
    for b0, b1, b2 in b:
        tonum = int.from_bytes(bytearray([b0, b1, b2]), 'big')
        outlist.append(tonum)
    return outlist


def LZtestProc(parssedCompressed, LZcompresseddata, origninalText):
    # this method preforms test for the LZ compression (unused in implementation)
    unparsed = deparsser(parssedCompressed)
    print("comparing to original unparsed...")
    for i in range(len(unparsed)):
        if unparsed[i] != LZcompresseddata[i]:
            print("location= ", i, " unparsed value= ", str(unparsed[i]), "compresseddata value= ",
                  str(compresseddata[i]))
    uncompressed = lz().decompress(unparsed)
    # compare the uncompressed string to the original text
    print("comparing to original text...")
    print('compression and decompression ended successfully') if uncompressed == origninalText else print(
        'error occurred')
    print('original string length= ', len(origninalText), origninalText[-5:])
    print('uncompressed length= ', len(uncompressed), uncompressed[-5:])
    for i in range(len(origninalText)):
        if uncompressed[i] != origninalText[i]:
            print("location= ", i, " uncompressed value= ", str(uncompressed[i]), "original value= ",
                  str(origninalText[i]))


def HuffTestProc(HuffCompressed, LZcompressedData):
    # this function will get the huffman compressed file and will decompress it and check if
    # the decompression performed well and outputs mismatches (unused it the implementation)
    uncompressedHuff = huffman().decompress(HuffCompressed)
    unparsedHuff = deparsser(uncompressedHuff)
    for i in range(len(LZcompressedData)):
        if unparsedHuff[i] != LZcompressedData[i]:
            print("location= ", i, " Huffcompressed value= ", str(unparsedHuff[i]), "LZcompressedData value= ",
                  str(LZcompressedData[i]))
    return 1


def compressionProcess(textToCompress):
    # this method handles the entire compression process
    # it preforms LZ compression and then huffman compression
    print("starting compression process")
    # starting lz compression process
    LZCompressor = lz()
    LZCompressedData = LZCompressor.copmress(textToCompress)
    parsedCompressed = compressedParser(LZCompressedData)
    # starting huffman compression process
    huffCompressed = huffman().compress(parsedCompressed)
    print("finished compression process")
    return huffCompressed


def decompressionProcess(textToDecompress):
    # this method handles the entire decompression process
    print("starting decompression process")
    uncompressedHuff = huffman().decompress(textToDecompress)
    unparsedHuff = deparsser(uncompressedHuff)
    LZdecompressed = lz().decompress(unparsedHuff)
    print("finished decompression process")
    return LZdecompressed


def main():
    # read textFile into a string
    with open('dickens.txt', 'r', encoding='cp1252') as txtfile:
        print("opening file")
        originalText = txtfile.read()
        print("finished opening file")
    overallcompressiontimestart = time.time()
    compressData = compressionProcess(originalText)
    '''test procedure-- you may uncomment to make it work
    # uncompressedData=decompressionProcess(compressData)
     if uncompressedData==originalText:
        print ("compression and decompression ended successfully")
    # run test procedure or write compressed to file
    # LZtestProc(parsedCompressed,LZCompressedData, originalText)
    # run Huffman compression test
    # HuffTestProc(huffCompressed, LZCompressedData)'''
    print('starting writing to file')
    with open('Information_Theory_Compressed_File.txt', 'w+b') as binfile:
        binfile.write(compressData)
    print("finished writing file in ", time.time() - overallcompressiontimestart, 'seconds')
    print('starting with decompression process')
    print('opening compressed file')
    with open('Information_Theory_Compressed_File.txt', 'rb') as binfile:
        compressDataFromFile=binfile.read()
    overalldecompressiontimestart = time.time()
    decompressedData=decompressionProcess(compressDataFromFile)
    with open('Information_Theory_deCompressed_File.txt', 'w+',encoding='cp1252') as decompressfile:
        decompressfile.write(decompressedData)
    print("finished writing file in ", time.time() - overalldecompressiontimestart, 'seconds')


class lz():
    # LZ compression class implements compression and decompression
    def __init__(self):
        pass

    def copmress(self, data):
        # this methos handles LZ compression on data
        indexes = dict()
        # initialize dictionary with 256 cp1252 symbols
        for i in range(1, 255):
            if i != 129 and i != 141 and i != 144 and i != 143 and i != 157:
                indexes[bytes([i]).decode('cp1252')] = i
        indexCounter = 255
        charOffset = 0
        sequence = data[charOffset]
        compressed = []
        # actual compression loop
        routine = len(data) - 1
        lastverifiedseq = ''
        startTime = time.time()
        while charOffset < routine:
            nextchar = data[charOffset + 1]
            if sequence in indexes.keys():
                lastverifiedseq = sequence
                sequence += nextchar
                charOffset += 1
            # sequence doesnt exist
            else:
                indexes[sequence] = indexCounter
                indexCounter += 1
                compressed.append(indexes[lastverifiedseq] if lastverifiedseq != '' else indexes[sequence[-1]])
                # charOffset += 1
                sequence = data[charOffset]
                lastverifiedseq = ''
        compressed.append(indexes[lastverifiedseq])
        compressed.append(indexes[nextchar])
        endTime = time.time()
        print('LZ compression ended in =', endTime - startTime, 'Seconds')
        return compressed

    def decompress(self, toDecompress):
        # gets a list of lists and decompresses it
        diction = dict()
        # initialize dictionary with 256 cp1252 symbols
        for i in range(255):
            if i != 129 and i != 141 and i != 144 and i != 143 and i != 157:
                diction[i] = bytes([i]).decode('cp1252')
        indexCounter = 255
        starttime = time.time()  # timer
        o = toDecompress[0]
        outputstring = []  # create output list
        outputstring.append(diction[o])
        for i in range(1, len(toDecompress)):
            n = toDecompress[i]
            if n not in diction.keys():
                s = diction[o]
                s = s + c
            else:
                s = diction[n]
            outputstring.append(s)
            c = s[0]
            diction[indexCounter] = diction[o] + c
            indexCounter += 1
            o = n
        print('LZ decompression ended in', time.time() - starttime,'Seconds')
        return ''.join(outputstring)


class huffman():
    # this method handles the huffman compression and decompression process
    def __init__(self):
        pass

    def compress(self, parsedByteArray):
        # huffman compression method
        print('starting huffman compression process')
        b = dict()
        for by in parsedByteArray:
            b[by] = b[by] + 1 if (by in b.keys()) else 1
        b = sorted(b.items(), key=lambda x: x[1])  # sorting from least frequent to most
        PQ = PriorityQueue()
        # iterate through all places in the array
        for value in b:
            # create node for each item, must check for the comparison of the priority queue and how its set
            node = huffNode(value[0], string='', isLeaf=True)
            # push node into the queue
            PQ.put(tuple((value[1], node)))
        print('building huffman coding tree')
        while PQ.qsize() > 1:
            # pop two nodes from the queue(they are minimal)
            freqRight, rightNd = PQ.get()
            freqLeft, leftNd = PQ.get()
            # group them under node which its frequency/value is the sum of the two children
            node = huffNode(rightNode=rightNd, leftNode=leftNd)
            PQ.put(tuple((freqLeft + freqRight, node)))
        huffroot = PQ.get()
        Stringdict = dict()
        recursiveString(huffroot[1], Stringdict)
        print('huffman compressing')
        compressedString = [Stringdict[by] for by in parsedByteArray]
        compressedString = ''.join(compressedString)
        compressedBytes = bytes(int(compressedString[i: i + 8], 2) for i in range(0, len(compressedString), 8))
        print('parsing huffman dictionary')
        parsedHuffDict = ",".join([str(key) + ',' + Stringdict[key] for key in Stringdict.keys()])
        print('finished parsing huffman dictionary')
        return bytes(parsedHuffDict.encode('mbcs')) + bytes('><'.encode('mbcs')) + compressedBytes

    def decompress(self, toDecompress):
        # huffman decompression method
        # separating parsed dictionary from compressed data
        toDecompress = toDecompress.split(bytes('><'.encode('mbcs')), 1)
        # unparsing the dictionary
        parsedDict = toDecompress[0].split(','.encode('mbcs'))
        parsedDict = {parsedDict[i + 1].decode('mbcs'): int(parsedDict[i].decode('mbcs')) for i in
                      range(0, len(parsedDict), 2)}
        # preparing the data to be decompressed
        binaryString = ''.join(["{0:08b}".format(byte) for byte in bytearray(toDecompress[1])])
        charOffset = 0
        outputList = []
        sequence = binaryString[charOffset]
        sequenceList = []
        while charOffset < len(binaryString) - 1:
            # there's a string match
            if sequence in parsedDict.keys():
                sequenceList.append(sequence)
                outputList.append(parsedDict[sequence])
                charOffset += 1
                sequence = binaryString[charOffset]
            # there's no string match
            else:
                charOffset += 1
                sequence += binaryString[charOffset]
        # solution for 8 bit completion in the remaining sequence
        for i in range(len(sequence), 1, -1):
            if sequence[-i:] in parsedDict.keys():
                outputList.append(parsedDict[sequence[-i:]])
                break
        return bytearray(outputList)


def recursiveString(node, dict):
    # this method assigns coding to leafs in the huffman tree recursively
    # recursion end condition  the node is a leaf
    if node.isLeaf:
        dict[node.value] = node.string
    else:
        thisString = node.string if node.string != None else ''
        if node.rightNode != None:
            node.rightNode.appendString(thisString + '1')
            recursiveString(node.rightNode, dict)
        if node.leftNode != None:
            node.leftNode.appendString(thisString + '0')
            recursiveString(node.leftNode, dict)


class huffNode():
    # implementation of huffman node
    def __init__(self, value=None, rightNode=None, leftNode=None, string=None, isLeaf=False):
        self.value = value
        self.rightNode = rightNode
        self.leftNode = leftNode
        self.string = string
        self.isLeaf = isLeaf

    def setValue(self, value):
        self.value = value

    def setRight(self, right):
        self.rightNode = right

    def setLeft(self, left):
        self.leftNode = left

    def appendString(self, char):
        self.string = char

    def __lt__(self, other):
        return True if other.isLeaf else False


# main function call
main()
