from utils.gmoApi import (
    getStatus,
    getPrice,
    gmoOrder,
    gmoCancel,
)
import pickle
import time

path = "research/models/"
model_rforest = pickle.load(open(path+"rforest_test.sav", "rb"))

def main() :
    while True :
        time.sleep(1)
        res = getPrice("BTC")
        print(res)

if __name__ == "__main__" :
    main()