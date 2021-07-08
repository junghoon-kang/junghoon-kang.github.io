import xml.etree.cElementTree as ET
from xml.dom import minidom


svg = ET.Element("svg")
g = ET.SubElement(svg, "g", attrib=dict(transform="translate(10, 20)"))

for i in range(53):
    _g = ET.SubElement(g, "g", attrib=dict(transform=f"translate({i*16}, 0)"))
    if i == 0:
        ET.SubElement(_g, "rect", attrib=dict(id="box", width="11", height="11", x="16", y="75", rx="2", ry="2"))
        ET.SubElement(_g, "rect", attrib=dict(id="box", width="11", height="11", x="16", y="90", rx="2", ry="2"))
    elif i == 52:
        ET.SubElement(_g, "rect", attrib=dict(id="box", width="11", height="11", x="-36", y="0",  rx="2", ry="2"))
        ET.SubElement(_g, "rect", attrib=dict(id="box", width="11", height="11", x="-36", y="15", rx="2", ry="2"))
        ET.SubElement(_g, "rect", attrib=dict(id="box", width="11", height="11", x="-36", y="30", rx="2", ry="2"))
        ET.SubElement(_g, "rect", attrib=dict(id="box", width="11", height="11", x="-36", y="45", rx="2", ry="2"))
        ET.SubElement(_g, "rect", attrib=dict(id="box", width="11", height="11", x="-36", y="60", rx="2", ry="2"))
    else:
        for j in range(7):
            ET.SubElement(_g, "rect", attrib=dict(id="box", width="11", height="11", x=f"{16-i}", y=f"{15*j}",  rx="2", ry="2"))

ET.SubElement(g, "text", attrib=dict(x="16", y="-8",  foo="Calendar-label")).text = "Jan"
ET.SubElement(g, "text", attrib=dict(x="106", y="-8", foo="Calendar-label")).text = "Feb"
ET.SubElement(g, "text", attrib=dict(x="166", y="-8", foo="Calendar-label")).text = "Mar"
ET.SubElement(g, "text", attrib=dict(x="226", y="-8", foo="Calendar-label")).text = "Arp"
ET.SubElement(g, "text", attrib=dict(x="286", y="-8", foo="Calendar-label")).text = "May"
ET.SubElement(g, "text", attrib=dict(x="361", y="-8", foo="Calendar-label")).text = "Jun"
ET.SubElement(g, "text", attrib=dict(x="421", y="-8", foo="Calendar-label")).text = "Jul"
ET.SubElement(g, "text", attrib=dict(x="481", y="-8", foo="Calendar-label")).text = "Aug"
ET.SubElement(g, "text", attrib=dict(x="556", y="-8", foo="Calendar-label")).text = "Sep"
ET.SubElement(g, "text", attrib=dict(x="616", y="-8", foo="Calendar-label")).text = "Oct"
ET.SubElement(g, "text", attrib=dict(x="691", y="-8", foo="Calendar-label")).text = "Nov"
ET.SubElement(g, "text", attrib=dict(x="751", y="-8", foo="Calendar-label")).text = "Dec"

svg_bstr = ET.tostring(svg, method="xml")
xml_str = minidom.parseString(svg_bstr).toprettyxml(indent="    ")
with open("index.html", "w") as f:
    f.write(
        "---\n"
        "layerout: default\n"
        "title: Home\n"
        "---\n"
    )
    xml_str = "\n".join(xml_str.splitlines()[1:])
    f.write(xml_str)
#from IPython import embed; embed(); assert False
