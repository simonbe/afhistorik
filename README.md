## Historical Job Postings API+Example



Requirements 
-----------------
- Anaconda 3.x
- Apache Spark

Computations 
-----------------
(Python + Spark)  
Calculates sparse vectors for occurences of all words/phrases used more than 20 times (~500k) across all job postings. These are saved to a gzipped pickle as { 'word1': [sparse vector 1], 'word2': [sparse vector 2] ... }  
Note that this computation will take several hours if run on a local machine. A pre-calculated matrix can be downloaded here.  

API 
-----------------
(Python + flask)  
Loads computed sparse vectors into memory. The sparse vectors are used as <a href="https://en.wikipedia.org/wiki/Bitmap_index">in-memory bitmaps</a>. Has a simple interpreter for a query syntax using bit operations (see notebook for examples). For a specific query, outputs sums for various variables such as months, years, employers and occupations.  
Link: 

Example app 
-----------------
(javascript + jQuery + d3)  
Visualizes some of the output from the API.  
Link: http://historik.azurewebsites.net

