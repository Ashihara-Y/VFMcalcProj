import pandas as pd
#import duckdb
from dataclasses import asdict, dataclass
from decimal import *
from pydantic import BaseModel
#import openpyxl
from collections import deque
import make_inputs_df
from sqlalchemy import create_engine, DECIMAL

engine = create_engine('sqlite:///VFM.db', echo=False)


#conn = duckdb.connect('VFM.duckdb')
#c = conn.cursor()
def risk_adj():
    inputs_pdt = make_inputs_df.main()

    LCC_kappuganpon_df = pd.read_sql_query("SELECT periods, shisetsu_seibihi_kappuganpon FROM LCC_table", engine)
    LCC_kappuganpon_df['shisetsu_seibihi_kappuganpon'] = LCC_kappuganpon_df['shisetsu_seibihi_kappuganpon'].map(lambda i: Decimal(i).quantize(Decimal('0.000001'), ROUND_HALF_UP))
    LCC_kappuganpon_df = LCC_kappuganpon_df.set_index('periods')
    LCC_kappuganpon_cumsum = LCC_kappuganpon_df.cumsum()
    LCC_kappuganpon_cumsum.loc[inputs_pdt.proj_years+1:, 'shisetsu_seibihi_kappuganpon'] = Decimal('0.000000')
    LCC_kappuganpon_cumsum_ls = LCC_kappuganpon_cumsum['shisetsu_seibihi_kappuganpon'].to_list()
    R = deque(LCC_kappuganpon_cumsum_ls)
    R.rotate(1)
    LCC_kappuganpon_cumsum_ls = list(R)

    SPC_SPCkeihi_SPCsetsuritsuhi_df = pd.read_sql_query("SELECT periods, SPC_keihi, SPC_setsuritsuhi FROM SPC_table",engine)
    periods = SPC_SPCkeihi_SPCsetsuritsuhi_df['periods'].to_list()
    SPC_SPCkeihi_SPCsetsuritsuhi_df['SPC_keihi'] = SPC_SPCkeihi_SPCsetsuritsuhi_df['SPC_keihi'].map(lambda i: Decimal(i).quantize(Decimal('0.000001'), ROUND_HALF_UP))
    SPC_SPCkeihi_SPCsetsuritsuhi_df['SPC_setsuritsuhi'] = SPC_SPCkeihi_SPCsetsuritsuhi_df['SPC_setsuritsuhi'].map(lambda i: Decimal(i).quantize(Decimal('0.000001'), ROUND_HALF_UP))
    SPC_SPCkeihi_SPCsetsuritduhi_df = SPC_SPCkeihi_SPCsetsuritsuhi_df.set_index('periods')
    SPC_keihi_sum = SPC_SPCkeihi_SPCsetsuritsuhi_df['SPC_keihi'].sum()
    SPC_seturitsuhi_sum = SPC_SPCkeihi_SPCsetsuritsuhi_df['SPC_setsuritsuhi'].sum()
    Shisetsu_seibihi_kappu = inputs_pdt.shisetsu_seibi_org_LCC * inputs_pdt.shisetsu_seibi_paymentschedule_kappu
    LCC_kappu_etc = Shisetsu_seibihi_kappu + inputs_pdt.SPC_shihon + (inputs_pdt.SPC_hiyou_nen * inputs_pdt.const_years)

    kanmin_kinrisa = (inputs_pdt.kijun_kinri + inputs_pdt.lg_spread) - inputs_pdt.chisai_kinri

    kanmin_ribaraihiyou_sa = pd.DataFrame(index=periods,columns=['LCC_kappuganpon_cumsum','seibihi_kappu_goukei','ribaraihiyou_sa']).fillna(Decimal('0.000000'))
    kanmin_ribaraihiyou_sa['LCC_kappuganpon_cumsum'] = LCC_kappuganpon_cumsum_ls
    kanmin_ribaraihiyou_sa.loc[inputs_pdt.const_years+1:inputs_pdt.proj_years+1,'seibihi_kappu_goukei'] = LCC_kappu_etc
    kanmin_ribaraihiyou_sa['ribaraihiyou_sa'] = (kanmin_ribaraihiyou_sa['seibihi_kappu_goukei'] - kanmin_ribaraihiyou_sa['LCC_kappuganpon_cumsum']) * kanmin_kinrisa#Ribaraihiyou_sa = [(Shisetsu_seibihi_kappu + SPC_relates - Kappuganpon_cumsum[i]) * kanmin_kinrisa for i in range(inputs_supl_pdt.target_years)]
    ribaraihiyou_sa_sum = kanmin_ribaraihiyou_sa['ribaraihiyou_sa'].sum()
    risk_adjust_gaku = ribaraihiyou_sa_sum + SPC_keihi_sum + SPC_seturitsuhi_sum + inputs_pdt.SPC_yobihi
    #print(risk_adjust_gaku)
    Risk_adjust_gaku_df = pd.DataFrame({'risk_adjust_gaku': [risk_adjust_gaku]})
    Risk_adjust_gaku_df.to_sql('Risk_table', engine, if_exists='replace', index=False, dtype={'risk_adjust_gaku': DECIMAL})
    #c.execute('CREATE OR REPLACE TABLE Risk_table AS SELECT * from Risk_adjust_gaku_df')
    #c.close()
    #Risk_df = c.sql("SELECT * FROM Risk_table").df()
    #print(Risk_df['risk_adjust_gaku'].loc[0])