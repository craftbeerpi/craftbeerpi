
# angular-canvas-gauge

This is an AngularJS 1.x directive for the excellent Mikhus's canv-gauge project we can found at https://github.com/Mikhus/canv-gauge

## Install

From bower :

`bower  install angular-canvas-gauge` 

## How this work?

Just add the "angular-canvas-gauge.js" or "angular-canvas-gauge.min.js" and inject the "angular-canvas-gauge" in your application's module.

Then add the "canvas-gauge" directive in your CANVAS tag, something like this:

    <canvas canvas-gauge id="myGauge" ...>

As you can see above the CANVAS tag must have an ID attribute. No other requeriment is needed. You can start to use all the "data-*" attributes that Mikhus's canv-gauge provide to us.

For example, you can place the "data-glow" attribute in your CANVAS tag like below:

    <canvas canvas-gauge id="myGauge" data-glow="{{Variable}}" ...>

Then, just set your "Variable" to "true" or "false" in order to show or hide the gauge's glow.

---

(c) 2016 David Esperalta - http://www.davidesperalta.com/
