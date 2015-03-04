# Python trilateration

Trilateration of samples recorded as distances to each of three
referenced GPS points. Input file format should be "name", "dist1",
"dist2", "dist3", "long1", "lat1", "long2", "lat2", "long3", "lat3"
where the distances are reported in meters, and the GPS coordinates
are in decimal degrees. See example file 'headless_mv_spatial.csv'

Adapted from a comment on stackoverflow here:
http://gis.stackexchange.com/questions/66/trilateration-using-3-latitude-and-longitude-points-and-3-distances/415#415

The wikipedia entry referenced in the comments is:
http://en.wikipedia.org/wiki/Geodetic_system#geodetic_to.2Ffrom_ECEF_coordinates

## Usage

`python triat.py --input inputCsvFile.csv --output outputCsvFile`

## Credits

Brian J. Sanderson \\
PhD Candidate \\
Dept. of Biology \\ 
University of Virginia \\
Charlottesville, VA 22903 \\
bjs8wk@virginia.edu

## License

TODO: copy license
