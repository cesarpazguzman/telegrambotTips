import json
import trendLive


def get_dict_file(file_path):
    rules = []
    with open(file_path) as json_file:
        data = json.load(json_file)
        for cases in data['cases']:
            rules.append(data['cases'][cases])

    return rules


def get_match_candidate(match, rule, lado):
    opponent = "Vis"
    if lado == "Vis": opponent = "Local"

    stats_by_minute = trendLive.get_stats_by_minute(match)

    if "over" in rule["posesion"] and \
            rule["posesion"]["over"] > float(match["Posesión de balón"][lado].replace('%', '')):
        return False

    if "under" in rule["posesion"] and \
            rule["posesion"]["under"] < float(match["Posesión de balón"][lado].replace('%', '')):
        return False

    if "goals" in rule:
        goals = int(match["Resultado"].split("-")[0 if lado == "Local" else 1])
        if "equal" in rule["goals"] and rule["goals"]["equal"] != goals: return False
        if "over" in rule["goals"] and rule["goals"]["over"] > goals: return False
        if "under" in rule["goals"] and rule["goals"]["under"] < goals: return False

    if "empate" in rule and rule['empate'] == 1:
        if int(match["Resultado"].split("-")[0]) != int(match["Resultado"].split("-")[1]):
            return False

    if "goalsOpponent" in rule:
        goalsOpponent = int(match["Resultado"].split("-")[1 if lado == "Local" else 0])
        if "equal" in rule["goalsOpponent"] and rule["goalsOpponent"]["equal"] != goalsOpponent: return False
        if "over" in rule["goalsOpponent"] and rule["goalsOpponent"]["over"] > goalsOpponent: return False
        if "under" in rule["goalsOpponent"] and rule["goalsOpponent"]["under"] < goalsOpponent: return False

    if "minute" in rule:
        if match["Estado"] == "Descanso":
            minute = 45
        else:
            minute = int(match["Estado"].split(":")[0])
        if "over" in rule["minute"] and rule["minute"]["over"] > minute: return False
        if "under" in rule["minute"] and rule["minute"]["under"] < minute: return False

    if "dif_goals_attemps" in rule:
        dif_goals_attemps = int(match["Remates"][lado]) - int(match["Remates"][opponent])
        if "over" in rule["dif_goals_attemps"] and rule["dif_goals_attemps"]["over"] > dif_goals_attemps: return False
        if "under" in rule["dif_goals_attemps"] and rule["dif_goals_attemps"]["under"] < dif_goals_attemps: return False

    if "dif_attacks" in rule:
        dif_attacks = int(match["Ataques"][lado]) - int(match["Ataques"][opponent])
        if "over" in rule["dif_attacks"] and rule["dif_attacks"]["over"] > dif_attacks: return False
        if "under" in rule["dif_attacks"] and rule["dif_attacks"]["under"] < dif_attacks: return False

    if "dif_dangerous_attacks" in rule:
        dif_dangerous_attacks = int(match["Ataques peligrosos"][lado]) - int(match["Ataques peligrosos"][opponent])
        if "over" in rule["dif_dangerous_attacks"] and \
                rule["dif_dangerous_attacks"]["over"] > dif_dangerous_attacks: return False
        if "under" in rule["dif_dangerous_attacks"] and \
                rule["dif_dangerous_attacks"]["under"] < dif_dangerous_attacks: return False

    if "dif_corners" in rule:
        dif_corners = int(match["Córneres"][lado]) - int(match["Córneres"][opponent])
        if "over" in rule["dif_corners"] and \
                rule["dif_corners"]["over"] > dif_corners: return False
        if "under" in rule["dif_corners"] and \
                rule["dif_corners"]["under"] < dif_corners: return False

    if "rematesByMin" in rule:
        if "over" in rule["rematesByMin"] and \
                rule["rematesByMin"]["over"] > stats_by_minute["Remates"][lado[0]]: return False
        if "under" in rule["rematesByMin"] and \
                rule["rematesByMin"]["under"] < stats_by_minute["Remates"][lado[0]]: return False

    if "ataquesByMin" in rule:
        if "over" in rule["ataquesByMin"] and \
                rule["ataquesByMin"]["over"] > stats_by_minute["Ataques"][lado[0]]: return False
        if "under" in rule["ataquesByMin"] and \
                rule["ataquesByMin"]["under"] < stats_by_minute["Ataques"][lado[0]]: return False

    return True


def get_matches_filtered(matches, rules_to_filter, matches_filter=[]):
    res = []
    print(matches)
    for match in matches:
        if match in matches_filter: continue

        print("match", match["Estado"], match["Local"], match["Vis"], match["Resultado"],
              match["Posesión de balón"]["Local"], match["Posesión de balón"]["Vis"],
              match["Remates"]["Local"], match["Remates"]["Vis"],
              match["Ataques"]["Local"], match["Ataques"]["Vis"],
              match["Ataques peligrosos"]["Local"], match["Ataques peligrosos"]["Vis"],
              match["Córneres"]["Local"], match["Córneres"]["Vis"])
        for rule in rules_to_filter:
            if get_match_candidate(match, rule, "Local") or get_match_candidate(match, rule, "Vis"):
                res.append(match)
                break

    return res
