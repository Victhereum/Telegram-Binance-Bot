# regex pattern to extract futures-order information
futures_pattern =r"(\w+)\/(\w+)\s*(LONG|SHORT)\s*🛑\s*Leverage\s*(\d+x)\s*Entries\s*(\d+\.\d+)\s*Target\s*1\s*(\d+\.\d+)\s*Target\s*2\s*(\d+\.\d+)\s*Target\s*3\s*(\d+\.\d+)\s*Target\s*4\s*(\d+\.\d+)\s*Target\s*5\s*(\d+\.\d+)\s*SL\s*(\d+\.\d+)"

# regex pattern to extract spot-order information
spot_pattern  = r"\$(\w+)\/(\w+)[\s\S]+?Buy Price\s+:\s+([\d.]+)"

scientific_pattern = r'^[-+]?[0-9]*\.?[0-9]+[eE][-+]?[0-9]+$'
