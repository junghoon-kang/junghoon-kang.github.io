import yaml
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

    date_elements = []
    for i in range(53):
        _g = ET.SubElement(g, "g", attrib=dict(transform=f"translate({i*16}, 0)"))
        if i == 0:
            date_elements.append( ET.SubElement(_g, "rect", attrib=get_rect_attrib_dict(16, 75)) )
            temp = ET.SubElement(_g, "rect", attrib=get_rect_attrib_dict(16, 90))
            temp.attrib["class"] = "calendar-day-color-L3"
            date_elements.append( temp )
        elif i == 52:
            date_elements.append( ET.SubElement(_g, "rect", attrib=get_rect_attrib_dict(-36, 0)) )
            date_elements.append( ET.SubElement(_g, "rect", attrib=get_rect_attrib_dict(-36, 15)) )
            date_elements.append( ET.SubElement(_g, "rect", attrib=get_rect_attrib_dict(-36, 30)) )
            date_elements.append( ET.SubElement(_g, "rect", attrib=get_rect_attrib_dict(-36, 45)) )
            date_elements.append( ET.SubElement(_g, "rect", attrib=get_rect_attrib_dict(-36, 60)) )
        else:
            for j in range(7):
                date_elements.append( ET.SubElement(_g, "rect", attrib=get_rect_attrib_dict(16-i, 15*j)) )

    for month, x in [("Jan",16), ("Feb",106), ("Mar",166), ("Apr",226), ("May",286), ("Jun",361), ("Jul",421), ("Aug",481), ("Oct",616), ("Nov",691), ("Dec",751)]:
        ET.SubElement(g, "text", attrib=get_month_label_attrib_dict(x, -8)).text = month

    for day, dy in [("Mon",25), ("Wed",56), ("Fri",85)]:
        ET.SubElement(g, "text", attrib=get_day_label_attrib_dict(-10, dy)).text = day

    return svg, date_elements

with open("_data/workout_log.yml", "r") as f:
    w = yaml.load(f, Loader=yaml.FullLoader)
from IPython import embed; embed(); assert False
svg, date_elements = create_activity_tracker()

svg_bstr = ET.tostring(svg, method="xml")
xml_str = minidom.parseString(svg_bstr).toprettyxml(indent="    ")
with open("_includes/activity_tracker.html", "w") as f:
    xml_str = "\n".join(xml_str.splitlines()[1:])
    f.write(xml_str)

