import requests


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

    return """
** {0} vs {1} ({26})** 
```
Resultado:{3}, Minuto:{2}
Pos:{4}/{5}, Remates:{6}({8})/{7}({9})
T.Libres:{10}/{11}, Paradas:{14}/{15}
Córners:{12}/{13}, Faltas:{16}/{17}
Tarjetas:{18}/{19}, Ataques:{20}/{21}
At. Peligrosos:{22}/{23}
CuotaL:{24}, CuotaV:{25}```""" \
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
                get_val(a, "Ataques peligrosos", "Local"), get_val(a, "Ataques peligrosos", "Vis"),
                a["cuotaL"], a["cuotaV"], a["ID"])
