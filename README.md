## Historical Job Postings API+Example

Repository for the statistics API and an example app for the dataset located at <https://jobtechdev.se/devguide/datasets/historical.html>.

### Requirements 
- Anaconda 3.x
- Apache Spark

### Computations 
(Python + Spark)  
Calculates sparse vectors for occurences of all words/phrases used more than 20 times (~500k) across all job postings. These are saved to a gzipped pickle. Note: This will take several hours if run on a local machine.  

### API 
(Python + flask)  
Loads computed sparse vectors into memory. These are used as <a href="https://en.wikipedia.org/wiki/Bitmap_index">in-memory bitmaps</a> for statistics calculations. Has a simple interpreter for a query syntax using bit operations (see notebook for examples). For a specific query, outputs sums for various variables such as months, years, employers and occupations.  
Link (+query 'javascript'): http://13.94.101.59:5000/realtime1/javascript  
Notebook: https://github.com/simonbe/afhistorik/blob/master/notebooks/API_description.ipynb

### Example app 
(javascript + d3)  
Visualizes some of the output from the API.  
Link: http://historik.azurewebsites.net

