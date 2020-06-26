###  Stack Club 2020 Summer Course

2020.06.26 Friday
### Project explanation
 
This is the "DIA" project.  Goal is to plant fake stars (PSFs) into a calexp, subtract a template, check that the transient is detected in the resulting diff image(s) and do some data visualization (plot a light curve, show some postage stamps).  

Possible extensions/variants: planting a grid of fakes of varying brightness and measuring detection efficiency; plant a cluster of closely-spaced fakes on top of bright galaxies (mimics strongly-lensed sources).  
Note: We think this doesn't exist in StackClub repos, but its somewhat redundant with ongoing DESC-DC2-DIA work.  
 
We're using the AP_pipeline for this, starting with HiTS2015 DECam data. 


## Structure of the project notebooks

1. 01_dia_data_discovery.ipynb : a nb for data exploration.  Answering the question: "If I have a data repo and I know it has some coadds in it, how do I find the info (visits, ccds, tracts, patches, dates) needed to make a time series of (calexp,coadd) pairs suitable for difference imaging and light curve construction?"
 - started by Markus Rabus in session 08

2. 02 planting fakes : adding fake PSFs to a calexp or series of calexps, with fixed RA,Dec across multiple epochs, so we can get a coherent light curve out of the source catalogs. 
 - started by Dani Chao in session 08

3. 03 running the ap_pipeline : making diff images using a set of cal



## Resource / reference notebooks to draw from : 

some resources that we can draw from for generating our stack club DIA notebook(s).
All are in ''StackClubCourse/Projects/DIA/''

1. DESC01_Create_Calexp_Repo.ipynb
2. DESC02_Fake_Injection.ipynb
3. DESC02a_Grid_Injection.ipynb

These three notebooks are from Shu Liu, PhD student working with Michael Wood-Vasey at Pitt.  Shu has been working on a DESC project, planting fake stars into DC2 images and measuring the detection efficiency, particularly around bright stars.   These are preliminary, and are very DC2-specific in some ways, but they work!

See https://github.com/LSSTDESC/dia_improvement/tree/update_tutorials/tutorials 
and https://docs.google.com/presentation/d/11cS7oeRglx8revYoh9z0kaXfb4biRRGTawBF15dB3C8/edit#slide=id.g851e3a1107_2_75

4. DESC04_dia_source_object_stamp.ipynb

Notebook developed by Michael Wood-Vasey as a DC2 analysis tutorial, showing how to work with DIAobject and DIAsource tables. 


5. SC01_DIA_How_To_Generate_a_Template_Image.ipynb

This is a Stack Club notebook from Phil Marshall's DIA branch. Does what it says on the tin. 

See https://github.com/LSSTScienceCollaborations/StackClub/tree/project/DIA/drphilmarshall/DIA

