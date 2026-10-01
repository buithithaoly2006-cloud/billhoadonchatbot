import streamlit as st

from datetime import datetime
st.image("logo.JPG")
import sqlite3

# =========================================================

# CẤU HÌNH

# =========================================================

st.set_page_config(

    page_title="Quán Trà Sữa",

    page_icon="🧋",

    layout="centered"

)

# =========================================================

# KẾT NỐI DATABASE TÍCH ĐIỂM

# =========================================================

conn = sqlite3.connect(

    "tich_diem.db",

    check_same_thread=False

)

cursor = conn.cursor()

cursor.execute("""

CREATE TABLE IF NOT EXISTS khach_hang (

    so_dien_thoai TEXT PRIMARY KEY,

    ten_khach TEXT,

    diem INTEGER DEFAULT 0

)

""")

conn.commit()

# =========================================================

# THÔNG TIN QUÁN

# =========================================================

TEN_QUAN = "🧋 QUÁN TRÀ SỮA"

DIA_CHI = "📍 Lê Hồng Phong, Phú Lợi"

# =========================================================

# MENU TRÀ SỮA

# =========================================================

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

# =========================================================

# SIZE

# =========================================================

SIZE = {

    "S": 0,

    "M": 5000,

    "L": 10000

}

# =========================================================

# TOPPING

# =========================================================

TOPPINGS = {

    "Không topping": 0,

    "Trân châu đen": 5000,

    "Trân châu trắng": 5000,

    "Thạch trái cây": 5000,

    "Pudding trứng": 7000,

    "Kem cheese": 8000,

    "Trân châu hoàng kim": 7000

}

# =========================================================

# SESSION STATE

# =========================================================

if "cart" not in st.session_state:

    st.session_state.cart = []

if "payment_done" not in st.session_state:

    st.session_state.payment_done = False

if "invoice" not in st.session_state:

    st.session_state.invoice = ""

if "points_earned" not in st.session_state:

    st.session_state.points_earned = 0

if "total_points" not in st.session_state:

    st.session_state.total_points = 0

# =========================================================

# HÀM LẤY ĐIỂM

# =========================================================

def lay_diem(so_dien_thoai):

    cursor.execute(

        """

        SELECT diem

        FROM khach_hang

        WHERE so_dien_thoai = ?

        """,

        (so_dien_thoai,)

    )

    result = cursor.fetchone()

    if result:

        return result[0]

    return 0

# =========================================================

# TIÊU ĐỀ

# =========================================================

st.title(TEN_QUAN)

st.write(

    f"**{DIA_CHI}**"

)

st.subheader("🧾 TÍNH HÓA ĐƠN")

st.divider()

# =========================================================

# THÔNG TIN KHÁCH HÀNG

# =========================================================

st.header("👤 Thông tin khách hàng")

ten_khach = st.text_input(

    "Tên khách hàng",

    placeholder="Nhập tên khách hàng..."

)

so_dien_thoai = st.text_input(

    "📱 Số điện thoại",

    placeholder="Nhập số điện thoại 10 số...",

    max_chars=10

)

diem_hien_tai = 0

if so_dien_thoai:

    if so_dien_thoai.isdigit() and len(so_dien_thoai) == 10:

        diem_hien_tai = lay_diem(so_dien_thoai)

        st.success(

            f"⭐ Khách hàng hiện có: "

            f"**{diem_hien_tai} điểm**"

        )

    elif not so_dien_thoai.isdigit():

        st.warning(

            "⚠️ Số điện thoại chỉ được nhập số!"

        )

    elif len(so_dien_thoai) != 10:

        st.warning(

            "⚠️ Số điện thoại phải có 10 số!"

        )

st.divider()

# =========================================================

# CHỌN NHIỀU MÓN

# =========================================================

st.header("🧋 Chọn món")

st.write(

    "Bạn có thể chọn **nhiều loại trà sữa cùng lúc**:"

)

