import fitz
import re

# Will Need To Change the Place where Output file will be created
def pdfToText(PDFName) -> list:
    doc = fitz.open(PDFName)
    totalText = ""
    
    for page in doc:
        totalText += page.get_text("Text")
        
    outputFile = open('pdfToText.txt', 'w')
    outputFile.write(totalText)
    outputFile.close()
    
    sentenceSplit = totalText.split('.')
    sentenceTokens = []
    
    for dat in sentenceSplit:
        dat = re.sub('\n', '', dat)
        dat = re.sub('\xa0', '', dat)
        sentenceTokens.append(dat)
    
    return sentenceTokens

a = pdfToText('test3.pdf')
print(a)