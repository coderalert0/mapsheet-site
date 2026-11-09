---
title: Free Topo Maps to Download as Geospatial PDF or GeoTIFF
description: Where to download free topographic maps for offline GPS use, from USGS US Topo, historical topos and topoBuilder to NRCan's legacy sheets and NSW topo maps.
h1: Where can I download free topo maps as geospatial PDFs?
nav: Free topo maps
answer: In the United States, the USGS gives away current US Topo maps, scanned historical topographic maps and custom OnDemand Topos as geospatial PDF or GeoTIFF files through topoView, The National Map Downloader and topoBuilder. Natural Resources Canada still hosts free CanTopo, CanMatrix and Toporama sheets, but they are legacy products that are no longer updated. New South Wales publishes its topographic series as free georeferenced PDFs.
related: what-is-a-geospatial-pdf, utm-and-mgrs-coordinates-explained, phone-gps-accuracy-in-the-field
---
## United States: three free USGS map products

**US Topo (2009 to present).** Each sheet has the same extent as the classic 7.5-minute, 1:24,000-scale quadrangle (scale varies in Alaska and Puerto Rico). The maps are built from The National Map's GIS data, published as layered geospatial PDFs whose layers you can switch on or off, projected in UTM, and printed with latitude/longitude and the US National Grid. The USGS describes them as "available for free and immediate download".

**Historical Topographic Map Collection (1884 to 2006).** Over 185,000 georeferenced scans of every scale and edition of printed USGS topographic maps at 1:250,000 and larger. topoView serves them as geospatial PDF, GeoTIFF, JPEG and KMZ files.

**OnDemand Topos.** topoBuilder makes a custom map centered wherever you choose, as a 7.5-Minute, 25K Recreational, 100K or 250K topo, in geospatial PDF or TIFF. It is free; you get a download link by email, "typically delivered within 24 hours but may take up to 5 business days."

Where to get them:

