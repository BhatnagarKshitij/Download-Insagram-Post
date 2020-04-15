from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
from urllib5 import validate
import requests
import os
from time import sleep
from datetime import datetime
import sys
start_time = datetime.now()
chromedriver_path = 'chromedriver.exe'

arg = len(sys.argv)
if arg>1:
    if sys.argv[1] == "--verbose":
        webdriver = webdriver.Chrome(executable_path=chromedriver_path)
        print("SHOWING BACKEND TOO....!!!<DEVELOPER MODE!!>")
    else:
        exit()
else:
    
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('window-size=1920x1080')
    options.add_argument("disable-gpu")
    # OR options.add_argument("--disable-gpu")

    #driver = webdriver.Chrome('chromedriver', chrome_options=options)
    webdriver = webdriver.Chrome(executable_path=chromedriver_path, chrome_options=options)




InstaUsername=""
InstaPassword=""
InstaAccount=""


def info():
    global InstaUsername
    InstaUsername=input("Enter Your Username/Email: ")
    global InstaPassword
    InstaPassword=input("Enter Your Password: ")
    global InstaAccount
    InstaAccount=input("Enter Insta Account username: ")
def instaLogin():
    print("WELCOME TO InstaDownloader by KSHITIJ")
    print("Navigating to Instagram Login Page")
    webdriver.get("https://www.instagram.com/accounts/login/?source=auth_switcher")
    sleep(2)
    username = webdriver.find_element_by_name("username")
    print("Entering Username")
    username.click()
    username.send_keys(InstaUsername)
    password=webdriver.find_element_by_name("password")
    print("Entering Password")
    password.click()
    password.send_keys(InstaPassword)
    sleep(2)
    loginButton=webdriver.find_element_by_css_selector("#react-root > section > main > div > article > div > div:nth-child(1) > div > form > div:nth-child(4) > button > div")
    sleep(1)
    loginButton.click()
    print("Logging in . . . ")

    sleep(2)
    if(len(webdriver.find_elements_by_class_name('eiCW-')) > 0):
        print("Incorrect Username or Password")
        exit()


def notNowNotification():
    try:
        print("Pressing Not Now!!!")
        notnow = webdriver.find_element_by_css_selector('body > div.RnEpo.Yx5HN > div > div > div.mt3GC > button.aOOlW.bIiDR')
        notnow.click()
    except:
        print("Maybe there is no Notification PopUp")


def goToProfile(profile):
    print("Navigating into "+InstaAccount)
    webdriver.get("https://www.instagram.com/"+InstaAccount+"/")
    if(len(webdriver.find_elements_by_class_name('error-container')) > 0):
        print("Account Doesnt Exists")
        exit()
    else:
        print(InstaAccount+" is opened")

def countNumberOfPost():
    try:
        print("Counting Number of Post")
        return(int(webdriver.find_element_by_class_name('g47SY').text))
    except:
        print("Some Error Occured")
        return(0)


def openFirstPicFromThumbnail():
    print("Opening First Thumbnail")
    sleep(2)
    try:
        openFirst=webdriver.find_element_by_class_name('v1Nh3')
       #openFirst=webdriver.find_element_by_xpath("/html/body/div[1]/section/main/div/div[3]/article/div[1]/div/div[1]/div[1]")
        hover=ActionChains(webdriver).move_to_element(openFirst).click().perform()
        openFirst.click;
        sleep(3)
    except:
        tryAgain=input("Cannot Open image: Would You like to try again PRESS 'Y' for YES 'N' for NO : ")
        if(tryAgain=='Y' or tryAgain=='y' or tryAgain=='YES' or tryAgain=='yes'):
            openFirstPicFromThumbnail()
        else:
            exit()
            
            
def createFolder(FolderName):
    if not os.path.exists(InstaAccount):
        print("Creating folder named: "+ FolderName)
        os.makedirs(FolderName)
    else:
        print("Folder Already Exist: Data will be overwritten!!!")

