import sys
sys.dont_write_bytecode = True
import os
import pandas as pd
import flet as ft
import joblib
import sqlite3
import duckdb
import tinydb
from tinydb import TinyDB
from ulid import ULID
import timeflake
import save_results as sr

# from simpledt import DataFrame
# import plotly.express as px


def calc_PSC_LCC(final_inputs):
    # final_inputs = joblib.load('final_inputs.joblib')

    shisetsu_seibi_total = float(final_inputs["shisetsu_seibi"])
    ijikanri_unnei_total = float(final_inputs["ijikanri_unnei"]) * (
        int(final_inputs["proj_years"]) - int(final_inputs["const_years"])
    )
    hojokin_kan = shisetsu_seibi_total * (float(final_inputs["hojo"]) / 100)
    if final_inputs["mgmt_type"] == "国":
        hojokin_kan = 0
    ribarai_kan = (
        (shisetsu_seibi_total - hojokin_kan)
        * float(final_inputs["kisai_jutou"])
        / 100
        * (1 - float(final_inputs["kisai_koufu"]) / 100)
        * float(final_inputs["chisai_kinri"])
    )
    if final_inputs["mgmt_type"] == "国":
        ribarai_kan = 0
    koufukin_kan = (
        (shisetsu_seibi_total - hojokin_kan)
        * float(final_inputs["kisai_jutou"])
        / 100
        * float(final_inputs["kisai_koufu"])
        / 100
    )

    shisetsu_seibi_reduc_total = shisetsu_seibi_total * (
        1 - float(final_inputs["reduc_shisetsu"]) / 100
    )
    ijikanri_unnei_reduc_total = ijikanri_unnei_total * (
        1 - float(final_inputs["reduc_ijikanri"]) / 100
    )

    shihon_hiritsu = 0.1
    SPC_capital = (shisetsu_seibi_reduc_total + ijikanri_unnei_reduc_total) * shihon_hiritsu
    SPC_yobihi = (shisetsu_seibi_reduc_total + ijikanri_unnei_reduc_total) * 0.1
    SPC_keihi_total = float(final_inputs["SPC_keihi"]) * int(final_inputs["proj_years"])
    if SPC_keihi_total == 0:
        SPC_capital = SPC_yobihi = 0
    hojokin_min = (shisetsu_seibi_reduc_total) * (float(final_inputs["hojo"]) / 100)
    ribarai_min = (
        (
            (
                (shisetsu_seibi_reduc_total - hojokin_min)
                * (1 - float(final_inputs["kisai_jutou"]) / 100)
            )
            + (SPC_capital + SPC_yobihi)
        )
        * (float(final_inputs["kijun_kinri"]) + float(final_inputs["lg_spread"]))
        / 100
    )
    ribarai_min_chisai = (
        (shisetsu_seibi_reduc_total - hojokin_min)
        * (float(final_inputs["kisai_jutou"]) / 100)
        * (1 - float(final_inputs["kisai_koufu"]) / 100)
        * float(final_inputs["chisai_kinri"])
    )
    koufukin_min = (
        (shisetsu_seibi_reduc_total - hojokin_min)
        * (float(final_inputs["kisai_jutou"]) / 100)
        * float(final_inputs["kisai_koufu"])
        / 100
    )

    ribarai_kanmin_sa = ribarai_min - ribarai_kan

    kappu_genka_s = (
        shisetsu_seibi_reduc_total
        + ijikanri_unnei_reduc_total
        + ribarai_min
        + SPC_capital
        + SPC_yobihi
        + SPC_keihi_total
    ) / (1 - float(final_inputs["zeimae_rieki"]) / 100)
    zeimae_rieki_gaku = kappu_genka_s * float(final_inputs["zeimae_rieki"]) / 100
    nouzei_gaku = zeimae_rieki_gaku * float(final_inputs["zei_total"]) / 100
    zeigo_rieki_gaku = zeimae_rieki_gaku - nouzei_gaku

    zei_modori_gaku = zeimae_rieki_gaku * float(final_inputs["zei_modori"]) / 100

    PSC_income_total = float(hojokin_kan + koufukin_kan)
    PSC_expense_total = float(
        shisetsu_seibi_total
        + ijikanri_unnei_total
        + ribarai_kan
        + ribarai_kanmin_sa
        + SPC_capital
        + SPC_yobihi
        + SPC_keihi_total
    )
    PSC_net_expense = float(PSC_expense_total - PSC_income_total)

    LCC_income_total = float(hojokin_min + koufukin_min + zei_modori_gaku)
    LCC_expense_total = float(
        shisetsu_seibi_reduc_total
        + ijikanri_unnei_reduc_total
        + ribarai_min
        + ribarai_min_chisai
        + zeimae_rieki_gaku
        + SPC_capital
        + SPC_yobihi
        + SPC_keihi_total
    )
    LCC_net_expense = float(LCC_expense_total - LCC_income_total)

    discount_rate = float(final_inputs["kijun_kinri"]) + float(
        final_inputs["kitai_bukka"]
    )

    ijikanri_years = int(final_inputs["proj_years"]) - int(final_inputs["const_years"])

    rakusatsu_ritsu = 0.95

    PSC_const_rate = shisetsu_seibi_total / (
        shisetsu_seibi_total + ijikanri_unnei_total
    )
    PSC_ijikanri_rate = ijikanri_unnei_total / (
        shisetsu_seibi_total + ijikanri_unnei_total
    )

    risk_adj_koufu = (
        ribarai_kanmin_sa + SPC_capital + SPC_keihi_total + SPC_yobihi - koufukin_kan
    )
    risk_adj_koufu_const = risk_adj_koufu * PSC_const_rate
    risk_adj_koufu_ijikanri = risk_adj_koufu * PSC_ijikanri_rate

    PSC_net_expense_const_kk = (
        risk_adj_koufu_const + shisetsu_seibi_total + ribarai_kan - hojokin_kan
    ) * rakusatsu_ritsu
    PSC_net_expense_ijikanri_kk = (
        risk_adj_koufu_ijikanri + ijikanri_unnei_total
    ) * rakusatsu_ritsu

    res_PSC_LCC = {
        "LCC_net_expense": LCC_net_expense,
        "PSC_net_expense_const_kk": PSC_net_expense_const_kk,
        "PSC_net_expense_ijikanri_kk": PSC_net_expense_ijikanri_kk,
        "proj_years": int(final_inputs["proj_years"]),
        "const_years": int(final_inputs["const_years"]),
        "ijikanri_years": ijikanri_years,
        "discount_rate": discount_rate,
        "rakusatsu_ritsu": rakusatsu_ritsu,
    }

    #joblib.dump(res_PSC_LCC, "res_PSC_LCC.joblib")
    return res_PSC_LCC


# class VFM:
def calc_VFM(res_PSC_LCC):
    # res_PSC_LCC = joblib.load('res_PSC_LCC.joblib')

    LCC_net_expense = float(res_PSC_LCC["LCC_net_expense"])
    PSC_net_expense_const_kk = float(res_PSC_LCC["PSC_net_expense_const_kk"])
    PSC_net_expense_ijikanri_kk = float(res_PSC_LCC["PSC_net_expense_ijikanri_kk"])
    proj_years = int(res_PSC_LCC["proj_years"])
    const_years = int(res_PSC_LCC["const_years"])
    ijikanri_years = int(res_PSC_LCC["ijikanri_years"])
    discount_rate = float(res_PSC_LCC["discount_rate"]) / 100

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

    sr.save_ddb(results, results_2)    #joblib.dump(results, "results.joblib")
