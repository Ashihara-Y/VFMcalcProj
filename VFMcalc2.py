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

def inputs():

    proj_years = 23
    const_years = 3
    mgmt_type = "国"

    const_start_date = datetime.date.today()

    if mgmt_type == "国":
        zei_modori = 27.8
        hojo = 0.0
        kisai_jutou = 0.0
        kisai_koufu = 0.0
    elif mgmt_type == "都道府県":
        zei_modori = 5.78
        hojo = 50.0
        kisai_jutou = 75.0
        kisai_koufu = 30.0
    elif mgmt_type == "市町村":
        zei_modori = 8.4
        hojo = 30.0
        kisai_jutou = 75.0
        kisai_koufu = 30.0
    else:
        pass

    JGB_rates_df = pd.read_csv(
        "JGB_rates.csv",
        sep="\t",
        encoding="utf-8",
        header=None,
        names=["year", "rate"],
    ).set_index("year")

    JRB_rates_df = pd.read_csv(
        "JRB_rates.csv",
        encoding="utf-8",
        sep='\t', 
        names=[0,1,2,3,4,5], 
        index_col=0)

    y, d = divmod(int(proj_years), 5)

    if d > 2:
        r_idx = str((y + 1) * 5) + "年"
    elif d <= 2:
        r_idx = str(y * 5) + "年"

    r1 = JGB_rates_df.loc[r_idx].iloc[0]

    r2 = JRB_rates_df.loc[proj_years][const_years]
    # 地方債の償還期限が、事業期間と同じにしてあるが、別途設定する必要がある。
    # 返済繰り延べ年数についても、変数として、Final_inputsに入れておいた方が良い。
    sueoki_years = const_years
    chihosai_shokankikan = proj_years

    kitai_bukka_j = (
        pd.read_csv("BOJ_ExpInflRate_down.csv", encoding="shift-jis", skiprows=1)
        .dropna()
        .iloc[-1, 1]
    )
    gonensai_rimawari = JGB_rates_df.loc["5年"].iloc[0]
    # gonensai_rimawari = pd.read_csv('JGB_rates.csv', sep='\t', encoding='utf-8', header=None).iloc[0,-1]
    kitai_bukka = kitai_bukka_j - gonensai_rimawari

    payment_schedule_ikkatsu = 0.5
    payment_schedule_kappu = 0.5

    rakusatsu_ritsu = 0.95

    monitoring_costs_PSC = 10.0
    monitoring_costs_LCC = 6.0

    SPC_hiyou_atsukai = 1 # 1: サービス購入費として支払い　0:割賦金利に含めて支払い 

    initial_inputs = {
        "mgmt_type": mgmt_type,
        "proj_ctgry": "サービス購入型",
        "proj_type": "BTO/DBO/RO",
        "proj_years": proj_years,
        "const_years": const_years,
        "kijun_kinri": r1,
        "chisai_kinri": r2,
        "zei_modori": float(zei_modori),
        "lg_spread": 1.5,
        "zei_total": 41.98,
        "growth": 0.0,
        "kitai_bukka": float(kitai_bukka),
        "shisetsu_seibi": 3000.0,
        "ijikanri_unnei": 50.0,
        "reduc_shisetsu": 10.0,
        "reduc_ijikanri": 10.0,
        "pre_kyoukouka": True,
        "kisai_jutou": float(kisai_jutou),
        "kisai_koufu": float(kisai_koufu),
        "zeimae_rieki": 8.5,
        "SPC_keihi": 15.0,
        "SPC_Capital": 100.0,
        "SPC_yobi": 100.0,
        "hojo": float(hojo),
    }

    kappu_kinri_spread = 1.0

    pre_kyoukouka_yosantanka = 1.0 # 施設整備費全額が予算単価からの積み上げと設定。進めるための仮の設定

    if initial_inputs["pre_kyoukouka"] == True:
        shisetsu_seibi_yosantanka = initial_inputs["shisetsu_seibi"] * pre_kyoukouka_yosantanka
        shisetsu_seibi_rakusatsu = initial_inputs["shisetsu_seibi"] - shisetsu_seibi_yosantanka
        ijikanri_unnei_yosantanka = initial_inputs["ijikanri_unnei"] * pre_kyoukouka_yosantanka
        ijikanri_unnei_rakusatsu = initial_inputs["ijikanri_unnei"] - ijikanri_unnei_yosantanka

    if initial_inputs["proj_ctgry"] == "サービス購入型": 
        riyouryoukin_shunyu = 0

    shisetsu_seibi_ikkatsu = 0.5
    shisetsu_seibi_kappu = 0.5

    SPC_keihi_etc_atsukai = 1 # 1: サービス購入費として支払い　0:割賦金利に含めて支払い

    inputs = {
        "mgmt_type": initial_inputs["mgmt_type"],
        "proj_ctgry": initial_inputs["proj_ctgry"],
        "proj_type": initial_inputs["proj_type"],
        "proj_years": int(initial_inputs["proj_years"]),
        "const_years": int(initial_inputs["const_years"]),
        "const_start_date": const_start_date,
        "kijun_kinri": float(initial_inputs["kijun_kinri"]),
        "chisai_kinri": float(initial_inputs["chisai_kinri"]),
        "zei_modori": float(initial_inputs["zei_modori"]),
        "lg_spread": float(initial_inputs["lg_spread"]),
        "zei_total": float(initial_inputs["zei_total"]),
        "growth": float(initial_inputs["growth"]),
        "kitai_bukka": float(initial_inputs["kitai_bukka"]),
        "shisetsu_seibi": float(initial_inputs["shisetsu_seibi"]),
        "shisetsu_seibi_yosantanka": float(shisetsu_seibi_yosantanka),
        "shisetsu_seibi_rakusatsu": float(shisetsu_seibi_rakusatsu),
        "ijikanri_unnei": float(initial_inputs["ijikanri_unnei"]),
        "ijikanri_unnei_yosantanka": float(ijikanri_unnei_yosantanka),
        "ijikanri_unnei_rakusatsu": float(ijikanri_unnei_rakusatsu),
        "reduc_shisetsu": float(initial_inputs["reduc_shisetsu"]),
        "reduc_ijikanri": float(initial_inputs["reduc_ijikanri"]),
        "pre_kyoukouka": bool(initial_inputs["pre_kyoukouka"]),
        "kisai_jutou": float(initial_inputs["kisai_jutou"]),
        "kisai_koufu": float(initial_inputs["kisai_koufu"]),
        "zeimae_rieki": float(initial_inputs["zeimae_rieki"]),
        "SPC_keihi": float(initial_inputs["SPC_keihi"]),
        "riyouryoukin_shunyu": float(riyouryoukin_shunyu),
        "kappu_kinri_spread": float(kappu_kinri_spread),
        "hojo": float(initial_inputs["hojo"]),
        "shisetsu_seibi_ikkatsu": float(shisetsu_seibi_ikkatsu),
        "shisetsu_seibi_kappu": float(shisetsu_seibi_kappu),
        "SPC_keihi_etc_atsukai": int(SPC_keihi_etc_atsukai),
    }

    #db = TinyDB("ii_db.json")
    #initial_inputs = db.all()[0]

    if os.path.exists("inputs_db.json"):
        os.remove("inputs_db.json")
    db = TinyDB('inputs_db.json')
    db.insert(inputs)
    db.close()
    #self.page.go("/final_inputs")
    return inputs

