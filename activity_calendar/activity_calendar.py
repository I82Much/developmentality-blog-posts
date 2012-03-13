import csv
import random
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
def main():
  if len(sys.argv) != 2:
    print >> sys.stderr, "Usage: python activity_calendar.py /path/to/activities"
    sys.exit(1)
    
  activity_file = open(sys.argv[1])
  activities = [line.strip() for line in activity_file]
  activity_file.close()
  
  # We have the raw activities; now we need to assign them to days
  january_1 = datetime.date(datetime.date.today().year, 1, 1)
  december_31 = datetime.date(datetime.date.today().year, 12, 31)
  
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