## FDA grants.gov scraper

Grants scraper is a simple scraping tool used to convert grant numbers into urls of main grant pages then urls of their documentation. The app then can parse the documentation for the "purpose" section and "Description" section.

The app requires an Excel spreadsheet as it's input and requires an "OPPORTUNITY NUMBER" column.

There are three formats for the grant documentation pages and there is no apparent reason for which format is used. I have defined them as type 1, 2, and 3; examples are as follows.
### Format examples
#### Type 1
![Alt text](README_img/Type_1_Format.png?raw=true "Title")
#### Type 2
![Alt text](README_img/Type_2_Format.png?raw=true "Title")
#### Type 3
![Alt text](README_img/Type_3_Format.png?raw=true "Title")

Generally the program can handle any of the formats but many of the error messages will output the format type which should make troubleshooting much easier.