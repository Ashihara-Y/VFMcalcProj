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
    ijikanri_unnei_years = proj_years - const_years

    mgmt_type = "市町村"
    proj_type = "BTO/DBO/RO"

    const_start_date = datetime.date.today()

    shisetsu_seibi = 3000.0
    ijikanri_unnei = 50.0

    reduc_shisetsu = 5.0/100
    reduc_ijikanri = 5.0/100

    zei_total = 41.98/100
    lg_spread = 1.5/100
    growth = 0.0
    zeimae_rieki = 8.5/100
    SPC_keihi = 15.0
    SPC_shihon = 100.0
    SPC_yobihi = 100.0

    if mgmt_type == "国":
        zei_modori = 27.8/100
        hojo = 0.0
        kisai_jutou = 0.0
        kisai_koufu = 0.0
    elif mgmt_type == "都道府県":
        zei_modori = 5.78/100
        hojo = 50.0/100
        kisai_jutou = 75.0/100
        kisai_koufu = 30.0/100
    elif mgmt_type == "市町村":
        zei_modori = 8.4/100
        hojo = 30.0/100
        kisai_jutou = 75.0/100
        kisai_koufu = 30.0/100
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
    kijun_kinri = r1 / 100
    chisai_kinri = r2 / 100

    # 地方債の償還期限を、事業期間と同じにしてあるが、別途設定する必要がある。
    chisai_sueoki_years = const_years
    chisai_shoukan_kikan = proj_years - const_years

    kitai_bukka_j = (
        pd.read_csv("BOJ_ExpInflRate_down.csv", encoding="shift-jis", skiprows=1)
        .dropna()
        .iloc[-1, 1]
    )
    gonensai_rimawari = JGB_rates_df.loc["5年"].iloc[0]
    # gonensai_rimawari = pd.read_csv('JGB_rates.csv', sep='\t', encoding='utf-8', header=None).iloc[0,-1]
    kitai_bukka = (kitai_bukka_j - gonensai_rimawari) / 100

    shisetsu_seibi_paymentschedule_ikkatsu = 0.5
    shisetsu_seibi_paymentschedule_kappu = 1- shisetsu_seibi_paymentschedule_ikkatsu

    rakusatsu_ritsu = 0.95

    kouritsusei_shisetsu_seibi = 0.05
    kouritsusei_ijikanri_unnei = 0.05

    advisory_fee = 25.0
    monitoring_costs_PSC = 10.0
    monitoring_costs_LCC = 6.0

    SPC_hiyou_atsukai = 1  # 1: サービス購入費として支払い　0:割賦金利に含めて支払い

    kappu_kinri_spread = 1.0 / 100

    kyoukouka_yosantanka_hiritsu = (
        1.0  # 施設整備費全額が予算単価からの積み上げと設定。進めるための仮の設定
    )

    pre_kyoukouka = True
    proj_ctgry = "サービス購入型"

    shisetsu_seibi_org = shisetsu_seibi
    ijikanri_unnei_org = ijikanri_unnei

    if pre_kyoukouka == True:
        shisetsu_seibi_yosantanka = shisetsu_seibi * kyoukouka_yosantanka_hiritsu
        shisetsu_seibi_rakusatsu = shisetsu_seibi - shisetsu_seibi_yosantanka
        shisetsu_seibi = (
            shisetsu_seibi_yosantanka * rakusatsu_ritsu + shisetsu_seibi_rakusatsu
        )

        ijikanri_unnei_yosantanka = ijikanri_unnei * kyoukouka_yosantanka_hiritsu
        ijikanri_unnei_rakusatsu = ijikanri_unnei - ijikanri_unnei_yosantanka
        ijikanri_unnei = (
            ijikanri_unnei_yosantanka * rakusatsu_ritsu + ijikanri_unnei_rakusatsu
        )

    # 期待される効率性を考慮
    shisetsu_seibi_LCC = shisetsu_seibi * kouritsusei_shisetsu_seibi
    ijikanri_unnei_LCC = ijikanri_unnei * kouritsusei_ijikanri_unnei

    # 期待される効率性を考慮（競争の効果反映なし版）
    shisetsu_seibi_org_LCC = shisetsu_seibi_org * kouritsusei_shisetsu_seibi
    ijikanri_unnei_org_LCC = ijikanri_unnei_org * kouritsusei_ijikanri_unnei

    if proj_ctgry == "サービス購入型":
        riyouryoukin_shunyu = 0

    # SPC_keihi_etc_atsukai = 1 # 1: サービス購入費として支払い　0:割賦金利に含めて支払い

    inputs_dict = {
        "advisory_fee": float(advisory_fee),
        "chisai_kinri": float(chisai_kinri),
        "chisai_shoukan_kikan": int(chisai_shoukan_kikan),
        "chisai_sueoki_years": int(chisai_sueoki_years),
        "const_years": int(const_years),
        "const_start_date": str(const_start_date),
        "growth": float(growth),
        "hojo": float(hojo),
        "ijikanri_unnei": float(ijikanri_unnei),
       "ijikanri_unnei_LCC": float(ijikanri_unnei_LCC), 
        "ijikanri_unnei_org": float(ijikanri_unnei_org),
        "ijikanri_unnei_org_LCC": float(ijikanri_unnei_org_LCC),
        "ijikanri_unnei_years": int(ijikanri_unnei_years),
        "kappu_kinri_spread": float(kappu_kinri_spread),
        "kijun_kinri": float(kijun_kinri),
        "kisai_jutou": float(kisai_jutou),
        "kisai_koufu": float(kisai_koufu),
        "kitai_bukka": float(kitai_bukka),
        "kyoukouka_yosantanka_hiritsu": float(kyoukouka_yosantanka_hiritsu),
        "lg_spread": float(lg_spread),
        "mgmt_type": str(mgmt_type),
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
        "shisetsu_seibi_LCC": float(shisetsu_seibi_LCC),
        "shisetsu_seibi_org": float(shisetsu_seibi_org),
        "shisetsu_seibi_org_LCC": float(shisetsu_seibi_org_LCC),
        "shisetsu_seibi_paymentschedule_ikkatsu": float(
            shisetsu_seibi_paymentschedule_ikkatsu
        ),
        "shisetsu_seibi_paymentschedule_kappu": float(
            shisetsu_seibi_paymentschedule_kappu
        ),
        "SPC_hiyou_atsukai": int(SPC_hiyou_atsukai),
        "SPC_keihi": float(SPC_keihi),
        "SPC_shihon": float(SPC_shihon),
        "SPC_yobihi": float(SPC_yobihi),
        "zei_modori": float(zei_modori),
        "zei_total": float(zei_total),
        "zeimae_rieki": float(zeimae_rieki),
    }

    if os.path.exists("inputs_db.json"):
        os.remove("inputs_db.json")
    db = TinyDB("inputs_db.json")
    db.insert(inputs_dict)
    db.close()
    # self.page.go("/final_inputs")
    return inputs_dict


