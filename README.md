Sloth (a collection of bears)
=============================
[WS2801](http://www.aliexpress.com/item/5m-roll-LED-digital-flexible-strip-WS2801-IC-256-scale-8-bit-32pcs-5050-RGB-leds/528477260.html
) (aka 'Dream Colour') [LED light strip control from the RaspberryPi](http://learn.adafruit.com/light-painting-with-raspberry-pi/). Relies on
the [AdaFruit Occidentalis Raspian](http://learn.adafruit.com/adafruit-raspberry-pi-educational-linux-distro/overview) image. The main purpose of this setup is to display
build information from our [Jenkins](http://jenkins-ci.org/) server, but it is intended that other displays
can be easily added.

### Development light-show visualization:
The sloth script accepts one parameter which is the driver used to display the lights. Supported drivers are:
  1. WS2801: draw led data to a SPI led strip
  2. Visualizer: pops up a raster window representing the led strip

By default sloth will load the WS2801 driver unless other driver is specified. Use the following command in development mode:

        sloth Visualizer

Note that DriverVisualizer requires [ActiveTcl](http://www.activestate.com/activetcl/downloads) on OS X and [TkInter](https://wiki.python.org/moin/TkInter) on Linux.
