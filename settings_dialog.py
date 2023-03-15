import os
from functools import partial

from qgis.PyQt.QtWidgets import QDialog, QDialogButtonBox
from qgis.PyQt.uic import loadUi

from .utils import fillTemplate, modified, profile, project, sha, version, versionName


class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        loadUi(os.path.join(os.path.dirname(__file__), "settings_dialog.ui"), self)

        self.templateLineEdit.valueChanged.connect(self.updatePreview)
        self.buttonBox.clicked.connect(self.buttonClicked)

        self.profileLabel.setText(profile())
        self.versionLabel.setText(version())
        self.versionNameLabel.setText(versionName())
        self.modifiedLabel.setText(modified())
        self.projectLabel.setText(project())
        self.shaLabel.setText(sha())
        self.updatePreview()

        self.profileButton.clicked.connect(
            partial(self.templateLineEdit.insert, "{profile}")
        )
        self.versionButton.clicked.connect(
            partial(self.templateLineEdit.insert, "{version}")
        )
        self.versionNameButton.clicked.connect(
            partial(self.templateLineEdit.insert, "{versionName}")
        )
        self.modifiedButton.clicked.connect(
            partial(self.templateLineEdit.insert, "{modified}")
        )
        self.projectButton.clicked.connect(
            partial(self.templateLineEdit.insert, "{project}")
        )
        self.shaButton.clicked.connect(partial(self.templateLineEdit.insert, "{sha}"))

    def updatePreview(self):
        caption = fillTemplate(self.templateLineEdit.value())
        if caption is not None:
            self.previewLabel.setText(caption)
        else:
            self.previewLabel.setText(self.tr("Invalid template"))

    def buttonClicked(self, button):
        if button == self.buttonBox.button(QDialogButtonBox.Reset):
            self.templateLineEdit.clearValue()
        elif button == self.buttonBox.button(QDialogButtonBox.Ok):
            self.accept()
        elif button == self.buttonBox.button(QDialogButtonBox.Cancel):
            self.reject()

    def exec(self, template):
        self.templateLineEdit.setText(template)
        self.modifiedLabel.setText(modified())
        self.projectLabel.setText(project())
        return super().exec()