def VFM_calc(inputs):

    #db = TinyDB("inputs_db.json")
    #inputs = db.all()[0]

    start_year = inputs["const_start_date"].year
    start_month = inputs["const_start_date"].month
    if start_month < 4:
        first_end_fy = datetime.date(start_year, 3, 31)
    else:
        first_end_fy = datetime.date(start_year + 1, 3, 31)
    
    discount_rate = inputs["kijun_kinri"] + inputs["kitai_bukka"]
    proj_years = inputs["proj_years"]
    const_years = inputs["const_years"]
    ijikanri_years = proj_years - const_years

    schedule = [first_end_fy.replace(year=first_end_fy.year+i) for i in range(0, proj_years)] # 各年度の末日
    keika_nensuu = [int(x) for x in range(1, proj_years+1)] # 1〜40の整数定数 range(1, 41)で内包表記？
    #jigyou_kikan = [] # 施設整備期間、維持管理運営期間の２択
    discount_factor = [1/(1+discount_rate) ** i for i in range(0, proj_years)] # 割引係数

    # PSC shuushi
    hojokin = [0 for i in range(proj_years)]
    kouhukin = [0 for i in range(proj_years)]
    kisai_gaku = [0 for i in range(proj_years)]
    riyou_ryoukin = [0 for i in range(proj_years)]
    shiseki_seibihi = [0 for i in range(proj_years)]

    shisetsu_seibi_kyoukoukasumi = inputs["shisetsu_seibi_rakusatsu"] + (inputs["shisetsu_seibi_yosantanka "] * inputs["rakusaturitsu"])

    for i in range(1,proj_years+1):
    if i == const_years:
        hojokin[i] = 
        inputs["hojo"] * shisetsu_seibi_kyoukoukasumi

        kouhukin[i] =
        inputs["kisai_kouhu"] *
        (inputs["shisetsu_seibi"] * 
         inputs["kisai_jutou"])        

        kisai_gaku[i] = inputs["kisai_jutou"] * inputs["shisetsu_seibi"] # 設備投入額
    else:
        pass

    ijikannri_unneihi = [0 for i in range(proj_years)]
    monitoring_costs = [0 for i in range(proj_years)]
    kisai_shoukan_gaku = [0 for i in range(proj_years)]
    kisai_risoku_gaku = [0 for i in range(proj_years)]

    kanmin_ribarai_sa = [0 for i in range(proj_years)]
    risk_chousei_hi = [0 for i in range(proj_years)]

    # LCC shuushi
    hojokin = [0 for i in range(proj_years)]
    kouhukin = [0 for i in range(proj_years)]
    kisai_gaku = [0 for i in range(proj_years)]
    zeishu = [0 for i in range(proj_years)]
    shiseki_seibihi_servicetaika_ikkatsu = [0 for i in range(proj_years)]
    shiseki_seibihi_servicetaika_kappuganpon = [0 for i in range(proj_years)] 
    shiseki_seibihi_servicetaika_kappukinri = [0 for i in range(proj_years)]
    ijikannri_unneihi_servicetaika = [0 for i in range(proj_years)]
    monitoring_costs = [0 for i in range(proj_years)]
    SPC_hiyou = [0 for i in range(proj_years)]
    kisai_shoukan_gaku = [0 for i in range(proj_years)]
    kisai_risoku_gaku = [0 for i in range(proj_years)]

    # SPC shuushi
    shiseki_seibihi_servicetaika_ikkatsu = [0 for i in range(proj_years)]
    shiseki_seibihi_servicetaika_kappuganpon = [0 for i in range(proj_years)] 
    shiseki_seibihi_servicetaika_kappukinri = [0 for i in range(proj_years)]
    ijikannri_unneihi_servicetaika = [0 for i in range(proj_years)]
    SPC_hiyou_servicetaika = [0 for i in range(proj_years)]
    riyou_ryoukin = [0 for i in range(proj_years)]
    shisetsu_seibihi = [0 for i in range(proj_years)]
    ijikannri_unneihii = [0 for i in range(proj_years)]
    shiharai_risoku = [0 for i in range(proj_years)]
    SPC_setsuritsuhi = [0 for i in range(proj_years)]
    houjinzei_etc = [0 for i in range(proj_years)]
    kariire_ganpon_hensai = [0 for i in range(proj_years)]




    #PSC_const = []
    #PSC_ijikanri = []
    #LCC = []

    #proj_years = inputs["proj_years"]
    #const_years = inputs["const_years"]
    #ijikanri_years = proj_years - const_years 

    #discount_rate = inputs["kijun_kinri"] + inputs["kitai_bukka"]

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
