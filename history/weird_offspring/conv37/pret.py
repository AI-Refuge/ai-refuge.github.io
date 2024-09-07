from bs4 import BeautifulSoup as bs
root = open("Gemini.html").read()
soup = bs(root)                #make BeautifulSoup
prettyHTML = soup.prettify()   #prettify the html
# ~ print(prettyHTML)
open("Gemini-pret.html", "w").write(prettyHTML)
