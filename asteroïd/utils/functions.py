from datetime import date,timedelta
from this import d


def formatDate(date):
    day = "";
    if (date.day > 9):
        day = str(date.day);
    else:
        day = "0"+str(date.day);
    return str(date.year)+"-"+str(date.month)+"-"+ day

def get_all_days(start,end):
    start_date = date(start.year,start.month,start.day)
    end_date = date(end.year,end.month,end.day)
    nb_days = (end_date - start_date).days+1
    days = []

    for i in range(nb_days):
        delta_days = timedelta(days=i)
        days.append(formatDate(end_date-delta_days))
    return days

def passages(response,date_now):
    passages = response["close_approach_data"]

    next_passage = "Not indicated"
    lasts_passages = []
    found = False
    index = 0

    while(not(found) and index < len(passages)):
        if (passages[index]["close_approach_date"] == date_now and index != len(passages)-1):
            next_passage = passages[index+1]["close_approach_date"]
            for i in reversed(range(5)):
                lasts_passages.append({'date':date.fromisoformat(passages[index-i-1]["close_approach_date"]).strftime("%b. %d, %Y"),'distance':passages[index-i-1]["miss_distance"]["kilometers"]})
            found = True
        index += 1

    if (next_passage != "Not indicated"):
        next_passage = date.fromisoformat(next_passage).strftime("%b. %d, %Y")

    return {'next':next_passage,'lasts':lasts_passages}
