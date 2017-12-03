import csv
import operator 
import pandas as pd

def pds_av(df):
	print(list(df))
	mode_cols = ['MARITAL_STATUS', 'sex', 'TOBACCO', 'state']
	mean_cols = ['OPTIONAL_INSURED', 'seconds', 'WEIGHT', 'PEOPLE_COVERED', 'HEIGHT', 'ANNUAL_INCOME']  
	for col in list(df):
		groupby_plan = df[col].groupby(df['PURCHASED'])
		if col in mode_cols:
			print(groupby_plan.agg(lambda x:x.value_counts().index[0]))
		if col in mean_cols:
			if col == 'seconds':
				print(groupby_plan.mean()/(3600*24*365))
			else:
				print(groupby_plan.mean())



def remove_p(df, new_name):
	keep_col = (list(df))[:-1]
	print(keep_col)
	new_f = df[keep_col]
	new_f.to_csv(new_name, index=False)


def age_to_long():
	#1979-09-08T22:11:38Z
	with open("nop_some_data.csv", "rb") as source:
		reader = csv.reader(source)
		with open("nop_data.csv", "wb") as result:
			writer = csv.writer(result)
			for line in reader:
				writer.writerow()

def main():
	df = pd.read_csv("age_data.csv")
	pds_av(df)

main()


'''
PURCHASED
Bronze      705244.440207
Gold        704768.639293
Platinum    705160.733963
Silver      705062.604787
Name: OPTIONAL_INSURED, dtype: float64
PURCHASED
Bronze      166.547694
Gold        166.351174
Platinum    166.512384
Silver      166.421888
Name: WEIGHT, dtype: float64
PURCHASED
Bronze      49.056995
Gold        49.077104
Platinum    49.042035
Silver      49.096434
Name: seconds, dtype: float64
PURCHASED
Bronze      M
Gold        M
Platinum    M
Silver      M
Name: MARITAL_STATUS, dtype: object
PURCHASED
Bronze      M
Gold        F
Platinum    M
Silver      F
Name: sex, dtype: object
PURCHASED
Bronze      1.897538
Gold        1.901426
Platinum    1.905438
Silver      1.898306
Name: PEOPLE_COVERED, dtype: float64
PURCHASED
Bronze      63.930446
Gold        63.920041
Platinum    63.913745
Silver      63.935067
Name: HEIGHT, dtype: float64
PURCHASED
Bronze      239839.344028
Gold        239972.670546
Platinum    240800.076654
Silver      240024.970570
Name: ANNUAL_INCOME, dtype: float64
PURCHASED
Bronze      No
Gold        No
Platinum    No
Silver      No
Name: TOBACCO, dtype: object
PURCHASED
Bronze      Texas
Gold        Texas
Platinum    Texas
Silver      Texas
Name: state, dtype: object
'''
