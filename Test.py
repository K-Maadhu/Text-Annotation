import pandas as pd

userlist = ['some', 'values']
userlist = pd.DataFrame(userlist)

keywords_file = 'Data\\User List.csv'
file_obj = open(keywords_file, 'w')
userlist.to_csv(keywords_file)
file_obj.close()