def isNextPostAvailable():
    if(len(webdriver.find_elements_by_class_name('coreSpriteRightPaginationArrow'))>0):
        return 1
    else:
        return 0
def nextPost():
    nextPost=webdriver.find_element_by_class_name("coreSpriteRightPaginationArrow")
    nextPost.click()

def isNextMediaAvailable():
    if len(webdriver.find_elements_by_class_name('coreSpriteRightChevron')) > 0:
        return 1
    else:
        return 0
        
def nextMedia():
    nextMedia=webdriver.find_element_by_class_name("coreSpriteRightChevron")
    nextMedia.click()

def isMediaVideo():
    if len(webdriver.find_elements_by_class_name('videoSpritePlayButton')) > 0:
        return 1
    else:
        return 0    


urls=[]


def getImageURL():
    elem = webdriver.find_element_by_class_name("_97aPb")
    source_code = elem.get_attribute("outerHTML")
    soup=BeautifulSoup(source_code,features="html.parser")
    for link in soup.find_all('img'):
        if link.get('src') not in urls:
            urls.append(link.get('src'))
def getVideoURL():
    elem = webdriver.find_element_by_class_name("_97aPb")
    source_code = elem.get_attribute("outerHTML")
    soup=BeautifulSoup(source_code,features="html.parser")
    for link in soup.find_all('video'):
        if link.get('src') not in urls:
            urls.append(link.get('src'))


        
def downloadMedia(Filename,url):
    with open(Filename, "wb") as f:
        f.write(requests.get(url).content)

def downloadAllMedia():
    index=1
    for downloadLinks in urls:
        if(downloadLinks.find('jpg')!= -1):
            ext=".jpg"
        elif(downloadLinks.find('mp4') != -1):
            ext=".mp4"
        Filename=InstaAccount+"\\"+str(index)+ext
        downloadMedia(Filename,downloadLinks)
        index+=1

        
#-----------------------------MAIN--------------------------------------#
info()
try:
    instaLogin()#Loign into Instagram
except:
    print("An Error occured!!! Trying ReLogin....")
    instaLogin()
else:
    print("Welcome "+InstaUsername)
    sleep(2)
    notNowNotification() #Pressing Not now popup

goToProfile(InstaAccount)
numberOfPost=countNumberOfPost()
print(InstaAccount +" has "+str(numberOfPost)+" Posts!! ")    
openFirstPicFromThumbnail()
createFolder(InstaAccount)

if numberOfPost == 0:
    print("No Post from this User ")
    exit()
else:
    print("Crawling each photo....")
    start_time_crawl = datetime.now()
    while int(isNextPostAvailable()):
        sleep(1)
        if int(isNextMediaAvailable()):
            sleep(1)
            if int(isMediaVideo()):
                sleep(1)
                getVideoURL()
            else:
                sleep(1)
                getImageURL()
            sleep(1)
            nextMedia()
        else:
            sleep(1)
            if int(isMediaVideo()):
                sleep(1)
                getVideoURL()
            else:
                sleep(1)
                getImageURL()
            sleep(1)
            nextPost()
        sleep(1)
    
    if int(isNextMediaAvailable()):
        sleep(1)
        if int(isMediaVideo()):
            sleep(1)
            getVideoURL()
        else:
            sleep(1)
            getImageURL()
        sleep(1)
    else:
        sleep(1)
        if int(isMediaVideo()):
            sleep(1)
            getVideoURL()
        else:
            sleep(1)
            getImageURL()
        sleep(1)
    
    end_time_crawl = datetime.now()

    downloadAllMedia()
    validate(urls,InstaAccount,InstaUsername,InstaPassword)
    end_time = datetime.now()
    print('Duration of whole process: {}'.format(end_time - start_time))
    print('Duration of crawling media: {}'.format(end_time_crawl - start_time_crawl))

#--------------------------END OF PROGRAM----------------------------------#
print("EVERTHING COMPLETED!!!")
webdriver.quit()
exit()