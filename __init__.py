"""
/***************************************************************************
 Custom TitleBar
 A QGIS plugin
 Adds the current QGIS version in the titlebar

                              -------------------
        begin                : 2020-04-29
        git sha              : $Format:%H$
        copyright            : (C) 2023 Yoann Quenach de Quivillic
        email                : yoann.quenach@gmail.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""


def classFactory(iface):
    from .custom_titlebar import CustomTitleBar

    return CustomTitleBar(iface)
