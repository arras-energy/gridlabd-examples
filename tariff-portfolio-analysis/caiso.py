"""Download CAISO data for specified year and node"""
import os,sys
year = int(sys.argv[1])
node = sys.argv[2]
for month in range(1,13):
    file = f"CAISO-{node}-{year}{month:02d}.csv"
    if not os.path.exists(file):
        print(f'downloading {file} CAISO...',file=sys.stderr)
        try:
            os.system(f"gridlabd market_data -m=CAISO -d={node} -s={year}{month:02d}01 -e={year+int(month/12)}{(month)%12+1:02d}01 > {file}")
        except:
            os.remove(file)
            e_type,e_value,e_trace = sys.exc_info()
            print(f'ERROR [{__name__}]: download of {file} from CAISO failed ({e_type.__name__} {e_value})',file=sys.stderr)
    sys.stderr.flush()
