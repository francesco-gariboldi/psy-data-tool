# psy-data-tool
My psychology master thesis project. A semi automatic linear regression models generation and comparison tool. Python and R are both used through Rpy2.

## **Instructions for Use: Software Requirements and Configuration**

The program will be available for download on Github.com.

It is my intention to create a software package for the project in the future, so the following configuration steps won't be necessary. For now, the configuration must be done manually and requires the following steps.

N.B. Commands to be run from the terminal (Linux) are prefixed with `$`.

### Linux or WSL2

To use this program, Linux or WSL2 (Windows Subsystem for Linux 2) is required.

### Jupyter Notebook

The code is designed to run in a Jupyter notebook, and it is highly recommended to use it with this software. In theory, it should also work on other software that supports Jupyter or compatible notebooks, but this has not been verified.

### Installing R

I recommend running the following command in the terminal, as doing it directly from a Jupyter notebook might cause issues due to password and admin permission requests (sudo) when the command is executed:

```bash
$ sudo apt-get install r-base-dev
```

instead of:

```bash
$ sudo apt-get install r-base
```

To ensure some tools and packages work properly, it may be necessary to grant the user full access permissions to the R libraries. In this case, find the R installation paths with:

```R
.libPaths()
```

and run in the shell (terminal):

```bash
$ sudo chmod -R 777 /usr/local/lib/R/site-library  
$ sudo chmod -R 777 /usr/lib/R/site-library  
$ sudo chmod -R 777 /usr/lib/R/library
```

### Creating a Virtual Environment with Venv

Since the development of the program used a virtual environment (with the `venv` command) in Python, the packages and code for this notebook are installed using:

`$ pip` with the `-m` option.

It is suggested to do the same. Installing packages in a virtual environment is a safer and more robust practice for package management, avoiding potential conflicts with packages and dependencies that may already be present on your computer.

### ! and %: Jupyter Magics

Some useful resources:

[Official statement from the creator of IPython/Jupyter](https://github.com/jupyterlab/jupyterlab-desktop/issues/234#issuecomment-928484514)

[Blog post from the creator of the %pip magic command](https://jakevdp.github.io/blog/2017/12/05/installing-python-packages-from-jupyter/)

[The pull request that introduced %pip and %conda magics](https://github.com/ipython/ipython/pull/11524)

`%pip` correctly resolves the appropriate virtual environment (the one used by the current kernel) in most edge cases, while `!pip` may not, leading to package installation in the wrong locations.

Since we are using a virtual environment (venv), it is advisable to use `%`.

### Installing Rpy2

Run the following command in a Jupyter notebook cell:

```jupyter
!python3 -m pip install rpy2
```

##### How to Set the R_HOME Environment Variable to Use rpy2 in a Jupyter Notebook

The **R** home directory is the top-level directory of the **R** installation in the operating system's filesystem. In an **R** session, the **R** home directory is often indicated in Linux through the `R_HOME` environment variable. It can also be found outside an **R** session with the command:

```bash
$ R RHOME
```

Here’s how you can set the `R_HOME` environment variable directly from a Python script for using rpy2:

```jupyter
import os  
  
os.environ['R_HOME'] = '/usr/lib/R'   # Replace with the output of the `R RHOME` command (run it in your terminal).
  
import rpy2
```

Alternatively, you can set the `R_HOME` environment variable in your shell’s configuration file before running the Python script:

```bash
# In the shell configuration file, depending on your Linux distribution
export R_HOME=$(R RHOME)
```

### Packages and Dependencies

##### Python Packages:

The required packages should be installed in the Python virtual environment you intend to use. Once you’ve opened the Jupyter notebook and activated the virtual environment, you can install all the Python packages (requirements) directly in a Jupyter notebook cell using the magic command:

```Jupyter notebook
%pip install -r requirements.txt
```

or from the terminal:

```bash
$ pip install -r requirements.txt 
``` 

The `requirements.txt` file is already included in the program folder downloadable from Github and contains all the necessary software requirements.

##### R Packages

Required R packages: 'lme4', 'lmerTest', 'emmeans', 'geepack', 'performance', 'graphics', 'ggplot2', 'gglm'.

Before installing the packages in Jupyter, run the following command in a cell, which loads the necessary extension to allow Python and Jupyter to communicate with the R environment:

```Jupyter notebook
%load_ext rpy2.ipython
```

## Two ways to install R packages in Jupyter via rpy2:
### 1) Through Python using rpy2
(recommended, as it allows the code to be used outside the Jupyter notebook. Just copy it into a Python script and it will work).

```jupyter
from rpy2.robjects.packages import importr 
``` 
  
### Import an R package into Jupyter

```jupyter
graphics = rpy2.robjects.packages.importr('package_name')
```

This step imports the R package into the embedded R environment, making all R objects available as Python objects.

N.B. There’s a peculiarity: R object names can contain a “.” (dot), while in Python the dot denotes an “attribute in a namespace.” For this reason, `importr` attempts to translate “.” into “_”. More details can be found in the [R packages documentation](https://rpy2.github.io/doc/latest/html/robjects_rpackages.html#robjects-packages).

### 2) If you want to install a list of packages together:

#### Create a list of packages 

```jupyter
packnames = ('lme4', 'lmerTest', 'emmeans', 'geepack', 'performance','graphics', 'ggplot2', 'gglm')
utils = rpy2.robjects.packages.importr("utils")
```

  
Select a mirror for the R packages:

```jupyter
utils.chooseCRANmirror(ind=1)  # Selects the first mirror in the list  
utils.install_packages(rpy2.robjects.vectors.StrVector(packnames))
```

At this point, all the requirements for running the program are satisfied.

Before using the xplore_data function standardize column names (to lower cased snake_case). It is necessary for the program to work:
```
df.columns = df.columns.str.replace('%', '').str.replace('(', '').str.replace(')', '').str.strip().str.lower().str.replace(' ', '_')
```

I would like to make a package of this project in the future, but I don't know if it's possible due to its hybrid nature (R and Python).
