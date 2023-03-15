import os.path
import re

from qgis.core import Qgis, QgsApplication, QgsProject
from qgis.utils import iface


def profile():
    if Qgis.versionInt() >= 33000:
        return iface.userProfileManager().userProfile().name()
    else:
        return os.path.basename(
            QgsApplication.instance().qgisSettingsDirPath().rstrip("/\\")
        )


def project():
    if QgsProject.instance().title():
        return QgsProject.instance().title()
    if QgsProject.instance().fileName():
        return QgsProject.instance().baseName()
    return QgsApplication.translate("QgisApp", "Untitled Project")


def versionName():
    return re.sub(r"^[\d\s.-]*", "", Qgis.version())


def version():
    strVersion = str(Qgis.versionInt())
    return "{}.{}.{}".format(strVersion[0], strVersion[1:3], strVersion[3:])


def sha():
    return Qgis.devVersion()


def modified():
    if QgsProject.instance().isDirty():
        return "*"
    return ""


def fillTemplate(template):
    parameters = {
        "modified": modified(),
        "project": project(),
        "version": version(),
        "sha": sha(),
        "version": version(),
        "versionName": versionName(),
        "profile": profile(),
    }
    try:
        return template.format_map(parameters)
    except (KeyError, ValueError):
        return None
