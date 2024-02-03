import requests
from bs4 import BeautifulSoup
from googletrans import Translator


class ArabicFredium :

    def __init__(self, url,lang) -> None:
        self.url = f"https://freedium.cfd/{url}"
        self.lang = lang
        req = requests.get(self.url)

        self.soup = BeautifulSoup(req.text,'html.parser')
        self.new_content = ""
        self.tr = Translator()


        for i in self.soup.find('body').contents : 
            try :
                values = list(i.attrs.values())

                if 'header' not in values : 
                    
                    if 'container' in values[0] : 
                        new_texts = self.change_ele_text(i,language=self.lang)
                        container = f"<div class='container w-full md:max-w-3xl mx-auto pt-20 break-words text-gray-900 dark:text-gray-200 bg-white dark:bg-gray-800'>{str(new_texts)}</div>"
                        self.new_content += container

                    else:
                        self.new_content += str(i)
            
            except AttributeError : 
                pass

    

    def change_ele_text (self,container,language=None) :
        new_main_content = []
        contents = container.find('div',{'class':'main-content'}).find_all('p')
        for i in contents : 

            new_content = [j for j in i.contents if '<code' not in str(j)]
            new_ele = ''
            for cont in new_content : 
                orig_txt = cont.text
                if language == 'ar' : 
                    try :
                        new_txt = self.tr.translate(dest='ar',text=orig_txt).text #f"{orig_txt} (Updated)"
                    except :
                        new_txt = orig_txt

                    new_ele += str(cont).replace(orig_txt,new_txt)
                elif language == 'en':
                    new_ele += str(cont)

            new_main_content += new_ele

            

        return ''.join(new_main_content)


    def build_page (self) : 

        self.html_page = f"""

        <!DOCTYPE html>
        <html lang="en">
            
            {self.soup.find('head')}

            <body class="dark:bg-gray-800 bg-white">
                {self.new_content}
            </body>

        </html>

        """

        return self.html_page