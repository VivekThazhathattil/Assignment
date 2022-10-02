import pandas as pd
import sys

if not sys.warnoptions:
    import warnings
    warnings.simplefilter("ignore")

DATA_DIR = "data"
INPUT_FILENAME = "input1.xlsx"
OUT_FILE_NAME = "output1.xlsx"

# read input excel file
df = pd.read_excel(DATA_DIR + "/" + INPUT_FILENAME, index_col=None);

# From the header, figure out the distinct test names: concept test #num, 
# full test #num etc and put it in a list
headers = [str(header).strip() for header in df.columns]

tests = [] # list to store test names
test_details = [] # list to store test specific details
non_test_details = [] # list to store userid, chapter-tag etc

for header in headers:
    if("test" in header.lower()):
        tests.append(header.partition('-')[0].strip().lower())
        test_details.append(header.partition('-')[2].strip().lower())
    else:
        non_test_details.append(header.strip().lower())

unique_tests = sorted(list(set(tests)))
unique_test_details = sorted(list(set(test_details)))

def get_matching_key(keys, match):
    for key in keys:
        if match.lower() in key.lower():
            return key
    return ""

def get_matching_key2(keys, match1, match2):
    for key in keys:
        if match1.lower() in key.lower() and match2.lower() in key.lower():
            return key
    return ""

names_key =get_matching_key(df.columns, "name")

students = [name for name in df[names_key]]

result_df = pd.DataFrame()

def append_row(df, row):
    return pd.concat([
                df,
                pd.DataFrame([row], columns=row.index)]
           ).reset_index(drop=True)

for student_no in range(len(students)):
    for test in unique_tests: 
        skip_flag = False
        row = {}

        for non_test_detail in non_test_details:
            key = get_matching_key(df.columns, non_test_detail)
            row[non_test_detail.title()] = df[key][student_no]
        
        row["Test name"] = test.title()

        for test_detail in unique_test_details:
            key = get_matching_key2(df.columns, test, test_detail)
            row[test_detail.title()] = df[key][student_no]
            if(isinstance(row[test_detail.title()], str)):
                skip_flag = True 
                break

        if not skip_flag:
            result_df = result_df.append(row, ignore_index=True)

result_df.to_excel(DATA_DIR + "/" + OUT_FILE_NAME, index=False)