danh_sach_mon = st.multiselect(

    "Chọn loại trà sữa",

    list(MENU.keys()),

    placeholder="Chọn một hoặc nhiều món..."

)

# =========================================================

# CẤU HÌNH TỪNG MÓN

# =========================================================

cac_mon_da_chon = []

if danh_sach_mon:

    st.subheader("⚙️ Tùy chỉnh từng món")

    for index, mon in enumerate(danh_sach_mon):

        with st.container(border=True):

            st.markdown(

                f"### 🧋 {index + 1}. {mon}"

            )

            # -----------------------------

            # SIZE

            # -----------------------------

            size = st.radio(

                "🥤 Size",

                ["S", "M", "L"],

                horizontal=True,

                key=f"size_{index}_{mon}"

            )

            col1, col2 = st.columns(2)

            with col1:

                so_luong = st.number_input(

                    "Số lượng",

                    min_value=1,

                    max_value=20,

                    value=1,

                    step=1,

                    key=f"so_luong_{index}_{mon}"

                )

                muc_duong = st.selectbox(

                    "Mức độ đường",

                    ["100%", "70%", "0%"],

                    key=f"duong_{index}_{mon}"

                )

            with col2:

                topping = st.selectbox(

                    "Topping",

                    list(TOPPINGS.keys()),

                    key=f"topping_{index}_{mon}"

                )

                muc_da = st.selectbox(

                    "Mức độ đá",

                    ["100%", "70%", "0%"],

                    key=f"da_{index}_{mon}"

                )

            # -----------------------------

            # TÍNH GIÁ

            # -----------------------------

            gia_mon = MENU[mon]

            gia_size = SIZE[size]

            gia_topping = TOPPINGS[topping]

            don_gia = (

                gia_mon

                + gia_size

                + gia_topping

            )

            thanh_tien = (

                don_gia

                * so_luong

            )

            st.info(

                f"🥤 Size: **{size}**  \n"

                f"💵 Đơn giá: **{don_gia:,} VNĐ**  \n"

                f"💰 Thành tiền: **{thanh_tien:,} VNĐ**"

            )

            # Lưu món

            cac_mon_da_chon.append({

                "mon": mon,

                "size": size,

                "so_luong": so_luong,

                "topping": topping,

                "duong": muc_duong,

                "da": muc_da,

                "don_gia": don_gia,

                "thanh_tien": thanh_tien

            })

# =========================================================

# TẠM TÍNH

# =========================================================

if cac_mon_da_chon:

    tong_tam_tinh = sum(

        item["thanh_tien"]

        for item in cac_mon_da_chon

    )

    st.subheader("💰 TẠM TÍNH")

    st.metric(

        label="Tổng tiền các món đã chọn",

        value=f"{tong_tam_tinh:,} VNĐ"

    )

# =========================================================

# THÊM TẤT CẢ MÓN

# =========================================================

if st.button(

    "➕ THÊM TẤT CẢ MÓN VÀO HÓA ĐƠN",

    use_container_width=True

):

    if ten_khach.strip() == "":

        st.warning(

            "⚠️ Vui lòng nhập tên khách hàng!"

        )

    elif (

        not so_dien_thoai.isdigit()

        or len(so_dien_thoai) != 10

    ):

        st.warning(

            "⚠️ Vui lòng nhập số điện thoại "

            "hợp lệ gồm 10 số!"

        )

    elif len(danh_sach_mon) == 0:

        st.warning(

            "⚠️ Vui lòng chọn ít nhất một món!"

        )

    else:

        for item in cac_mon_da_chon:

            st.session_state.cart.append(item)

        st.success(

            f"✅ Đã thêm "

            f"**{len(cac_mon_da_chon)} món** "

            f"vào hóa đơn!"

        )

# =========================================================

# HÓA ĐƠN

# =========================================================

st.divider()

st.header("🧾 HÓA ĐƠN")

if len(st.session_state.cart) == 0:

    st.info(

        "Chưa có món nào trong hóa đơn."

    )

