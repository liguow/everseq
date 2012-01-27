* INSTALL Guide For EVER-seq (Evaluation Experiment of RNA-seq) package

Time-stamp: <Oct/20/2011 13:52:01 Liguo Wang>

Please check the following instructions to complete your installation.

* Prerequisite

** Python version must be greater than or equal to 2.5 to run scripts
within  EVER-seq package. We recommend using the version 2.7
** C compiler: gcc

* Install from source

This package uses Python's distutils tools for source installations. To
install a source distribution of this package, unpack the distribution 
tarball and open up a command terminal. Go to the directory where you
unpacked EVER-seq, and simply run the install script :

$ python setup.py install

By default, the script will install python library and executable
codes globally, which means you need to be root or administrator of
the machine so as to complete the installation. Please contact the
administrator of that machine if you want their help. If you need to
provide a nonstandard install prefix, or any other nonstandard
options, you can provide many command line options to the install
script. Use the --help option to see a brief list of available options:

$ python setup.py --help

For example, if I want to install everything under my own HOME
directory, use this command:

$ python setup.py install --prefix=/home/liguow

* Configure environment variables

After running the setup script, you might need to add the install
location to your PYTHONPATH and PATH environment variables. The
process for doing this varies on each platform, but the general
concept is the same across platforms.

** PYTHONPATH

To set up your PYTHONPATH environment variable, you'll need to add the
value PREFIX/lib/pythonX.Y/site-packages to your existing
PYTHONPATH. In this value, X.Y stands for the major-minor version of
Python you are using (such as 2.4 or 2.5 ; you can find this with
sys.version[:3] from a Python command line). PREFIX is the install
prefix where you installed CALFS. If you did not specify a prefix on
the command line, EVER-seq package will be installed using Python's 
sys.prefix value.

On Linux, using bash, I include the new value in my PYTHONPATH by
adding this line to my ~/.bashrc:

$ export PYTHONPATH=/home/liguow/lib/python2.7/site-packages:$PYTHONPATH

Using Windows, you need to open up the system properties dialog, and
locate the tab labeled Environment. Add your value to the PYTHONPATH
variable, or create a new PYTHONPATH variable if there isn't one
already.


** PATH

Just like your PYTHONPATH, you'll also need to add a new value to your
PATH environment variable so that you can use the scripts within EVER-seq
package by simply typing their names on command line directly. Unlike the 
PYTHONPATH value, however, this time you'll need to add PREFIX/bin to your 
PATH environment variable. The process for updating this is the same as
described above for the PYTHONPATH variable.

$ export PATH=/home/liguow/bin:$PATH

