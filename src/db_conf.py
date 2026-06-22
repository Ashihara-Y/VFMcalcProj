import os
from google.cloud import firestore
import pandas as pd
import logging
from sqlalchemy import create_engine

logging = logging.getLogger(__name__)

ENGINE_VFM = create_engine('sqlite:///VFM.db', echo=False, connect_args={"check_same_thread": False})
db = firestore.Client()

def check_data_ownership(calc_id: str, user_id: str) ->bool:
  if not clac_id or user_id:
    logger.warning("検証エラー：　必須の引数が不足しています")
    return False
  try:
    doc_ref = db.collection("calc_histories").document(calc_id)
    doc = doc_ref.get()

    if not doc.exists:
      logger.warning(f"指定された算定結果が見つかりません。(calc_id: {calc_id})")
      return False
    
    record = doc.to_dict()

    db_calc_id = record.get("calc_id")
    if db_calc_id != calc_id:
      logger.error(f"セキュリティ警告：　ドキュメントIDとレコード内のcalc_idが不一致です。　"f"要求ID:{calc_id}, DB内ID：{db_calc_id}")
      return False

    owner_id = record.get("user_id")
    is_shared = record.get("is_shared", False)

    if owner_id == user_id:
      logger.info(f"認可成功：所有者本人によるアクセスです。(calc_id: {calc_id})")
      return True
    elif is_shared:
      logger.info(f"認可成功：共有リンクによるアクセスを許可しました。(calc_id: {calc_id})")
      return True
    else:
      logger.warning(f"認可ブロック：アクセス権限がありません。(calc_id:{calc_id}, 要求者:{user_id})")
      return False
  except Exception as e:
    logger.error(f"FireStoreへのクエリ実行中に例外が発生しました：{e}")
    return False
