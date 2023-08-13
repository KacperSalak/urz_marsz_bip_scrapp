from dwnld_raw_data import dwnld_data
from build_df_from_json import build_combined_df

# download data and save data from each website into json file
dwnld_data()

# after manual deletion of last couple records from each file
# build a pandas data frame combinig all records
df = build_combined_df() 