Simulation Analysis of Road infrastructure
===============
This repository provides codes which have been used for Humanitarian Aid supply analysis in Bangladesh.

Data Cleaning
---------------
The road infrastructure data provided in Bangladesh official database contains many errors, mostly in its geographical location.

This is how it looks like in the beginning:
![alt text](https://user-images.githubusercontent.com/37578231/37669467-3263bf14-2c67-11e8-8c2a-9e32f334d396.png)

The cleaning process highly depends on **local regression**, one of the machine learning algorithms. By detecting outliers in this way and re-locating them onto the most probable location, the road data is now in the right order:

![alt text](https://user-images.githubusercontent.com/37578231/37669467-3263bf14-2c67-11e8-8c2a-9e32f334d396.png)
