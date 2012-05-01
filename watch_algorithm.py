LINES = [
'ITLISASTIME'
'ACQUARTERDC'
'TWENTYFIVEX'
'HALFBTENFTO'
'PASTERUNINE'
'ONESIXTHREE'
'FOURFIVETWO'
'EIGHTELEVEN'
'SEVENTWELVE'
'TENSEOCLOCK'
]

WORDS = [
'IT', 'IS'
'QUARTER',
'TWENTY', 'TWENTYFIVE', 'FIVE'
'HALF', 'TEN', 'TO'
'PAST', 'NINE'
'ONE','SIX','THREE',
'FOUR','FIVE','TWO',
'EIGHT','ELEVEN'
'SEVEN','TWELVE',
'TEN'
'OCLOCK'
]

0 - hour o'clock
5 - five past
10 - ten past
15 quarter past
20 twenty past
25 twentyfive past
30 half past
35 twentyfive to
40 twenty to
45 quarter to
50 ten to
55 five to

TIME_STRINGS = {
  0: 'IT IS {HOUR} OCLOCK',
  5: 'IT IS FIVE PAST {HOUR}',
  10: 'IT IS TEN PAST {HOUR}',
  15: 'IT IS QUARTER PAST {HOUR}',
  20 'IT IS TWENTY PAST {HOUR}'
  25 'IT IS TWENTYFIVE PAST {HOUR}'
  30 'IT IS HALF PAST {HOUR}'
  35 'IT IS TWENTYFIVE TO {HOUR}'
  40 'IT IS TWENTY TO {HOUR}'
  45 'IT IS QUARTER TO {HOUR}'
  50 ten to
  55 five to
  



}


def GetTimeString(datetime):
  """Returns the textual description of the time"""
  
  
  