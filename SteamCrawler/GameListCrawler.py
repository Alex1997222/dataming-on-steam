import urllib
import requests
import re
import json
import properties

# Get Steam Game List
def getGameList(game_queue):
    for type, page in zip(properties.game_type, properties.game_page):
        print("start to crawl"+type+"and"+str(page))
        for sp in range(page):
            url = 'https://store.steampowered.com/contenthub/querypaginated/tags/{0}/render/?query=&start={1}&count=15&cc=CN&l=schinese&v=4&tag={2}' \
                .format('TopSellers', sp * 15, urllib.parse.quote(type))
            response = requests.get(url, properties.headers).text
            com = re.compile('https://store.steampowered.com/app/(.*?)/(.*?)/')
            com1 = re.compile('href="(.*?)"')
            result = re.sub(r'\\', '', response)
            result = re.findall(com1, result)
            print("start to crawl page: %d" % (sp + 1))
            for dat in result:
                game_id = re.findall(com, str(dat))[0][0]
                game_url = str(dat)
                game_queue.put(json.dumps({"id":game_id,"url":game_url}))
            print('page %d finished!' % (sp + 1))
        print(type+"and"+str(page)+"done!")
    print("all work complete!")
