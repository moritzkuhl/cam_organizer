import os
import shutil
import datetime
from datetime import datetime
#import PIL.Image
import exifread
import time
import exiftool
import locale
import click
#locale.setlocale(locale.LC_TIME, 'de_DE.UTF-8')
exiftool.ExifTool(r"C:\Program Files\exiftool\exiftool.exe")

class CamerarollOrganizer:
    def __init__(self, dirname='',mode=None, language =None):
        self.images = os.listdir(dirname)
        self.dirname = dirname
        if mode is None:
            self.mode = "move"
        else:
            self.mode = mode
        # if language is None:
        #     

    def convertStrToDatetime(self, date_str):
        return datetime.strptime(str(date_str), "%Y:%m:%d %H:%M:%S")

    def get_creation_date(self, fname):
        if fname.lower().endswith(('.jpg', '.jpeg', '.png')):
             with open(os.path.join(self.dirname, fname), 'rb') as f:
                tags = exifread.process_file(f)
                #print(tags)
                if 'EXIF DateTimeOriginal' in tags:
                    return datetime.strptime(str(tags['EXIF DateTimeOriginal']), '%Y:%m:%d %H:%M:%S')
                else:
                    print("unknown Datafile --> Take creation Date as Fallback. Please Review for yourself if this file was moved incorrectly")
                    ti_m = os.path.getmtime(os.path.join(self.dirname, fname))
                    m_ti = time.ctime(ti_m)
                    print(datetime.strptime(str(m_ti), "%a %b %d %H:%M:%S %Y"))
                    return datetime.strptime(str(m_ti), "%a %b %d %H:%M:%S %Y")
            
            
            # with PIL.Image.open(os.path.join(self.dirname, fname)) as img:
            #     exif = img._getexif()
            #     ts = exif.get(306) if exif else None
            #     if ts:
            #         ts = self.preprocess_exif(ts)
            #         date = ts.split(' ')[0]
            #         return datetime.strptime(date, '%Y:%m:%d')
            #     else:
            #         print("unknown Datafile --> Take creation Date as Fallback")
            #         ti_m = os.path.getmtime(os.path.join(self.dirname, fname))
            #         m_ti = time.ctime(ti_m)
            #         print(datetime.strptime(str(m_ti), "%a %b  %d %H:%M:%S %Y"))
            #         return datetime.strptime(str(m_ti), "%a %b  %d %H:%M:%S %Y")
        
        # elif fname.lower().endswith(('.mp4', ".gif")):
        #     with open(os.path.join(self.dirname, fname), 'rb') as f:
        #         tags = exifread.process_file(f)
        #         if tags == {}:
        #             print("Empty Exif Data --> Please Review for yourself if this file was moved incorrectly")
        #         if 'EXIF DateTimeOriginal' in tags:
        #             print("Exif DATA Gefunden")
        #             return datetime.datetime.strptime(str(tags['EXIF DateTimeOriginal']), '%Y:%m:%d %H:%M:%S')
        #         else:
        #             print("unknown Datafile --> Take creation Date as Fallback")
        #             ti_m = os.path.getmtime(os.path.join(self.dirname, fname))
        #             m_ti = time.ctime(ti_m)
        #             print(datetime.strptime(str(m_ti), "%a %b  %d %H:%M:%S %Y"))
        #             return datetime.strptime(str(m_ti), "%a %b %d %H:%M:%S %Y")
        
        # elif fname.lower().endswith('.mov'):
        #     with open(os.path.join(self.dirname, fname), 'rb') as f:
        #         tags = exifread.process_file(f)
        #         if tags == {}:
        #             print("Empty Exif Data --> Please Review for yourself if this file was moved incorrectly")
        #         print(tags)
        #         if 'Create Date' in tags:
        #             print("Exif DATA Gefunden")
        #             return datetime.datetime.strptime(str(tags['Create Date']), '%Y:%m:%d %H:%M:%S')
        #         else:
        #             print("unknown Datafile --> Take creation Date as Fallback")
        #             ti_m = os.path.getmtime(os.path.join(self.dirname, fname))
        #             m_ti = time.ctime(ti_m)
        #             print(datetime.strptime(str(m_ti), "%a %b  %d %H:%M:%S %Y"))
        #             return datetime.strptime(str(m_ti), "%a %b %d %H:%M:%S %Y")

        elif fname.lower().endswith(('.mp4', '.mov', ".gif")):
            with exiftool.ExifToolHelper() as et:
                print(os.path.join(self.dirname, fname))
                metadata = et.get_metadata(os.path.join(self.dirname, fname))
            if metadata:
                print(metadata[0])
                video_creation_date = metadata[0]['QuickTime:CreateDate']
                #print(type(video_creation_date))
                #print(video_creation_date)
                converted_video_creation_date = self.convertStrToDatetime(
                    video_creation_date)
                #print(converted_video_creation_date)
                print("mp4 Korrekt gefunden")
                return converted_video_creation_date
            else:
                print("No Video Metadata --> Take creation date as best guess")
                ti_m = os.path.getmtime(os.path.join(self.dirname, fname))
                m_ti = time.ctime(ti_m)
                return datetime.strptime(str(m_ti), "%a %b %d %H:%M:%S %Y")

        elif fname.lower().endswith('.heic'):
            with open(os.path.join(self.dirname, fname), 'rb') as f:
                tags = exifread.process_file(f)
                if 'EXIF DateTimeOriginal' in tags:
                    return datetime.strptime(str(tags['EXIF DateTimeOriginal']), '%Y:%m:%d %H:%M:%S')
                else:
                    return None
        else:
            ti_m = os.path.getmtime(os.path.join(self.dirname, fname))
            m_ti = time.ctime(ti_m)
            return datetime.strptime(str(m_ti), "%a %b %d %H:%M:%S %Y")

    def preprocess_exif(self, data):
        data = data.strip()
        data = data.strip('\x00')
        return data

    def sort_by_year(self):
        for fname in self.images:
            locale.setlocale(locale.LC_TIME, 'de_DE.UTF-8')
            creation_date = self.get_creation_date(fname)
            if creation_date:
                year = creation_date.strftime('%Y')
                if not os.path.isdir(year):
                    os.mkdir(year)
                if self.mode in ("move", "m"):
                    shutil.move(os.path.join(self.dirname, fname),
                            os.path.join(year, fname))
                else:
                    shutil.copy(os.path.join(self.dirname, fname),
                            os.path.join(year, fname))
                # print("File {} moved from {} to {} successfully".format(fname, os.path.join(self.dirname, fname), os.path.join(year, fname)))
            else:
                print("Unable to get creation date for file:", fname)

    def sort_by_yr_month(self):
        for fname in self.images:
            print(fname)
            creation_date = self.get_creation_date(fname)
            print(creation_date)
            if creation_date:
                #locale.setlocale(locale.LC_TIME, 'de_DE.UTF-8')
                year = creation_date.strftime('%Y')
                month = creation_date.strftime('%m_%B')
                #month = creation_date.strftime('%b')
                if not os.path.isdir(year):
                    os.mkdir(year)
                if not os.path.isdir(os.path.join(year, month)):
                    os.mkdir(os.path.join(year, month))
                if self.mode in ("move", "m"):
                    shutil.move(os.path.join(self.dirname, fname),
                            os.path.join(year,month, fname))
                else:
                    shutil.copy(os.path.join(self.dirname, fname),
                            os.path.join(year,month, fname))
                print("File {} moved from {} to {} successfully".format(
                    fname, os.path.join(self.dirname, fname), os.path.join(year, month, fname)))
            else:
                print("Unable to get creation date for file:", fname)

    def sort_by_month(self):
        for fname in self.images:
            # locale.setlocale(locale.LC_TIME, 'de_DE.UTF-8')
            creation_date = self.get_creation_date(fname)
            if creation_date:
                month = creation_date.strftime('%m_%B')
                if not os.path.isdir(month):
                    os.mkdir(month)
                if self.mode in ("move", "m"):
                    shutil.move(os.path.join(self.dirname, fname),
                            os.path.join(month, fname))
                else:
                    shutil.copy(os.path.join(self.dirname, fname),
                            os.path.join(month, fname))
                print("File {} moved from {} to {} successfully".format(fname, os.path.join(self.dirname, fname), os.path.join(month, fname)))
            else:
                print("Unable to get creation date for file:", fname)


@click.command()
@click.option('-gd', '--goaldirectory', default=None, help='Path to the directory where photos/videos should be sorted.')
@click.option('-a', '--action', type=click.Choice(['move', 'copy'], case_sensitive=False), default='copy', help='Action to perform: "move" or "copy" (default is "copy").')
@click.argument('source_directory', type=click.Path(exists=True, file_okay=False))
def cli(goaldirectory, action,source_directory):
    
    # organizer.sort_by_year()
    if not goaldirectory:
        goaldirectory = 'test'
    if action == 'move':
        # Example usage:
        organizer = CamerarollOrganizer('test',mode='m')
        organizer.sort_by_month()
    else:
        organizer = CamerarollOrganizer('test')
        organizer.sort_by_month()


if __name__ == '__main__':
    cli()