from selenium import webdriver
import selenium as sn
import time
import sys

browser = webdriver.Firefox()
goal = sys.argv[1]
query = sys.argv[2]
url = 'https://www.youtube.com/results?search_query='+ query
browser.get(url)

watch_links = []
links = []
link_num = 0
x = '0'
y = '1000'
while link_num < int(goal):
    elems = browser.find_elements_by_xpath("//a[@href]")
    for elem in elems:
        watch_links.append(elem.get_attribute("href"))
    for w in watch_links:
        if w.startswith('https://www.youtube.com/watch?') and w not in links:
            links.append(w)
            print(w)
            link_num = link_num + 1
        if link_num == goal:
            break   
    browser.execute_script("window.scrollTo(" + x +"," +  y + ")")
    x = y
    y = str(int(x) + 1000)  
