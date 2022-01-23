/*
 * View model for Timelapse Purger
 *
 * Author: jneilliii
 * License: AGPLv3
 */
$(function() {
    function TimelapsepurgerViewModel(parameters) {
        var self = this;

        self.settingsViewModel = parameters[0];

        // TODO: Implement your plugin's view model here.
    }

    OCTOPRINT_VIEWMODELS.push({
        construct: TimelapsepurgerViewModel,
        dependencies: ["settingsViewModel"],
        elements: ["#settings_plugin_timelapsepurger"]
    });
});
