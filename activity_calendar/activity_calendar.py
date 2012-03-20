import csv
import random
import re
import sys
import datetime
from collections import defaultdict
# 2012-03-12
# Simple script which takes a list of activities, one per line, and generates an output csv file suitable
# for importing into Google Calendar.
# This output csv contains one column for date and one for the description of the activity
# This script outputs to standard out; output can easily be redirected to a csv file as necessary
# Google Calendar CSV format described at http://support.google.com/calendar/bin/answer.py?hl=en&answer=45656

HEADER_ROW = ['Subject','Start Date']

CALENDAR_CSV_FILE_INDEX = 1
ACTIVITY_FILE_INDEX = 2

CURRENT_YEAR = datetime.date.today().year

def ParseHolidayCalendar(calendar_tuples):
  dates = []
  
  # 3 tuple - start date, end date, description
  
  # general format of the file is one column per month, each row is a separate date or range of days
  # e.g. 
  # January,February,March,April,May,June,July ,August,September,October,November,December,,Websites
  # 1- New Year's Day,2- Crepe Day/Groundhog Day,2- Dr. Seuss Day,1- April Fool's Day,1- Batman Day; Mother Goose Day,1- Donut Day; Dinosaur Day; Oscar the Grouch's Birthday,1- US Postage Stamp Day; Creative Ice Cream Flavors Day,1-7- International Clown Week,2-8- National Waffle Week,1-5- National Newspaper Week,1- All Saints' Day,1-7- Cookie Cutter Week,,http://www.brownielocks.com/month2.html
  
  date_range_regexp = re.compile('(\d+)-(\d+)-?(.*)')
  single_date_regexp = re.compile('(\d+)-?(.*)')
  
  for row in calendar_tuples:
    # Some rows have extra columns, skip them
    num_columns = min(12, len(row))
        
    for column in range(num_columns):
      cell = row[column]
      # 1 based months
      month = column + 1
      if cell == '':
        continue
      date_range = date_range_regexp.search(cell)
      single_date = single_date_regexp.search(cell)
      if date_range:
        groups = date_range.groups()
        first_day = int(groups[0])
        second_date = int(groups[1])
        description = groups[2]
        #print first_day, second_date, description
        
        start_date = datetime.date(CURRENT_YEAR, month, first_day)
        end_date = datetime.date(CURRENT_YEAR, month, second_date)
        
        dates.append(tuple[start_date, end_date, description])
        
        pass
      elif single_date:
        groups = single_date.groups()
        first_day = int(groups[0])
        second_day = first_day
        description = groups[1]
        #print first_day, description
        start_date = datetime.date(CURRENT_YEAR, month, first_day)
        end_date = datetime.date(CURRENT_YEAR, month, second_date)
        
        dates.append(tuple[start_date, end_date, description])
      else:
        print >> sys.stderr, 'Couldn\'t parse date from %s' %(cell)
  
  return sorted(dates)

def main():
  
  
  if len(sys.argv) != 3:
    print >> sys.stderr, "Usage: python activity_calendar.py /path/to/calendar /path/to/activities"
    sys.exit(1)
  
  calendar_reader = csv.reader(open(sys.argv[CALENDAR_CSV_FILE_INDEX], 'rb'), delimiter=',')
  # Skip header
  calendar_rows = [row for row in calendar_reader][1:]
  
  print ParseHolidayCalendar(calendar_rows)
  
  sys.exit(1)
    
  activity_file = open(sys.argv[ACTIVITY_FILE_INDEX], 'rb')
  activities = [line.strip() for line in activity_file]
  activity_file.close()
  
  # We have the raw activities; now we need to assign them to days
  january_1 = datetime.date(CURRENT_YEAR, 1, 1)
  december_31 = datetime.date(CURRENT_YEAR, 12, 31)
  
  january_1_ordinal = january_1.toordinal()
  december_31_ordinal = december_31.toordinal()
  
  days_of_year = [datetime.date.fromordinal(x) for x in range(january_1_ordinal, december_31_ordinal + 1)]
  # Group the dates by month
  months = defaultdict(list)
  for date in days_of_year:
    months[date.month].append(date)
  
  # A flattened mapping from date to activity
  date_to_activity_dict = {}
  for month in months:
    dates = months[month]
    # creates a list of (date, activity description) pairs
    monthly_activities = zip(dates, random.sample(activities, len(dates)))
    for date, activity in monthly_activities:
      date_to_activity_dict[date] = activity
    
  writer = csv.writer(sys.stdout)
  writer.writerow(HEADER_ROW)
  
  for date, activity in sorted(date_to_activity_dict.items()):
    # Google Docs needs the date in mm/dd/yy format
    date_string = date.strftime("%m/%d/%y") 
    writer.writerow([activity, date_string])
  
if __name__ == '__main__':
  main()