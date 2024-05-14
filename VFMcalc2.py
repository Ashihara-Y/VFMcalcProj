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
import scipy
from scipy import optimize


def inputs():

    proj_years = 23
    const_years = 3
    mgmt_type = "国"
    proj_type = "BTO/DBO/RO"

    const_start_date = datetime.date.today()

    shisetsu_seibi = 3000.0
    ijikanri_unnei = 50.0

    reduc_shisetsu = 5.0
    reduc_ijikanri = 5.0

    zei_total = 41.98
    lg_spread = 1.5
    growth = 0.0
    zeimae_rieki = 8.5
    SPC_keihi = 15.0
    SPC_capital = 100.0
    SPC_yobi = 100.0

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
        sep="\t",
        names=[0, 1, 2, 3, 4, 5],
        index_col=0,
    )

    y, d = divmod(int(proj_years), 5)

    if d > 2:
        r_idx = str((y + 1) * 5) + "年"
    elif d <= 2:
        r_idx = str(y * 5) + "年"

    r1 = JGB_rates_df.loc[r_idx].iloc[0]
    r2 = JRB_rates_df.loc[proj_years][const_years]
    kijun_kinri = r1
    chisai_kinri = r2

    # 地方債の償還期限が、事業期間と同じにしてあるが、別途設定する必要がある。
    # 返済繰り延べ年数についても、変数として、Final_inputsに入れておいた方が良い。
    sueoki_years = const_years
    chisai_shokan_kikan = proj_years

    kitai_bukka_j = (
        pd.read_csv("BOJ_ExpInflRate_down.csv", encoding="shift-jis", skiprows=1)
        .dropna()
        .iloc[-1, 1]
    )
    gonensai_rimawari = JGB_rates_df.loc["5年"].iloc[0]
    # gonensai_rimawari = pd.read_csv('JGB_rates.csv', sep='\t', encoding='utf-8', header=None).iloc[0,-1]
    kitai_bukka = kitai_bukka_j - gonensai_rimawari

    shisetsu_seibi_paymentschedule_ikkatsu = 0.5
    shisetsu_seibi_paymentschedule_kappu = 0.5

    rakusatsu_ritsu = 0.95

    monitoring_costs_PSC = 10.0
    monitoring_costs_LCC = 6.0

    SPC_hiyou_atsukai = 1  # 1: サービス購入費として支払い　0:割賦金利に含めて支払い

    kappu_kinri_spread = 1.0

    kyoukouka_yosantanka_hiritsu = (
        1.0  # 施設整備費全額が予算単価からの積み上げと設定。進めるための仮の設定
    )

    pre_kyoukouka = True
    proj_ctgry = "サービス購入型"

    if pre_kyoukouka == True:
        shisetsu_seibi_yosantanka = shisetsu_seibi * kyoukouka_yosantanka_hiritsu
        shisetsu_seibi_rakusatsu = shisetsu_seibi - shisetsu_seibi_yosantanka
        ijikanri_unnei_yosantanka = ijikanri_unnei * kyoukouka_yosantanka_hiritsu
        ijikanri_unnei_rakusatsu = ijikanri_unnei - ijikanri_unnei_yosantanka

    if proj_ctgry == "サービス購入型":
        riyouryoukin_shunyu = 0

    SPC_keihi_etc_atsukai = 1  # 1: サービス購入費として支払い　0:割賦金利に含めて支払い

    inputs = {
        "chisai_kinri": float(chisai_kinri),
        "chisai_shokan_kikan": int(chisai_shokan_kikan),
        "const_years": int(const_years),
        "const_start_date": const_start_date,
        "growth": float(growth),
        "hojo": float(hojo),
        "ijikanri_unnei": float(ijikanri_unnei),
        "ijikanri_unnei_yosantanka": float(ijikanri_unnei_yosantanka),
        "ijikanri_unnei_rakusatsu": float(ijikanri_unnei_rakusatsu),
        "kappu_kinri_spread": float(kappu_kinri_spread),
        "kijun_kinri": float(kijun_kinri),
        "kisai_jutou": float(kisai_jutou),
        "kisai_koufu": float(kisai_koufu),
        "kitai_bukka": float(kitai_bukka),
        "kyoukouka_yosantanka_hiritsu": float(kyoukouka_yosantanka_hiritsu),
        "lg_spread": float(lg_spread),
        "mgmt_type": mgmt_type,
        "monitoring_costs_LCC": float(monitoring_costs_LCC),
        "monitoring_costs_PSC": float(monitoring_costs_PSC),
        "pre_kyoukouka": bool(pre_kyoukouka),
        "proj_ctgry": str(proj_ctgry),
        "proj_type": str(proj_type),
        "proj_years": int(proj_years),
        "rakusatsu_ritsu": float(rakusatsu_ritsu),
        "reduc_shisetsu": float(reduc_shisetsu),
        "reduc_ijikanri": float(reduc_ijikanri),
        "riyouryoukin_shunyu": float(riyouryoukin_shunyu),
        "shisetsu_seibi": float(shisetsu_seibi),
        "shisetsu_seibi_yosantanka": float(shisetsu_seibi_yosantanka),
        "shisetsu_seibi_rakusatsu": float(shisetsu_seibi_rakusatsu),
        "shisetsu_seibi_paymentschedule_ikkatsu": float(
            shisetsu_seibi_paymentschedule_ikkatsu
        ),
        "shisetsu_seibi_paymentschedule_kappu": float(
            shisetsu_seibi_paymentschedule_kappu
        ),
        "SPC_hiyou_atsukai": int(SPC_hiyou_atsukai),
        "SPC_keihi": float(SPC_keihi),
        "SPC_keihi_etc_atsukai": int(SPC_keihi_etc_atsukai),
        "sueoki_years": int(sueoki_years),
        "zei_modori": float(zei_modori),
        "zei_total": float(zei_total),
        "zeimae_rieki": float(zeimae_rieki),
    }

    # db = TinyDB("ii_db.json")
    # initial_inputs = db.all()[0]

    if os.path.exists("inputs_db.json"):
        os.remove("inputs_db.json")
    db = TinyDB("inputs_db.json")
    db.insert(inputs)
    db.close()
    # self.page.go("/final_inputs")
    return inputs


