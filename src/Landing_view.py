import flet as ft

@ft.control
class LandingContainer(ft.Column):
    def __init__(self, on_action, current_locale):
        super().__init__()

        self.expand = True
        #self.alignmentMainAxisAlignment.CENTER
        self.on_action = on_action
        self.current_locale = current_locale

        self.build_ui(self)

    # コンテンツ定義
    def build_ui(self, e):

        # 1. ホーム（前回の4つボタン。一部スタイル調整）
        home_content = ft.Container(
            padding=30,
            content=ft.Column([
                ft.Text("VFMcalc サービスメニュー", size=22, weight="bold"),
                ft.Row([
                    self._action_card(ft.Icons.PERSON_ADD, "新規登録", "Auth0で作成", "login"),
                    self._action_card(ft.Icons.LOGIN, "サインイン", "既存の方", "login"),
                ]),
                ft.Row([
                    self._action_card(ft.Icons.ADD_CHART, "新規算定", "シミュレーション開始", "/initial_inputs"),
                    self._action_card(ft.Icons.LIST_ALT, "履歴確認", "算定結果の管理", "/view_saved"),
                ]),
            ], spacing=20)
        )

        # 2. 当サービスについて
        about_content = ft.Container(
            padding=30,
            content=ft.Column([
                ft.Text("VFMcalc Professional について", size=22, weight="bold"),
                ft.Text("本サービスは、公共施設整備におけるPFI事業等のVFM（Value for Money）を迅速かつ精緻に算定するための専門ツールです。", size=16),
                ft.Text("【試験的サービスの内容】", weight="bold"),
                ft.Text("API参照実装としてのWebアプリを先行公開"),
                ft.Text("従量制料金：1時間 1,000円（Stripe決済）"),
                ft.Text("将来的なAPI連携を見据えた高度な算定ロジックを搭載"),
            ], spacing=15)
        )

        # 3. 注意事項・法務
        legal_content = ft.Container(
            padding=30,
            content=ft.Column([
                ft.Text("ご利用上の注意事項", size=22, weight="bold"),
                ft.ExpansionTile(
                    title=ft.Text("利用規約・免責事項"),
                    controls=[ft.Text("本算定結果は入力値に基づく試算であり、将来の経済状況を保証するものではありません。実際の政策決定にあたっては専門家の確認を推奨します。")]
                ),
                ft.ExpansionTile(
                    title=ft.Text("プライバシーポリシー"),
                    controls=[ft.Text("入力されたデータはSSL/TLSにより暗号化され、Auth0による厳格な認証管理の下で保護されます。")]
                ),
                ft.ExpansionTile(
                    title=ft.Text("特定商取引法に基づく表示"),
                    controls=[ft.Text("販売価格：1,000円/時。支払方法：クレジットカード（Stripe）。)")]
                ),
            ])
        )

        # 4. お問い合わせ
        contact_content = ft.Container(
            padding=30,
            content=ft.Column([
                ft.Text("お問い合わせ", size=22, weight="bold"),
                ft.Text("サービスに関するご質問、API連携のご相談は以下のフォームより承ります。", size=16),
                ft.TextField(label="メールアドレス"),
                ft.TextField(label="件名"),
                ft.TextField(label="内容", multiline=True, min_lines=3),
                ft.Button(content="送信する", icon=ft.Icons.SEND),
            ], spacing=15)
        )

        # タブの構築
        self.tabs = ft.Tabs(
                selected_index=0,
                length=4,
                animation_duration=300,
                content = ft.Column(
                    expand=True,    
                    controls=[
                        ft.TabBar(
                            tabs=[
                                ft.Tab(
                                    label="ホーム",
                                    icon=ft.Icons.HOME,
                                ),
                                ft.Tab(
                                    label="当サービスについて",
                                    icon=ft.Icons.INFO,
                                ),
                                ft.Tab(
                                    label="注意事項",
                                    icon=ft.Icons.GAVEL,
                                ),
                                ft.Tab(
                                    label="お問い合わせ",
                                    icon=ft.Icons.CONTACT_SUPPORT,
                                ),
                            ],
                        ),
                        ft.TabBarView(
                            expand=True,
                            controls=[
                                ft.Container(
                                    content=home_content,
                                    #alignment=ft.MainAxisAlignment.SPACE_AROUND,
                                    ),
                                    #width=2100,
                                    #padding=10,
                                    #margin=10,
                                    #height=1000,
                                #),
                                ft.Container(
                                    content=about_content
                                    #alignment=ft.MainAxisAlignment.SPACE_AROUND,
                                    ),
                                    #width=2100,
                                    #padding=10,
                                    #height=4000,
                                    #margin=10,
                                #),
                                ft.Container(
                                    content=legal_content
                                    #alignment=ft.MainAxisAlignment.SPACE_AROUND,
                                    ),
                                    #width=2100,
                                    #padding=10,
                                    #height=2000,
                                    #margin=10,
                                #),
                                ft.Container(
                                    content=contact_content
                                    #alignment=ft.MainAxisAlignment.SPACE_AROUND,
                                    ),
                                    #width=2100,
                                    #padding=10,
                                    #height=3000,
                                    #margin=10,
                                #),
                            ],       
                        )
                    ],
                ),
            )
        #]

        self.controls = [self.tabs]

    def _action_card(self, icon, text, subtext, route):
        return ft.Container(
            content=ft.Column([
                ft.Icon(icon, size=30, color=ft.Colors.BLUE_800),
                ft.Text(text, weight="bold"),
                ft.Text(subtext, size=10, color="grey"),
            ], alignment="center", horizontal_alignment="center"),
            padding=20, border_radius=10,
            expand=1, ink=True, on_click=lambda _: self.on_action(route)
        )
