import sys

sys.dont_write_bytecode = True
#import os
from tinydb import TinyDB, Query
import save_results as sr
import PSC_calc
import PSC_calc_DBO
import PSC_calc_BOT
import PSC_calc_BT
import LCC_calc
import LCC_calc_DBO
import LCC_calc_BOT
import LCC_calc_BT
import SPC_calc
import SPC_calc_DBO
import SPC_calc_BOT
import SPC_calc_BT
import make_present_value
import risk_adjustment
import risk_adjustment_DBO
import risk_adjustment_BOT
import risk_adjustment_BT
import check_SPC_cashForPPayment
import check_SPC_cashForPPayment_DBO
import check_SPC_cashForPPayment_BOT
import check_SPC_cashForPPayment_BT


def VFM_calc():
    db = TinyDB("fi_db.json")
    inputs = db.all()[0]

    proj_type = inputs['proj_type']

    if proj_type == "BTO":

        PSC_calc.PSC_calc()
        LCC_calc.LCC_calc()
        SPC_calc.SPC_calc()
        risk_adjustment.risk_adj()
        make_present_value.make_pv()
        check_SPC_cashForPPayment.check_cash()
        sr.make_df_addID_saveDB()
    
    if proj_type == "DBO(SPCなし)":

        PSC_calc_DBO.PSC_calc()
        LCC_calc_DBO.LCC_calc()
        SPC_calc_DBO.SPC_calc()
        risk_adjustment_DBO.risk_adj()
        make_present_value.make_pv()
        check_SPC_cashForPPayment_DBO.check_cash()
        sr.make_df_addID_saveDB()
    
    if proj_type == "BOT/BOO":

        PSC_calc_BOT.PSC_calc()
        LCC_calc_BOT.LCC_calc()
        SPC_calc_BOT.SPC_calc()
        risk_adjustment_BOT.risk_adj()
        make_present_value.make_pv()
        check_SPC_cashForPPayment_BOT.check_cash()
        sr.make_df_addID_saveDB()
    
    elif proj_type == "BT/DB(いずれもSPCなし)":
        PSC_calc_BT.PSC_calc()
        LCC_calc_BT.LCC_calc()
        SPC_calc_BT.SPC_calc()        
        risk_adjustment_BT.risk_adj()
        make_present_value.make_pv()
        check_SPC_cashForPPayment_BT.check_cash()
        sr.make_df_addID_saveDB()


if __name__ == "__main__":
    VFM_calc()
