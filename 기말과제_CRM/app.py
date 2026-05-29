import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
import base64
import os

st.set_page_config(page_title="AI CRM 의사결정 시스템", page_icon="⭐", layout="wide")

def get_base64_image(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode()
    return ""

logo_base64 = get_base64_image("logo.png")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Gugi&family=Sunflower:wght@300;500;700&display=swap');

html, body, p, span, label, h2, h3 {
    font-family: 'Sunflower', sans-serif !important;
}

input[type="radio"] {
    accent-color: #80cbc4 !important;
}

[data-testid="stHeader"] {
    background: transparent !important;
    border-bottom: none !important;
}

[data-testid="stToolbar"] {
    display: none !important;
}

[data-testid="stHeader"] [data-testid="stDecoration"] {
    display: none !important;
}

[data-testid="stSidebar"] {
    transform: none !important;
    min-width: 300px !important;
    max-width: 300px !important;
    background: linear-gradient(180deg, #f0fafa 0%, #fef6f0 100%) !important;
    border-right: 2px solid #b2dfdb !important;
}

[data-testid="stSidebarCollapseButton"] {
    display: none !important;
}

[data-testid="collapsedControl"] {
    display: none !important;
}

[data-testid="stSidebar"] p,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] span {
    color: #4a9e9a !important;
    font-family: 'Sunflower', sans-serif !important;
}

[data-baseweb="radio"] label span:first-child {
    background-color: transparent !important;
    border-color: #80cbc4 !important;
}

[data-baseweb="radio"] [aria-checked="true"] span:first-child {
    background-color: #80cbc4 !important;
    border-color: #80cbc4 !important;
    outline: none !important;
    box-shadow: none !important;
}

[data-testid="stSlider"] [role="slider"] {
    background-color: #80cbc4 !important;
    border-color: #80cbc4 !important;
    box-shadow: none !important;
}

[data-testid="stSlider"] > div > div > div > div > div[style] {
    background: #80cbc4 !important;
}

div[data-testid="stSlider"] > div > div > div > div {
    background: #b2dfdb !important;
}

*:focus {
    outline: none !important;
    box-shadow: none !important;
}

a, a:visited {
    color: #80cbc4 !important;
}

button[data-testid="stNumberInputStepUp"]:hover,
button[data-testid="stNumberInputStepDown"]:hover {
    background-color: #e0f2f1 !important;
    color: #4a9e9a !important;
}

.stApp {
    background: linear-gradient(180deg, #f7fffe 0%, #fff8f4 100%);
    color: #4a6a68;
}

div[data-testid="stRadio"] {
    background-color: #ffffff !important;
    border-radius: 16px !important;
    border: 2.5px solid #b2dfdb !important;
    padding: 15px 20px !important;
}

div[data-testid="stRadio"],
div[data-testid="stRadio"] *,
div[data-baseweb="radio"] *,
.stSelectbox *,
.stNumberInput *,
.stTextInput *,
.stSlider * {
    outline: none !important;
    box-shadow: none !important;
    -webkit-tap-highlight-color: transparent !important;
}

div[data-baseweb="select"] > div,
div[data-baseweb="select"] button,
div[data-baseweb="select"] span,
input {
    outline: none !important;
    box-shadow: none !important;
}

div[data-testid="stRadio"] > div {
    border: none !important;
}

.stSelectbox div, .stNumberInput div, .stSlider div, .stTextInput div {
    border-radius: 14px !important;
}

.stSlider > div > div > div > div {
    background: #b2dfdb !important;
}

.stRadio label {
    color: #4a9e9a !important;
    font-weight: 700 !important;
}

h1, h2, h3 {
    color: #4a9e9a !important;
    font-family: 'Gugi', cursive !important;
}

.report-card, .ai-card {
    background: linear-gradient(135deg, #ffffff 0%, #f0fafa 100%);
    padding: 28px;
    border-radius: 25px;
    border: 2px solid #b2dfdb;
    box-shadow: 0 6px 20px rgba(128, 203, 196, 0.15);
}

.stButton button {
    background: linear-gradient(90deg, #f9c9b0, #80cbc4) !important;
    color: white !important;
    border: none !important;
    border-radius: 15px !important;
    font-weight: 700 !important;
    padding: 10px 20px !important;
}

.stButton button:focus,
.stButton button:active {
    outline: none !important;
    box-shadow: none !important;
}

[data-testid="stAlert"] {
    border-radius: 15px !important;
    border: none !important;
}

.custom-footer {
    position: fixed;
    right: 20px;
    bottom: 15px;
    background: rgba(255,255,255,0.8);
    backdrop-filter: blur(10px);
    color: #4a9e9a;
    padding: 10px 18px;
    border-radius: 20px;
    font-size: 14px;
    font-weight: 700;
    border: 1px solid #b2dfdb;
    z-index: 999;
    display: flex;
    align-items: center;
    gap: 10px;
}

.footer-logo {
    height: 28px;
    width: auto;
}

.main-content {
    margin-bottom: 80px;
}

.js-plotly-plot {
    border-radius: 20px;
    overflow: hidden;
}

.metric-badge {
    background: linear-gradient(135deg, #f0fafa, #fef6f0);
    border: 1.5px solid #b2dfdb;
    border-radius: 16px;
    padding: 16px 20px;
    margin-bottom: 12px;
    text-align: center;
}

.metric-badge .value {
    font-size: 28px;
    font-weight: 700;
    color: #4a9e9a;
    font-family: 'Gugi', cursive;
}

.metric-badge .label {
    font-size: 13px;
    color: #f0956a;
    margin-top: 4px;
}
</style>
""", unsafe_allow_html=True)


@st.cache_resource
def load_data_and_models():
    try:
        df = pd.read_csv("adventureworks_clean.csv")
        df.columns = df.columns.str.strip()

        required = ["Order Quantity", "Unit Price", "Standard Cost", "Sales Amount"]
        for col in required:
            if col not in df.columns:
                raise ValueError(f"Missing column: {col}")

        df = df.dropna(subset=required)

        has_territory = "Country" in df.columns
        has_category = "Category" in df.columns
        month_col = "Month_num" if "Month_num" in df.columns else ("Month" if "Month" in df.columns else None)

        feature_cols = ["Order Quantity", "Unit Price", "Standard Cost"]

        if has_territory:
            le_territory = LabelEncoder()
            df["Territory_enc"] = le_territory.fit_transform(df["Country"].astype(str))
            feature_cols.append("Territory_enc")
            territory_classes = le_territory.classes_
        else:
            le_territory = None
            territory_classes = None

        if has_category:
            le_category = LabelEncoder()
            df["Category_enc"] = le_category.fit_transform(df["Category"].astype(str))
            feature_cols.append("Category_enc")
            category_classes = le_category.classes_
        else:
            le_category = None
            category_classes = None

        if month_col:
            if df[month_col].dtype == object:
                month_order = ["January","February","March","April","May","June",
                               "July","August","September","October","November","December"]
                df["Month_num"] = df[month_col].apply(lambda x: month_order.index(x) + 1 if x in month_order else 6)
                month_col = "Month_num"
            feature_cols.append("Month_num")

        X = df[feature_cols]
        y_sales = df["Sales Amount"]

        X_train, X_test, y_train, y_test = train_test_split(X, y_sales, test_size=0.2, random_state=42)
        sales_model = RandomForestRegressor(n_estimators=200, random_state=42, n_jobs=-1)
        sales_model.fit(X_train, y_train)
        r2 = r2_score(y_test, sales_model.predict(X_test))

        territory_model = None
        if has_territory and len(territory_classes) > 1:
            Xt_train, Xt_test, yt_train, yt_test = train_test_split(
                df[["Order Quantity", "Unit Price", "Standard Cost"]],
                df["Territory_enc"], test_size=0.2, random_state=42
            )
            territory_model = RandomForestClassifier(n_estimators=200, random_state=42, n_jobs=-1)
            territory_model.fit(Xt_train, yt_train)

        season_model = None
        if has_category and month_col and len(category_classes) > 1:
            Xs_train, Xs_test, ys_train, ys_test = train_test_split(
                df[["Month_num", "Order Quantity", "Unit Price"]],
                df["Category_enc"], test_size=0.2, random_state=42
            )
            season_model = RandomForestClassifier(n_estimators=200, random_state=42, n_jobs=-1)
            season_model.fit(Xs_train, ys_train)

        return {
            "df": df,
            "sales_model": sales_model,
            "territory_model": territory_model,
            "season_model": season_model,
            "feature_cols": feature_cols,
            "territory_classes": territory_classes,
            "category_classes": category_classes,
            "le_territory": le_territory,
            "le_category": le_category,
            "r2": r2,
            "has_territory": has_territory,
            "has_category": has_category,
            "month_col": month_col,
        }

    except Exception as e:
        np.random.seed(42)
        n = 1000
        territories = ["United States", "Australia", "Canada", "United Kingdom", "France", "Germany"]
        categories = ["Bikes", "Accessories", "Clothing", "Components"]
        months = np.random.randint(1, 13, n)
        qtys = np.random.randint(1, 7, n)
        prices = np.random.uniform(5, 2500, n)
        costs = prices * np.random.uniform(0.4, 0.75, n)
        terr_idx = np.random.randint(0, len(territories), n)
        cat_idx = np.random.randint(0, len(categories), n)

        season_bonus = np.where(np.isin(months, [3,4,5,6]), 1.15,
                        np.where(np.isin(months, [11,12]), 1.25, 1.0))
        sales = qtys * prices * season_bonus * np.random.uniform(0.85, 1.15, n)

        df = pd.DataFrame({
            "Order Quantity": qtys,
            "Unit Price": prices,
            "Standard Cost": costs,
            "Sales Amount": sales,
            "Country": [territories[i] for i in terr_idx],
            "Category": [categories[i] for i in cat_idx],
            "Month_num": months,
            "Territory_enc": terr_idx,
            "Category_enc": cat_idx,
        })

        feature_cols = ["Order Quantity", "Unit Price", "Standard Cost", "Territory_enc", "Category_enc", "Month_num"]
        X = df[feature_cols]
        y_sales = df["Sales Amount"]
        X_train, X_test, y_train, y_test = train_test_split(X, y_sales, test_size=0.2, random_state=42)
        sales_model = RandomForestRegressor(n_estimators=200, random_state=42, n_jobs=-1)
        sales_model.fit(X_train, y_train)
        r2 = r2_score(y_test, sales_model.predict(X_test))

        territory_model = RandomForestClassifier(n_estimators=200, random_state=42, n_jobs=-1)
        territory_model.fit(df[["Order Quantity", "Unit Price", "Standard Cost"]], df["Territory_enc"])

        season_model = RandomForestClassifier(n_estimators=200, random_state=42, n_jobs=-1)
        season_model.fit(df[["Month_num", "Order Quantity", "Unit Price"]], df["Category_enc"])

        le_territory = LabelEncoder().fit([territories[i] for i in terr_idx])
        le_category = LabelEncoder().fit([categories[i] for i in cat_idx])

        return {
            "df": df,
            "sales_model": sales_model,
            "territory_model": territory_model,
            "season_model": season_model,
            "feature_cols": feature_cols,
            "territory_classes": np.array(territories),
            "category_classes": np.array(categories),
            "le_territory": le_territory,
            "le_category": le_category,
            "r2": r2,
            "has_territory": True,
            "has_category": True,
            "month_col": "Month_num",
        }

data = load_data_and_models()
df = data["df"]

with st.sidebar:
    st.markdown("# 메뉴")
    menu = st.radio("분석 단계 선택:", ["홈", "매출 예측 리포트", "시즌별 전략 추천", "3D 시뮬레이션"])
    st.markdown("---")
    st.markdown("### 시뮬레이션 설정")
    customer_type = st.selectbox("거래 대상", ["도매 및 대리점", "일반 개인 고객"])
    order_quantity = st.slider("주문 수량", 1, 6, 1)
    unit_price = st.number_input("제품 단가", value=462)
    standard_cost = st.number_input("제조 원가", value=400)

    if data["has_territory"] and data["territory_classes"] is not None:
        territory_choice = st.selectbox("판매 지역", list(data["territory_classes"]))
    else:
        territory_choice = None

    if data["month_col"]:
        month_choice = st.slider("월 (계절 분석용)", 1, 12, 6)
    else:
        month_choice = 6

st.markdown('<div class="main-content">', unsafe_allow_html=True)

if menu == "홈":
    st.title("AI CRM 의사결정 시스템")
    st.markdown("### 환영합니다")
    st.write("왼쪽 메뉴를 사용하여 머신러닝 분석을 시작하세요. 각 단계는 독립적으로 작동하며 비즈니스 의사결정을 지원합니다.")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""
        <div class="metric-badge">
            <div class="value">{len(df):,}</div>
            <div class="label">학습 데이터 수</div>
        </div>""", unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="metric-badge">
            <div class="value">{data['r2']*100:.1f}%</div>
            <div class="label">모델 정확도 (R²)</div>
        </div>""", unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div class="metric-badge">
            <div class="value">{len(data["feature_cols"])}</div>
            <div class="label">학습 피처 수</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 모델이 학습한 피처 중요도")

    importances = data["sales_model"].feature_importances_
    feat_df = pd.DataFrame({
        "피처": data["feature_cols"],
        "중요도": importances
    }).sort_values("중요도", ascending=True)

    fig = px.bar(feat_df, x="중요도", y="피처", orientation="h",
                 color="중요도", color_continuous_scale="Teal")
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#4a9e9a"),
        coloraxis_showscale=False,
        height=300,
        margin=dict(l=0, r=0, t=10, b=0)
    )
    st.plotly_chart(fig, use_container_width=True)

elif menu == "매출 예측 리포트":
    st.title("실시간 매출 예측 분석")

    input_dict = {
        "Order Quantity": order_quantity,
        "Unit Price": unit_price,
        "Standard Cost": standard_cost,
    }

    if "Territory_enc" in data["feature_cols"] and territory_choice is not None:
        input_dict["Territory_enc"] = list(data["territory_classes"]).index(territory_choice)

    if "Category_enc" in data["feature_cols"]:
        input_dict["Category_enc"] = 0

    if "Month_num" in data["feature_cols"]:
        input_dict["Month_num"] = month_choice

    input_data = pd.DataFrame([input_dict])[data["feature_cols"]]

    predicted_sales = int(round(data["sales_model"].predict(input_data)[0]))
    total_cost = int(order_quantity * standard_cost)
    net_profit = predicted_sales - total_cost
    margin_rate = int(round((net_profit / predicted_sales) * 100)) if predicted_sales > 0 else 0

    col1, col2 = st.columns(2)

    with col1:
        profit_color = "#4a9e9a" if net_profit > 0 else "#e57373"
        st.markdown(f"""
        <div class="report-card">
            <h3>재무 예측 결과</h3>
            <p>예상 총 매출: <b>${predicted_sales:,}</b></p>
            <p>총 제조 원가: <b>${total_cost:,}</b></p>
            <hr style='border-color:#b2dfdb;'>
            <h2 style='color:{profit_color};'>최종 순수익: ${net_profit:,}</h2>
            <p>마진율: {margin_rate}%</p>
            <p style='font-size:12px; color:#80cbc4;'>모델 학습 정확도 (R²): {data['r2']*100:.1f}%</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("### 비즈니스 인사이트")
        if net_profit > 0:
            st.success(f"현재 전략은 안정적인 수익 흐름을 보여주고 있습니다. 마진율 {margin_rate}%.")
        else:
            st.warning("현재 설정은 손실이 예상됩니다. 단가를 올리거나 원가를 낮춰보세요.")

        if data["territory_model"] is not None and territory_choice is None:
            pred_terr_idx = data["territory_model"].predict([[order_quantity, unit_price, standard_cost]])[0]
            pred_territory = data["territory_classes"][pred_terr_idx]
            proba = data["territory_model"].predict_proba([[order_quantity, unit_price, standard_cost]])[0]
            top_prob = round(max(proba) * 100, 1)
            st.info(f"AI 추천 판매 지역: **{pred_territory}** (신뢰도 {top_prob}%)")

    st.markdown("---")
    st.markdown("### 수량별 예측 매출 곡선")

    qty_range = list(range(1, 7))
    pred_sales_list = []
    for q in qty_range:
        row = dict(input_dict)
        row["Order Quantity"] = q
        pred_row = pd.DataFrame([row])[data["feature_cols"]]
        pred_sales_list.append(data["sales_model"].predict(pred_row)[0])

    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(
        x=qty_range, y=pred_sales_list,
        mode="lines+markers",
        line=dict(color="#80cbc4", width=3),
        marker=dict(color="#f9c9b0", size=8),
        name="예측 매출"
    ))
    fig2.add_vline(x=order_quantity, line_dash="dash", line_color="#4a9e9a",
                   annotation_text="현재 수량", annotation_font_color="#4a9e9a")
    fig2.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#4a9e9a"),
        xaxis=dict(title="주문 수량", gridcolor="#e0f2f1", tickmode="linear", dtick=1),
        yaxis=dict(title="예측 매출 ($)", gridcolor="#e0f2f1"),
        height=350,
        margin=dict(l=0, r=0, t=20, b=0)
    )
    st.plotly_chart(fig2, use_container_width=True)

elif menu == "시즌별 전략 추천":
    st.title("시즌 및 글로벌 마케팅 전략")

    if "Category" in df.columns and "Country" in df.columns:

        season_map = {
            "봄 (3–5월)": [3, 4, 5],
            "여름 (6–8월)": [6, 7, 8],
            "가을 (9–11월)": [9, 10, 11],
            "겨울 (12–2월)": [12, 1, 2],
        }
        season = st.select_slider("시즌 선택", options=list(season_map.keys()))
        season_months = season_map[season]

        if "Month_num" in df.columns:
            season_df = df[df["Month_num"].isin(season_months)]
        else:
            season_df = df.copy()

        st.markdown("---")
        st.markdown("### 국가별 카테고리 판매 비중 (마케팅 기회 지도)")
        st.write("Bikes 비중이 높고 Accessories/Clothing 비중이 낮은 국가일수록 크로스셀링 프로모션 효과가 클 것으로 예측됩니다.")

        country_cat = season_df.groupby(["Country", "Category"])["Sales Amount"].sum().reset_index()
        country_total = country_cat.groupby("Country")["Sales Amount"].sum().reset_index()
        country_total.columns = ["Country", "Total"]
        country_cat = country_cat.merge(country_total, on="Country")
        country_cat["비중 (%)"] = (country_cat["Sales Amount"] / country_cat["Total"] * 100).round(1)

        global_avg = df.groupby("Category")["Sales Amount"].sum()
        global_avg_pct = (global_avg / global_avg.sum() * 100).round(1)
        bikes_global_avg = global_avg_pct.get("Bikes", 70)
        non_bikes_global_avg = 100 - bikes_global_avg

        fig_map = px.bar(
            country_cat,
            x="Country", y="비중 (%)", color="Category",
            color_discrete_map={
                "Bikes": "#80cbc4",
                "Accessories": "#f9c9b0",
                "Clothing": "#b2ebf2",
                "Components": "#ffe0b2"
            },
            barmode="stack",
            text="비중 (%)"
        )
        fig_map.update_traces(texttemplate="%{text:.0f}%", textposition="inside")
        fig_map.add_hline(
            y=bikes_global_avg,
            line_dash="dash", line_color="#e57373",
            annotation_text=f"글로벌 Bikes 평균 {bikes_global_avg:.0f}%",
            annotation_font_color="#e57373"
        )
        fig_map.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#4a9e9a"),
            xaxis=dict(title="국가", gridcolor="#e0f2f1"),
            yaxis=dict(title="매출 비중 (%)", gridcolor="#e0f2f1"),
            legend=dict(title="카테고리"),
            height=420,
            margin=dict(l=0, r=0, t=20, b=0)
        )
        st.plotly_chart(fig_map, use_container_width=True)

        st.markdown("---")
        st.markdown("### 국가별 마케팅 기회 점수")
        st.write("Bikes 비중이 글로벌 평균보다 높은 국가 = Accessories/Clothing 크로스셀링 여지가 큽니다.")

        bikes_by_country = country_cat[country_cat["Category"] == "Bikes"][["Country", "비중 (%)"]].copy()
        bikes_by_country.columns = ["Country", "Bikes 비중 (%)"]
        bikes_by_country["기회 점수"] = (bikes_by_country["Bikes 비중 (%)"] - bikes_global_avg).round(1)
        bikes_by_country["기회 점수"] = bikes_by_country["기회 점수"].clip(lower=0)
        bikes_by_country = bikes_by_country.sort_values("기회 점수", ascending=False)

        fig_opp = px.bar(
            bikes_by_country, x="기회 점수", y="Country", orientation="h",
            color="기회 점수",
            color_continuous_scale="Oranges",
            text=bikes_by_country["기회 점수"].apply(lambda x: f"+{x:.1f}%p")
        )
        fig_opp.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#4a9e9a"),
            xaxis=dict(title="글로벌 평균 대비 Bikes 초과 비중 (%p)", gridcolor="#e0f2f1"),
            coloraxis_showscale=False,
            height=320,
            margin=dict(l=0, r=0, t=10, b=0)
        )
        st.plotly_chart(fig_opp, use_container_width=True)

        top_opportunity = bikes_by_country.iloc[0]["Country"] if len(bikes_by_country) > 0 else "N/A"
        top_score = bikes_by_country.iloc[0]["기회 점수"] if len(bikes_by_country) > 0 else 0

        st.markdown("---")
        st.markdown("### 자전거 구매 고객 크로스셀 추천 (번들 전략)")
        st.write("Bikes를 구매한 고객이 함께 구매한 카테고리 분포입니다. 할인 번들 구성 시 참고하세요.")

        bike_orders = df[df["Category"] == "Bikes"]["SalesOrderLineKey"].unique() if "SalesOrderLineKey" in df.columns else None

        if bike_orders is not None and "SalesOrderLineKey" in df.columns:
            crosssell_df = df[
                (df["SalesOrderLineKey"].isin(bike_orders)) & (df["Category"] != "Bikes")
            ]
            if len(crosssell_df) > 0:
                crosssell_counts = crosssell_df.groupby(["Category", "Subcategory"])["Sales Amount"].sum().reset_index()
                crosssell_counts = crosssell_counts.sort_values("Sales Amount", ascending=False).head(10)
                crosssell_counts["매출"] = crosssell_counts["Sales Amount"].apply(lambda x: f"${x:,.0f}")

                fig_cs = px.bar(
                    crosssell_counts, x="Sales Amount", y="Subcategory", orientation="h",
                    color="Category",
                    color_discrete_map={
                        "Accessories": "#f9c9b0",
                        "Clothing": "#b2ebf2",
                        "Components": "#ffe0b2"
                    },
                    text="매출"
                )
                fig_cs.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    font=dict(color="#4a9e9a"),
                    xaxis=dict(title="총 매출 ($)", gridcolor="#e0f2f1"),
                    height=380,
                    margin=dict(l=0, r=0, t=10, b=0)
                )
                st.plotly_chart(fig_cs, use_container_width=True)

                top_sub = crosssell_counts.iloc[0]["Subcategory"]
                top_cat_cs = crosssell_counts.iloc[0]["Category"]
                st.markdown(f"""
                <div class="ai-card">
                    <h3>번들 프로모션 전략 제안</h3>
                    <p><b>최우선 타겟 국가:</b> {top_opportunity} (Bikes 집중도 글로벌 평균 대비 +{top_score:.1f}%p 초과)</p>
                    <p><b>추천 번들 상품:</b> Bikes + {top_sub} ({top_cat_cs})</p>
                    <p><b>전략:</b> {top_opportunity} 시장에서 자전거 구매 고객에게 {top_sub} 할인 쿠폰을 제공하여 객단가를 높이고 카테고리 침투율을 개선합니다.</p>
                    <p><b>시즌:</b> {season} 집중 프로모션 권장</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.info("동일 주문 내 크로스셀 데이터가 없습니다.")
        else:
            st.markdown(f"""
            <div class="ai-card">
                <h3>번들 프로모션 전략 제안</h3>
                <p><b>최우선 타겟 국가:</b> {top_opportunity} (Bikes 집중도 글로벌 평균 대비 +{top_score:.1f}%p 초과)</p>
                <p><b>추천 번들:</b> Bikes 구매 고객에게 Accessories 10~15% 할인 쿠폰 제공</p>
                <p><b>전략:</b> {season} 시즌 집중 크로스셀링 프로모션으로 카테고리 침투율 개선</p>
            </div>
            """, unsafe_allow_html=True)

    else:
        st.warning("Category 또는 Country 컬럼이 없습니다. 데이터 전처리를 먼저 실행해주세요.")

elif menu == "3D 시뮬레이션":
    st.title("인터랙티브 3D 매출 곡면")
    st.write("수량과 가격 조합에 따른 AI 예측 매출을 3D로 확인하세요. 마우스로 드래그하여 회전할 수 있습니다.")

    q_axis = np.linspace(1, 6, 6)
    p_axis = np.linspace(unit_price * 0.5, unit_price * 1.5, 25)

    Q, P = np.meshgrid(q_axis, p_axis)

    base_input = {col: 0 for col in data["feature_cols"]}
    base_input["Standard Cost"] = standard_cost
    if "Territory_enc" in data["feature_cols"] and territory_choice is not None:
        base_input["Territory_enc"] = list(data["territory_classes"]).index(territory_choice)
    if "Category_enc" in data["feature_cols"]:
        base_input["Category_enc"] = 0
    if "Month_num" in data["feature_cols"]:
        base_input["Month_num"] = month_choice

    rows = []
    for i in range(Q.shape[0]):
        for j in range(Q.shape[1]):
            row = dict(base_input)
            row["Order Quantity"] = Q[i, j]
            row["Unit Price"] = P[i, j]
            rows.append(row)

    batch_df = pd.DataFrame(rows)[data["feature_cols"]]
    preds = data["sales_model"].predict(batch_df)
    Z = preds.reshape(Q.shape)

    fig = go.Figure(data=[go.Surface(
        z=Z, x=Q, y=P,
        colorscale="Teal",
        showscale=True,
        colorbar=dict(title="예측 매출")
    )])

    fig.update_layout(
        scene=dict(
            xaxis=dict(title="수량", gridcolor="#b2dfdb",
                       tickfont=dict(color="#4a9e9a"), title_font=dict(color="#4a9e9a")),
            yaxis=dict(title="가격", gridcolor="#b2dfdb",
                       tickfont=dict(color="#4a9e9a"), title_font=dict(color="#4a9e9a")),
            zaxis=dict(title="예측 매출", gridcolor="#b2dfdb",
                       tickfont=dict(color="#4a9e9a"), title_font=dict(color="#4a9e9a")),
            bgcolor="rgba(0,0,0,0)"
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=0, r=0, b=0, t=0),
        height=600
    )

    st.plotly_chart(fig, use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)

logo_html = f'<img src="data:image/png;base64,{logo_base64}" class="footer-logo">' if logo_base64 else ""
st.markdown(f"""
<div class="custom-footer">
    {logo_html}
    <span>2555041</span>
</div>
""", unsafe_allow_html=True)