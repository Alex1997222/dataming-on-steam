# Remote Sever Configration
ip = '1.116.235.45'
port = 3306
user = 'root'
password = 'Wps1997222#'

# Mysql
db = 'steamData'
user = 'root'
password = 'Wps1997222#'
charset='utf8mb4'

# Redis
DB5 : friend relationship
DB6 : user's owned game

# File Directory
SteamCrawler
├── GameListCrawler.py
├── README.md
├── crawler `crawler module`
│   ├── gameBriefCrawler.py
│   ├── reviewCrawler.py
│   └── userCrawler.py
├── data `data we crawler`
│   └── steamData.sql
├── gameCrawler.py
├── main.py `main file`
├── properties.py `configeration of the crawler`
├── sqlPool `mysql connection module`
│   ├── dbDbUtilsInit.py
│   ├── sqlHelper.py
│   └── sqlPoolConfig.py
├── userCrawler.py
└── utils
    ├── gameUtils.py
    ├── redisUtis.py
    └── sqlUtils.py