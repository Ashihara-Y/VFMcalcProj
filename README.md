# VFMcalc Project (v0.5)

[![License: BSL 1.1](https://img.shields.io/badge/License-BSL%201.1-blue.svg)](LICENSE)
[![Status: Beta (Market Research)](https://img.shields.io/badge/Status-Beta-orange.svg)]()

公共施設等の整備（PPP/PFI事業）における**VFM（Value for Money）算定**を自動化・効率化するためのWebアプリケーションおよび計算エンジンのソースコードです。

本リポジトリは、将来的に提供予定の「VFM算定API」の**参照実装（Reference Implementation）**として、計算ロジックの透明性と公的ガイドラインへの準拠性を証明するために公開されています。

---

## ⚖️ ライセンスと利用条件（重要）

本プロジェクトはオープンソース（OSS）ではありません。**Business Source License 1.1 (BSL 1.1)** を採用しています。本リポジトリ内のすべてのソースコード、設定ファイル、ドキュメントが保護の対象となります。

利用者は、以下の条件を遵守する必要があります。

### ✅ 無償で許可されること（Non-Production Use）
* 算定ロジックの正確性や、内閣府のPFI導入ガイドライン等への準拠性を**監査・検証**する目的でのコード閲覧。
* ダミーデータを用いたローカル環境でのテスト実行、およびコードレビュー。

### ❌ 禁止されていること（Production Use）
以下の「本番利用（業務利用）」は固く禁じられており、発覚した場合はライセンス違反となります。
* **実際の公共・民間プロジェクトの提案書、報告書、内部検討のために算定結果を出力すること。**
* コンサルティング業務やアドバイザリー業務の一環として本コードを実行すること。
* 本コードを利用して、独自のSaaSやAPIサービスを構築・提供すること。

> 💡 **実務でのVFM算定をご希望の方へ**
> 業務利用（Production Use）を目的とする場合は、次項の「公式Webアプリ」をご利用いただくか、個別商用ライセンスのご相談をお願いいたします。

---

## 🚀 公式Webアプリのご案内（業務利用はこちら）

コンサルティングファーム、監査法人、自治体の皆様が実務でVFM算定を行うための公式環境として、現在**試験的サービス（市場調査フェーズ）**を提供しています。

面倒なサブスクリプション契約は不要で、プロジェクトの稼働状況に合わせて柔軟に経費処理できる**従量課金制（タイムチャージ）**を採用しています。

* **利用料金:** 1時間あたり 1,000円（税別）
* **特徴:** 最新の法制度・ガイドラインに準拠したセキュアなサーバー環境での算定実行
* **アクセス:** [ここに公式WebアプリのURLを記載]

---

## 🏢 エンタープライズ向けのご相談（個別商用ライセンス）

自社のセキュリティポリシー（閉域網での運用必須など）により、外部のWebアプリやAPIを利用できない法人様向けに、以下のご提供が可能です。

* **現状有姿（As-Is）でのローカル実行許諾ライセンス（年間契約）**
* **算定ロジックと公的ガイドラインの対応関係を解説した「算定根拠仕様書」の提供**

これらのメニューは、システム導入サポートを伴わない「権利とドメイン知識の提供」に特化しております。詳細につきましては、[連絡先メールアドレス] までお問い合わせください。

---

## 📅 将来のOSS化について（Change Date）

本バージョンのソースコードは、リリースから4年後の **2030年4月28日** をもって自動的に `Apache License 2.0` へ移行し、完全なオープンソースとなります。これにより、公共インフラに関わる算定システムとしての永続的な透明性と、ベンダーロックインの排除をお約束します。

---

## Acknowledgments / Attribution (CC BY 4.0)

The VFM (Value for Money) calculation algorithm implemented in this repository is based on the "VFM Calculation Sheet" (Excel format) trial-distributed by the Cabinet Office, Government of Japan, in March 2025. 

The original material was provided under the Creative Commons Attribution 4.0 International License (CC BY 4.0). 
- **Original Author:** Cabinet Office, Government of Japan
- **License:** [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)
- **Modifications:** The original spreadsheet-based calculation logic has been adapted and implemented as a Python-based web application and API by this project.

*Note: While the foundational calculation algorithm is attributed to the original CC BY 4.0 material, the specific source code, software implementation, and architecture in this repository (the "Licensed Work") are governed by the Business Source License 1.1 (BSL 1.1), as detailed in the `LICENSE` file.*

---

## 免責事項
本リポジトリのソースコードは「現状有姿（As-Is）」で提供され、特定のプロジェクトへの適合性や完全性を保証するものではありません。算定結果の最終的な利用責任は、利用者に帰属します。

---

## For your help
Please refer on the detail to the following link made by DeepWiki.
[Detail by DeepWiki](https://deepwiki.com/Ashihara-Y/VFMcalcProj/1-overview)
...
