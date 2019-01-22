#%% [markdown]
# # 若干小工具
# 
# ## 将剪贴板内容去掉\n，去掉中文之间空格

#%%
import pyperclip, re
txtsrc = pyperclip.paste()
reReturn = re.compile(r'\r|\n|\r\n')
reSpcBetwnChnChara = re.compile(r'([\u4e00-\u9fa5])\s+([\u4e00-\u9fa5])')
txtsrc = re.sub(reReturn,'',txtsrc)
txtsrc = re.sub(reSpcBetwnChnChara,r'\1\2',txtsrc)

dict_key = r"１２３４５６７８９０ａｂｃｄｅｆｇｈｉｊｋｌｍｎｏｐｑｒｓｔｕｖｗｘｙｚＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺ，．／！＠＃＄％＾＆＊（）＜＞？；＇：｛｝＿＋－＝"
dict_val = r"1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ,./!@#$%^&*()<>？;':{}_+-="
dict_ = {}
reQuanjiao = re.compile(r'[{0}]'.format(dict_key))
for i in range(len(dict_key)):
    dict_[dict_key[i]]=dict_val[i]
dict_['＂']='"'

def quanjiao2banjiao(mo):
    c = mo.group(0)
    return dict_[c]

txtsrc = re.sub(reQuanjiao,quanjiao2banjiao,txtsrc)
print(txtsrc)
pyperclip.copy(txtsrc)

#%% [markdown]
# ## manual sequencer

#%%
import pyperclip,re
txt = pyperclip.paste().strip()
delim = ""
if '\r' in txt:
    delim += '\r'
if '\n' in txt:
    delim += '\n'
print('delim:%r'%delim)
startNum = 1
tlist = txt.split(delim)
for i in range(len(tlist)):
    tlist[i] = startNum+i
tlist = list(map(lambda e:str(e),tlist))
rst = delim.join(tlist)
print(rst)
pyperclip.copy(rst)

#%% [markdown]
# ## gene sequence converter

#%%
import pyperclip
class converter:
    dict_ = {
    'a':'t',
    't':'a',
    'c':'g',
    'g':'c',
    }
    def __init__(self,seq):
        self.seq = seq.lower()
        self.seqlist = list(self.seq)
    def complement(self):
        self.seqlist = list(map(lambda e:self.dict_[e],self.seqlist))
        return self
    def dna2rna(self):
        self.seqlist = list(map(lambda e:e.replace('t','u'),self.seqlist))
        return self
    def rna2dna(self):
        self.seqlist = list(map(lambda e:e.replace('u','t'),self.seqlist))
        return self
    def reverse(self):
        self.seqlist.reverse()
        return self
    def getSeq(self):
        return ''.join(self.seqlist)
    
seqori = pyperclip.paste()  
seq1 = converter(seqori)
rst = seq1.rna2dna().complement().dna2rna().reverse().getSeq()
print(rst)
pyperclip.copy(rst)

#%% [markdown]
# ## 文库文档下载

#%%
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import re
from selenium.webdriver.support.ui import WebDriverWait
import time
import pyperclip
browser = webdriver.Chrome()
browser.get('https://wenku.baidu.com/view/6b5d50c608a1284ac850438e.html')
# first finishe fire up the driver and load the page


#%%
moreBtn = browser.find_element_by_class_name('moreBtn')
moreBtn.click()
pageInput = browser.find_element_by_class_name('page-input')
datalist = []
reTopVal = re.compile(r'top: (\d+)px')
def contentExtract(pageNum):
    pageInput.clear()
    pageInput.send_keys(str(pageNum))
    pageInput.send_keys(u'\ue007')
    pageElemId = "pageNo-"+str(pageNum)
    print(pageElemId)
    time.sleep(1)
    elem = browser.find_element_by_id(pageElemId)
    subelems = elem.find_elements_by_class_name("reader-word-layer")
    def getYpos(e):
        """获取一个字符block的style里面的top属性，相关的regex在函数外面已经compile完成"""
        mo = reTopVal.search(e.get_attribute('style'))
        return mo.group(1)
    def lineMerging(elems):
        """根据位置top信息判断是否属于一行，如果是新的一行加上换行符以后再连接文字"""
        topTemp = ""
        rstString = ""
        for e in elems:
            if topTemp == getYpos(e):
                rstString += e.text
            else:
                topTemp = getYpos(e)
                rstString += '\r\n' + e.text
        return rstString
    return lineMerging(subelems)
