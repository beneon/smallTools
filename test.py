import os,PyPDF2,pyperclip
pathofcwd = r"D:\junming zheng\CloudStation\..."
# ^ 需要处理的pdf存放位置
class pdfReader:
    # ^ 处理pdf的一个类，把和pdf处理有关的代码都放在这里了
    blankPdfPath = r'D:\junming zheng\smallToolsGit\smallTools\pdfSmallTools\blank.pdf'
    # ^ 空白页pdf存放位置
    def __init__(self,pdfPath):
        self.pdfPath = pdfPath
        self.blankPageFile, self.blankPage = self.openAndReadit(self.blankPdfPath)
        self.pdfFile, self.pdfReader = self.openAndReadit(self.pdfPath)
    
    def openAndReadit(self,pdfpath):
        """
        generate the pdfReader object for given path in parameter
        """
        pdfFile = open(pdfpath, 'rb')
        pdfReader = PyPDF2.PdfFileReader(pdfFile)
        return (pdfFile,pdfReader)

    def appendBlank(self):
        """
        no para, return a pdf writer with blankPage appended
        """
        pdfWriter = PyPDF2.PdfFileWriter()
        for pageNum in range(self.pdfReader.numPages):
            pageObj = self.pdfReader.getPage(pageNum)
            pdfWriter.addPage(pageObj)
        # add the blank page:
        pdfWriter.addPage(self.blankPage.getPage(0))
        return pdfWriter
    
    def closeAllFile(self):
        self.blankPageFile.close()
        self.pdfFile.close()

os.chdir(pathofcwd)
fileList = os.listdir()

pdfList = filter(
    lambda e:os.path.splitext(e)[1]=='.pdf',
    fileList
)
# ^ 过滤文件列表，只保留pdf

pdfReaderList = map(
    lambda e:pdfReader(e),
    pdfList
)
# ^ 根据pdf文件路径生成pdfReader类

pdfReaderList = filter(
    lambda e: e.pdfReader.numPages % 2 == 1,
    pdfReaderList
)
# ^ 只保留奇数页pdf的pdfReader类

pdfReaderList = list(pdfReaderList)

for pdfReader in pdfReaderList:
    pdfAddBlankWriter = pdfReader.appendBlank()
    outputPath = os.path.splitext(pdfReader.pdfPath)[0]+'_addBlank'+'.pdf'
    pdfOutputFile = open(outputPath,'wb')
    pdfAddBlankWriter.write(pdfOutputFile)
    pdfOutputFile.close()
    pdfReader.closeAllFile()
    print("preparing to output as:%s" % outputPath)
