# Image Organizer

Check out the tutorial
[Image Organizer](https://medium.com/@somilshah112/organize-your-photos-with-python-automation-fe1595326b48)

## Prerequisites

You need to have the Exiftool installed: https://exiftool.org/
The Exiftool reads the metadata of the several image/video files.

## Install Requirements

    pip install -r requirements.txt
    pip install .

## Usage

    cameraroll_organizer -gd /path/to/goal -a copy /path/to/source

## Available Sortingtype Functions

- sort_by_year  (Sorts by Year) 
- sort_by_device (Sorts by Device Name)
- sort_by_yr_month (Sorts by Year and Month)
- sort_by_device_yr_month (Sorts By Device, Year and Month)

## Next Steps
- make sorting types an argument in CLI App
- specify which files shall be copied/moved over
