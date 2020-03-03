import gridlabd
import sys, getopt
# import traceback
import os


try : 
    gridlabd.command('--profile')
    gridlabd.command('--version')
    # gridlabd.command('--redirect')
    # gridlabd.command('all')

    gridlabd.command("virtual_islanding_model.glm")
    gridlabd.start('wait')
    print('\n')
except Exception as e:
    sys.stderr.write(f'Unhandled Exception in run_gridlabd_main.py: {e}')
    sys.stderr.write(traceback.format_exc())
    raise e
