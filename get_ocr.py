import time
import easyocr
from tadhar import find_text_in_adhar
from tpan import find_text_in_pan
import pytesseract
import re
import cv2 as cv
import numpy as np

pan_card_varifier  = ['[NCOME TAX DEPARTMEMT' ,'IRCOME TLX DFPARTMENT' ,'ENCOMETAX DEPARTMENT']
pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

def get_ocr(path):
    img = cv.imread(path)
    img = unsharp_mask(img)
    # OCR Using tesseract
    text = pytesseract.image_to_string(img)
    lines = text
    #  OCR Using easyocr
    reader = easyocr.Reader(['en' ])   # initialize the reader
    result = reader.readtext(path)  # exract the text from the image
    a = cv.imread(path)
    textnew = []
    '''
    For Bounding rectangle boxes where text is found
    '''
    for i in result:
        textnew.append(i[1])
        try:
            cv.rectangle(a, (i[0][0]), (i[0][2]), (0,255,0), 1)
        except Exception as e:
            print("error occured while drawing box on image due to :",e)

    t= time.time()
    new_img_path = f'static/{t%1}.jpg'
    cv.imwrite(new_img_path , a)
    '''
    Classifying the document type
    '''
    for i in textnew:
        if i in pan_card_varifier:
            print("pan card **********--------")
            data = find_text_in_pan(text , textnew)
            return data , text , textnew , new_img_path
        
    for wordlist in lines.split('\n'):
        xx = wordlist.split()
        if [w for w in xx if re.search('(INOOMETAX|DEPARTMENT|IN|COME|TAX|DEPARTMENT)$', w)] :   #IN COME TAX DEPARTMENT
            
            # print("************ it is pan")
            data = find_text_in_pan(text , textnew )
            break
        else:
            # print("***************   No PAN")
            data = find_text_in_adhar(text , textnew)
    return data , text , textnew , new_img_path
   
    


def unsharp_mask(image, kernel_size=(5, 5), sigma=1.0, amount=1.0, threshold=0):
    """Return a sharpened version of the image, using an unsharp mask."""
    blurred = cv.GaussianBlur(image, kernel_size, sigma)
    sharpened = float(amount + 1) * image - float(amount) * blurred
    sharpened = np.maximum(sharpened, np.zeros(sharpened.shape))
    sharpened = np.minimum(sharpened, 255 * np.ones(sharpened.shape))
    sharpened = sharpened.round().astype(np.uint8)
    if threshold > 0:
        low_contrast_mask = np.absolute(image - blurred) < threshold
        np.copyto(sharpened, image, where=low_contrast_mask)
    return sharpened