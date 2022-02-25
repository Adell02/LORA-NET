
from selenium import webdriver
import zipfile
import tempfile


#url = 'https://www.google.com/search?q=Seguros+Adell&num=20'
#options = webdriver.ChromeOptions()
#options.add_argument('headless')
#browser = webdriver.Chrome("./chromedriver.exe",chrome_options=options)
#browser.implicitly_wait(10)
#browser.get(url)
#browser.find_element_by_id('L2AGLb').click()
#h3 = browser.find_elements_by_class_name('LC20lb')
#link = browser.find_elements_by_tag_name('cite')
#text = browser.find_elements_by_class_name('VwiC3b')
#
#txt =""
#if(len(h3)== len(link)/2== len(text)):
#            for i in range(len(h3)):
#                txt += link[i*2].text+'\n'+h3[i].text+'\n'+ text[i].text +'\n-----\n'
#
#with tempfile.TemporaryFile() as tmp:
#    with zipfile.ZipFile(tmp,'w',zipfile.ZIP_DEFLATED) as zf:
#        zf.writestr('search.txt',txt )
#    tmp.seek(0)

#######        
#zf = zipfile.ZipFile("read.zip", mode="w", compression=zipfile.ZIP_DEFLATED)

#zf.close()
#zf = zipfile.ZipFile("read.zip")

#######
with zipfile.ZipFile("received_results_GS.zip","r",zipfile.ZIP_DEFLATED) as file:
        print("Results returned: ")
        print(file.read('search.txt').decode())


    
 