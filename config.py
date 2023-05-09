import pandas as pd

NUM_EMPLOYEES = 7

date_format = '%Y-%m-%dT%H:%M'

min_date = pd.Timestamp.today().normalize()

max_date = min_date + pd.DateOffset(days=31)

min_date_str, max_date_str = (d.strftime(date_format)
                              for d in (min_date, max_date))
