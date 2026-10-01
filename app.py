import streamlit as st

from datetime import datetime

# =========================

# CẤU HÌNH TRANG

# =========================

st.set_page_config(

    page_title="Trà Sữa - Tính Bill",

    page_icon="🧋",

    layout="centered"

)

# =========================

# DỮ LIỆU MENU

# =========================

MENU = {

    "Trà sữa truyền thống": 30000,

    "Trà sữa matcha": 35000,

    "Trà sữa socola": 35000,

    "Trà sữa dâu": 35000,

    "Trà sữa khoai môn": 38000,

    "Trà sữa caramel": 38000,

    "Trà đào": 30000,

    "Trà vải": 30000,

    "Trà chanh": 25000

}

TOPPINGS = {

    "Không topping": 0,

    "Trân châu đen": 5000,

    "Trân châu trắng": 5000,

    "Thạch trái cây": 5000,

    "Pudding trứng": 7000,

    "Kem cheese": 8000,

    "Trân châu hoàng kim": 7000

}

MUC_DUONG = ["100%", "70%", "0%"]

MUC_DA = ["100%", "70%", "0%"]

# =========================

# KHỞI TẠO SESSION STATE

# =========================

if "cart" not in st.session_state:

    st.session_state.cart = []

# =========================

# TIÊU ĐỀ

# =========================

st.title("🧋 QUÁN TRÀ SỮA")

st.subheader("💰 Tính hóa đơn")

st.divider()

# =========================

# THÔNG TIN KHÁCH HÀNG

# =========================

st.header("👤 Thông tin khách hàng")

ten_khach = st.text_input(

    "Tên khách hàng",

    placeholder="Nhập tên khách hàng..."

)

st.divider()

# =========================

# CHỌN MÓN

# =========================

st.header("🧋 Chọn món")

col1, col2 = st.columns(2)

with col1:

    mon = st.selectbox(

        "Loại trà sữa",

        list(MENU.keys())

    )

    so_luong = st.number_input(

        "Số lượng",

        min_value=1,

        max_value=20,

        value=1,

        step=1

    )

with col2:

    topping = st.selectbox(

        "Topping",

        list(TOPPINGS.keys())

    )

    muc_duong = st.selectbox(

        "Mức độ đường",

        MUC_DUONG

    )

    muc_da = st.selectbox(

        "Mức độ đá",

        MUC_DA

    )

# Giá

gia_mon = MENU[mon]

gia_topping = TOPPINGS[topping]

don_gia = gia_mon + gia_topping

thanh_tien = don_gia * so_luong

st.info(

    f"💵 Đơn giá: **{don_gia:,} VNĐ** | "

    f"Thành tiền: **{thanh_tien:,} VNĐ**"

)

# =========================

# NÚT THÊM VÀO BILL

# =========================

if st.button("➕ Thêm món vào hóa đơn", use_container_width=True):

    if ten_khach.strip() == "":

        st.warning("⚠️ Vui lòng nhập tên khách hàng!")

    else:

        item = {

            "mon": mon,

            "so_luong": so_luong,

            "topping": topping,

            "duong": muc_duong,

            "da": muc_da,

            "don_gia": don_gia,

            "thanh_tien": thanh_tien

        }

        st.session_state.cart.append(item)

        st.success(f"✅ Đã thêm {mon} vào hóa đơn!")

# =========================

# HIỂN THỊ HÓA ĐƠN

# =========================

st.divider()

st.header("🧾 HÓA ĐƠN")

if len(st.session_state.cart) == 0:

    st.write("Chưa có món nào trong hóa đơn.")

else:

    tong_tien = 0

    for i, item in enumerate(st.session_state.cart):

        tong_tien += item["thanh_tien"]

        with st.container(border=True):

            st.markdown(

                f"### {i + 1}. {item['mon']}"

            )

            col1, col2 = st.columns(2)

            with col1:

                st.write(f"**Số lượng:** {item['so_luong']}")

                st.write(f"**Topping:** {item['topping']}")

                st.write(f"**Mức đường:** {item['duong']}")

            with col2:

                st.write(f"**Mức đá:** {item['da']}")

                st.write(

                    f"**Đơn giá:** {item['don_gia']:,} VNĐ"

                )

                st.write(

                    f"**Thành tiền:** {item['thanh_tien']:,} VNĐ"

                )

    st.divider()

    # =========================

    # TỔNG TIỀN

    # =========================

    st.markdown(

        f"""

        <div style="

            background-color:#f5f5f5;

            padding:20px;

            border-radius:10px;

            text-align:center;

        ">

            <h2>TỔNG THANH TOÁN</h2>

            <h1 style="color:#e91e63;">

                {tong_tien:,} VNĐ

            </h1>

        </div>

        """,

        unsafe_allow_html=True

    )

    st.write("")

    # =========================

    # TẠO NỘI DUNG HÓA ĐƠN

    # =========================

    thoi_gian = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    noi_dung_hoa_don = ""

    noi_dung_hoa_don += "=" * 45 + "\n"

    noi_dung_hoa_don += "          HOA DON TRA SUA\n"

    noi_dung_hoa_don += "=" * 45 + "\n"

    noi_dung_hoa_don += f"Khach hang: {ten_khach}\n"

    noi_dung_hoa_don += f"Thoi gian: {thoi_gian}\n"

    noi_dung_hoa_don += "-" * 45 + "\n"

    for i, item in enumerate(st.session_state.cart):

        noi_dung_hoa_don += f"\n{i + 1}. {item['mon']}\n"

        noi_dung_hoa_don += (

            f"   So luong: {item['so_luong']}\n"

        )

        noi_dung_hoa_don += (

            f"   Topping: {item['topping']}\n"

        )

        noi_dung_hoa_don += (

            f"   Duong: {item['duong']}\n"

        )

        noi_dung_hoa_don += (

            f"   Da: {item['da']}\n"

        )

        noi_dung_hoa_don += (

            f"   Don gia: {item['don_gia']:,} VNĐ\n"

        )

        noi_dung_hoa_don += (

            f"   Thanh tien: {item['thanh_tien']:,} VNĐ\n"

        )

    noi_dung_hoa_don += "\n" + "-" * 45 + "\n"

    noi_dung_hoa_don += (

        f"TONG THANH TOAN: {tong_tien:,} VNĐ\n"

    )

    noi_dung_hoa_don += "=" * 45 + "\n"

    noi_dung_hoa_don += "       CAM ON QUY KHACH!\n"

    noi_dung_hoa_don += "=" * 45

    # =========================

    # NÚT THANH TOÁN

    # =========================

    if st.button(

        "💳 THANH TOÁN",

        use_container_width=True,

        type="primary"

    ):

        st.success(

            f"✅ Thanh toán thành công! "

            f"Tổng tiền: {tong_tien:,} VNĐ"

        )

        # Tên file hóa đơn

        ten_file = (

            f"hoa_don_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"

        )

        st.download_button(

            label="📥 Tải hóa đơn",

            data=noi_dung_hoa_don,

            file_name=ten_file,

            mime="text/plain",

            use_container_width=True

        )

    # =========================

    # XÓA HÓA ĐƠN

    # =========================

    if st.button(

        "🗑️ Xóa hóa đơn",

        use_container_width=True

    ):

        st.session_state.cart = []

        st.rerun()
