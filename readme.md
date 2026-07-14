# INDOT Interchanges

This project documents the process used to gather interchange data for Indiana from the Indiana Department of Transportation (INDOT) and prepare it for use in improving interchange information on the Waze map.

## Data Source

The interchange data was retrieved from the INDOT ArcGIS service using a Python script. The script pulled the interchange layer from the INDOT MapServer, extracted key fields such as interchange name, highway name, mile marker, latitude, longitude, and generated a Waze editor permalink for each location.

## Workflow

The workflow included both automated and manual steps:

- A Python script was used to pull the raw interchange data from INDOT.
- The data was exported into CSV files for review and cleanup.
- Future interchanges were set aside for later review.
- Duplicate interchanges were identified and separated out to avoid repeated entries.
- A mix of manual review and scripted processing was used to refine the dataset into a more usable format.

## Purpose

This dataset will be used to support improvements to interchanges in Indiana on the Waze map by helping identify locations that need to be reviewed, corrected, or added.

## Files

- script.py - Python script used to retrieve and format the interchange data
- indot_interchanges_v1.csv - initial version of the collected interchange data
- indot_interchanges_final.csv - refined dataset after manual and scripted cleanup
