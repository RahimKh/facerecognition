import requests
import json

url='https://newnorm.sagecity.io/member/detectNewRegistrationForFaceRecognition'


url_reg = 'http://127.0.0.1:5000/api/facerec/reg'


url_confirm = "https://newnorm.sagecity.io/member/setUserAsProcessedByFaceRecognition?id="



def registre_images(r):
    n=len(r)
    while(n>0):
        img_b64=r[n-1]['photo']
        id=r[n-1]['id']
        payload={"id":id, "image":img_b64}
        print('processing id :',id)
        r2=requests.post(url_reg, data=payload)
        if (r2.json()['msg']=="success"):
            payload  = {}
            headers = {
            'Connection': 'keep-alive',
            'Accept': 'application/json, text/plain, */*',
            'DNT': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36',
            'Content-Type': 'text/plain',
            'Origin': 'http://localhost:4501',
            'Sec-Fetch-Site': 'same-site',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Dest': 'empty',
            'Referer': 'http://localhost:4501/',
            'Accept-Language': 'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7,ar;q=0.6'
            }
            url_con=url_confirm+str(id)
            response = requests.request("PUT", url_con, headers=headers, data = payload)

            print(response.text.encode('utf8'))
            n=n-1
            print(n)
        else :
            print(r2.json())
            n=n-1
            

if __name__=="__main__":
    r=requests.get(url)
    js=json.loads(r.text)
    print(len(js))
    registre_images(js)