import time
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
import trendLive

def check_exists_by_xpath(driver, xpath):
    try:
        return driver.find_element_by_xpath(xpath).text
    except:
        return False


def get_stats_match_lives(options, analizar):
    driver = webdriver.Chrome("C:/Users/59002272/Downloads/chromedriver_win32/chromedriver.exe", options=options)
    res = []
    analizar_eliminar = []
    for url in analizar:
        driver.get(url)
        time.sleep(1)

        c = driver.page_source
        soup = BeautifulSoup(c, "html.parser")

        if "Remates" not in c or "Posesión de balón" not in c:
            analizar_eliminar.append(url)
            continue

        estado = soup.find(id="flashscore").find_all("span", class_="r")

        if estado and len(estado) == 3:
            estado = estado[2].get_text()
        elif estado and len(estado) == 2:
            estado = estado[1].get_text()

        if not estado or isinstance(estado, bool) or (estado!="Descanso" and
                int(estado.split(":")[0].replace('+',''))) > 88 \
                or estado == "Finalizado":
            analizar_eliminar.append(url)
            trendLive.remove_match_tracking(url.replace("https://www.flashscore.es/partido/", "")
                                            .replace("/#estadisticas-del-partido;0", ""))
            continue

        if estado == "Descanso" or int(estado.split(":")[0]) < 12:
            continue

        resultado = soup.find(id="event_detail_current_result").get_text()

        print(url)
        equipos = soup.find_all("div", {"class": "tname__text"})
        local = equipos[0].find('a').get_text()
        visitante = equipos[1].find('a').get_text()

        # if resultado != '0 - 0':
        #    analizar.remove(url)
        #    continue

        try:
            cuotas = soup.find(id="default-live-odds").find_all("span", {"class": "odds value"})
        except:
            cuotas = None
        try:
            cuotaX2 = round(1.0 / (1 - (1.0 / float(cuotas[0].get_text().replace('\n', '')) - 0.05)), 2)
        except:
            cuotaX2= -1

        try:
            cuota1X = round(1.0 / (1 - (1.0 / float(cuotas[2].get_text().replace('\n', '')) - 0.05)), 2)
        except:
            cuota1X= -1

        stats = {"Estado": estado, "Local": local, "Vis": visitante, "Resultado": resultado,
                 "cuotaL": cuotas and cuotas[0].get_text().replace('\n', '') or -1,
                 "cuotaV": cuotas and cuotas[2].get_text().replace('\n', '') or -1,
                 "cuota1X":cuota1X, "cuotaX2":cuotaX2,
                 "ID": url.replace("https://www.flashscore.es/partido/", "").replace("/#estadisticas-del-partido;0",
                                                                                     "")}

        i = 0
        stats_match = soup.find(id="tab-statistics-0-statistic").find_all("div", {"class": "statRow"})
        while True:
            try:
                val1 = stats_match[i].find_all("div", {"class": "statText statText--homeValue"})[0].get_text()
                title = stats_match[i].find_all("div", {"class": "statText statText--titleValue"})[0].get_text()
                val2 = stats_match[i].find_all("div", {"class": "statText statText--awayValue"})[0].get_text()

                stats[title] = {"Local": val1, "Vis": val2}
                i += 1
            except:
                break

        res.append(stats)
        trendLive.add_values_match(stats)

    driver.quit()

    return res, analizar_eliminar


def get_matches_live(driver, analizar_eliminar):
    driver.get("https://www.flashscore.es/?rd=mismarcadores.com")
    time.sleep(3)
    analizar = []

    for jugador in driver.find_elements_by_xpath('.//div[contains(@class, "event__match")]'):
        estado_actual = check_exists_by_xpath(driver, '//*[@id="{0}"]/img'.format(jugador.get_attribute("id")))

        if not isinstance(estado_actual, bool) and not estado_actual:
            url = "https://www.flashscore.es/partido/{0}/#estadisticas-del-partido;0".format(
                jugador.get_attribute("id").replace("g_1_", ""))
            if url not in analizar_eliminar: analizar.append(url)

    print(analizar)
    print("Partidos: {0}".format(len(analizar)))
    return analizar


def get_matches_live2(driver, analizar_eliminar=[]):
    driver.get("https://www.flashscore.es/?rd=mismarcadores.com")
    time.sleep(3)
    analizar = []

    c = driver.page_source
    soup = BeautifulSoup(c, "html.parser")
    all = soup.find_all("div", {"class": "event__match"})

    for partido in all:
        if partido.find("img"):
            url = "https://www.flashscore.es/partido/{0}/#estadisticas-del-partido;0".format(
                partido.get("id").replace("g_1_", ""))
            if url not in analizar_eliminar:
                analizar.append(url)

    print(len(analizar), analizar)

    return analizar
