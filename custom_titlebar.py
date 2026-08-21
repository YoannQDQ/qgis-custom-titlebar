import configparser
from pathlib import Path

from qgis.core import QgsApplication
from qgis.PyQt.QtCore import QSettings, QTranslator
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction, QDialog, QMessageBox, QWidget

from .settings_dialog import SettingsDialog
from .utils import fillTemplate

DEFAULT_TEMPLATE = "{modified}{project} — QGIS {version}-{versionName} [{profile}]"


class CustomTitleBar:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = Path(__file__).parent
        # initialize locale
        locale = QSettings().value("locale/userLocale")[0:2]
        locale_path = self.plugin_dir / "i18n" / f"CustomTitleBar_{locale}.qm"

        if locale_path.exists():
            self.translator = QTranslator()
            self.translator.load(str(locale_path))
            QgsApplication.installTranslator(self.translator)
        self.settings = QSettings()
        self.settings.beginGroup("plugins/custom_titlebar")
        self.template = self.settings.value("template", DEFAULT_TEMPLATE)
        self.actions = []

    def tr(self, message):
        """Get the translation for a string using Qt translation API."""
        return QgsApplication.translate("CustomTitleBar", message)

    def initGui(self):
        self.iface.mainWindow().windowTitleChanged.connect(self.updateTitleBarText)
        self.updateTitleBarText()

        self.plugin_menu = self.iface.pluginMenu().addMenu(
            self.icon(), "Custom TitleBar"
        )

        self.about_action = QAction(
            QgsApplication.getThemeIcon("mIconInfo.svg"),
            self.tr("About"),
            parent=self.iface.mainWindow(),
        )
        self.about_action.triggered.connect(self.show_about)

        self.settings_action = QAction(
            QgsApplication.getThemeIcon("console/iconSettingsConsole.svg"),
            self.tr("Settings"),
            parent=self.iface.mainWindow(),
        )
        self.settings_action.triggered.connect(self.show_settings)

        self.plugin_menu.addAction(self.about_action)
        self.plugin_menu.addAction(self.settings_action)

        self.dialog = SettingsDialog(self.iface.mainWindow())

    def icon(self):
        return QIcon(str(self.plugin_dir / "icon.svg"))

    def unload(self):
        self.iface.pluginMenu().removeAction(self.plugin_menu.menuAction())
        self.iface.mainWindow().windowTitleChanged.disconnect(self.updateTitleBarText)

    def updateTitleBarText(self):
        caption = fillTemplate(self.template)
        if caption is not None and caption != self.iface.mainWindow().windowTitle():
            self.iface.mainWindow().setWindowTitle(caption)

    def setTemplate(self, template):
        caption = fillTemplate(template)
        if caption is not None:
            self.template = template
            self.updateTitleBarText()
            self.settings.setValue("template", template)

    def show_about(self):
        # Used to display plugin icon in the about message box
        bogus = QWidget(self.iface.mainWindow())
        bogus.setWindowIcon(self.icon())
        cfg = configparser.ConfigParser()
        cfg.read(self.plugin_dir / "metadata.txt")
        version = cfg.get("general", "version")
        QMessageBox.about(
            bogus,
            self.tr("About Custom TitleBar"),
            "<b>Version</b> {}<br><br>"
            "<b>{}</b> : <a href=https://github.com/YoannQDQ/qgis-custom-titlebar>GitHub</a><br>"
            "<b>{}</b> : <a href=https://github.com/YoannQDQ/qgis-custom-titlebar/issues>GitHub</a><br>"
            "<b>{}</b> : <a href=https://github.com/YoannQDQ/qgis-custom-titlebar>GitHub</a>".format(
                version,
                self.tr("Source code"),
                self.tr("Report issues"),
                self.tr("Documentation"),
            ),
        )
        bogus.deleteLater()

    def show_settings(self):
        res = self.dialog.exec(self.template)
        if res == QDialog.DialogCode.Accepted:
            self.setTemplate(self.dialog.templateLineEdit.value())
