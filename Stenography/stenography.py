#Arthur LeBlanc
#6810 Project 4

from PIL import Image
import math

verbose = False
EOFCHAR = '00011010'
byteLength = 8
 
def getMaxBytes(width, height):
    #returns the max number of characters that can be encoded in the file
    return math.floor(width*height/8)

def getFileName(prompt):
    #splits the name into file and extension - to easily save a new file
    imageFile = input(prompt + '\n')    

    extPos = imageFile.rfind('.')
    imageName = imageFile[:extPos]
    imageExtension = imageFile[extPos:]

    return imageName, imageExtension

def posUpdate(posX, posY, width, height):
    #updates the position of the x and y coordinates
    posX += 1
    if posX >= width:
        posY += 1 
        posX = 0
        if posY >= height:
            raise ValueError('pixel dimension length exceeded')
    return posX, posY

def encryptImage():
    imageName, imageExtension = getFileName('What picture would you like to modify? Please specify a file in the current folder.')
    imageFile = Image.open(imageName + imageExtension)
    width, height = imageFile.size
    maxBytes = getMaxBytes(width, height)
    message = input('what message would you like encoded?\n')
    #to ensure the message is less than the max number of bytes
    #the final byte must be an EOF marker
    if len(message) > maxBytes - 1:
        print('message exceeds encoding length, only encoding {} characters'.format(maxBytes))
        message = message[:maxBytes]
        print('encoded message will be: {}'.format(message))

    messageHex = ''
    for x in message:
        bit = '' +  format(ord(x), 'b')
        if len(bit) < byteLength:
            diff = byteLength - len(bit)
            for i in range(diff):
                bit = '0' + bit
        messageHex += bit + ' '
    messageHex = messageHex + EOFCHAR #add end of file character
    messageHex = messageHex.split(' ') #create from a list of characters

    if verbose:
        print('bits of message will be: {}'.format(messageHex))
        print('bit 1: {}, bit 2: {}'.format(messageHex[0], messageHex[1]))

    #scale = 16
    #numBits = 8
    #messageBin = bin(int(messageHex, scale))[2:].zfill(numBits)
    
    def messageBitRGB(imageFile, posX, posY, bit):
        pixel = imageFile.getpixel((posX, posY))
        rBit = pixel[0]
        if verbose:
            print('rbit before: {}'.format(rBit))
        if bit == '1':
            if rBit%2 != 1:
                #images could be either black(0) or white(255)
                #both cases should work
                if rBit < 125:
                    rBit += 1
                else:
                    rBit -= 1
        else:
            if rBit%2 != 0:
                if rBit < 125:
                    rBit += 1
                else:
                    rBit -= 1
        if verbose:
            print('rbit after: {}'.format(rBit))
            print('bits: {}'.format(pixel))
        newPixel = list(pixel)
        newPixel[0] = rBit
        newPixel = tuple(newPixel)
        return newPixel
 
    posX = 0
    posY = 0
    for c in messageHex:
        if verbose:
            print(c)
        for bit in c:
            pixel = messageBitRGB(imageFile, posX, posY, bit)
            if verbose:
                print(pixel)
            imageFile.putpixel((posX, posY), pixel)
            if verbose:
                print('{} vs. {} at ({}, {})'.format(str(imageFile.getpixel((posX, posY))), str(pixel), posX, posY))
            posX, posY = posUpdate(posX, posY, width, height)
 
    newFileName = imageName + '-stenograph' + imageExtension

    imageFile.save(newFileName)

    imageFile.close()
    print('message "{}" encoded in file {}'.format(message, newFileName))
    return

def deencryptImage(quick = False): #TODO: perform testing on this
    imageName, imageExtension = getFileName('What picture would you like to deencrypt? Please specify a file in the current folder.')
    
    imageFile = Image.open(imageName + imageExtension)
    width, height = imageFile.size

    stop = False
    posX = 0
    posY = 0
    messageBits = ['']
    posMessage = 0
    posBit = 0
   
    #count = 0
    if verbose:
        print(messageBits)
        max = 4*8

    def getMessageBit(imageFile, posX, posY):
        pixel = imageFile.getpixel((posX, posY))
        #rBit, gBit, bBit = imageFile.getpixel((posX, posY))
        if verbose:
            print('bits: {} at ({}, {})'.format(pixel, posX, posY))
        return pixel[0]%2

    while not stop:# and count < max:
        #count += 1
        bit = '' + str(getMessageBit(imageFile, posX, posY))
        
        if posBit < byteLength:
            messageBits[posMessage]+=str(bit)
            posBit += 1
        else:
            if messageBits[posMessage] == EOFCHAR:
                if verbose:
                    print('found EOFCHAR')
                messageBits = messageBits[:posMessage]
                #stop = True
                break

            messageBits.append(str(bit))
            posBit = 1
            posMessage += 1

        #posX, posY = posUpdate(posX, posY, width, height)
        try:
            if posY >= height - 1 and posX >= width - 1:
                #stop = True
                break
            else:
                posX, posY = posUpdate(posX, posY, width, height)
        except ValueError as ve:
            print(ve)
            break

    if verbose:
        print('the encrypted message was: {}'.format(messageBits))

    message = ''
    for c in messageBits:
        if len(c) == 8: #in case the message was cut short or there was no coded message
            message += chr(int(c, 2))

    print('the final message was: "{}"'.format(message))
    return 

def StenographyLoop():
    selections = {}
    selectionsStr = '1: encryptImage, 2: deencryptImage, any other number: quit'
    

    stop = False
    while not stop:
        print(selectionsStr)
        select = int(input('please choose a selection: \n'))
        if select == 1:
            encryptImage()
        elif select == 2:
            deencryptImage()
        else:
            print('choice other than 1 or 2, quitting')
            stop = True

StenographyLoop()
exit()

