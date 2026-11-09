---
title: Wildfire Incident Maps on Your Phone, Offline
description: Where US wildfire incident maps are posted, what the QR codes on printed maps open, why most are geospatial PDFs, and how to keep the current day's maps on a phone with no signal.
h1: How do I get a fire's incident maps onto my phone for use with no signal?
nav: Incident maps offline
answer: US incident teams post their public maps on the NIFC File Share at ftp.wildfire.gov, under public/incident_specific_maps, sorted by geographic area, year and incident. The QR code printed on an incident map often opens that incident's QR folder, which the team overwrites with the current maps. The maps are almost always geospatial PDFs exported from ArcGIS Pro, so any GeoPDF-capable app shows your position on them offline once they are downloaded. Incident Action Plans are not in the public area: since May 4, 2026 they sit behind a FAMAuth sign-in.
related: what-is-a-geospatial-pdf, phone-gps-accuracy-in-the-field, utm-and-mgrs-coordinates-explained
---
## Where the maps are posted

The National Interagency Fire Center's file share, [ftp.wildfire.gov](https://ftp.wildfire.gov/), has two areas. NWCG's GIS standards (PMS 936-1, [NIFC File Share and QR Codes](https://www.nwcg.gov/publications/pms936-1/nifc-files-share-and-qr-codes)) describe them: the **Incident Specific Maps** area "does not require authentication and is intended for publicly available files such as maps", while the **Incident Specific Data** area "is not available to the public and requires authentication via FAMAuth." The file share's home page notes that the authenticated area has required FAMAuth since May 4, 2026 and that the path to the public maps did not change.

Public maps live at `https://ftp.wildfire.gov/public/incident_specific_maps/`, in one folder per geographic area coordination center (Alaska, Northern and Southern California, Eastern, Great Basin, Northern Rockies, Northwest, Rocky Mountain, Southern, Southwest). Most areas then have a folder per year (`2026/`); the Northwest groups incidents by state (`2026_Incidents_Washington/`, `2026_Incidents_Oregon/`). Each incident has its own folder, named like `2026_IncidentName`, usually with:

- `QR/`: the current set of maps; teams overwrite it as maps are updated
- `Products/<date>/`: everything produced for each operational day
- `IR/<date>/`: the night infrared flight products

## What the QR code on a printed map opens

PMS 936-1 says a QR code "when scanned, will quickly access the URL of the map location." Of 42 QR codes we decoded from 2026 incident maps, 21 pointed at the incident's `QR/` folder rather than at one file; those keep working all week, because the folder is overwritten with the current maps. Others point at a single PDF. Scanning it in a phone's camera opens a plain folder listing; a map app that understands folder links can list the maps and download the ones you pick.

## Why they work in GeoPDF apps

Incident maps are exported from ArcGIS Pro, and NWCG's guidance ([Geospatial PDF](https://www.nwcg.gov/publications/pms936-1/create-incident-maps-and-digital-products/geospatial-pdf)) notes that PDFs exported from ArcGIS are geo-enabled and work in any software that reads GeoPDFs. When we checked a sample of 39 PDFs from 2026 incident folders, 37 carried the ISO 32000 geospatial tags; the two that didn't were a strategic planning page and a suppression repair plan, not maps. ([What makes a PDF geospatial](what-is-a-geospatial-pdf.html).)

## Keeping today's maps with no signal

1. **Download before you lose signal.** Maps are 0.4 to 26 MB; a day's set is usually a handful of files.
2. **Check the date in the file name.** Teams name files with the GeoOps file namer, which includes the date, for example `ops_..._20260819_...pdf`.
3. **Check the folder again each shift.** Because `QR/` is overwritten, yesterday's copy on your phone does not update itself.
4. **Mind your position's accuracy.** A phone's GPS is good to a few metres in the open and worse under canopy or in canyons ([phone GPS accuracy in the field](phone-gps-accuracy-in-the-field.html)).

## Current perimeters between map updates

Printed and posted maps show the perimeter as of their date. Between updates, the interagency **WFIGS current perimeters** layer (published by NIFC, refreshed every few minutes when incident GIS staff update it) and **NASA FIRMS** satellite hotspots show newer information, but both can lag, miss fire or include heat that is not fire. Neither replaces the incident's briefings, which remain the source for operations and safety.

## How Mapsheet helps

In Mapsheet, **+ › From a link or QR code** opens an incident's folder and lists its maps; you pick what to download, and **Watch this folder** marks maps that are new or changed next time you check. **••• › Fires** draws current perimeters, incidents and satellite hotspots on your maps, saved for offline use, and a US fire whose name matches an incident folder links straight to its maps. Mapsheet does not make, check or change any of these maps.
