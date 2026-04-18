import streamlit as st
import pandas as pd
from datetime import datetime

# 页面配置
st.set_page_config(page_title="农社直通车", page_icon="🌱", layout="wide")
st.title("🌱 农社直通车 - 农产品社区直供平台")

# 侧边栏菜单
menu = st.sidebar.radio("菜单", ["居民下单", "居委会汇总", "农户管理", "平台介绍"])

# ===================== 居民下单（本地图片修复版） =====================
if menu == "居民下单":
    st.subheader("🛒 居民下单")

    with st.expander("今日可购农产品", expanded=True):
        col1, col2, col3 = st.columns(3)

        # 1. 红富士苹果（本地图片，文件名完全匹配）
        with col1:
            st.image("apple.jpg.jpg", caption="红富士苹果", width=200)
            st.write("5.8 元/斤")
            apple_num = st.number_input("苹果购买斤数", 0, 100, 0, key="apple")

        # 2. 露天西红柿（本地图片，文件名完全匹配）
        with col2:
            st.image("tamato.jpg.jpg", caption="露天西红柿", width=200)
            st.write("3.5 元/斤")
            tomato_num = st.number_input("西红柿购买斤数", 0, 100, 0, key="tomato")

        # 3. 农家大白菜（本地图片，文件名完全匹配）
        with col3:
            st.image("cabbage.jpg.jpg", caption="农家大白菜", width=200)
            st.write("1.2 元/斤")
            cabbage_num = st.number_input("白菜购买斤数", 0, 100, 0, key="cabbage")

    # 订单信息填写
    st.divider()
    name = st.text_input("姓名")
    addr = st.text_input("楼号-单元-室号")
    phone = st.text_input("联系电话")

    # 提交订单逻辑
    if st.button("✅ 提交订单"):
        if not addr:
            st.warning("请填写楼号-单元-室号！")
        elif apple_num + tomato_num + cabbage_num == 0:
            st.warning("请至少选择一种农产品！")
        else:
            total = apple_num*5.8 + tomato_num*3.5 + cabbage_num*1.2
            st.success(f"""
            ✅ 下单成功！
            👤 姓名：{name or "未填写"}
            🏠 地址：{addr}
            📞 电话：{phone or "未填写"}
            🧾 订单总价：{total:.2f} 元
            🕒 预计明日下午送达社区自提点
            """)
            # 保存订单
            if "orders" not in st.session_state:
                st.session_state.orders = []
            st.session_state.orders.append({
                "时间": datetime.now().strftime("%m-%d %H:%M"),
                "姓名": name,
                "地址": addr,
                "电话": phone,
                "苹果": apple_num,
                "西红柿": tomato_num,
                "白菜": cabbage_num,
                "总价": round(total,2)
            })

# ===================== 居委会汇总 =====================
elif menu == "居委会汇总":
    st.subheader("🏛️ 居委会订单汇总")
    if "orders" not in st.session_state or len(st.session_state.orders) == 0:
        st.info("暂无订单")
    else:
        df = pd.DataFrame(st.session_state.orders)
        st.dataframe(df, use_container_width=True)

        total_apple = df["苹果"].sum()
        total_tomato = df["西红柿"].sum()
        total_cabbage = df["白菜"].sum()
        total_money = df["总价"].sum()

        st.subheader("📦 配送汇总单（给农户）")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("苹果总斤数", f"{total_apple} 斤")
        col2.metric("西红柿总斤数", f"{total_tomato} 斤")
        col3.metric("白菜总斤数", f"{total_cabbage} 斤")
        col4.metric("订单总金额", f"¥{total_money:.2f}")

        if st.button("🧹 清空今日订单"):
            st.session_state.orders = []
            st.rerun()

# ===================== 农户管理 =====================
elif menu == "农户管理":
    st.subheader("👨‍🌾 农户端 · 查看配送需求")
    if "orders" not in st.session_state or len(st.session_state.orders) == 0:
        st.info("暂无订单需求")
    else:
        df = pd.DataFrame(st.session_state.orders)
        total_apple = df["苹果"].sum()
        total_tomato = df["西红柿"].sum()
        total_cabbage = df["白菜"].sum()

        st.metric("今日总需求量", f"苹果 {total_apple} 斤｜西红柿 {total_tomato} 斤｜白菜 {total_cabbage} 斤")
        st.dataframe(df[["地址", "苹果", "西红柿", "白菜", "总价"]], use_container_width=True)
        st.success("请按以上数量采摘，统一配送至社区居委会！")

# ===================== 平台介绍 =====================
elif menu == "平台介绍":
    st.subheader("📖 农社直通车 · 产品介绍")
    st.markdown("""
**本产品是面向城市社区与周边农户的B2B2C预定式直供平台**
通过居委会组织预定、农户集中配送，砍掉中间环节，实现田间到餐桌直达。

### 核心模式
- 农户直采 · 零中间商
- 居委会集单 · 信任背书
- 居民预定 · 按需采摘
- 集中配送 · 社区自提

### 核心价值
✅ 农户：稳定销路、提高售价
✅ 居民：新鲜便宜、源头直供
✅ 居委会：便民服务、增强凝聚力
✅ 社会：助农增收、绿色低碳
""")