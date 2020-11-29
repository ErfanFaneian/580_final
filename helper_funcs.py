from scipy import stats
from collections import Iterable


## STATS SECTION ## 


# This function makes it easier to get readable print-outputs for the normality test
def normaltest_Print(array, dataset_name):
    k2, p_val = stats.normaltest(array)
    print("\n" + dataset_name + "--- Dataset Stats:\n" + "Size of " + dataset_name + " Dataset = " + str(len(array)) + "\nNormality Test-->\n")
    print("p value = " + str(p_val) + "\n")

    if (p_val > 0.05):
        print("We cannot reject the null hypothesis that the distribution of values in the '" + dataset_name + "' dataset is normal.")
    else:
        print("We reject the null hypothesis that the distribution of values in the '" + dataset_name + "' dataset is normal.")
       

## DATA CLEANING/FORMATTING SECTION ##
       
    
# some list-like value columns contain inconsistent delimiters. (i.e. sometimes they are delimted by '||' and other times by '|')
# this list comprehension function fixes that
def norm_nestedList(nestedList):
    norm_list = []
    for item in nestedList:
        l = list(item)
        l = [i for i, next_i in zip(l, l[1:] + [None]) #for each list, create a copy, and compare items such
                 if (i, next_i) != ('|', '|')]         #that the 'first' and 'next' items (relative to the
        l = [i for i, next_i in zip(l, l[1:] + [None]) #original list) are always compared. Remove consecutive
                 if (i, next_i) != (':', ':')]         #duplicates of the specified characters
        s = ''.join(l)
        norm_list.append(s)
    return norm_list

# when reading nested lists in a column from a CSV, these are initially imported as strings
# to convert them back to lists, use this function
def listify(df, col_name):
    new_col = []
    for stringlist in df[col_name]:
        list_val = eval(stringlist)
        new_col.append(list_val)
    df[col_name] = new_col
    return df

# to make statistics more convenient, this function is included to flatten nested lists into
# one-dimensional, regular ol' lists
def flatten(lis):
     for item in lis:
         if isinstance(item, Iterable) and not isinstance(item, str):
             for x in flatten(item):
                 yield x
         else:        
             yield item
                
# some list like string values contain random digits. this function gets rid of those
def pluck_digits(df, col_name):
    norm_lis = []
    for each in df[col_name]:
        result = ''.join([i for i in each if not i.isdigit()])
        norm_lis.append(result)
    df[col_name] = norm_lis
    return df

def spearmantest_Print(x, y, x_name, y_name):
    print("The null hypothesis is that values in the '" +x_name+ "' dataset do not correlate with the values in the '" +y_name+ "' dataset. \n")
    sp_r, p_value = stats.spearmanr(x, y)
    if (p_value > 0.05):
        print("We cannot reject the null hypothesis. \n")
    else:
        print("We reject the null hypothesis. \n")
    print("Spearman's R Correlation Coeffecient = " + str(sp_r) + "\n" + "p value = " + str(p_value) + "\n")