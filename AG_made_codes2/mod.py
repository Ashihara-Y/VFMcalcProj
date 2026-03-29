import re

path = "AG_made_codes2/src/Final_InputsT2.py"
with open(path, "r", encoding="utf-8") as f:
    text = f.read()

# 1. Imports
if "import dataclasses" not in text:
    text = text.replace("import flet as ft", "import flet as ft\nfrom final_inputs_models import InitialInputsData, UIInputsData, CalculatedFinancialData\nimport dataclasses")

# 2. init() 内のTinyDB読込を削除
text = re.sub(r'\s*db = TinyDB\("ii_db\.json"\)\n\s*self\.initial_inputs = db\.all\(\)\[0\]', '', text)

# 3. __init__
if "def __init__(self" not in text:
    init_str = "    def __init__(self, initial_data: 'InitialInputsData', *args, **kwargs):\n        super().__init__(*args, **kwargs)\n        self.initial_inputs = initial_data\n\n    def init(self):"
    text = text.replace("    def init(self):", init_str, 1)

# 4. dict -> dot
text = re.sub(r'self\.initial_inputs\["([^"]+)"\]', r'self.initial_inputs.\1', text)
text = re.sub(r"self\.initial_inputs\['([^']+)'\]", r"self.initial_inputs.\1", text)
text = re.sub(r'inputs\["([^"]+)"\]', r'inputs.\1', text)
text = re.sub(r"inputs\['([^']+)'\]", r"inputs.\1", text)

# 5. return UIInputsData
text = re.sub(r'(return\s*)(\{[\s\S]*?\})', r'\1UIInputsData(**\2)', text)

# 6. final_inputs
text = re.sub(r'(final_inputs\s*=\s*)(\{[\s\S]*?\})', r'\1CalculatedFinancialData(**\2)', text)

# 7. save_to_db
save_repl = '''    def _save_to_db(self, data):
        data_dict = dataclasses.asdict(data)
        self.page.session.set("final_inputs", data_dict)'''
text = re.sub(r'    def _save_to_db\(self, data\):.*?(?:\n\n|\Z)', save_repl, text, flags=re.DOTALL)

with open(path, "w", encoding="utf-8") as f:
    f.write(text)
print("Done")
