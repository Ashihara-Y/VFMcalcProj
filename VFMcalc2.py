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

def __init__(self):
        super().__init__()
        self.title = "最終入力"
        self.width = 500
        self.height = 1000
        self.resizable = True

        db = TinyDB("ii_db.json")
        self.initial_inputs = db.all()[0]


initial_inputs = {
            "mgmt_type": self.dd1.value,
            "proj_ctgry": self.dd2.value,
            "proj_type": self.dd3.value,
            "proj_years": self.dd4.value,
            "const_years": self.dd5.value,
            "kijun_kinri": r1,
            "chisai_kinri": r2,
            "zei_modori": float(zei_modori),
            "lg_spread": 1.5,
            "zei_total": 41.98,
            "growth": 0.0,
            "kitai_bukka": float(kitai_bukka),
            "shisetsu_seibi": 2000.0,
            "ijikanri_unnei": 50.0,
            "reduc_shisetsu": 10.0,
            "reduc_ijikanri": 10.0,
            "pre_kyoukouka": False,
            "kisai_jutou": float(kisai_jutou),
            "kisai_koufu": float(kisai_koufu),
            "zeimae_rieki": 8.5,
            "SPC_keihi": 15.0,
            "hojo": float(hojo),
        }

    final_inputs = {
            "mgmt_type": self.initial_inputs["mgmt_type"],
            "proj_ctgry": self.initial_inputs["proj_ctgry"],
            "proj_type": self.initial_inputs["proj_type"],
            "proj_years": int(self.initial_inputs["proj_years"]),
            "const_years": int(self.initial_inputs["const_years"]),
            "kijun_kinri": float(self.initial_inputs["kijun_kinri"]),
            "chisai_kinri": float(self.initial_inputs["chisai_kinri"]),
            "zei_modori": float(self.initial_inputs["zei_modori"]),
            "lg_spread": float(self.initial_inputs["lg_spread"]),
            "zei_total": float(self.initial_inputs["zei_total"]),
            "growth": float(self.initial_inputs["growth"]),
            "kitai_bukka": float(self.initial_inputs["kitai_bukka"]),
            "shisetsu_seibi": float(self.sl3.value),
            "ijikanri_unnei": float(self.sl4.value),
            "reduc_shisetsu": float(self.sl5.value),
            "reduc_ijikanri": float(self.sl6.value),
            "pre_kyoukouka": bool(self.initial_inputs["pre_kyoukouka"]),
            "kisai_jutou": float(self.sl7.value),
            "kisai_koufu": float(self.sl8.value),
            "zeimae_rieki": float(self.initial_inputs["zeimae_rieki"]),
            "SPC_keihi": float(self.sl10.value),
            "hojo": float(self.sl9.value),
        }

        if os.path.exists("ii_db.json"):
            os.remove("ii_db.json")
        db = TinyDB('ii_db.json')
        db.insert(initial_inputs)
        db.close()
        self.page.go("/final_inputs")

            PSC_const = []
    PSC_ijikanri = []
    LCC = []

    for i in range(proj_years):
        LCC.append(LCC_net_expense / proj_years)

    for i in range(const_years):
        PSC_const.append(PSC_net_expense_const_kk / const_years)

    for i in range(ijikanri_years):
        PSC_ijikanri.append(PSC_net_expense_ijikanri_kk / ijikanri_years)

    df_LCC = pd.DataFrame(LCC, columns=["LCC_net_expense"])

    df_PSC_const = pd.DataFrame(PSC_const, columns=["PSC_net_expense_const"])
    df_PSC_ijikanri = pd.DataFrame(PSC_ijikanri, columns=["PSC_net_expense_iji"])

    # LCC
    LCC_discount_factor = [
        (1 / (1 + discount_rate)) ** i for i in range(1, proj_years + 1)
    ]
    df_LCC["LCC_discount_factor"] = LCC_discount_factor
    # calculate the present value of each cash flow
    df_LCC["LCC_present_value"] = (
        df_LCC["LCC_net_expense"] * df_LCC["LCC_discount_factor"]
    )
    # 成長率、NWC, CAPEXは、現時点で省略、今後のバージョンで追加予定

    # PSC
    PSC_const_discount_factor = [
        (1 / (1 - discount_rate)) ** i for i in reversed(range(const_years))
    ]
    PSC_iji_discount_factor = [
        (1 / (1 + discount_rate)) ** i for i in range(1, ijikanri_years + 1)
    ]
    df_PSC_const["PSC_const_discount_factor"] = PSC_const_discount_factor
    df_PSC_ijikanri["PSC_iji_discount_factor"] = PSC_iji_discount_factor
    df_PSC_const["PSC_const_present_value"] = (
        df_PSC_const["PSC_net_expense_const"]
        * df_PSC_const["PSC_const_discount_factor"]
    )
    df_PSC_ijikanri["PSC_iji_present_value"] = (
        df_PSC_ijikanri["PSC_net_expense_iji"]
        * df_PSC_ijikanri["PSC_iji_discount_factor"]
    )

    df_PSC = pd.concat(
        [
            df_PSC_const["PSC_const_present_value"],
            df_PSC_ijikanri["PSC_iji_present_value"],
        ]
    ).reset_index(drop=True)
    df_PSC.columns = ["PSC_present_value"]

    df_PV_cf = pd.concat([df_PSC, df_LCC["LCC_present_value"]], axis=1)
    df_PV_cf = df_PV_cf.set_axis(["PSC_present_value", "LCC_present_value"], axis=1)
    df_PV_cf['LCC_discount_factor'] = LCC_discount_factor
    PSC_discount_factor = PSC_const_discount_factor + PSC_iji_discount_factor
    df_PV_cf['PSC_discount_factor'] = PSC_discount_factor
    dic_PV_cf = df_PV_cf.to_dict()

    res_PSC_LCC_df = pd.DataFrame(res_PSC_LCC, index=[0])
    res_PSC_LCC_df = res_PSC_LCC_df.reindex(columns=[
        "LCC_net_expense",
        "PSC_net_expense_const_kk",
        "PSC_net_expense_ijikanri_kk",
        "ijikanri_years",
        "discount_rate",
        "rakusatsu_ritsu",
        ]
    )

    PSC = df_PV_cf["PSC_present_value"].sum()
    LCC = df_PV_cf["LCC_present_value"].sum()
    VFM = PSC - LCC
    VFM_percent = VFM / PSC * 100
    PSC_LCC_VFM_df = pd.DataFrame(
        {
            "PSC": PSC,
            "LCC": LCC,
            "VFM": VFM,
            "VFM_percent": VFM_percent,
        },
        index=[0],
    )

    results = {
        "LCC_net_expense": format(res_PSC_LCC['LCC_net_expense'], '.3f'),
        "PSC_net_expense_const_kk": format(res_PSC_LCC['PSC_net_expense_const_kk'], '.3f'),
        "PSC_net_expense_ijikanri_kk": format(res_PSC_LCC['PSC_net_expense_ijikanri_kk'], '.3f'),
        "ijikanri_years": res_PSC_LCC['ijikanri_years'],
        "discount_rate": format(res_PSC_LCC['discount_rate'], '.3f'),
        "rakusatsu_ritsu": res_PSC_LCC['rakusatsu_ritsu'],
        "PSC": format(PSC, '.3f'), #Float to DataFrame to SQLite
        "LCC": format(LCC, '.3f'), #Float to DataFrame to SQLite
        "VFM": format(VFM, '.3f'), #Float to DataFrame to SQLite
        "VFM_percent": format(VFM_percent, '.3f'), #Float to DataFrame to SQLite
    }

    results_2 =  dic_PV_cf

    return results, results_2