def VFM_calc():

    db = TinyDB("inputs_db.json")
    inputs = db.all()[0]

    start_year = datetime.datetime.strptime(inputs["const_start_date"], "%Y-%m-%d").year
    start_month = datetime.datetime.strptime(
        inputs["const_start_date"], "%Y-%m-%d"
    ).month
    if start_month < 4:
        first_end_fy = datetime.date(start_year, 3, 31)
    else:
        first_end_fy = datetime.date(start_year + 1, 3, 31)

    discount_rate = inputs["kijun_kinri"] + inputs["kitai_bukka"]
    proj_years = inputs["proj_years"]
    const_years = inputs["const_years"]
    ijikanri_years = proj_years - const_years
    target_years = const_years + inputs["chisai_sueoki_years"] + inputs["chisai_shoukan_kikan"]
    shokan_kaishi_jiki = const_years + inputs["chisai_sueoki_years"] + 1

    schedule = [
        first_end_fy.replace(year=first_end_fy.year + i) for i in range(0, proj_years)
    ]  # 各年度の末日

    discount_factor = [
        1 / (1 + discount_rate) ** i for i in range(0, target_years)
    ]  # 割引係数

    def PSC():
        # PSC shuushi income
        hojokin = [0 for i in range(target_years)]
        kouhukin = [0 for i in range(target_years)]
        kisai_gaku = [0 for i in range(target_years)]
        riyou_ryoukin = [0 for i in range(target_years)]

        for i in range(1, proj_years + 1):
            if i == const_years:
                j = i - 1
                hojokin[j] = (inputs["hojo"] / 100) * inputs[
                # hojokin[j] = (inputs["hojo"]) * inputs[
                    "shisetsu_seibi"
                ]  # 投資への補助金
                kisai_gaku[j] = (inputs["kisai_jutou"] / 100) * (
                # kisai_gaku[j] = (inputs["kisai_jutou"]) * (
                    inputs["shisetsu_seibi"] - hojokin[j]
                )  # 地方債起債額
                kouhukin[j] = kisai_gaku[j] * (
                    inputs["kisai_koufu"] / 100
                    # inputs["kisai_koufu"]
                )  #  起債への交付金額
            else:
                pass

        # PSC shuushi payments
        shisetsu_seibihi = [0 for i in range(target_years)]
        ijikanri_unneihi = [0 for i in range(target_years)]
        monitoring_costs = [inputs["monitoring_costs_PSC"]  for i in range(target_years)]
        kisai_shokan_gaku = [0 for i in range(proj_years)]
        kisai_risoku_gaku = [0 for i in range(proj_years)]
        kisai_zansai = [0 for i in range(proj_years)]

        kisai_gaku_sclr = (inputs["kisai_jutou"] / 100) * inputs["shisetsu_seibi"]
        # kisai_gaku_sclr = (inputs["kisai_jutou"]) * inputs["shisetsu_seibi"]
        chisai_ganpon_shokan_gaku = kisai_gaku_sclr / inputs["chisai_shokan_kikan"]

        for i in range(1, proj_years + 1):
            if i < const_years:
                pass
            elif i == const_years:
                j = i - 1
                shisetsu_seibihi[j] = inputs["shisetsu_seibi"]
            elif i > const_years:
                j = i - 1
                chisai_ganpon_shokansumi_gaku = 0
                ijikanri_unneihi[j] = inputs["ijikanri_unnei"]
                # kisai_zansai_sclr = kisai_gaku_sclr - chisai_ganpon_shokansumi_gaku
                if (
                    shokan_kaishi_jiki > i
                    and kisai_gaku_sclr > 0
                    and kisai_zansai_sclr > 0
                ):
                    chisai_ganpon_shokansumi_gaku += 0
                    kisai_zansai_sclr = kisai_gaku_sclr - chisai_ganpon_shokansumi_gaku
                    kisai_risoku_gaku[j] = kisai_zansai_sclr * (
                        inputs["chisai_kinri"] / 100
                        # inputs["chisai_kinri"]
                    )
                elif (
                    shokan_kaishi_jiki <= i
                    and kisai_gaku_sclr > 0
                    and kisai_zansai_sclr > 0
                ):
                    kisai_shokan_gaku[j] = chisai_ganpon_shokan_gaku
                    chisai_ganpon_shokansumi_gaku = chisai_ganpon_shokan_gaku * (
                        i - (shokan_kaishi_jiki - 1)
                    )
                    kisai_zansai_sclr = kisai_gaku_sclr - chisai_ganpon_shokansumi_gaku
                    kisai_zansai[j] = kisai_zansai_sclr
                    kisai_risoku_gaku[j] = kisai_zansai_sclr * (
                        inputs["chisai_kinri"] / 100
                        # inputs["chisai_kinri"]
                    )
                else:
                    pass
            else:
                pass

        # PSC incomes, paymentsそれぞれをDFにして、横にマージして、収支を出す。
        PSC_incomes = {
            "hojokin": hojokin,
            "kouhukin": kouhukin,
            "kisai_gaku": kisai_gaku,
            "riyou_ryoukin": riyou_ryoukin,
        }
        PSC_incomes_df = pd.DataFrame(PSC_incomes)
        PSC_incomes_df["incomes_total"] = (
            PSC_incomes_df["hojokin"]
            + PSC_incomes_df["kouhukin"]
            + PSC_incomes_df["kisai_gaku"]
            + PSC_incomes_df["riyou_ryoukin"]
        )

        PSC_payments = {
            "shisetsu_seibihi": shisetsu_seibihi,
            "ijikanri_unneihi": ijikanri_unneihi,
            "monitoring_costs": monitoring_costs,
            "kisai_shokan_gaku": kisai_shokan_gaku,
            "kisai_risoku_gaku": kisai_risoku_gaku,
        }
        PSC_payments_df = pd.DataFrame(PSC_payments)
        PSC_payments_df["payments_total"] = (
            PSC_payments_df["shisetsu_seibihi"]
            + PSC_payments_df["ijikanri_unneihi"]
            + PSC_payments_df["monitoring_costs"]
            + PSC_payments_df["kisai_shokan_gaku"]
            + PSC_payments_df["kisai_risoku_gaku"]
        )

        Schedule = pd.DataFrame(schedule, columns=["schedule"])
        PSC = pd.concat([Schedule, PSC_incomes_df, PSC_payments_df], axis=1)
        PSC["kisai_zansai"] = pd.DataFrame(kisai_zansai)
        PSC["net_payments"] = (
            PSC_incomes_df["payments_total"] - PSC_payments_df["incomes_total"]
        )

        # 官民利払い費用の差とSPC経費の合計を「リスク調整額」とし、それをPSC_balanceに加える。
        # ただし、官民利払い費用の差は、金利差に「サービス対価の割賦元本分」をかけることで算出する。このため、LCCの計算が先に必要。
        # その後、PSC_balanceをdiscount_factorで現在価値化して、総額を出す。
        # その結果を競争の効果反映済のPSCとする。
        #    kanmin_ribarai_sa = [0 for i in range(proj_years)]
        #    kanmin_ribarai_sa_df = pd.DataFrame(kanmin_ribarai_sa)
        #    risk_chousei_gaku = kanmin_ribarai_sa_df.sum() + (inputs["SPC_keihi"] * proj_years) + inputs["SPC_shihon"] + inputs["SPC_yobihi"]

        return PSC

    def LCC():
        # LCC shuushi incomes
        hojokin = [0 for i in range(proj_years)]
        kouhukin = [0 for i in range(proj_years)]
        kisai_gaku = [0 for i in range(proj_years)]
        zeishu = [0 for i in range(proj_years)]

        # LCC shuushi payments
        shiseki_seibihi_servicetaika_ikkatsu = [0 for i in range(proj_years)]
        shiseki_seibihi_servicetaika_kappuganpon = [0 for i in range(proj_years)]
        shiseki_seibihi_servicetaika_kappukinri = [0 for i in range(proj_years)]
        ijikannri_unneihi_servicetaika = [0 for i in range(proj_years)]
        monitoring_costs = [0 for i in range(proj_years)]
        SPC_hiyou = [0 for i in range(proj_years)]
        kisai_shoukan_gaku = [0 for i in range(proj_years)]
        kisai_risoku_gaku = [0 for i in range(proj_years)]

        return LCC

    def SPC():
        # SPC shuushi incomes
        shiseki_seibihi_servicetaika_ikkatsu = [0 for i in range(proj_years)]
        shiseki_seibihi_servicetaika_kappuganpon = [0 for i in range(proj_years)]
        shiseki_seibihi_servicetaika_kappukinri = [0 for i in range(proj_years)]
        ijikannri_unneihi_servicetaika = [0 for i in range(proj_years)]
        SPC_hiyou_servicetaika = [0 for i in range(proj_years)]
        riyou_ryoukin = [0 for i in range(proj_years)]

        # SPC shuushi payments
        shisetsu_seibihi = [0 for i in range(proj_years)]
        ijikannri_unneihii = [0 for i in range(proj_years)]
        shiharai_risoku = [0 for i in range(proj_years)]
        SPC_setsuritsuhi = [0 for i in range(proj_years)]
        houjinzei_etc = [0 for i in range(proj_years)]
        kariire_ganpon_hensai = [0 for i in range(proj_years)]

        return SPC


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
