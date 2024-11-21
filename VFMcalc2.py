import sys

sys.dont_write_bytecode = True
import os
import pandas as pd
import flet as ft
import tinydb
from tinydb import TinyDB
from ulid import ULID
import timeflake
import save_results as sr
import datetime
import dateutils
import pyxirr
import PSC_calc, LCC_calc, SPC_calc
import make_present_value, risk_adjustment, check_SPC_cashForPPayment, save_results


def VFM_calc():

    PSC_calc()
    LCC_calc()
    SPC_calc()
    risk_adjustment()
    make_present_value()
    check_SPC_cashForPPayment()
    save_results()



if __name__ == "__main__":
    VFM_calc()
