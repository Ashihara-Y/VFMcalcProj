import sys

sys.dont_write_bytecode = True
import os
import save_results as sr
import PSC_calc, LCC_calc, SPC_calc
import make_present_value, risk_adjustment, check_SPC_cashForPPayment, save_results, view_saved


def VFM_calc():

    PSC_calc()
    LCC_calc()
    SPC_calc()
    risk_adjustment()
    make_present_value()
    check_SPC_cashForPPayment()
    save_results.addID()
    save_results.save_ddb()
    view_saved.View_saved()
    



if __name__ == "__main__":
    VFM_calc()
