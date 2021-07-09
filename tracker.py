import yaml
import datetime
import xml.etree.cElementTree as ET
from xml.dom import minidom


def get_rect_attrib_dict(x, y):
    return {
        "class": "calendar-day-color-L0",
        "width": "11",
        "height": "11",
        "x": str(x),
        "y": str(y),
        "rx": "2",
        "ry": "2",
    }

def get_month_label_attrib_dict(x, y):
    return {
        "class": "calendar-label-month",
        "x": str(x),
        "y": str(y),
    }

def get_day_label_attrib_dict(dx, dy):
    return {
        "class": "calendar-label-month",
        "dx": str(dx),
        "dy": str(dy),
        "text-anchor": "start",
    }

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
                date_elements.append( ET.SubElement(_g, "rect", attrib=get_rect_attrib_dict(16-i, 15*j)) )
        else:
            if i == 0:
                for j in range(first_weekday, 6):
                    date_elements.append( ET.SubElement(_g, "rect", attrib=get_rect_attrib_dict(16, 15*(j+1))) )
            elif i == 52:
                for j in range(first_weekday+1):
                    date_elements.append( ET.SubElement(_g, "rect", attrib=get_rect_attrib_dict(-36, 15*j)) )
            else:
                for j in range(7):
                    date_elements.append( ET.SubElement(_g, "rect", attrib=get_rect_attrib_dict(16-i, 15*j)) )

    start_date = datetime.date(year, 1, 1)
    for i in range(364):
        date = start_date + datetime.timedelta(i)
        date_elements[i].attrib["data-date"] = str(date)

    for month, x in [("Jan",16), ("Feb",106), ("Mar",166), ("Apr",226), ("May",286), ("Jun",361), ("Jul",421), ("Aug",481), ("Oct",616), ("Nov",691), ("Dec",751)]:
        ET.SubElement(g, "text", attrib=get_month_label_attrib_dict(x, -8)).text = month

    for day, dy in [("Mon",25), ("Wed",56), ("Fri",85)]:
        ET.SubElement(g, "text", attrib=get_day_label_attrib_dict(-10, dy)).text = day

    return svg, date_elements

def create_workout_tracker(year=2021):
    svg, date_elements = create_activity_tracker()
    with open("_data/workout_log.yml", "r") as f:
        w = yaml.load(f, Loader=yaml.FullLoader)
        for date, log in w.items():
            i = (date - datetime.date(year, 1, 1)).days
            date_elements[i].attrib["class"] = "calendar-day-color-L3"
#from IPython import embed; embed(); assert False

svg_bstr = ET.tostring(svg, method="xml")
xml_str = minidom.parseString(svg_bstr).toprettyxml(indent="    ")
with open("_includes/activity_tracker.html", "w") as f:
    xml_str = "\n".join(xml_str.splitlines()[1:])
    f.write(xml_str)

