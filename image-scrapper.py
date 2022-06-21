import os
import requests as re
from bs4 import BeautifulSoup

googe_img_url_parts = ["https://www.google.com/search?q=","&source=lnms&tbm=isch&sa=X"]

user_agent = {

    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"
}

save_folder = 'dataset'

def is_int(number):
    try:
        int(number)
        return True
    except:
        print("Quantity is not an integer!")

def is_float(ratios,position,numeric_ratios):
    try:
        numeric_ratios[position] = float(ratios[position])
    except:
        print(f"Number {ratios[position]} with wrong format!")
        
def ask_user():
    is_valid = [False,False,False]
    
    while is_valid[0] != True:
        subject = input('Enter the subject that you want to download a dataset: ')
        if (subject != ''):
            is_valid[0] = True
        
    while is_valid[1] != True:
        quantity = input('Enter the number of images that you want: ')         
        if (is_int(quantity) == True):
            is_valid[1] = True
        
    while is_valid[2] != True:
        ratio = input('Enter the ratio (sum = 1) for train,validation,test in the format like (<train>;<validation>;<test>): ')
        ratios = ratio.split(';')
        numeric_ratios = [0]*len(ratios)
        if (len(ratios) != 3):
            print('Number of ratios different of three')
        else:
            for i in range(len(ratios)):
                is_float(ratios,i,numeric_ratios)
            if (sum(numeric_ratios) != 1):
                print('Ratios sum different of 1')
            else:
                is_valid[2] =  True
            
    return subject,quantity,ratios

def download_images(subject, quantity):
    print('searching...')
    
    search_url = googe_img_url_parts[0] + subject + googe_img_url_parts[1]
    
    response = re.get(search_url, headers = user_agent)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    results = soup.findAll('img',{'class':'rg_i Q4LuWd'})
    
    count = 0

    img_links = []

    for img in results:
        try:
            img_links.append(img['data-src'])
            count += 1
            if(count >= quantity):
                break
        except KeyError:
            continue
            
    print('downloading pictures...')
    
    for i, link in enumerate(img_links):
        response = re.get(link)        
        
        image_name = f'{subject}{str(i+1)}.jpg'
        file_name = os.path.join(save_folder,image_name)
        
        with open(file_name, 'wb') as fh:
            fh.write(response.content)


def main():
    
    if not os.path.exists(save_folder):
        os.mkdir(save_folder)
    
    subject, quantity, ratios = ask_user()
    download_images(subject, int(quantity))

main()