def VFM_calc(inputs):

    # db = TinyDB("inputs_db.json")
    # inputs = db.all()[0]

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

    schedule = [
        first_end_fy.replace(year=first_end_fy.year + i) for i in range(0, proj_years)
    ]  # 各年度の末日
    keika_nensuu = [
        int(x) for x in range(1, proj_years + 1)
    ]  # 1〜40の整数定数 range(1, 41)で内包表記？
    # jigyou_kikan = [] # 施設整備期間、維持管理運営期間の２択
    discount_factor = [
        1 / (1 + discount_rate) ** i for i in range(0, proj_years)
    ]  # 割引係数
    shokan_kaishi_jiki = const_years + inputs["sueoki_years"] + 1

    # PSC shuushi income
    hojokin = [0 for i in range(proj_years)]
    kouhukin = [0 for i in range(proj_years)]
    kisai_gaku = [0 for i in range(proj_years)]
    riyou_ryoukin = [0 for i in range(proj_years)]

    for i in range(1, proj_years + 1):
        if i == const_years:
            hojokin[i] = inputs["hojo"] * inputs["shisetsu_seibi"]  # 投資への補助金
            kisai_gaku[i] = (
                inputs["kisai_jutou"] * inputs["shisetsu_seibi"]
            )  # 地方債起債額
            kouhukin[i] = kisai_gaku[i] * inputs["kisai_kouhu"]  #  起債への交付金額
        else:
            pass

    # PSC shuushi payments
    shisetsu_seibihi = [0 for i in range(proj_years)]
    ijikannri_unneihi = [0 for i in range(proj_years)]
    monitoring_costs = [inputs["monitoring_consts_psc"] for i in range(proj_years)]
    kisai_shokan_gaku = [0 for i in range(proj_years)]
    kisai_risoku_gaku = [0 for i in range(proj_years)]

    kisai_gaku = inputs["kisai_jutou"] * inputs["shisetsu_seibi"]
    chisai_ganpon_shokan_gaku = kisai_gaku / inputs["chisai_shokan_kikan"]

    for i in range(1, proj_years + 1):
        if i == const_years:
            shisetsu_seibihi[i] = inputs["shisetsu_seibi"]
        elif const_years < i:
            chisai_ganpon_shokansumi_gaku = chisai_ganpon_shokan_gaku * (
                i - const_years
            )
            ijikannri_unneihi[i] = inputs["ijikanri_unnei"]
            chisai_zansai = kisai_gaku - chisai_ganpon_shokansumi_gaku
            if shokan_kaishi_jiki <= i and kisai_gaku > 0 and chisai_zansai > 0:
                kisai_shokan_gaku[i] = chisai_ganpon_shokan_gaku
                kisai_risoku_gaku[i] = chisai_zansai * inputs["chisai_kinri"]
        else:
            pass

    # PSC income, paymentsそれぞれをDFにして、横にマージして、収支を出す。
    df_hojokin = pd.DataFrame(hojokin, columns=["hojokin"])
    df_kouhukin = pd.DataFrame(kouhukin, columns=["kouhukin"])
    df_kisai_gaku = pd.DataFrame(kisai_gaku, columns=["kisai_gaku"])
    df_riyou_ryoukin = pd.DataFrame(riyou_ryoukin, columns=["riyou_ryoukin"])
    PSC_income = pd.concat(
        [df_hojokin, df_kouhukin, df_kisai_gaku, df_riyou_ryoukin], axis=1
    )

    df_shisetsu_seibihi = pd.DataFrame(shisetsu_seibihi, columns=["shisetsu_seibihi"])
    df_ijikannri_unneihi = pd.DataFrame(
        ijikannri_unneihi, columns=["ijikannri_unneihi"]
    )
    df_monitoring_costs = pd.DataFrame(monitoring_costs, columns=["monitoring_costs"])
    df_kisai_shokan_gaku = pd.DataFrame(
        kisai_shokan_gaku, columns=["kisai_shokan_gaku"]
    )
    df_kisai_risoku_gaku = pd.DataFrame(
        kisai_risoku_gaku, columns=["kisai_risoku_gaku"]
    )
    PSC_payments = pd.concat(
        [
            df_shisetsu_seibihi,
            df_ijikannri_unneihi,
            df_monitoring_costs,
            df_kisai_shokan_gaku,
            df_kisai_risoku_gaku,
        ],
        axis=1,
    )

    PSC_balance = PSC_income - PSC_payments
    Schedule = pd.DataFrame(schedule, columns=["schedule"])
    PSC = pd.concat([Schedule, PSC_income, PSC_payments, PSC_balance], axis=1)

    kanmin_ribarai_sa = [0 for i in range(proj_years)]
    risk_chousei_gaku = [0 for i in range(proj_years)]

    if inputs["pre_kyoukouka"] == True and inputs["kyoukouka_yosantanka_hiritsu"] == 0:
        kyoukouka_hannei_hiritsu = 1.0
    elif inputs["pre_kyoukouka"] == True and inputs["kyoukouka_yosantanka_hiritsu"] > 0:
        kyoukouka_hannei_hiritsu = 1 - (1 - inputs["rakusatsu_ritsu"]) * (
            (inputs["shisetsu_seibi_yosantanka"] + inputs["ijikanri_unnei_yosantanka"])
            / (inputs["shisetsu_seibi"] + inputs["ijikanri_unnei"])
        )
    else:
        pass

    # 官民利払い費用の差とSPC経費の合計を「リスク調整額」とし、それをPSC_balanceに加える。
    # その後、PSC_balanceをdiscount_factorで現在価値化して、総額を出し、それにkyoukouka_hannei_hiritsuをかける。
    # その結果を競争の効果反映済のPSCとする。

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

    # PSC_const = []
    # PSC_ijikanri = []
    # LCC = []

    # proj_years = inputs["proj_years"]
    # const_years = inputs["const_years"]
    # ijikanri_years = proj_years - const_years

    # discount_rate = inputs["kijun_kinri"] + inputs["kitai_bukka"]


