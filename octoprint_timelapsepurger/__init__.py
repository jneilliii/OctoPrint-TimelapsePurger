# coding=utf-8
from __future__ import absolute_import


import octoprint.plugin
from octoprint.events import Events
import os
import time


class TimelapsepurgerPlugin(octoprint.plugin.SettingsPlugin,
                            octoprint.plugin.AssetPlugin,
                            octoprint.plugin.TemplatePlugin,
                            octoprint.plugin.EventHandlerPlugin,
                            octoprint.plugin.StartupPlugin
                            ):

    def __init__(self):
        self.monitored_events = [Events.MOVIE_DONE, Events.STARTUP]

    def on_after_startup(self):
        if hasattr(Events, "PLUGIN_OCTOLAPSE_MOVIE_DONE"):
            self.monitored_events.append(Events.PLUGIN_OCTOLAPSE_MOVIE_DONE)

    def on_event(self, event, payload):
        if event in self.monitored_events:
            if self._settings.get_int(["cut_off_length"]) > 0:
                self._logger.debug("Purging timelapses older than {} days.".format(self._settings.get(["cut_off_length"])))
                path = self._settings.getBaseFolder("timelapse")
                now = time.time()
                for file in os.listdir(path):
                    file = os.path.join(path, file)
                    if os.stat(file).st_mtime < now - self._settings.get_int(["cut_off_length"]) * 86400:
                        if os.path.isfile(file):
                            self._logger.debug("Deleting {}.".format(file))
                            try:
                                os.remove(file)
                            except Exception:
                                self._logger.error("There was an error removing the file {}".format(file))

    # ~~ SettingsPlugin mixin

    def get_settings_defaults(self):
        return {
            "cut_off_length": 0
        }

    # ~~ AssetPlugin mixin

    def get_assets(self):
        return {
            "js": ["js/timelapsepurger.js"]
        }

    # ~~ TemplatePlugin mixin

    def get_template_vars(self):
        return {"plugin_version": self._plugin_version}

    # ~~ Softwareupdate hook

    def get_update_information(self):
        return {
            "timelapsepurger": {
                "displayName": "Timelapse Purger",
                "displayVersion": self._plugin_version,
                "type": "github_release",
                "user": "jneilliii",
                "repo": "OctoPrint-TimelapsePurger",
                "current": self._plugin_version,
                "pip": "https://github.com/jneilliii/OctoPrint-TimelapsePurger/archive/{target_version}.zip",
            }
        }


__plugin_name__ = "Timelapse Purger"
__plugin_pythoncompat__ = ">=3,<4"  # only python 3

def __plugin_load__():
    global __plugin_implementation__
    __plugin_implementation__ = TimelapsepurgerPlugin()

    global __plugin_hooks__
    __plugin_hooks__ = {
        "octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information
    }
