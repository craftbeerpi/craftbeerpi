/**
 * 'showNotification' callback.
 *
 * @callback ShowNotificationCallback
 * @param {error} [error] - The error object in case of any error
 * @param {function} [hide] - The hide notification function
 */

/**
 * @ngdoc method
 * @function
 * @memberof! webNotification
 * @alias webNotification.initWebNotification
 * @private
 *
 * @description
 * Initializes the angular web notification service.
 *
 * @param {object} notifyLib - The HTML5 notification library instance
 */
(function initWebNotification(notifyLib) {
    'use strict';

    var webNotification = window.angular.module('angular-web-notification', []);

    /**
     * @ngdoc service
     * @name webNotification
     * @namespace webNotification
     * @author Sagie Gur-Ari
     * @returns {object} The service instance
     *
     * @description
     * The web notification service wraps the HTML 5 Web Notifications API as an angular service.
     */
    webNotification.factory('webNotification', function onCreateService() {
        var service = {};

        /**
         * True to enable automatic requesting of permissions if needed.
         *
         * @memberof! webNotification
         * @alias webNotification.allowRequest
         * @public
         */
        service.allowRequest = true; //true to enable automatic requesting of permissions if needed

        Object.defineProperty(service, 'permissionGranted', {
            /**
             * Returns the permission granted value.
             *
             * @function
             * @memberof! webNotification
             * @private
             * @returns {boolean} True if permission is granted, else false
             */
            get: function getPermission() {
                var permission = notifyLib.permissionLevel();

                /**
                 * True if permission is granted, else false.
                 *
                 * @memberof! webNotification
                 * @alias webNotification.permissionGranted
                 * @public
                 */
                var permissionGranted = false;
                if (permission === notifyLib.PERMISSION_GRANTED) {
                    permissionGranted = true;
                }

                return permissionGranted;
            }
        });

        /**
         * @ngdoc method
         * @function
         * @memberof! webNotification
         * @alias webNotification.isEnabled
         * @private
         *
         * @description
         * Checks if web notifications are permitted.
         *
         * @returns {boolean} True if allowed to show web notifications
         */
        var isEnabled = function () {
            var enabled = notifyLib.isSupported;

            if (enabled) {
                enabled = service.permissionGranted;
            }

            return enabled;
        };

        /**
         * @ngdoc method
         * @function
         * @memberof! webNotification
         * @alias webNotification.createAndDisplayNotification
         * @private
         *
         * @description
         * Displays the web notification and returning a 'hide' notification function.
         *
         * @param {string} title - The notification title text (defaulted to empty string if null is provided)
         * @param {object} options - Holds the notification data (web notification API spec for more info)
         * @param {number} [options.autoClose] - Auto closes the notification after the provided amount of millies (0 or undefined for no auto close)
         * @param {function} [options.onClick] - An optional onclick event handler
         * @returns {function} The hide notification function
         */
        var createAndDisplayNotification = function (title, options) {
            var autoClose = 0;
            if (options && options.autoClose && (typeof options.autoClose === 'number')) {
                autoClose = options.autoClose;
            }
            notifyLib.config({
                autoClose: autoClose
            });

            var notification = notifyLib.createNotification(title, options);

            //add onclick handler
            if (options.onClick && notification && notification.webNotification) {
                notification.webNotification.onclick = options.onClick;
            }

            return function hideNotification() {
                notification.close();
            };
        };

        /**
         * @ngdoc method
         * @function
         * @memberof! webNotification
         * @alias webNotification.parseInput
         * @private
         *
         * @description
         * Returns an object with the show notification input.
         *
         * @param {array} argumentsArray - An array of all arguments provided to the show notification function
         * @returns {object} The parsed data
         */
        var parseInput = function (argumentsArray) {
            //callback is always the last argument
            var callback = argumentsArray.pop();

            var title = null;
            var options = null;
            if (argumentsArray.length === 2) {
                title = argumentsArray[0];
                options = argumentsArray[1];
            } else if (argumentsArray.length === 1) {
                var value = argumentsArray.pop();
                if (typeof value === 'string') {
                    title = value;
                    options = {};
                } else {
                    title = '';
                    options = value;
                }
            }

            //set defaults
            title = title || '';
            options = options || {};

            return {
                callback: callback,
                title: title,
                options: options
            };
        };

        /**
         * Shows the notification based on the provided input.<br>
         * The callback invoked will get an error object (in case of an error, null in
         * case of no errors) and a 'hide' function which can be used to hide the notification.
         *
         * @function
         * @memberof! webNotification
         * @alias webNotification.showNotification
         * @public
         * @param {string} [title] - The notification title text (defaulted to empty string if null is provided)
         * @param {object} [options] - Holds the notification data (web notification API spec for more info)
         * @param {number} [options.autoClose] - Auto closes the notification after the provided amount of millies (0 or undefined for no auto close)
         * @param {function} [options.onClick] - An optional onclick event handler
         * @param {ShowNotificationCallback} callback - Called after the show is handled.
         * @example
         * ```js
         * webNotification.showNotification('Example Notification', {
         *    body: 'Notification Text...',
         *    icon: 'my-icon.ico',
         *    onClick: function onNotificationClicked() {
         *      console.log('Notification clicked.');
         *    },
         *    autoClose: 4000 //auto close the notification after 4 seconds (you can manually close it via hide function)
         * }, function onShow(error, hide) {
         *    if (error) {
         *        window.alert('Unable to show notification: ' + error.message);
         *    } else {
         *        setTimeout(function hideNotification() {
         *            hide();
         *        }, 5000);
         *    }
         * });
         * ```
         */
        service.showNotification = function () {
            //convert to array to enable modifications
            var argumentsArray = Array.prototype.slice.call(arguments, 0);

            if ((argumentsArray.length >= 1) && (argumentsArray.length <= 3)) {
                var data = parseInput(argumentsArray);

                //get values
                var callback = data.callback;
                var title = data.title;
                var options = data.options;

                var hideNotification = null;
                if (isEnabled()) {
                    hideNotification = createAndDisplayNotification(title, options);
                    callback(null, hideNotification);
                } else if (service.allowRequest) {
                    notifyLib.requestPermission(function onRequestDone() {
                        if (isEnabled()) {
                            hideNotification = createAndDisplayNotification(title, options);
                            callback(null, hideNotification);
                        } else {
                            callback(new Error('Notifications are not enabled.'), null);
                        }
                    });
                } else {
                    callback(new Error('Notifications are not enabled.'), null);
                }
            }
        };

        return service;
    });
}(window.notify));
