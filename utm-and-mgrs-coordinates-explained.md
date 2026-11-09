# How do UTM and MGRS coordinates work?

> UTM divides the world into 60 zones, each 6° of longitude wide, and gives every point an easting and a northing in meters inside its zone. MGRS, and the US National Grid that matches it, write the same UTM numbers with a latitude band letter and a two-letter code for each 100 km square, so 18SUJ23480647 pins a point to 10 m. Always note the datum, because NAD27 and NAD83 UTM values for the same spot typically differ by around 200 m.

Source page: https://coderalert0.github.io/mapsheet-site/utm-and-mgrs-coordinates-explained.html
Checked against its sources on November 8, 2026. Published by Mapsheet, an offline PDF map app with GPS for iPhone and iPad.

## UTM zones

The Universal Transverse Mercator (UTM) grid divides the world into 60 north-south zones, each 6° of longitude wide. Zone 1 runs from 180° to 174° west, and the numbers increase eastward to zone 60. The lower 48 United States fall in 10 zones, from zone 10 on the West Coast to zone 19 in New England. Inside each zone, coordinates are measured in meters, north and east.

## Easting and northing

- **Easting.** The central meridian of every zone is given an easting of 500,000 m. Points west of it have eastings below 500,000; points east of it, above.
- **Northing.** In the northern hemisphere, northing is measured from zero at the equator. To avoid negative numbers for locations south of the equator, the equator is assigned a false northing of 10,000,000 m, and values decrease going south. A southern-hemisphere northing of 6,250,000 m is therefore 3,750 km south of the equator.

Because every zone repeats the same numbers, a UTM coordinate is incomplete without its zone and hemisphere.

## Reading a grid reference on a map

USGS 7.5-minute quadrangles show the UTM grid every 1,000 m, as blue ticks in the margin or as full grid lines. Each tick is labeled with its 1,000-meter value, and the full value is printed on the ticks nearest the southeast and northwest corners.

Read right, then up. The USGS fact sheet's example: the grid line to the west of point P is 357,000 m east, and the line to the south is 4,276,000 m north. P is 800 m east and 750 m north of those lines, so its coordinates are 357,800 m east, 4,276,750 m north.

## MGRS and the US National Grid

The US National Grid (USNG) standard says its coordinates "shall be identical to the MGRS numbering scheme" across the United States. A full reference has three parts:

1. **Grid zone designation**, such as `18S`: the UTM zone number plus a latitude band letter. There are 20 bands, lettered C to X without I and O, generally 8° high, starting at 80° south.
2. **100,000-meter square**, such as `UJ`: two letters. The first identifies the column, the second the row.
3. **Easting then northing** inside that square, always with the same number of digits for each.

| Reference | Digits | Precision |
|---|---|---|
| 18SUJ20 | 2 | 10 km |
| 18SUJ2306 | 4 | 1 km |
| 18SUJ234064 | 6 | 100 m |
| 18SUJ23480647 | 8 | 10 m |
| 18SUJ2348306479 | 10 | 1 m |

The digits are the UTM coordinate with its leading digits replaced by the square letters. The standard's Washington Monument example is UTM zone 18, 323,483 m east, 4,306,479 m north, which is 18SUJ2348306479. The `S` is a latitude band in the northern hemisphere, not "south". For general field work the standard calls 100 m or 10 m precision typical.

## Why the datum matters

The same numbers mean different places on different datums. The USNG standard uses NAD83 or its international equivalent, WGS84, and requires NAD27 values to be labeled. Its example: one point is 18SUJ23480647 on NAD83 and 18SUJ23450626 (NAD 27), references that differ by 30 m in easting and 210 m in northing.

- **NAD27 to NAD83:** in the lower 48 states the shift is 10 to 100 m in latitude/longitude, and UTM values change by around 200 m (USGS).
- **NAD83 and WGS84:** NOAA notes the WGS 84 (G1150) realization differs from NAD 83 (1986) by about 2 m, and that except at the largest map scales the two can be treated as equivalent horizontally.
- **Which maps use which:** most USGS maps published through 2006 use NAD27; US Topos are georeferenced to NAD83 or WGS84 ([where to get them](https://coderalert0.github.io/mapsheet-site/free-topo-maps-as-geospatial-pdf.md)).

Check the datum printed on the map before you compare its grid with GPS coordinates.

## How Mapsheet does it

Mapsheet goes to typed coordinates in decimal degrees, degrees-minutes(-seconds), UTM or MGRS/USNG and shows distance and bearing to your points. CSV exports include UTM columns.

## Frequently asked questions

### What does the letter after a UTM zone number mean?

In MGRS and USNG it is the 8° latitude band, so `18S` is a band in the northern hemisphere. Esri's documentation notes that in plain UTM notation the letter "usually represents a latitude band" as well. If a coordinate gives only N or S, confirm which convention it uses.

### How many digits should I give in an MGRS reference?

Give the precision you actually have. Eight digits (10 m) suits most field positions. Ten digits claims 1 m, much finer than typical phone accuracy of about 4.9 m under open sky ([phone GPS accuracy](https://coderalert0.github.io/mapsheet-site/phone-gps-accuracy-in-the-field.md)).

### Is NAD83 the same as WGS84?

Close, not identical: about 2 m apart for the realizations NOAA compares, and treated as equivalent except at the largest map scales. NAD27 is a different matter, with UTM shifts of around 200 m.

## Sources

- [USGS Fact Sheet 077-01: The Universal Transverse Mercator (UTM) Grid](https://pubs.usgs.gov/fs/2001/0077/report.pdf)
- [FGDC-STD-011-2001: United States National Grid](https://www.fgdc.gov/standards/projects/FGDC-standards-projects/usng/fgdc_std_011_2001_usng.pdf)
- [USGS FAQ: How large is the NAD 27 to NAD 83 shift?](https://www.usgs.gov/faqs/how-large-north-american-datum-1927-nad-27-nad-83-shift)
- [USGS FAQ: Why are USGS historical topographic maps referenced to outdated datums?](https://www.usgs.gov/faqs/why-are-usgs-historical-topographic-maps-referenced-outdated-datums)
- [GPS.gov: GPS Accuracy](https://www.gps.gov/gps-accuracy)
- [NOAA VDatum: A tutorial on datums](https://vdatum.noaa.gov/docs/datums.html)
- [Esri ArcGIS Help 10.1: MGRS](https://resources.arcgis.com/en/help/main/10.1/000n/000n00000056000000.htm)
- [Esri ArcGIS Pro: Supported notation formats](https://pro.arcgis.com/en/pro-app/3.6/tool-reference/data-management/supported-notation-formats.htm)
