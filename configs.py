from os import path, getenv

class Config:
    API_ID = int(getenv('API_ID','10982967'))
    API_HASH = getenv('API_HASH','abb3cfd55b9c8e848aa87cc01d5567d4')
    BOT_TOKEN = getenv('BOT_TOKEN','6231066095:AAEHMcBBB-qTPjMkCGWXydi64az_saTnb-w')

config = Config()
