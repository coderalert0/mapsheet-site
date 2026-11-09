---
title: How Accurate Is Phone GPS in the Field and Under Trees?
description: Phone GPS accuracy in open sky and under forest canopy, from GPS.gov and peer-reviewed field tests, and how waiting, averaging and external receivers help.
h1: How accurate is phone GPS in the field?
nav: Phone GPS accuracy
answer: Under open sky, GPS.gov says smartphones are typically accurate to within a 4.9 m (16 ft) radius. Under forest canopy, peer-reviewed tests have measured root-mean-square errors of about 4 to 15 m depending on the phone and the canopy, and in one leaf-off forest test no handheld device reached sub-meter accuracy. Waiting for the fix to settle, averaging and an external GNSS receiver with corrections all help.
related: what-is-a-geospatial-pdf, free-topo-maps-as-geospatial-pdf, utm-and-mgrs-coordinates-explained
---
## Open sky: about 5 meters

GPS.gov states that "GPS-enabled smartphones are typically accurate to within a 4.9 m (16 ft.) radius under open sky." The figure is the mean measured by a smartphone lab with over a thousand participants in a hundred countries (van Diggelen and Enge, ION GNSS+ 2015).

The US government commits to a daily global average user range error of 2.0 m or better, with 95% probability. GPS.gov notes that this figure describes the signal in space, not the accuracy of a user's receiver. On the ground, accuracy is degraded by signal blockage from "buildings, bridges, trees, etc.", indoor use, reflected signals (multipath), satellite geometry, atmospheric conditions and receiver quality.

## Under forest canopy: worse, and it varies by phone

| Study | Devices | Conditions | Horizontal error |
|---|---|---|---|
| Purfürst 2022, *Sensors* | 10 Android phones and a Trimble Geo 7X | 15 forest sites in Germany; about 10-minute static sessions; error of every 1-second fix | Phones: DRMS 4.56 m (best) to 14.59 m (worst). Multi-frequency phones 6.99 m, single-frequency 9.13 m. Corrected Trimble reference 3.26 m |
| Lee et al. 2023, *PLOS ONE* | iPhone 12 Pro, Garmin Oregon 700, Trimble Juno T41 | Leaf-off deciduous forest in Georgia, USA; 26 points visited 20 times; each position an average of 10 fixes over about 30 seconds | Average RMSE: iPhone 3.91 m, Garmin 8.11 m, Trimble 3.45 m |

Purfürst found "a strong significant correlation between canopy density and positional accuracy" and big differences even between identical phones. Lee and colleagues concluded that "sub-meter positional accuracy was not attainable by any of the devices employed in forested conditions." Purfürst also cites studies in which open-area accuracy was two to six times better than under forest.

## What helps

- **Wait for the fix to settle.** Apple's documentation says the first fix "may take several seconds", and that iOS may send another update "if the hardware gathers a more accurate location reading." Watch the accuracy number drop before you mark a point.
- **Average.** Purfürst cites studies in which longer averaging "can usually improve it significantly", while noting that even 2 minutes of waiting is too long in everyday work.
- **Use an external receiver with corrections.** GPS.gov says dual-frequency receivers and/or augmentation systems "can enable real-time positioning within a few centimeters." In Tomaštík and Everett's 2023 *Sensors* study, a low-cost dual-frequency receiver (u-blox F9P), recording 20 minutes and post-processed against a reference station 2.4 km away, had median errors under 5 cm beneath canopy. A Pixel 5 phone's raw data, processed the same way, came out at about 1.5 m.

## Reading the accuracy number

On iPhone and iPad, the number is Core Location's `horizontalAccuracy`: "The radius of uncertainty for the location, measured in meters." The reported latitude and longitude are the center of that circle, and a negative value means the position is invalid. Apple's documentation does not state a confidence level.

Android defines its number as a radius with a 68% chance that the true location is inside it, so roughly one fix in three falls outside the circle. On either platform, the number is the device's own estimate, not a check against a surveyed point.

## How Mapsheet does it

Mapsheet shows your GPS position on your own [geospatial PDFs](what-is-a-geospatial-pdf.html) and GeoTIFFs offline, and Bluetooth GNSS receivers that provide location to iOS work with it. On the Crew plan, GPS averaging averages fixes over 30 seconds and shows the standard error, which reflects how tightly the fixes agreed, not how close the average is to the true point.

## Frequently asked questions

### Why does my phone show ±3 m when I'm clearly farther off?

The figure is an estimate, not a measurement. On Android it is defined to contain the true position only 68% of the time, and under trees GPS.gov lists both signal blockage and reflected signals as sources of error.

### How long should I average a point under trees?

None of the studies above found a waiting time that makes a phone sub-meter under canopy. Lee's 30-second averages gave about 4 m RMSE with an iPhone, and the same paper cites earlier work in which 10 minutes of observation under canopy, even with post-processing, did not reach sub-meter accuracy.

### Will an external GNSS receiver get me sub-meter accuracy under canopy?

It depends on the receiver and on corrections. The centimeter-level results above came from a dual-frequency receiver post-processed against a reference station, and GPS.gov credits "dual-frequency receivers and/or augmentation systems" for real-time centimeter work. The mapping-grade Trimble Juno T41 in Lee's test averaged 3.45 m RMSE.

## Sources

- [GPS.gov: GPS Accuracy](https://www.gps.gov/gps-accuracy)
- [Purfürst T. (2022). Evaluation of Static Autonomous GNSS Positioning Accuracy Using Single-, Dual-, and Tri-Frequency Smartphones in Forest Canopy Environments. Sensors 22(3):1289](https://pmc.ncbi.nlm.nih.gov/articles/PMC8838512/)
- [Lee T., Bettinger P., Merry K., Cieszewski C. (2023). The effects of nearby trees on the positional accuracy of GNSS receivers in a forest environment. PLOS ONE 18(3):e0283090](https://pmc.ncbi.nlm.nih.gov/articles/PMC10016660/)
- [Tomaštík J., Everett T. (2023). Static Positioning under Tree Canopy Using Low-Cost GNSS Receivers and Adapted RTKLIB Software. Sensors 23(6):3136](https://pmc.ncbi.nlm.nih.gov/articles/PMC10056071/)
- [van Diggelen F., Enge P. (2015). The World's first GPS MOOC and Worldwide Laboratory using Smartphones. ION GNSS+ 2015](https://www.ion.org/publications/abstract.cfm?articleID=13079)
- [Apple Developer: CLLocation horizontalAccuracy](https://developer.apple.com/documentation/corelocation/cllocation/horizontalaccuracy)
- [Apple Developer: CLLocationManager startUpdatingLocation()](https://developer.apple.com/documentation/corelocation/cllocationmanager/startupdatinglocation%28%29)
- [Android Developers: Location (getAccuracy)](https://developer.android.com/reference/android/location/Location)
