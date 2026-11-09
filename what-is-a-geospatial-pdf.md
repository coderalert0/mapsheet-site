# What is a geospatial PDF?

> A geospatial (georeferenced) PDF is an ordinary PDF map that also stores the information needed to convert any point on the page into real-world coordinates. The coordinates are written inside the file, using either the ISO 32000 geospatial measure dictionary or the older OGC best-practice encoding (LGIDict), so a GPS app can place your position on the map without a network connection.

Source page: https://coderalert0.github.io/mapsheet-site/what-is-a-geospatial-pdf.html
Checked against its sources on November 8, 2026. Published by Mapsheet, an offline PDF map app with GPS for iPhone and iPad.

## What makes a PDF geospatial

A normal PDF only knows page positions. A geospatial PDF adds a few objects that tie those positions to a coordinate reference system: the datum, the projection, and how page points line up with map coordinates. The OGC document says this "allows association of an arbitrary coordinate reference system to a PDF illustration", so software can convert in both directions.

A map that shows UTM ticks or a graticule in its margin is not geospatial unless those objects are present. The printed grid is only ink.

## The two ways coordinates are stored

| | ISO 32000 encoding | OGC best practice (LGIDict) |
|---|---|---|
| Origin | Adobe, Acrobat 9 (June 2008), as Extension Level 3 to PDF 1.7 | Layton Graphics Inc. in the early 2000s; maintained by TerraGo Technologies from 2005 |
| Where it lives | A measure dictionary with subtype GEO, attached to a viewport (a region of the page) or to an image or form object | An `LGIDict` entry on the page object: one map frame or an array of map frames |
| How points are tied | Latitude/longitude control points (`GPTS`) matched to positions inside the viewport (`LPTS`) | A `Registration` array of point pairs (PDF x, PDF y, map x, map y), or a transformation matrix (`CTM`) |
| Coordinate system | An EPSG code or WKT | A `Projection` dictionary using the document's own datum and projection codes |
| Status | Part of ISO 32000-2 (PDF 2.0), published 2017 | OGC 08-139r3, dated 17 January 2011, an OGC Best Practice, "not an OGC Standard" |

The OGC encoding marks the map's boundary with a `Neatline`, required when a page holds several map frames, such as an inset. The OGC document also admits that its datum, ellipsoid and coordinate system codes "do not conform to the EPSG database".

GDAL, the open-source geospatial library, reads both encodings, labels the OGC one "not recommended", and since version 3.11 writes only ISO 32000.

## How ArcGIS Pro, QGIS and the USGS make them

- **ArcGIS Pro.** In the Export pane, **Export georeference information** will "include geospatial information from the map frames", so supported PDF readers can extract x,y coordinates. **Layers and attributes** adds PDF layers and, optionally, feature attributes.
- **QGIS.** Exporting a print layout to PDF or TIFF creates georeferenced output by default; **Append georeference information** works only if the reference map is on the first page. **Create Geospatial PDF** adds map themes and vector feature information.
- **USGS.** US Topo maps are built from The National Map's GIS data and published as layered geospatial PDFs. The Library of Congress records that US Topos moved to the ISO 32000 encoding in 2017, while the Historical Topographic Map Collection still uses the OGC encoding ([where to download them](https://coderalert0.github.io/mapsheet-site/free-topo-maps-as-geospatial-pdf.md)).

## How to tell whether a PDF has coordinates

1. **Run `gdalinfo` on it.** GDAL reads geospatial PDFs "by extracting georeferencing information". `gdalinfo` prints the file's coordinate system in WKT and its corner coordinates. If no coordinate system appears, there is nothing for a GPS app to use.
2. **Check the datum it reports.** GDAL treats unrecognized OGC-encoding datums as WGS 84-based, so a file can open and still sit in the wrong place; datums can differ by hundreds of meters ([datums explained](https://coderalert0.github.io/mapsheet-site/utm-and-mgrs-coordinates-explained.md)).
3. **Check how it was made.** A PDF exported with the georeference option off, or a scan, has no coordinates at all.

## How Mapsheet does it

Mapsheet opens your own geospatial PDFs and GeoTIFFs on iPhone and iPad and shows your GPS position on them with no connection. You can drop points, record tracks and measure lines and areas on the map, then export GPX, KML, KMZ or CSV. The Free plan holds 3 maps at a time.

## Frequently asked questions

### Is a geospatial PDF the same as a georeferenced PDF?

Yes, both describe a PDF that carries its own coordinates. You will also see GeoPDF® (TerraGo's trademark for its geospatial PDFs); the OGC document notes that following its encoding gives no right to use that trademark.

### Which encoding should new maps use?

ISO 32000. It is part of PDF 2.0, the USGS moved US Topo to it in 2017, and GDAL now writes nothing else. Map readers still need the OGC encoding for older files, including the USGS historical scans.

### Can I add coordinates to a scanned map?

Yes, with a GIS. The QGIS Georeferencer aligns "unreferenced raster or vector layers to known coordinate systems using Ground Control Points" and can save the result as a GeoTIFF.

## Sources

- [OGC 08-139r3: PDF Georegistration Encoding Best Practice Version 2.2](https://docs.ogc.org/bp/08-139r3/08-139r3.pdf)
- [Library of Congress, Sustainability of Digital Formats: PDF 1.7 ExtensionLevel 3, Geospatial Encoding (Adobe), fdd000315](https://loc.gov/preservation/digital/formats/fdd/fdd000315.shtml)
- [Library of Congress, Sustainability of Digital Formats: TerraGo file format, fdd000522](https://www.loc.gov/preservation/digital/formats/fdd/fdd000522.shtml)
- [Library of Congress, Sustainability of Digital Formats: OGC Best Practice 08-139 encoding, fdd000312](https://loc.gov/preservation/digital/formats/fdd/fdd000312.shtml)
- [Esri: Export to PDF, ArcGIS Pro documentation](https://doc.esri.com/en/arcgis-pro/latest/help/sharing/overview/pdf-export.html)
- [QGIS Documentation: Creating an Output (print layouts)](https://docs.qgis.org/latest/en/docs/user_manual/print_layout/create_output.html)
- [QGIS Documentation: Georeferencer](https://docs.qgis.org/latest/en/docs/user_manual/managing_data_source/georeferencer.html)
- [USGS: US Topo, Maps for America](https://www.usgs.gov/programs/national-geospatial-program/us-topo-maps-america)
- [USGS FAQ: Why are USGS historical topographic maps referenced to outdated datums?](https://www.usgs.gov/faqs/why-are-usgs-historical-topographic-maps-referenced-outdated-datums)
- [GDAL: PDF, Geospatial PDF raster driver](https://gdal.org/en/stable/drivers/raster/pdf.html)
- [GDAL: gdalinfo](https://gdal.org/en/stable/programs/gdalinfo.html)
- [iText 5 API: MeasureGeospatial (ISO 32000 geospatial measure dictionary entries)](https://api.itextpdf.com/iText5/java/5.5.13.1/com/itextpdf/text/pdf/spatial/MeasureGeospatial.html)
