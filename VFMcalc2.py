import sys

sys.dont_write_bytecode = True
import os
import save_results as sr
import PSC_calc
import LCC_calc
import SPC_calc
import make_present_value, risk_adjustment, check_SPC_cashForPPayment


def VFM_calc():

    PSC_calc.PSC_calc()
    LCC_calc.LCC_calc()
    SPC_calc.SPC_calc()
    risk_adjustment
    make_present_value
    check_SPC_cashForPPayment
    sr.Save_results.make_df()
    sr.Save_results.make_summary_add_ids()
    sr.Save_results.save_db()
    #view_saved.View_saved()
    



if __name__ == "__main__":
    VFM_calc()