else:

    tong_tien = 0

    for i, item in enumerate(

        st.session_state.cart

    ):

        tong_tien += item["thanh_tien"]

        st.markdown(

            f"### 🧋 {i + 1}. {item['mon']}"

        )

        col1, col2 = st.columns(2)

        with col1:

            st.write(

                f"**Size:** "

                f"{item['size']}"

            )

            st.write(

                f"**Số lượng:** "

                f"{item['so_luong']}"

            )

            st.write(

                f"**Topping:** "

                f"{item['topping']}"

            )

            st.write(

                f"**Đường:** "

                f"{item['duong']}"

            )

        with col2:

            st.write(

                f"**Đá:** "

                f"{item['da']}"

            )

            st.write(

                f"**Đơn giá:** "

                f"{item['don_gia']:,} VNĐ"

            )

            st.write(

                f"**Thành tiền:** "

                f"{item['thanh_tien']:,} VNĐ"

            )

        st.divider()

    # =====================================================

    # TỔNG TIỀN

    # =====================================================

    st.subheader("💰 TỔNG THANH TOÁN")

    st.metric(

        label="Số tiền cần thanh toán",

        value=f"{tong_tien:,} VNĐ"

    )

    # =====================================================

    # TÍCH ĐIỂM

    # =====================================================

    diem_duoc_tich = tong_tien // 10000

    st.info(

        f"⭐ Đơn hàng này được tích: "

        f"**{diem_duoc_tich} điểm**"

    )

    st.divider()

    # =====================================================

    # THANH TOÁN

    # =====================================================

    if not st.session_state.payment_done:

        if st.button(

            "💳 THANH TOÁN",

            use_container_width=True,

            type="primary"

        ):

            if ten_khach.strip() == "":

                st.warning(

                    "⚠️ Vui lòng nhập tên khách hàng!"

                )

            elif (

                not so_dien_thoai.isdigit()

                or len(so_dien_thoai) != 10

            ):

                st.warning(

                    "⚠️ Số điện thoại phải có 10 số!"

                )

            else:

                # -----------------------------------------

                # KIỂM TRA KHÁCH HÀNG

                # -----------------------------------------

                cursor.execute(

                    """

                    SELECT diem

                    FROM khach_hang

                    WHERE so_dien_thoai = ?

                    """,

                    (so_dien_thoai,)

                )

                result = cursor.fetchone()

                # -----------------------------------------

                # KHÁCH HÀNG CŨ

                # -----------------------------------------

                if result:

                    diem_cu = result[0]

                    diem_moi = (

                        diem_cu

                        + diem_duoc_tich

                    )

                    cursor.execute(

                        """

                        UPDATE khach_hang

                        SET ten_khach = ?,

                            diem = ?

                        WHERE so_dien_thoai = ?

                        """,

                        (

                            ten_khach,

                            diem_moi,

                            so_dien_thoai

                        )

                    )

                # -----------------------------------------

                # KHÁCH HÀNG MỚI

                # -----------------------------------------

                else:

                    diem_moi = diem_duoc_tich

                    cursor.execute(

                        """

                        INSERT INTO khach_hang

                        (

                            so_dien_thoai,

                            ten_khach,

                            diem

                        )

                        VALUES (?, ?, ?)

                        """,

                        (

                            so_dien_thoai,

                            ten_khach,

                            diem_moi

                        )

                    )

                conn.commit()

                # -----------------------------------------

                # TẠO HÓA ĐƠN

                # -----------------------------------------

                thoi_gian = datetime.now().strftime(

                    "%d/%m/%Y %H:%M:%S"

                )

                noi_dung_hoa_don = ""

                noi_dung_hoa_don += (

                    "============================================\n"

                )

                noi_dung_hoa_don += (

                    "              HOA DON TRA SUA\n"

                )

                noi_dung_hoa_don += (

                    f"Dia chi: "

                    f"{DIA_CHI.replace('📍 ', '')}\n"

                )

                noi_dung_hoa_don += (

                    "============================================\n"

                )

                noi_dung_hoa_don += (

                    f"Khach hang: "

                    f"{ten_khach}\n"

                )

                noi_dung_hoa_don += (

                    f"So dien thoai: "

                    f"{so_dien_thoai}\n"

                )

                noi_dung_hoa_don += (

                    f"Thoi gian: "

                    f"{thoi_gian}\n"

                )

                noi_dung_hoa_don += (

                    "--------------------------------------------\n"

                )

                # -----------------------------------------

                # CHI TIẾT MÓN

                # -----------------------------------------

                for i, item in enumerate(

                    st.session_state.cart

                ):

                    noi_dung_hoa_don += (

                        f"\n{i + 1}. "

                        f"{item['mon']}\n"

                    )

                    noi_dung_hoa_don += (

                        f"   Size: "

                        f"{item['size']}\n"

                    )

                    noi_dung_hoa_don += (

                        f"   So luong: "

                        f"{item['so_luong']}\n"

                    )

                    noi_dung_hoa_don += (

                        f"   Topping: "

                        f"{item['topping']}\n"

                    )

                    noi_dung_hoa_don += (

                        f"   Muc duong: "

                        f"{item['duong']}\n"

                    )

                    noi_dung_hoa_don += (

                        f"   Muc da: "

                        f"{item['da']}\n"

                    )

                    noi_dung_hoa_don += (

                        f"   Don gia: "

                        f"{item['don_gia']:,} VND\n"

                    )

                    noi_dung_hoa_don += (

                        f"   Thanh tien: "

                        f"{item['thanh_tien']:,} VND\n"

                    )

                # -----------------------------------------

                # TỔNG HÓA ĐƠN

                # -----------------------------------------

                noi_dung_hoa_don += (

                    "\n--------------------------------------------\n"

                )

                noi_dung_hoa_don += (

                    f"TONG THANH TOAN: "

                    f"{tong_tien:,} VND\n"

                )

                noi_dung_hoa_don += (

                    f"Diem tich them: "

                    f"{diem_duoc_tich} diem\n"

                )

                noi_dung_hoa_don += (

                    f"Tong diem: "

                    f"{diem_moi} diem\n"

                )

                noi_dung_hoa_don += (

                    "============================================\n"

                )

                noi_dung_hoa_don += (

                    "           CAM ON QUY KHACH!\n"

                )

                noi_dung_hoa_don += (

                    "============================================\n"

                )

                # -----------------------------------------

                # LƯU TRẠNG THÁI

                # -----------------------------------------

                st.session_state.payment_done = True

                st.session_state.invoice = (

                    noi_dung_hoa_don

                )

                st.session_state.points_earned = (

                    diem_duoc_tich

                )

                st.session_state.total_points = (

                    diem_moi

                )

                st.rerun()

    # =====================================================

    # SAU KHI THANH TOÁN

    # =====================================================

    if st.session_state.payment_done:

        st.success(

            "✅ THANH TOÁN THÀNH CÔNG!"

        )

        st.success(

            f"⭐ Bạn được cộng "

            f"**{st.session_state.points_earned} điểm**"

        )

        st.info(

            f"🎁 Tổng điểm hiện tại: "

            f"**{st.session_state.total_points} điểm**"

        )

        # =================================================

        # TẢI HÓA ĐƠN

        # =================================================

        ten_file = (

            "hoa_don_"

            + datetime.now().strftime(

                "%Y%m%d_%H%M%S"

            )

            + ".txt"

        )

        st.download_button(

            label="📥 TẢI HÓA ĐƠN",

            data=st.session_state.invoice,

            file_name=ten_file,

            mime="text/plain",

            use_container_width=True

        )

    # =====================================================

    # TẠO HÓA ĐƠN MỚI

    # =====================================================

    if st.button(

        "🗑️ TẠO HÓA ĐƠN MỚI",

        use_container_width=True

    ):

        st.session_state.cart = []

        st.session_state.payment_done = False

        st.session_state.invoice = ""

        st.session_state.points_earned = 0

        st.session_state.total_points = 0

        st.rer
