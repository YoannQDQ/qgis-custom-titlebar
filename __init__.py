"""
Custom TitleBar
A QGIS plugin
Adds the current QGIS version in the titlebar
"""


def classFactory(iface):
    from .custom_titlebar import CustomTitleBar

    return CustomTitleBar(iface)
