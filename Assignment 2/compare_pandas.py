'''
These are for comparing frames with numeric data only.
'''

def compare_frames(df1, df2, precision=0.011, na=-999, dtype=False):
    if not ((df1.index == df2.index).all() and (df1.columns == df2.columns).all()):
        print('------DataFrame indices--------')
        print('  df1:', df1.index)
        print('  df2:', df2.index)
        print('------DataFrame columns--------')
        print('  df1:', df1.columns)
        print('  df2:', df2.columns)
        print('------DataFrame shape----------')
        print('  df1:', df1.values.shape)
        print('  df2:', df2.values.shape)
        print('-------------------------------')
        return False
    if dtype:
        for col in df1:
            if not df1[col].dtype == df2[col].dtype:
                print('------DataFrame column dtypes differ ----------')
                print('  col:', col)
                print('  df1:', df1[col].dtype)
                print('  df2:', df2[col].dtype)
                print('-----------------------------------------------')
                return False
    df1 = df1.fillna(na) # slower but safer - use inplace=True for speed
    df2 = df2.fillna(na)
    bools = abs(df1.values - df2.values) < precision
    if bools.all():
        return True
    indices = (bools.argmin() // bools.shape[1], bools.argmin() % bools.shape[1])
    print('********* DataFrame contents differ *********')
    print('   ', str(bools[indices[0], indices[1]]), 'at indices:', indices[0], indices[1])
    print('   ', df1.iloc[indices[0], indices[1]], '!=', df2.iloc[indices[0], indices[1]])
    print('*********************************************')
    return False

def compare_frames_str(df1, df2, na='', dtype=False):
    ''' 
    For frames filled with string values or any other value that
    can be compared with ==
    '''
    if not ((df1.index == df2.index).all() and (df1.columns == df2.columns).all()):
        print('------DataFrame indices--------')
        print('  df1:', df1.index)
        print('  df2:', df2.index)
        print('------DataFrame columns--------')
        print('  df1:', df1.columns)
        print('  df2:', df2.columns)
        print('------DataFrame shape----------')
        print('  df1:', df1.values.shape)
        print('  df2:', df2.values.shape)
        print('-------------------------------')
        return False
    df1 = df1.fillna(na) # slower but safer - use inplace=True for speed
    df2 = df2.fillna(na)
    for i in df1.index:
        for j in df1.columns:
            if df1.loc[i, j] != df2.loc[i, j]:
                print('********* DataFrame contents differ *********')
                print('    Problem at labels:', i, j)
                print('   ', df1.loc[i, j], '!=', df2.loc[i, j])
                print('*********************************************')
                return False
    if dtype:
        for i in df1.index:
            for j in df1.columns:
                if type(df1.loc[i, j]) != type(df2.loc[i, j]):
                    print('********* DataFrame types differ *********')
                    print('    Problem at labels:', i, j)
                    print('   ', type(df1.loc[i, j]), '!=', type(df2.loc[i, j]))
                    print('*********************************************')
                    return False
    return True
    
def compare_frames_vals_only_disordered(df1, df2, precision=0.011, dtype=False):
    ''' 
    --> If using on DataFrames, pass in values array only!!!
    Rows can be in any order. 
    Must have at least one row in each frame/array/lol.
    Will work on arrays.
    '''
    if not len(df1) == len(df2):
        print('------Number of rows differ ----------')
        print('  len(df1):', len(df1))
        print('  len(df2):', len(df2))
        return False
    if not len(df1[0]) == len(df2[0]):
        print('------Number of columns differ ----------')
        print('  len(df1[0]):', len(df1[0]))
        print('  len(df2[0]):', len(df2[0]))
        return False
    '''
    # This stuff works on DataFrames only.
    if dtype:
        for col in df1:
            if not df1[col].dtype == df2[col].dtype:
                print('------DataFrame column dtypes differ ----------')
                print('  col:', col)
                print('  df1:', df1[col].dtype)
                print('  df2:', df2[col].dtype)
                print('-----------------------------------------------')
                return False
    df1 = df1.fillna(na) # slower but safer - use inplace=True for speed
    df2 = df2.fillna(na)
    '''
    # Could optimize if certain that no duplicate rows
    for i in range(len(df1)):
        found = False
        for j in range(len(df1)):
            bools = abs(df1.iloc[i] - df2.iloc[j]) < precision
            if bools.all():
                found = True
                break
        if not found:
            return False
    return True

def compare_series(s1, s2, precision=0.011, na=-999, dtype=False, name=False):
    if name and not s1.name == s2.name:
        print('------Series names--------')
        print('  s1: ', s1.name) 
        print('  s2: ', s2.name) 
        print('-------------------------------')
        return False    
    if dtype and not s1.dtype == s2.dtype:
        print('------Series datatypes--------')
        print('  s1: ', s1.dtype) 
        print('  s2: ', s2.dtype) 
        print('-------------------------------')
        return False    
    if not (s1.index == s2.index).all():
        # if ever an index of floats, might need a version with a tolerance
        print('------Series indices--------')
        print('  s1: ', s1.index) # could go ahead and find the differing position and provide it's
        print('  s2: ', s2.index) # index and the differing values
        print('-------------------------------')
        return False
    s1 = s1.fillna(na) # slower but safer - use inplace=True for speed
    s2 = s2.fillna(na)
    bools = abs(s1.values - s2.values) < precision
    if bools.all():
        return True
    index = bools.argmin()
    print('********* Series contents differ *********')
    print('   ', str(bools[index]), 'at index:', index)
    print('   ', s1.iloc[index],  '!=', s2.iloc[index])
    print('******************************************')
    return False
    
def compare_series_str(s1, s2, dtype=False, name=False, na=''):
    if name and not s1.name == s2.name:
        print('------Series names--------')
        print('  s1: ', s1.name) 
        print('  s2: ', s2.name) 
        print('-------------------------------')
        return False    
    if dtype and not s1.dtype == s2.dtype:
        print('------Series datatypes--------')
        print('  s1: ', s1.dtype) 
        print('  s2: ', s2.dtype) 
        print('-------------------------------')
        return False    
    if not (s1.index == s2.index).all():
        # if ever an index of floats, might need a version with a tolerance
        print('------Series indices--------')
        print('  s1: ', s1.index) # could go ahead and find the differing position and provide it's
        print('  s2: ', s2.index) # index and the differing values
        print('-------------------------------')
        return False
    s1 = s1.fillna(na) # slower but safer - use inplace=True for speed
    s2 = s2.fillna(na)
    for label in s1.index:
        if s1.loc[label] != s2.loc[label]:
            print('********* Series contents differ *********')
            print('    Problem at index:', label)
            print('   ', s1.loc[label],  '!=', s2.loc[label])
            print('******************************************')
            return False
    return True
    
def compare_lists(l1, l2, tol=0.001):
    end = min(len(l1), len(l2))
    for i in range(end):
        if abs(l1[i] - l2[i]) > tol:
            print("********* List contents differ at index:", i, "*********")
            print('   ', l1[i],  '!=', l2[i])
            print('*******************************************')
            return False
    if len(l1) != len(l2):
            print("**** All corresponding elements equal but list lengths differ: ****")
            print('  Length list 1:', len(l1))
            print('  Length list 2:', len(l2))
            print('*******************************************')
            return False
    return True
    
def compare_los(l1, l2, tol=0.001, show=True, skip_str_lens=False):
    eol = min(len(l1), len(l2)) # end of list
    for i in range(eol):
        eos = min(len(l1[i]), len(l2[i])) # end of string
        if l1[i] != l2[i]:
            if not skip_str_lens and len(l1[i]) != len(l2[i]):
                print("********* Strings differ at list index:", i, "*********")
                print("********* Strings have different lengths: *********")
                print("  Length string 1:", len(l1[i]))
                print("  Length string 2:", len(l2[i]))
                print('*******************************************')
                return False
            for j in range(eos):
                if l1[i][j] != l2[i][j]:
                    print("********* Strings differ at list index:", i, "*********")
                    print("********* Strings differ at character:", j, "*********")
                    print('   ', l1[i][j],  '!=', l2[i][j])
                    if show:
                        print("--------- String 1: ---------")
                        print(l1[i])
                        print("--------- String 2: ---------")
                        print(l2[i])
                    print('*******************************************')
                    return False
    if len(l1) != len(l2):
        print("**** All corresponding elements equal but list lengths differ: ****")
        print('  Length list 1:', len(l1))
        print('  Length list 2:', len(l2))
        if show:
            print("--------- String 1: ---------")
            print(l1[i])
            print("--------- String 2: ---------")
            print(l2[i])
        print('*******************************************')
        return False
    return True
    
def compare_lols(l1, l2, tol=0.001):
    if len(l1) != len(l2):
        print("**** The lol's have different lengths (numbers of inner lists): ****")
        print('  Length list 1:', len(l1))
        print('  Length list 2:', len(l2))
        print('*******************************************')
        return False
    for i in range(len(l1)):
        if len(l1[i]) != len(l2[i]):
                print("**** Inner list lengths differ for row " + str(i) + ": ****")
                print('  Length inner list lol 1:', len(l1[i]))
                print('  Length inner list lol 2:', len(l2[i]))
                print('*******************************************')
                return False
        for j in range(len(l1)):
            if type(l1[i][j]) != type(l2[i][j]):
                print("********* Element types differ at indices:", str(i) + ',', j, "*********")
                print('   ', type(l1[i][j]),  '!=', type(l2[i][j]))
                print('*******************************************')
                return False
            if abs(l1[i][j] - l2[i][j]) > tol:
                print("********* List contents differ at indices:", str(i) + ',', j, "*********")
                print('   ', l1[i][j],  '!=', l2[i][j])
                print('*******************************************')
                return False
    return True
    
