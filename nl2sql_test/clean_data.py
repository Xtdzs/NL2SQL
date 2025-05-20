import pandas as pd

eval_data_path = "eval_data/eval_data.csv"
save_path = "eval_data/eval_data_unique.csv"

# Load eval data
eval_df = pd.read_csv(eval_data_path, encoding="gbk", quoting=1)

# Check for duplicates
duplicates = eval_df[eval_df.duplicated(subset=["nl"], keep=False)]
if not duplicates.empty:
    print("Duplicates found:")
    print(duplicates)
else:
    print("No duplicates found.")
    
# save the unique data
eval_df.drop_duplicates(subset=["nl"], keep="first", inplace=True)
eval_df.to_csv(save_path, index=False, encoding="gbk", quoting=1)
print(f"Unique eval data saved to {save_path}.")