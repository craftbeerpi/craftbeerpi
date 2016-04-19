/*!
 * AngularJS 1.x directive for excellent Mikhus's HTML5 Canvas Gauge
 *
 * https://github.com/Mikhus/canv-gauge
 * https://github.com/dec/angular-canvas-gauge
 *
 * This code is subject to MIT license.
 *
 * Copyright (c) 2016 David Esperalta - http://www.davidesperalta.com/
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy of
 * this software and associated documentation files (the "Software"), to deal in
 * the Software without restriction, including without limitation the rights to use,
 * copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the
 * Software, and to permit persons to whom the Software is furnished to do so,
 * subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in all
 * copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
 * FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
 * COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
 * IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
 * CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
 *
 */
angular.module('angular-canvas-gauge', []).directive('canvasGauge', function() {

  return {
    restrict: 'A',
    link: function(scope, element, attributes) {

      // Defaultl Gauge's config/options
      var
        options = {
          renderTo: attributes.id,
          value: 0,
          width: 200,
          height: 200,
          title: false,
          maxValue: 100,
          minValue: 0,
          majorTicks: [],
          minorTicks: 10,
          strokeTicks: true,
          units: false,
          valueFormat: {
            'int': 3,
            'dec': 2
          },
          glow: true,
          animation: {
            delay: 10,
            duration: 250,
            fn: 'cycle'
          },
          colors: {
            plate: '#fff',
            majorTicks: '#444',
            minorTicks: '#666',
            title: '#888',
            units: '#888',
            numbers: '#444',
            needle: {
              start: 'rgba(240, 128, 128, 1)',
              end: 'rgba(255, 160, 122, .9)',
              circle: {
                outerStart: '#f0f0f0',
                outerEnd: '#ccc',
                innerStart: '#e8e8e8',
                innerEnd: '#f5f5f5'
              },
              shadowUp: 'rgba(2, 255, 255, 0.2)',
              shadowDown: 'rgba(188, 143, 143, 0.45)'
            },
            valueBox: {
              rectStart: '#888',
              rectEnd: '#666',
              background: '#babab2',
              shadow: 'rgba(0, 0, 0, 1)'
            },
            valueText: {
              foreground: '#444',
              shadow: 'rgba(0, 0, 0, 0.3)'
            },
            circle: {
              shadow: 'rgba(0, 0, 0, 0.5)',
              outerStart: '#ddd',
              outerEnd: '#aaa',
              middleStart: '#eee',
              middleEnd: '#f0f0f0',
              innerStart: '#fafafa',
              innerEnd: '#ccc'
            }
          },
          circles: {
            outerVisible: true,
            middleVisible: true,
            innerVisible: true
          },
          valueBox: {
            visible: true
          },
          valueText: {
            visible: true
          },
          highlights: [{
            from: 20,
            to: 60,
            color: '#eee'
          }, {
            from: 60,
            to: 80,
            color: '#ccc'
          }, {
            from: 80,
            to: 100,
            color: '#999'
          }]
        };

      // We can draw now the Gauge using the default options
      var
        gauge = new Gauge(options);
      gauge.draw();

      // This function is taken "as is" (with little minor changes) from the
      // canv-gauge project. If someday such project implement this function
      // in a public way, then we can simply use it and remove from here.
      // The function is used to parse the gauge's "hightlights" attribute.
      var
        parseHightlights = function(value) {
          var
            result = [];

          if (value === '') {
            return result;
          }

          var
            hls = value.match(/(?:(?:-?\d*\.)?(-?\d+){1,2} ){2}(?:(?:#|0x)?(?:[0-9A-F|a-f]){3,8}|rgba?\(.*?\))/g);

          if (hls === null) {
            return result;
          }

          for (var j = 0, l = hls.length; j < l; j++) {
            var
              cfg = hls[j].trim().split(/\s+/),
              hlCfg = {};

            if (cfg[0] && cfg[0] != '') {
              hlCfg.from = cfg[0];
            }

            if (cfg[1] && cfg[1] != '') {
              hlCfg.to = cfg[1];
            }

            if (cfg[2] && cfg[2] != '') {
              hlCfg.color = cfg[2];
            }

            result.push(hlCfg);
          }
          return result;
        };

      // Auxiliar function to find true directive's arguments
      var
        isTrue = function(value) {
          return value === 'true';
        };

      // Auxiliar function to retrive the gauge's current config
      var
        getConfig = function() {
          return gauge.updateConfig({}).config;
        };

      /* Observers for the directive attributes */

      attributes.$observe('value', function(value) {
        gauge.setValue(value);
      });

      attributes.$observe('valueFormat', function(value) {
        var
          arg = value.split('.');
        gauge.updateConfig(getConfig().valueFormat['int'] = arg[0] || undefined);
        gauge.updateConfig(getConfig().valueFormat['dec'] = arg[1] || undefined);
      });

      attributes.$observe('glow', function(value) {
        gauge.updateConfig({glow: isTrue(value)});
      });

      attributes.$observe('title', function(value) {
        gauge.updateConfig({title: value});
      });

      attributes.$observe('units', function(value) {
        gauge.updateConfig({units: value});
      });

      attributes.$observe('width', function(value) {
        gauge.updateConfig({width: value});
      });

      attributes.$observe('height', function(value) {
        gauge.updateConfig({height: value});
      });

      attributes.$observe('minValue', function(value) {
        gauge.updateConfig({minValue: value});
      });

      attributes.$observe('maxValue', function(value) {
        gauge.updateConfig({maxValue: parseFloat(value)});
      });

      attributes.$observe('minorTicks', function(value) {
        gauge.updateConfig({minorTicks: parseFloat(value)});
      });

      attributes.$observe('majorTicks', function(value) {
        // canv-gauge expect an array here. From an string like "0 10 20 30"
        // canv-gauge expect [0, 10, 20, 30], so simply uses the split function
        gauge.updateConfig({majorTicks: value.split(' ')});
      });

      attributes.$observe('highlights', function(value) {
        // canv-gauge expect a complex object for this argument, take above to
        // the "parseHightlights" function, who parses the attribute's string.
        gauge.updateConfig({highlights: parseHightlights(value)});
      });

      attributes.$observe('strokeTicks', function(value) {
        gauge.updateConfig({strokeTicks: isTrue(value)});
      });

      attributes.$observe('animationFn', function(value) {
        gauge.updateConfig(getConfig().animation.fn = value);
      });

      attributes.$observe('animationDelay', function(value) {
        gauge.updateConfig(getConfig().animation.delay = parseFloat(value));
      });

      attributes.$observe('animationDuration', function(value) {
        gauge.updateConfig(getConfig().animation.duration = parseFloat(value));
      });

      attributes.$observe('colorsPlate', function(value) {
        gauge.updateConfig(getConfig().colors.plate = value);
      });

      attributes.$observe('colorsUnits', function(value) {
        gauge.updateConfig(getConfig().colors.units = value);
      });

      attributes.$observe('colorsTitle', function(value) {
        gauge.updateConfig(getConfig().colors.title = value);
      });

      attributes.$observe('colorsNumbers', function(value) {
        gauge.updateConfig(getConfig().colors.numbers = value);
      });

      attributes.$observe('colorsNeedleStart', function(value) {
        gauge.updateConfig(getConfig().colors.needle.start = value);
      });

      attributes.$observe('colorsNeedleEnd', function(value) {
        gauge.updateConfig(getConfig().colors.needle.end = value);
      });

      attributes.$observe('colorsNeedleShadowup', function(value) {
        gauge.updateConfig(getConfig().colors.needle.shadowUp = value);
      });

      attributes.$observe('colorsNeedleShadowdown', function(value) {
        gauge.updateConfig(getConfig().colors.needle.shadowDown = value);
      });

      attributes.$observe('colorsNeedleCircleOuterstart', function(value) {
        gauge.updateConfig(getConfig().colors.needle.circle.outerStart = value);
      });

      attributes.$observe('colorsNeedleCircleOuterend', function(value) {
        gauge.updateConfig(getConfig().colors.needle.circle.outerEnd = value);
      });

      attributes.$observe('colorsNeedleCircleInnerstart', function(value) {
        gauge.updateConfig(getConfig().colors.needle.circle.innerStart = value);
      });

      attributes.$observe('colorsNeedleCircleInnerend', function(value) {
        gauge.updateConfig(getConfig().colors.needle.circle.innerEnd = value);
      });

      attributes.$observe('colorsValueboxRectstart', function(value) {
        gauge.updateConfig(getConfig().colors.valueBox.rectStart = value);
      });

      attributes.$observe('colorsValueboxRectend', function(value) {
        gauge.updateConfig(getConfig().colors.valueBox.rectEnd = value);
      });

      attributes.$observe('colorsValueboxBackground', function(value) {
        gauge.updateConfig(getConfig().colors.valueBox.background = value);
      });

      attributes.$observe('colorsValueboxShadow', function(value) {
        gauge.updateConfig(getConfig().colors.valueBox.shadow = value);
      });

      attributes.$observe('colorsValuetextForeground', function(value) {
        gauge.updateConfig(getConfig().colors.valueText.foreground = value);
      });

      attributes.$observe('colorsValuetextShadow', function(value) {
        gauge.updateConfig(getConfig().colors.valueText.shadow = value);
      });

      attributes.$observe('colorsCircleShadow', function(value) {
        gauge.updateConfig(getConfig().colors.circle.shadow = value);
      });

      attributes.$observe('colorsCircleOuterstart', function(value) {
        gauge.updateConfig(getConfig().colors.circle.outerStart = value);
      });

      attributes.$observe('colorsCircleOuterend', function(value) {
        gauge.updateConfig(getConfig().colors.circle.outerEnd = value);
      });

      attributes.$observe('colorsCircleMiddlestart', function(value) {
        gauge.updateConfig(getConfig().colors.circle.middleStart = value);
      });

      attributes.$observe('colorsCircleMiddleend', function(value) {
        gauge.updateConfig(getConfig().colors.circle.middleEnd = value);
      });

      attributes.$observe('colorsCircleInnerstart', function(value) {
        gauge.updateConfig(getConfig().colors.circle.innerStart = value);
      });

      attributes.$observe('colorsCircleInnerend', function(value) {
        gauge.updateConfig(getConfig().colors.circle.innerEnd = value);
      });

      attributes.$observe('colorsMinorTicks', function(value) {
        gauge.updateConfig(getConfig().colors.minorTicks = value);
      });

      attributes.$observe('colorsMajorTicks', function(value) {
        gauge.updateConfig(getConfig().colors.majorTicks = value);
      });

      attributes.$observe('valueboxVisible', function(value) {
        gauge.updateConfig(getConfig().valueBox.visible = isTrue(value));
      });

      attributes.$observe('valuetextVisible', function(value) {
        gauge.updateConfig(getConfig().valueText.visible = isTrue(value));
      });

      attributes.$observe('circlesOutervisible', function(value) {
        gauge.updateConfig(getConfig().circles.outerVisible = isTrue(value));
      });

      attributes.$observe('circlesMiddlevisible', function(value) {
        gauge.updateConfig(getConfig().circles.middleVisible = isTrue(value));
      });

      attributes.$observe('circlesInnervisible', function(value) {
        gauge.updateConfig(getConfig().circles.innerVisible = isTrue(value));
      });
    }
  }
});