- **topoView** ([ngmdb.usgs.gov/topoview/viewer](https://ngmdb.usgs.gov/topoview/viewer/)) for browsing and downloading single maps, historical or US Topo, as geospatial PDF, GeoTIFF, JPEG or KMZ.
- **The National Map Downloader** ([apps.nationalmap.gov/downloader](https://apps.nationalmap.gov/downloader/)) for bulk orders of up to 5,000 maps at once.
- **topoBuilder** ([topobuilder.nationalmap.gov](https://topobuilder.nationalmap.gov/)) for OnDemand Topos.

Watch the datum. Most USGS maps published through 2006 use NAD27, while US Topos are georeferenced to NAD83 or WGS84 ([why the datum matters](utm-and-mgrs-coordinates-explained.html)).

## Canada: Natural Resources Canada's legacy sheets

NRCan's free topographic rasters are still online under the Open Government Licence – Canada, but their catalogue records call them legacy products, and NRCan's FAQ answers "No" to updates for every one.

| Product | Scale | Formats | Coverage | Data validity |
|---|---|---|---|---|
| CanTopo | 1:50,000 | PDF, geospatial PDF, TIFF, GeoTIFF | About 2,234 maps, 22% of the landmass, mainly northern Canada | 1946–2012 (average 2007) |
| CanMatrix, Georeferenced | 1:50,000 and 1:250,000 | GeoTIFF | Georeferenced scans of printed maps | 1944–2012 collection |
| Toporama | 1:50,000 | GeoTIFF, in UTM or latitude/longitude | All of Canada (15,308 files) | 1944–2012 (average 1998) |

The georeferenced products use NAD83, and NRCan rates CanTopo and Toporama at "30 metres or better". Skip the CanMatrix Print Ready PDFs and TIFFs: they are not georeferenced.

Download directories:

- CanTopo and CanMatrix: [ftp.maps.canada.ca/pub/nrcan_rncan/raster/topographic/](https://ftp.maps.canada.ca/pub/nrcan_rncan/raster/topographic/). The 1:50,000 sheets sit in folders named by National Topographic System number, for example `50k/031/b/05/` for sheet 31B/05. A KMZ index is in `index/`.
- Toporama: [ftp.maps.canada.ca/pub/nrcan_rncan/raster/toporama/](https://ftp.maps.canada.ca/pub/nrcan_rncan/raster/toporama/), with `50k_utm_tif/` and `50k_geo_tif/` folders.

## Australia: New South Wales

The NSW Government publishes its topographic series as "geo-referenced PDFs, so you can use them on GPS devices, phones or tablets". Scales are 1:25,000 in the east, 1:50,000 in the central region and 1:100,000 in the far west. Download from the [NSW Topographic Maps viewer](https://portal.spatial.nsw.gov.au/portal/apps/webappviewer/index.html?id=06e3c2e0de1e4efda863854048c613c6) or the [Spatial Collaboration Portal](https://portal.spatial.nsw.gov.au/client/toolsandviewers). The maps are free to use and print under Creative Commons 4.0. Printing at 100% scale needs a large-format printer; most sheets finish at 1135 mm × 580 mm.

## How Mapsheet does it

Mapsheet shows your GPS position offline on geospatial PDFs and GeoTIFFs you have downloaded, on iPhone and iPad. The Free plan holds 3 maps at a time. A crew pack sends maps and points to a whole crew in one file, so everyone carries the same sheets.

## Frequently asked questions

### Are USGS topo maps really free?

Yes. US Topos, the historical scans and OnDemand Topos are all free to download. Printed copies are sold through the USGS Store, the only USGS website for buying printed topographic maps.

### Why doesn't my old USGS map line up with my GPS?

It is probably on NAD27. The USGS says the NAD27 to NAD83 shift of the latitude/longitude graticule is 10 to 100 m on the ground across the lower 48 states, and UTM grid values change by around 200 m. Check the datum in the map collar, and where you can, use a US Topo, which is on NAD83 or WGS84.

### Does NRCan publish current topographic maps?

Not as ready-made map sheets. Its current topographic data is CanVec: more than 60 feature classes in 8 themes, delivered as file geodatabases or shapefiles, which you would have to style into a map in GIS software yourself.

## Sources

- [USGS: US Topo, Maps for America](https://www.usgs.gov/programs/national-geospatial-program/us-topo-maps-america)
- [USGS: Historical Topographic Maps, Preserving the Past](https://www.usgs.gov/programs/national-geospatial-program/historical-topographic-maps-preserving-past)
- [USGS: Topographic Map Access Points](https://www.usgs.gov/the-national-map-data-delivery/topographic-map-access-points)
- [USGS: topoBuilder](https://www.usgs.gov/programs/national-geospatial-program/topobuilder)
- [USGS FAQ: How do I find, download, or order topographic maps?](https://www.usgs.gov/faqs/how-do-i-find-download-or-order-topographic-maps)
- [USGS FAQ: Why are USGS historical topographic maps referenced to outdated datums?](https://www.usgs.gov/faqs/why-are-usgs-historical-topographic-maps-referenced-outdated-datums)
- [USGS FAQ: How large is the NAD 27 to NAD 83 shift?](https://www.usgs.gov/faqs/how-large-north-american-datum-1927-nad-27-nad-83-shift)
- [Open Government Portal: Digital Topographic Raster Maps, 1944-2012](https://open.canada.ca/data/en/dataset/d248b5be-5887-4cfb-942f-d425d82e6ea9)
- [Open Government Portal: Toporama, 1945-2013](https://open.canada.ca/data/en/dataset/ff383f5c-0772-46f3-84df-c2cb860d0da2)
- [Natural Resources Canada: Geomatics frequently asked questions](https://natural-resources.canada.ca/science-data/science-research/geomatics/frequently-asked-questions)
- [Open Government Portal: Topographic Data of Canada, CanVec Series](https://open.canada.ca/data/en/dataset/8ba2aa2a-7bb9-4448-b4d7-f164409fe056)
- [NRCan download directory: raster/topographic](https://ftp.maps.canada.ca/pub/nrcan_rncan/raster/topographic/)
- [NRCan download directory: raster/toporama](https://ftp.maps.canada.ca/pub/nrcan_rncan/raster/toporama/)
- [NSW Government: NSW topographic maps](https://www.nsw.gov.au/environment-land-and-water/spatial-data-and-mapping/topographic-maps)
