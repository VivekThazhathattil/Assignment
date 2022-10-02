import pandas as pd
import sys

# suppress warnings: mainly deprecated pandas append function warning
if not sys.warnoptions:
    import warnings
    warnings.simplefilter("ignore")

# define the input and output files here
DATA_DIR = "data"
INPUT_FILENAME = "input1.xlsx"
OUT_FILE_NAME = "output1.xlsx"

# read input excel file
df = pd.read_excel(DATA_DIR + "/" + INPUT_FILENAME, index_col=None);

# get the headers of the dataframe
headers = [str(header).strip() for header in df.columns]

tests = [] # list to store test names
test_details = [] # list to store test specific details
non_test_details = [] # list to store userid, chapter-tag etc

# collect the test names, various test statistics and other details and 
#store them in the lists - tests, test_details, non_test_details
for header in headers:
    if("test" in header.lower()):
        tests.append(header.partition('-')[0].strip().lower())
        test_details.append(header.partition('-')[2].strip().lower())
    else:
        non_test_details.append(header.strip().lower())

# filter out duplicate names and sort the list strings lexicographically
unique_tests = sorted(list(set(tests)))
unique_test_details = sorted(list(set(test_details)))


# function to get the column name with matching substring
def get_matching_key(keys, match):
    for key in keys:
        if match.lower() in key.lower():
            return key
    return ""

# function to get the column name based on two matching substrings
def get_matching_key2(keys, match1, match2):
    for key in keys:
        if match1.lower() in key.lower() and match2.lower() in key.lower():
            return key
    return ""

# get the column name for Names of the student column
names_key =get_matching_key(df.columns, "name")

# get the student names (Potential problem of duplicate names not handled)
students = [name for name in df[names_key]]

# define result dataframe which will be returned at the end
result_df = pd.DataFrame()

# collect the test stats for each test of each student in separate rows
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

# output the result in a new xlsx file
result_df.to_excel(DATA_DIR + "/" + OUT_FILE_NAME, index=False)
