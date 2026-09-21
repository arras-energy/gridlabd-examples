# read_results.py
#
# Load output files
#

import sys
import os
import re
import math
import pandas as pd

result = []

print(f"Extracting results to {sys.argv[1]}/results.csv",file=sys.stderr,end="...")

try:
    os.unlink(f"{sys.argv[1]}/results.csv.gz")
except:
    pass
    
for file in sorted([x for x in os.listdir(sys.argv[1]) if x.endswith(".csv")]):
    df = pd.read_csv(f"{sys.argv[1]}/{file}",index_col=["timestamp"])
    df.columns = [".".join([file.replace(".csv",""),x]) for x in df.columns]
    result.append(df)

result = pd.concat(result,axis=1).stack(level=0).to_frame("value")

result.drop(result[result.value=="+0+0j"].index,inplace=True)

def to_complex(z):
    _float_re = r"[+-]?(?:\d+\.\d*|\.\d+|\d+)(?:[eE][+-]?\d+)?"
    try:
        match z[-1]:
            case "i":
                r,i = map(float,re.match(f"({_float_re})({_float_re})i", z).groups())
                return complex(r,i)
            case "j":
                r,i = map(float,re.match(f"({_float_re})({_float_re})j", z).groups())
                return complex(r,i)
            case "r":
                m, a = map(float,re.match(f"({_float_re})({_float_re})r", z).groups())
                return complex(m * math.cos(a), m * math.sin(a))
            case "d":
                m, a = map(float,re.match(f"({_float_re})({_float_re})d", z).groups())
                a *= math.pi / 180.0
                return complex(m * math.cos(a), m * math.sin(a))
            case _:
                raise ValueError("invalid gridlabd complex")
    except Exception as err:
        print(f"{z=} not a valid complex")
        raise
        return complex(0, 0)

result.value = [to_complex(x) for x in result.value]

result.to_csv(f"{sys.argv[1]}/results.csv.gz",header=True,index=True,compression="gzip")

print("done",file=sys.stderr)
