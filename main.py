import streamlit as st
from rdkit import Chem
from rdkit.Chem import Draw
from pubchempy import get_compounds

st.set_page_config(page_title="ChemTranslator", layout="centered")
st.title("🧪 ChemTranslator: SMILES 분자 시각화")

st.markdown("""
이 앱은 간단한 **SMILES 분자식**을 입력하면, 분자의 구조를 시각화해주는 도구입니다.
👉 예시: `CCO`, `CC(=O)O`, `C1=CC=CC=C1`
""")

smiles = st.text_input("SMILES 문자열을 입력하세요:", "CCO")
if smiles:
    mol = Chem.MolFromSmiles(smiles)
    if mol:
        st.subheader("🔍 분자 구조 시각화")
        st.image(Draw.MolToImage(mol, size=(300, 300)))
    else:
        st.error("유효하지 않은 SMILES 구조입니다.")

compound_info = {
    "CCO": "에탄올 - 알코올, 친수성 용매",
    "CC(=O)O": "아세트산 - 식초의 성분",
    "C1=CC=CC=C1": "벤젠 - 방향족 화합물"
}
desc = compound_info.get(smiles, "설명이 준비되지 않았어요.")
st.write(f"📖 설명: {desc}")

query = st.text_input("자연어로 화합물 검색 (예: 식초의 주요 성분)")
if query:
    result = get_compounds(query, 'name')
    if result:
        mol2 = Chem.MolFromSmiles(result[0].isomeric_smiles)
        if mol2:
            st.subheader("📌 자연어 검색 결과")
            st.image(Draw.MolToImage(mol2, size=(300, 300)))
            st.write(f"🔬 SMILES: `{result[0].isomeric_smiles}`")
        else:
            st.error("구조 이미지를 불러올 수 없습니다.")
    else:
        st.error("화합물을 찾을 수 없습니다.")
