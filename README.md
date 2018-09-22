Simulation Analysis of Road infrastructure
===============
This repository provides codes which have been used for Humanitarian Aid supply analysis in Bangladesh.

Data Cleaning
---------------
The road infrastructure data provided in Bangladesh official database contains many errors, mostly in its geographical location.

This is how it looks like in the beginning and after the cleaning.
![1](https://user-images.githubusercontent.com/37578231/37669467-3263bf14-2c67-11e8-8c2a-9e32f334d396.png)

The cleaning process highly utilizes **local regression** method, one of the machine learning algorithms. By detecting outliers in this way and re-locating them onto the most probable location, the road data was corrected in the right order:

![2](https://user-images.githubusercontent.com/37578231/45920976-d317ba00-beac-11e8-9648-f59f98b34c56.png)

Model building
---------------
The model was built by simulation software package, namely Simio. When all roads and bridges are modeled in Simio, one add-in is used to efficiently create thousands of objects (entity, server, path, nodes, etc.) automatically.

Data Visualization
---------------
The main purpose is to show explicitly how traffic volume and its economic value change over path. It is shown that the traffic volume peaks nearby Dhaka. (the capital city)
![3](https://user-images.githubusercontent.com/37578231/45921042-f3944400-bead-11e8-9a31-fd375d401746.png)


Integrate with mySQL
---------------
Simio simulation model and Python visualization tool are integrated on the mySQL (middle ware) environment. The simulation data is flowing from Simio model through mySQL to Python in order to visualize the state variables in our interest. In other way around, some events can be triggered from Python script (such as bridges are broken) and the events occurs in Simio **during its execution**.
![4](https://user-images.githubusercontent.com/37578231/45921163-a5cd0b00-beb0-11e8-9185-e0715e616303.png)
