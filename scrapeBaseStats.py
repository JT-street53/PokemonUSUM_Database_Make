# -*- coding: utf-8 -*-

from Class import entities
from Class import bean
from Class import scrapeYakkun
from Class import dao

def scrape(url, connect):
    pkmBean = bean.PokemonBean()
    tmp = scrapeYakkun.ScrapeYakkun.scrape(url, pkmBean)
    pkmBean = tmp[0]
    print("[ scrapeBaseStats.py ] : scraping&installing ★★★ " + pkmBean.name + " ★★★")
    dao.PokemonDao.insertPkmBeanData(pkmBean, connect)
    dao.AcquirableMoveDao.insertAcquirableMovesData(pkmBean, connect)
    dao.CaptureLocationDao.insertCaptureLocationData(pkmBean, connect)
    dao.EvolutionDao.insertEvolutionData(pkmBean, connect)
    if tmp[1] != None:
        scrape(tmp[1], connect)

def main():
    bulbasaurURL = entities.WebPage.TETTEIKOURYAKU_BULBASAUR
    # mysqlへの接続を指定
    with dao.Connector(entities.Dao.ACCOUNT) as connect:
        scrape(bulbasaurURL, connect)
    print("[ scrapeBaseStats.py ] : ************finished scraping&installing.************")
    
if __name__ == '__main__':

    main()

