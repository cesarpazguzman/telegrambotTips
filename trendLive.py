
matches_tracking = {}

def add_values_match(match):
    def get_val(d, key1, key2):
        if key1 not in d: return -1

        return d[key1][key2]

    match_id = match['ID']
    minute = int(match['Estado'].split(':')[0])
    if match_id not in matches_tracking:
        matches_tracking[match_id] = {}

    matches_tracking[match_id][minute] = {
        'Resultado':match['Resultado'],
        'Goles':{'L':match['Resultado'].split('-')[0], 'V':match['Resultado'].split('-')[1]},
        'Remates':{'L':match['Remates']['Local'], 'V':match['Remates']['Vis']},
        'RematesPuerta': {'L': match['Remates a puerta']['Local'], 'V': match['Remates a puerta']['Vis']},
        'Posesion':{'L':match['Posesión de balón']['Local'].replace('%',''),
                    'V':match['Posesión de balón']['Vis'].replace('%','')},
        'Corner':{'L':get_val(match,'Córneres','Local'), 'V':get_val(match,'Córneres','Vis')},
        'Pases':{'L':get_val(match,'Pases totales','Local'), 'V':get_val(match,'Pases totales','Vis')},
        'Ataques':{'L':get_val(match,'Ataques','Local'), 'V':get_val(match,'Ataques','Vis')},
        'Ataques peligrosos':{'L':get_val(match,'Ataques peligrosos','Local'),
                              'V':get_val(match,'Ataques peligrosos','Vis')},}


def remove_match_tracking(match_id):
    if match_id in matches_tracking:
        del matches_tracking[match_id]


def get_match_trend(match, last_min=15):
    current_min = int(match['Estado'].split(':')[0])
    min_dif = int(current_min) - last_min
    match_track = matches_tracking[match['ID']]

    #If the first tracking is lower than 'last_min' I return it because is the lowest.
    if int(list(match_track.keys())[0])>min_dif:
        return get_dif_var_match(match_track[int(list(match_track.keys())[0])],
                                 match_track[int(list(match_track.keys())[-1])],
                                 int(list(match_track.keys())[0]))

    for minute in match_track:
        if minute > min_dif:
            return get_dif_var_match(match_track[minute], match_track[int(list(match_track.keys())[-1])],minute)


def get_dif_var_match(match_min1, match_min2, desde):
    return {
        'Desde':desde,'ResultadoDesde':match_min1['Resultado'],
        'Goles':{'L':int(match_min2['Goles']['L'])-int(match_min1['Goles']['L']),
                 'V':int(match_min2['Goles']['V'])-int(match_min1['Goles']['V'])},
        'Remates': {'L': int(match_min2['Remates']['L']) - int(match_min1['Remates']['L']),
                  'V': int(match_min2['Remates']['V']) - int(match_min1['Remates']['V'])},
        'RematesPuerta': {'L': int(match_min2['RematesPuerta']['L']) - int(match_min1['RematesPuerta']['L']),
                    'V': int(match_min2['RematesPuerta']['V']) - int(match_min1['RematesPuerta']['V'])},
        'Posesion': {'L': int(match_min2['Posesion']['L']) - int(match_min1['Posesion']['L']),
                  'V': int(match_min2['Posesion']['V']) - int(match_min1['Posesion']['V'])},
        'Corner': {'L': int(match_min2['Corner']['L']) - int(match_min1['Corner']['L']),
                  'V': int(match_min2['Corner']['V']) - int(match_min1['Corner']['V'])},
        'Pases': {'L': int(match_min2['Pases']['L']) - int(match_min1['Pases']['L']),
                   'V': int(match_min2['Pases']['V']) - int(match_min1['Pases']['V'])},
        'Ataques': {'L': int(match_min2['Ataques']['L']) - int(match_min1['Ataques']['L']),
                   'V': int(match_min2['Ataques']['V']) - int(match_min1['Ataques']['V'])},
        'Ataques peligrosos': {'L': int(match_min2['Ataques peligrosos']['L'])-int(match_min1['Ataques peligrosos']['L']),
                    'V': int(match_min2['Ataques peligrosos']['V']) - int(match_min1['Ataques peligrosos']['V'])},
    }
