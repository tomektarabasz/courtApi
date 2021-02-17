from excel_to_db.mongo_modyfication import tt
import time
start= time.perf_counter()
tt()
dif = time.perf_counter() - start
print("This is time = {}".format(dif))