#    PSC = df_PV_cf["PSC_present_value"].sum()
#    LCC = df_PV_cf["LCC_present_value"].sum()
#    VFM = PSC - LCC
#    VFM_percent = VFM / PSC * 100
#    PSC_LCC_VFM_df = pd.DataFrame(
#        {
#            "PSC": PSC,
#            "LCC": LCC,
#            "VFM": VFM,
#            "VFM_percent": VFM_percent,
#        },
#        index=[0],
#    )

#    results = {
#        "LCC_net_expense": format(res_PSC_LCC['LCC_net_expense'], '.3f'),
#        "PSC_net_expense_const_kk": format(res_PSC_LCC['PSC_net_expense_const_kk'], '.3f'),
#        "PSC_net_expense_ijikanri_kk": format(res_PSC_LCC['PSC_net_expense_ijikanri_kk'], '.3f'),
#        "ijikanri_years": res_PSC_LCC['ijikanri_years'],
#        "discount_rate": format(res_PSC_LCC['discount_rate'], '.3f'),
#        "rakusatsu_ritsu": res_PSC_LCC['rakusatsu_ritsu'],
#        "PSC": format(PSC, '.3f'), #Float to DataFrame to SQLite
#        "LCC": format(LCC, '.3f'), #Float to DataFrame to SQLite
#        "VFM": format(VFM, '.3f'), #Float to DataFrame to SQLite
#        "VFM_percent": format(VFM_percent, '.3f'), #Float to DataFrame to SQLite
#    }

#    results_2 =  dic_PV_cf

#    return results, results_2
