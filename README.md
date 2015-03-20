`SEQMAK`
========

`SEQMAK` (pronounced SEC-mac) is a near clone of SEQUIN which was written by Ned Seeman ([1][first], [2][second]). The main differences are

* much of the repetitive nature of SEQUIN has been automated,

* exception handling has been much improved, and

* all features have been modularized, making the code much easier to read, learn, and maintain.

As is the case with SEQUIN, kinetic and thermodynamic factors are not taken into
account when designing structures with SEQMAK . Only different combinations of DNA bases are considered. If you would like to consider other factors when designing your DNA structure, you may want to use a more complex program such as [DNAdesign](http://dna.caltech.edu/DNAdesign/).


Dependencies
------------
`SEQMAK` is written in Python 2.7. In order to run the program you must have Python installed on your computer (preferably version 2.7x but version 2.4x should also work). This software has not been tested with Python 3.0 or higher, so I cannot guarantee it will work under those environments. If you do not have Python installed on your computer, you may download the latest version at [http://www.python.org/download/](http://www.python.org/download/).

All python package dependencies can be installed using `pip`. `pip` does not come pre-installed  with the python virtual machine, so you need to install it manually.

* Install pip (if you do not have it installed)

`# yum install python-pip`
	
or 

`$ sudo apt-get install python-pip`
	
for GNU/linux machines.

* Upgrade `pip`.

`$ sudo pip install pip --upgrade`

* Install all required dependencies by typing
   
`$ pip install -r requirements.txt`



Usage
-----

Read the *Introduction* of the manual for information on running the program.




[first]: <http://www.cell.com/biophysj/abstract/S0006-3495(83)84292-1>
"N. C. Seeman and N. R. Kallenbach, *"Design of immobile Nucleic Acid Junctions"*,  *Biophysical Journal* **44**, 201-209 (1983)"

[second]: <http://www.tandfonline.com/doi/abs/10.1080/07391102.1990.10507829#preview>
"N. C. Seeman, *"De Novo Design of Sequences for Nucleic Acid Structural Engineering"*, *Journal of Biomolecular Structure & Dynamics* **8**, 573-581 (1990)"
