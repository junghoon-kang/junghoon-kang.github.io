import yaml
import datetime
import xml.etree.cElementTree as ET
import numpy as np
from xml.dom import minidom


def create_workout_tracker(year=2021):
    svg, date_elements = create_activity_tracker(year)
    with open("_data/workout_log.yml", "r") as f:
        w = yaml.load(f, Loader=yaml.FullLoader)
        for date, log in w.items():
            if date.year == year:
                i = (date - datetime.date(year, 1, 1)).days
                date_elements[i].attrib["class"] = "calendar-day-color-L3"
            else:
                print(f"date.year does not match the tracker year ({year}): {date}, {log}")

    svg_bstr = ET.tostring(svg, method="xml")
    xml_str = minidom.parseString(svg_bstr).toprettyxml(indent="    ")
    with open(f"_includes/workout_tracker_{year}.html", "w") as f:
        xml_str = "\n".join(xml_str.splitlines()[1:])
        f.write(xml_str)

def create_activity_tracker(year=2021):
    svg = ET.Element("svg", attrib=dict(width="828", height="128"))
    g = ET.SubElement(svg, "g", attrib=dict(transform="translate(10, 20)"))

    first_weekday = datetime.date(year, 1, 1).weekday()  # 6 is Sunday
    num_weeks = 52 if first_weekday == 6 else 53

    date_elements = []
    for i in range(num_weeks):
        _g = ET.SubElement(g, "g", attrib=dict(transform=f"translate({i*16}, 0)"))
        if num_weeks == 52:
            for j in range(7):
                date_elements.append( ET.SubElement(_g, "rect", attrib=_get_rect_attrib_dict(16-i, 15*j)) )
        else:
            if i == 0:
                for j in range(first_weekday, 6):
                    date_elements.append( ET.SubElement(_g, "rect", attrib=_get_rect_attrib_dict(16, 15*(j+1))) )
            elif i == 52:
                for j in range(first_weekday+1):
                    date_elements.append( ET.SubElement(_g, "rect", attrib=_get_rect_attrib_dict(-36, 15*j)) )
            else:
                for j in range(7):
                    date_elements.append( ET.SubElement(_g, "rect", attrib=_get_rect_attrib_dict(16-i, 15*j)) )

    start_date = datetime.date(year, 1, 1)
    for i in range(364):
        date = start_date + datetime.timedelta(i)
        date_elements[i].attrib["data-date"] = str(date)

    for month, x in _get_month_label_position_tuples(year):
        ET.SubElement(g, "text", attrib=_get_month_label_attrib_dict(x, -8)).text = month

    for day, dy in [("Mon",25), ("Wed",56), ("Fri",85)]:
        ET.SubElement(g, "text", attrib=_get_day_label_attrib_dict(-10, dy)).text = day

    return svg, date_elements

def _get_rect_attrib_dict(x, y):
    return {
        "class": "calendar-day-color-L0",
        "width": "11",
        "height": "11",
        "x": str(x),
        "y": str(y),
        "rx": "2",
        "ry": "2",
    }

def _get_month_label_attrib_dict(x, y):
    return {
        "class": "calendar-label-month",
        "x": str(x),
        "y": str(y),
    }

def _get_day_label_attrib_dict(dx, dy):
    return {
        "class": "calendar-label-month",
        "dx": str(dx),
        "dy": str(dy),
        "text-anchor": "start",
    }

def _get_month_label_position_tuples(year=2021):
    first_weekday = datetime.date(year, 1, 1).weekday()
    if first_weekday == 6:
        num_days_first_week = 7
    else:
        num_days_first_week = 6 - first_weekday

    tuples = [("Jan",16)]
    for i, month in enumerate(["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]):
        if i == 0: continue
        days = (datetime.date(year, i+1, 1) - datetime.date(year, 1, 1)).days
        weeks = int(np.ceil( (days - num_days_first_week) / 7 )) + 1
        tuples.append( (month, 16+15*weeks) )
    return tuples


if __name__ == "__main__":
    create_workout_tracker(year=2021)
    #from IPython import embed; embed(); assert False
