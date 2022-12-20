#!/usr/bin/env python
# coding: utf-8

# # Archive: Link metadata to photos

# In[1]:


## install required packages

# create requirements.txt
get_ipython().system(' echo "pandas==1.1.4" > requirements.txt')
get_ipython().system(' echo "numpy==1.19.4" >> requirements.txt')
get_ipython().system(' echo "tqdm==4.54.0" >> requirements.txt')
#! echo "xlrd==1.2.0" >> requirements.txt

# install requirements
get_ipython().system(' pip install -r requirements.txt')


# In[2]:


## import required packages

import os, ast
import pandas as pd
import numpy as np
from time import time
from tqdm import tqdm

tqdm.pandas()


# In[3]:


# Start timer
t0 = time()


# ## 0. Variables to be modified

# In[4]:


# path to photos root
path_photos = 'base photos/photos terrains'

# path to cartes root
path_cartes = 'base photos/cartes'


# ## 1. Creation of a dictionnary storing each folder code with the matching metadata

# In[5]:


def read_all_sheets(path):
    """
    creates a dataframe with all sheets concatenated from an excel file
    """
    xl = pd.ExcelFile(path)
    n_sheets = len(xl.sheet_names)
    for i in range(0, n_sheets):
        if i == 0:
            df = xl.parse(i)
        else:
            df = df.append(xl.parse(i))
    return df


# In[6]:


def gather_cartes_info(path):
    """
    creates a list of dataframes,
    each dataframe containing the information of each sites for a specific type
    
    ignores all files that do not work
    """

    cartes_info = []
    files = os.listdir(path)
    
    for file in files:
        try:
            df_file = read_all_sheets(path + '/' + file)
            cartes_info += [df_file]
        except Exception as e:
            print('\nFile discarded as a carte :', file)
            print('Error :', e)
            
    return(cartes_info)


# In[7]:


def remove_digits(string):
    """
    removes all digits from a string
    """
    return ''.join([i for i in string if not i.isdigit()])


# In[8]:


def get_code_dictionary(list_df_files):
    """
    returns a dictionary, the keys are the code types, the values are the associated dataframes
    """
        
    code_dictionary = {}

    for df in list_df_files:

        first_code = df['Code Folder'].iloc[0]
        code_root = remove_digits(first_code)

        code_dictionary[code_root] = df

    return code_dictionary


# In[9]:


cartes_info = gather_cartes_info(path_cartes)


# In[10]:


code_dictionary = get_code_dictionary(cartes_info)


# In[11]:


print(code_dictionary.keys())


# ## 2. Creation of a dataframe containing all photo names and their code folders

# In[12]:


def get_list_of_files(dir_name):
    # create a list of file and sub directories 
    # names in the given directory 
    list_of_files = os.listdir(dir_name)
    all_files = list()
    # Iterate over all the entries
    for entry in list_of_files:
        # Create full path
        full_path = os.path.join(dir_name, entry)
        # If entry is a directory then get the list of files in this directory 
        if os.path.isdir(full_path):
            all_files = all_files + get_list_of_files(full_path)
        else:
            all_files.append(full_path)
                
    return all_files


# In[13]:


def match_code_photos(photos):
    
    # Create empty dataframe
    photos_info = pd.DataFrame(columns = ['photo_name','code_folder', 'path_folder'])
    
    
    # add photo infos to dataframe
    for i in tqdm(range(0,len(photos))):

        # Exclude files with '#' in the path
        if photos[i].find('#') == -1 :

            split_path = photos[i].split('/')

            photo = split_path[-1]

            # Exclude non '.jpg' or '.JPG' files
            if (photo.split('.')[-1] == 'JPG') | (photo.split('.')[-1] == 'jpg'):

                folder_name = split_path[-2]
                code_folder = folder_name.split(' ')[-1]
                path_folder = '/'.join(photos[i].split('/')[:-1])

                # add photo infos to dataframe
                s = pd.Series([photo,code_folder, path_folder],index=['photo_name','code_folder', 'path_folder'])
                photos_info = photos_info.append(s,ignore_index=True)

    print("{} photos were found, {} were discarded because a '#' was found in the path".format(i,i-photos_info.shape[0]))
    print("dataframe contains {} photos before duplicate management".format(photos_info.shape[0]))

    # Aggregate photos in multiple folder (add '+' in code_folder)
    photos_info = photos_info.groupby('photo_name').agg(
                    {'code_folder':(lambda x: '+'.join(x)),
                     'path_folder':(lambda x: list(x))}).reset_index()

    print('dataframe contains {} photos after duplicate management'.format(photos_info.shape[0]))
    
    return photos_info


