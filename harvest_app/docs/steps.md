The steps I did to get the categories for mobility group:
Cleaning:
- Drop unnecessary columns like, short postcode, full postcode, sales region etc.
- Drop rows where the selected columns are all empty.
- rename columns to easier names (optional)
- Remove whitespaces (optional)
- Shorten postcode (only when this isn't already there)
- save

Manipulation:
- use extract potential conversions on price agreed column.
- save

Merging:
- Merge manipulated data with health data.
- save

Cluster:
- cluster merged on # converted
- save

Adwords page
