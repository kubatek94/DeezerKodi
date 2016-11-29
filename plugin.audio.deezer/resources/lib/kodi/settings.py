import xml.etree.ElementTree as ET

class Settings(object):
    settings = {}
    onChange = [] #users can add callbacks here to be notified whenever a setting has been changed in the UI

    def __init__(self, addon, path):
        self._addon = addon
        self._path = path
        self.settings = self.read()

    def read(self):
        tree = ET.parse(self._path)
        settings = {}
        for setting in tree.getroot().iterfind('setting'):
            settings[setting.attrib['id']] = self._addon.getSetting(setting.attrib['id'])
        return settings

    def open(self):
        self._addon.openSettings()
        freshSettings = self.read()
        if self.onChange:
            changes = [{k: {'old':self.settings[k], 'new':freshSettings[k]}} for k in freshSettings if self.settings[k] != freshSettings[k]]
            self.settings = freshSettings
            for listener in self.onChange:
                listener(changes)
        else:
            self.settings = freshSettings

    def __setitem__(self, key, value):
        self.settings[key] = value
        self._addon.setSetting(key, value)

    def __getitem__(self, item):
        return self.settings[item]

    def __iter__(self):
        return self.settings.__iter__()

    def __contains__(self, item):
        return self.settings.__contains__(item)