# In[14]:


photos = get_list_of_files(path_photos)


# In[15]:


photos_info = match_code_photos(photos)


# ## 3. Match photos & site information

# In[16]:


def add_metadata(photos_info, code_dictionary):
    photos_info['metadata'] = [[] for _ in range(len(photos_info))]


    for i in tqdm(range(0,len(photos_info))):
        code_folder = photos_info.iloc[i].code_folder

        code_list = code_folder.split('+')

        for code in code_list:    
            code_type = remove_digits(code)
            try :
                df_code = code_dictionary[code_type]
                row_code = df_code[df_code['Code Folder'] == code]
                metadata = row_code[['Code Display',
                                     'Name',
                                     'Type',
                                     'Latitude',
                                     'Longitude',
                                     'Location',
                                     'Region']].values.tolist()[0]
                photos_info.iloc[i,3] += [metadata]

            except Exception as z:
                print('metadata not added for line ',i,'because error with: ', z)
                
    return photos_info


# In[17]:


def sentence(metadata):
    
    n_codes = len(metadata)
    
    if n_codes == 0:
        return ""
    
    else:
    
        sites = ""

        for i, metadata_i in enumerate(metadata):
            
            code, name, type_code, latitude, longitude, location, region = metadata_i
            
            site_i = f"{name} (code: {code}, type: {type_code}, coordinates: {longitude}°N {latitude}°E)"
            
            if i != n_codes - 1:
                site_i += ', '
            else:
                site_i += '. '
            
            sites += site_i

        if n_codes == 1:
            intro = "This is a picture of a heritage site in Ladakh. "
            intro_p2 = "The site is: "

        if n_codes > 1:
            intro = "This is a picture of " + str(n_codes) + " heritage sites in Ladakh. "
            intro_p2 = "The sites are: "
        
        location_sentence = f"Location: {location} ({region}). "
        
        sentence = intro + location_sentence + intro_p2 + sites + "More information: ladakharchaeology.com"
        
        return sentence


# In[18]:


def add_sentences(photos_info):
    photos_info['sentence'] = photos_info.metadata.progress_apply(lambda x: sentence(x))
    return photos_info


# In[19]:


photos_info = add_metadata(photos_info, code_dictionary)


# In[20]:


photos_info = add_sentences(photos_info)


# In[21]:


# End timer
t1 = time() - t0
print(t1)


# In[22]:


## Save photos_info into a .csv file
photos_info.to_csv('photos_info.csv')


# ## 4. Reshape file

# In[23]:


dict_authors = {'QD': "Devers,Quentin,0000-0001-8469-0165"}


# In[24]:


photos_info = pd.read_csv('photos_info.csv', index_col=0)
photos_info['path_folder'] = photos_info['path_folder'].apply(lambda x: ast.literal_eval(x))
photos_info['metadata'] = photos_info['metadata'].apply(lambda x: ast.literal_eval(x))
photos_info


# In[25]:


photos_info['Status'] = 'pending'


# In[26]:


photos_info['Title'] = photos_info['photo_name'].apply(lambda x: x.split('.')[0].split('-')[-1])


# In[27]:


photos_info['Path'] = photos_info['path_folder'].apply(lambda x: x[0]) + '/' + photos_info['photo_name']


# In[28]:


photos_info['Description'] = photos_info['sentence']


# In[29]:


