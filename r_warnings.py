import rpy2

# Capture and print R warnings
def print_r_warnings():
    r_warnings = rpy2.robjects.r('warnings()')
    print(r_warnings)