from scour import scour
from inkex import SvgDocumentElement
from lxml import etree
import copy

def get_proper_svg_string(
    svg: SvgDocumentElement,
    indent_type: str,
    number_of_indents: int,
    optimize: bool
) -> str:
    if optimize:
        svg_string = etree.tostring(svg, encoding="unicode")

        scour_options = scour.sanitizeOptions()

        scour_options.strip_xml_prolog = True
        scour_options.indent_type = indent_type
        scour_options.indent_depth = number_of_indents

        proper_svg_string = scour.scourString(svg_string, scour_options)
    else:
        if indent_type == "space":
            indent = " "
        elif indent_type == "tab":
            indent = "\t"

        svg_copy = copy.deepcopy(svg)

        etree.indent(svg_copy, space=indent * number_of_indents)

        proper_svg_string = etree.tostring(svg_copy, encoding="unicode", pretty_print=True)

    return proper_svg_string