photos_info['Creator'] = photos_info['photo_name'].apply(lambda x: dict_authors[x[0:2]])


# In[30]:


photos_info['Year'] = photos_info['photo_name'].apply(lambda x: x.split('.')[0].split('-')[1])


# In[31]:


photos_info['Type'] = 'Image' #'http://purl.org/coar/resource_type/c_c513'


# In[32]:


photos_info['License'] = 'CC-BY-NC-4.0'


# In[33]:


def extract_keywords(row):

    try:
    
        list_keywords = [' '.join(list(reversed(row['Creator'].split(',')[0:2]))), # creator
        row.metadata[0][6], # Region
        row.metadata[0][5], # Location
        row.metadata[0][2]  # Type
                        ]

        code_type = list(list(zip(*row.metadata))[0])
        
        return list_keywords + code_type
    
    except Exception as e:
        print("Error for photo: {} / type: {} / metadata: {} // Error: {}".format(row.photo_name,
                                                                                  row.code_folder,
                                                                                  row.metadata,
                                                                                  e)
             )

        return ['']*4


# In[ ]:





# In[34]:


photos_info[photos_info.apply(lambda row: extract_keywords(row),axis=1).isna()]


# In[35]:


photos_info['Keywords'] = photos_info.apply(lambda row: extract_keywords(row),axis=1)


# In[36]:


photos_info['Collections'] = photos_info['Keywords'].apply(lambda x: ','.join(x[3:]))
photos_info['Keywords'] = photos_info['Keywords'].apply(lambda x: ','.join(x))


# In[ ]:





# In[37]:


photos_info = photos_info.filter(['Status', 'Title', 'Path', 'Description', 'Creator', 'Year', 'Keywords', 'Type', 'License', 'Collections'])
photos_info


# In[38]:


photos_info.to_csv('photos_info_nkl.csv', index=False)


# In[39]:


get_ipython().system(' jupyter nbconvert --to script archive.ipynb')


# In[ ]:





# ## Draft

# In[3]:


wt = pd.read_csv('base photos/wetransfer_2022-11-04_1301/photos_info.csv')


# In[4]:


wt_nkl = pd.read_csv('base photos/wetransfer_2022-11-04_1301/photos_info_nkl.csv')


# In[5]:


wt[wt.metadata == '[]']


# In[6]:


wt[wt.sentence == '']


# In[7]:


wt_nkl.shape


# In[8]:


wt.shape


# In[9]:


wt_nkl[wt_nkl.Description == '']


# In[10]:


wt_nkl


# In[11]:


wt.photo_name


# In[13]:


wt.photo_name.apply(lambda x: x[0:2]).value_counts()


# In[14]:


wt


# In[15]:


list(wt[wt.photo_name == 'Skyiu old chorten complex09.3.JPG'].path_folder)


# In[16]:


wt_nkl.Keywords.apply(lambda x: len(x.split(',')[4:])).value_counts()


# In[20]:


from itertools import chain
pd.DataFrame(set(list(chain(*list(wt_nkl.Keywords.apply(lambda x: x.split(',')[4:])),[])))).to_csv('list_code_sites.csv')


# In[30]:


list(wt_nkl[wt_nkl.Keywords.apply(lambda x: x.split(',')[4] == 'Petroglyphs')].Keywords)


# In[36]:


wt_nkl[wt_nkl.Keywords.apply(lambda x: x.split(',')[4] == 'Petroglyphs')]


# In[41]:


wt.loc[7779].metadata


# In[45]:


test_1 = pd.DataFrame(set(list(chain(*list(wt_nkl.Keywords.apply(lambda x: x.split(',')[4:])),[]))), columns=['Region'])


# In[49]:


test_1[test_1.Region.apply(lambda x: len(x)>5)]


# In[51]:


set(list(wt_nkl[wt_nkl.Keywords.apply(lambda x: x.split(',')[4] in ['Petroglyphs', "Petroglyphs and Pictographs"])].Keywords))


# In[ ]:




