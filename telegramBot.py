import requests
import trendLive

def telegram_bot_send_text(bot_message, token, chat_id):
    send_text = 'https://api.telegram.org/bot' + token + '/sendMessage?chat_id=' + \
                chat_id + '&parse_mode=Markdown&text=' + bot_message
    response = requests.get(send_text)
    return response.json()


def send_matches_telegram(matches, token, chat_id):
    for match in matches:
        telegram_bot_send_text(get_mensaje(match), token, chat_id)


def get_mensaje(a):
    def get_val(d, key1, key2):
        if key1 not in d: return -1

        return d[key1][key2]

    trend = trendLive.get_match_trend(a)
    stats_bm = trendLive.get_stats_by_minute(a)

    return """
 ** {0} vs {1}{55} ** 
```
Resultado:{3}, Minuto:{2}
Pos:{4}/{5}, Remates:{6}({8})/{7}({9})
Paradas:{14}/{15}, Córners:{12}/{13}, 
Ataques:{20}/{21}, Peligr.:{22}%/{23}%
1:{24}, 2:{25}, 1X:{44}, X2:{45}

----Stats min.{43}, {46}----
Pos:{29}%/{30}%, Remates:{31}({41})/{32}({42}),
Córners:{35}/{36}, Ataques:{37}/{38}
Peligrosos:{39}%/{40}% 

----Stats por minuto-----
Remates:{47}/{48}
Ataques:{49}/{50}
Peligrosos:{53}/{54}
Corners:{51}/{52}```""" \
        .format(a["Local"], a["Vis"], a["Estado"].replace(" ", ""), a["Resultado"].replace(" ", ""),
                get_val(a, "Posesión de balón", "Local").replace(' ', ''),
                get_val(a, "Posesión de balón", "Vis").replace(' ', ''),
                get_val(a, "Remates", "Local"), get_val(a, "Remates", "Vis"), get_val(a, "Remates a puerta", "Local"),
                get_val(a, "Remates a puerta", "Vis"), get_val(a, "Tiros libres", "Local"),
                get_val(a, "Tiros libres", "Vis"),
                get_val(a, "Córneres", "Local"), get_val(a, "Córneres", "Vis"), get_val(a, "Paradas", "Local"),
                get_val(a, "Paradas", "Vis"),
                get_val(a, "Faltas", "Local"), get_val(a, "Faltas", "Vis"), get_val(a, "Tarjetas amarillas", "Local"),
                get_val(a, "Tarjetas amarillas", "Vis"), get_val(a, "Ataques", "Local"), get_val(a, "Ataques", "Vis"),
                round(int(get_val(a, "Ataques peligrosos", "Local"))/max(int(get_val(a, "Ataques", "Local")),1)*100,0),
                round(int(get_val(a, "Ataques peligrosos", "Vis"))/max(int(get_val(a, "Ataques", "Vis")),1)*100,0),
                a["cuotaL"], a["cuotaV"], a["ID"], get_val(a,'Pases totales', 'Local'), get_val(a,'Pases totales','Vis'),
                trend['Posesion']['L'], trend['Posesion']['V'], trend['Remates']['L'], trend['Remates']['V'],
                trend['Pases']['L'], trend['Pases']['V'], trend['Corner']['L'], trend['Corner']['V'],
                trend['Ataques']['L'], trend['Ataques']['V'],
                round(int(trend['Ataques peligrosos']['L'])/max(int(trend['Ataques']['L']),1)*100,0),
                round(int(trend['Ataques peligrosos']['V'])/max(int(trend['Ataques']['V']),1)*100,0),
                trend['RematesPuerta']['L'], trend['RematesPuerta']['V'], trend['Desde'],a["cuota1X"], a["cuotaX2"],
                trend['ResultadoDesde'],
                stats_bm['Remates']['L'], stats_bm['Remates']['V'],stats_bm['Ataques']['L'], stats_bm['Ataques']['V'],
                stats_bm['Corners']['L'], stats_bm['Corners']['V'],stats_bm['Peligrosos']['L'],
                stats_bm['Peligrosos']['V'],
                " - Hay rojas" if int(get_val(a, "Tarjetas rojas", "Vis"))+int(get_val(a, "Tarjetas rojas", "Local"))>-2 else "")