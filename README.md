# Wiki-Search-Engine
I did this mini project in the course Information Retrieval and Extraction. This project contains code for creating a search engine from scratch in python.

### Libraries used:
```
NLTK,PyStemmer,re,math,xml.sax
```
## File Structure:
indexer.py is used for indexing the fies
search.py for carrying out the search operations
merging.py and split.py to split them for the same.
The bonus folder contains a special indexer and searcher for the hindi search results and queries
### Optimisations:
All the numbers are stored in hex number with and no spaces are used to reduce space. To optimise this f strings are used to speed up the process.
merger and split for merging the final index file using mergesort technique so that it can be done in O log(n). This stores the final index in sorted ways which can be later split. Words with length greater than 45 were removed in primary index creation

split for splitting the final merged file, this is simple and is an O(n) process with each file having close to 15000 files per 
### Results
Index is of size 317.5 MB for smaller file and ~ 340 seconds for index creation, merging and splitting.
### Format
Format of index creation m:doc number, t:title occurences,l:external links, i:information box, o:body,r:references,n:categories

## Instructions to run
### Indexer
python3 indexer.py ```data_path``` ```final_folder_path```  ```stats.txt```
### Merger
python3 merging.py ```path_to_folder```
### Splitter
python3 split.py ```final_folder``` ```merged_index``` ```secondary_file```
### Searching
python3 search.py ```query_file```
This will output results in a query_op.txt in the same directory.