pageTtl = int(browser.find_element_by_class_name('page-count').text[1:])
# 这里根据最大页码手动填写一下范围。如果最大页码在50页以内就可以直接用pageTtl，但是如果超过了50页，这里要分两块才行
for i in range(pageTtl):
    print(i+1)
    datalist.append(contentExtract(i+1))
pyperclip.copy('\r\n'.join(datalist))

#%% [markdown]
# ## 手动提取百度文档页面内容

#%%
from bs4 import BeautifulSoup as bs
import pyperclip as pclp
import re
txt = pclp.paste()
soup = bs(txt,'html.parser')

reTopVal = re.compile(r'top:\s?(\d+)px')

def getYpos(e):
    """获取一个字符block的style里面的top属性，相关的regex在函数外面已经compile完成"""
    mo = reTopVal.search(e.attrs['style'])
    return mo.group(1)
def lineMerging(elems):
    """根据位置top信息判断是否属于一行，如果是新的一行加上换行符以后再连接文字"""
    topTemp = ""
    rstString = ""
    for e in elems:
        if topTemp == getYpos(e):
            rstString += e.text
        else:
            topTemp = getYpos(e)
            rstString += '\r\n' + e.text
    return rstString
paraElems = soup.find_all('p')
rst = lineMerging(paraElems)
pclp.copy(rst)

#%% [markdown]
# ## 在文件夹名字前面加上拼音首字母前缀
# 

#%%
from pypinyin import lazy_pinyin
import os,shutil,re,pyperclip
pathofcwd = pyperclip.paste()
assert os.path.isdir(pathofcwd),'"{}" is not path'.format(pathofcwd)
os.chdir(pyperclip.paste())
reChnFirst = re.compile(r'[\u4e00-\u9fa5]')
dirList = list(filter(lambda e:os.path.isdir(e) and reChnFirst.match(e.strip()) != None,os.listdir()))
  
def renameDirWithPY (dirname):
    prefix = ''
    for e in lazy_pinyin(dirname)[:3]:
        prefix += e[0]
    prefix += '_'
    return prefix+dirname

for e in dirList:
    shutil.move(e,renameDirWithPY(e))
 
os.listdir()

#%% [markdown]
# ## 将奇数页的pdf末尾补平

#%%
import os,PyPDF2,pyperclip
pathofcwd = r"D:\junming zheng\CloudStation\..."
# ^ 需要处理的pdf存放位置
class pdfReader:
    # ^ 处理pdf的一个类，把和pdf处理有关的代码都放在这里了
    blankPdfPath = r'D:\junming zheng\smallToolsGit\smallTools\...'
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

#%% [markdown]
# ## markdown >> zhihu recognized markdown
# 
# 知乎现在可以导入markdown，但是对于代码块的支持很奇怪。现在我的工作流是用evermonkey（visual code的一个插件）通过markdown写一个evernote笔记，然后把其中evernote的内容存储成一个md文件，上传到知乎的编辑器里面。但是知乎编辑器对markdown的支持确实很奇怪（只认第一个\`\`\`，后面的是不认的），所以这段代码的作用是把代码块（\`\`\`c# ... \`\`\`）转换成只有开头有\`\`\`

#%%
import os,re
os.chdir(r'C:\Users\kyk\Desktop')
mdfile = open('test.md',encoding='utf8')
mdfileoutput = open('test_out.md','w',encoding='utf8')
reCodeBlockStart = re.compile(r'```.+')
reCodeBlockEnd = re.compile(r'```$')
mdreader = mdfile.readlines()

def lineProc(line):
    if reCodeBlockEnd.search(line)!=None:
        return ''
    elif reCodeBlockStart.search(line)!=None:
        return '```\n'
    else:
        return line
#     line里面**有**\n
for line in mdreader:
    mdfileoutput.write(lineProc(line))
    
mdfile.close()
mdfileoutput.close()

#%% [markdown]
# ## pdf 中文复制异常情况处理
# 
# 比如说这种: 新型微纳米 生物活性玻璃 生物活性玻璃 生物活性玻璃 生物活性玻璃 生物活性玻璃 研究及应用进展 研究及应用进展 研究及应用进展 研究及应用进展 研究及应用进展
# 
# 其实应该是:新型微纳米生物活性玻璃研究及应用进展

#%%
import pyperclip as pclp
txt = pclp.paste()
txtarr = txt.split(" ")
print(txtarr)
txtfiltered = [e for i,e in enumerate(txtarr) if not e in txtarr[i-1]]
print(txtfiltered)
pclp.copy("".join(txtfiltered))


