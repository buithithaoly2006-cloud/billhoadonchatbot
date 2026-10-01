import streamlit as st

import sqlite3
st.image("logo.JPG")
from datetime import datetime

import requests

# =========================================================

# CẤU HÌNH TRANG

# =========================================================

st.set_page_config(

    page_title="Quán Trà Sữa",

    page_icon="🧋",

    layout="wide"

)

# =========================================================

# THÔNG TIN QUÁN

# =========================================================

TEN_QUAN = "🧋 QUÁN TRÀ SỮA"

DIA_CHI = "📍 Lê Hồng Phong, Phú Lợi"

# =========================================================

# MENU

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

SIZE = {

    "S": 0,

    "M": 5000,

    "L": 10000

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

# =========================================================

# DATABASE TÍCH ĐIỂM

# =========================================================

conn = sqlite3.connect("tich_diem.db", check_same_thread=False)

cursor = conn.cursor()

cursor.execute("""

CREATE TABLE IF NOT EXISTS khach_hang (

    so_dien_thoai TEXT PRIMARY KEY,

    ten_khach TEXT,

    diem INTEGER DEFAULT 0

)

""")

conn.commit()

def lay_diem(so_dien_thoai):

    if not so_dien_thoai:

        return 0

    cursor.execute(

        "SELECT diem FROM khach_hang WHERE so_dien_thoai = ?",

        (so_dien_thoai,)

    )

    result = cursor.fetchone()

    if result:

        return result[0]

    return 0

def cap_nhat_diem(so_dien_thoai, ten_khach, diem_cong):

    if not so_dien_thoai:

        return

    cursor.execute(

        "SELECT diem FROM khach_hang WHERE so_dien_thoai = ?",

        (so_dien_thoai,)

    )

    result = cursor.fetchone()

    if result:

        cursor.execute(

            """

            UPDATE khach_hang

            SET ten_khach = ?, diem = diem + ?

            WHERE so_dien_thoai = ?

            """,

            (ten_khach, diem_cong, so_dien_thoai)

        )

    else:

        cursor.execute(

            """

            INSERT INTO khach_hang

            (so_dien_thoai, ten_khach, diem)

            VALUES (?, ?, ?)

            """,

            (so_dien_thoai, ten_khach, diem_cong)

        )

    conn.commit()

# =========================================================

# API OPENROUTER

# =========================================================

try:

    OPENROUTER_API_KEY = st.secrets["OPENROUTER_API_KEY"]

except Exception:

    OPENROUTER_API_KEY = ""

def tra_loi_chatbot(cau_hoi, lich_su_chat):

    if not OPENROUTER_API_KEY:

        return (

            "⚠️ Chưa tìm thấy OpenRouter API Key.\n\n"

            "Bạn hãy tạo file:\n"

            ".streamlit/secrets.toml\n\n"

            "và thêm:\n"

            'OPENROUTER_API_KEY = "KEY_CUA_BAN"'

        )

    menu_text = "\n".join(

        [f"- {ten}: {gia:,} VNĐ" for ten, gia in MENU.items()]

    )

    size_text = "\n".join(

        [f"- Size {size}: +{gia:,} VNĐ" for size, gia in SIZE.items()]

    )

    topping_text = "\n".join(

        [f"- {ten}: +{gia:,} VNĐ" for ten, gia in TOPPINGS.items()]

    )

    system_prompt = f"""

Bạn là chatbot của {TEN_QUAN}.

Địa chỉ:

{DIA_CHI}

Bạn chuyên tư vấn cho khách hàng về quán trà sữa.

MENU:

{menu_text}

GIÁ SIZE:

{size_text}

TOPPING:

{topping_text}

QUY ĐỊNH:

- 10.000 VNĐ = 1 điểm tích lũy.

- Trả lời bằng tiếng Việt.

- Trả lời thân thiện, dễ hiểu, ngắn gọn.

- Khi khách hỏi giá, hãy dựa đúng menu ở trên.

- Không tự bịa thêm món hoặc giá không có trong menu.

- Nếu khách hỏi món nào ngon, có thể gợi ý dựa trên menu.

- Nếu khách hỏi tổng tiền, hãy hướng dẫn họ chọn món trong phần đặt hàng.

- Nếu khách hỏi về tích điểm, giải thích 10.000 VNĐ = 1 điểm.

"""

    messages = [

        {

            "role": "system",

            "content": system_prompt

        }

    ]

    # Thêm lịch sử trò chuyện

    for message in lich_su_chat[-10:]:

        messages.append(message)

    messages.append({

        "role": "user",

        "content": cau_hoi

    })

    try:

        response = requests.post(

            "https://openrouter.ai/api/v1/chat/completions",

            headers={

                "Authorization": f"Bearer {OPENROUTER_API_KEY}",

                "Content-Type": "application/json"

            },

            json={

                # Router miễn phí

                "model": "openrouter/free",

                "messages": messages,

                "temperature": 0.7,

                "max_tokens": 500

            },

            timeout=60

        )

        if response.status_code != 200:

            try:

                error_data = response.json()

                return (

                    "❌ OpenRouter báo lỗi:\n\n"

                    + str(error_data)

                )

            except:

                return (

                    f"❌ OpenRouter báo lỗi HTTP "

                    f"{response.status_code}"

                )

        data = response.json()

        if "choices" not in data:

            return "❌ Không nhận được câu trả lời từ AI."

        return data["choices"][0]["message"]["content"]

    except requests.exceptions.Timeout:

        return "⏰ Chatbot phản hồi quá lâu. Bạn thử hỏi lại nhé."

    except requests.exceptions.RequestException as e:

        return f"❌ Không kết nối được OpenRouter: {e}"

    except Exception as e:

        return f"❌ Có lỗi xảy ra: {e}"

# =========================================================

# SESSION STATE

# =========================================================

if "lich_su_chat" not in st.session_state:

    st.session_state.lich_su_chat = []

if "hoa_don" not in st.session_state:

    st.session_state.hoa_don = ""

if "da_thanh_toan" not in st.session_state:

    st.session_state.da_thanh_toan = False

# =========================================================

# TIÊU ĐỀ

# =========================================================

st.title(TEN_QUAN)

st.write(DIA_CHI)

st.divider()

# =========================================================

# THÔNG TIN KHÁCH HÀNG

# =========================================================

st.subheader("👤 Thông tin khách hàng")

col1, col2 = st.columns(2)

with col1:

    ten_khach = st.text_input(

        "Tên khách hàng",

        placeholder="Nhập tên khách hàng"

    )

with col2:

    so_dien_thoai = st.text_input(

        "Số điện thoại",

        placeholder="Nhập 10 số"

    )

# =========================================================

# KIỂM TRA SỐ ĐIỆN THOẠI

# =========================================================

so_dien_thoai_hop_le = (

    so_dien_thoai.isdigit()

    and len(so_dien_thoai) == 10

)

diem_hien_tai = 0

if so_dien_thoai_hop_le:

    diem_hien_tai = lay_diem(so_dien_thoai)

    st.info(

        f"⭐ Điểm hiện tại của khách hàng: "

        f"**{diem_hien_tai} điểm**"

    )

elif so_dien_thoai:

    st.warning("⚠️ Số điện thoại phải gồm đúng 10 chữ số.")

st.divider()

# =========================================================

# CHỌN MÓN

# =========================================================

st.subheader("🧋 Chọn món")

mon_da_chon = st.multiselect(

    "Chọn một hoặc nhiều món:",

    list(MENU.keys())

)

# =========================================================

# CẤU HÌNH TỪNG MÓN

# =========================================================

gio_hang = []

for i, mon in enumerate(mon_da_chon):

    st.markdown(f"### 🥤 {mon}")

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:

        size = st.selectbox(

            "Size",

            list(SIZE.keys()),

            key=f"size_{i}"

        )

    with col2:

        so_luong = st.number_input(

            "Số lượng",

            min_value=1,

            max_value=20,

            value=1,

            step=1,

            key=f"sl_{i}"

        )

    with col3:

        duong = st.selectbox(

            "Đường",

            ["100%", "70%", "0%"],

            key=f"duong_{i}"

        )

    with col4:

        da = st.selectbox(

            "Đá",

            ["100%", "70%", "0%"],

            key=f"da_{i}"

        )

    with col5:

        topping = st.selectbox(

            "Topping",

            list(TOPPINGS.keys()),

            key=f"topping_{i}"

        )

    gia_1_ly = (

        MENU[mon]

        + SIZE[size]

        + TOPPINGS[topping]

    )

    thanh_tien = gia_1_ly * so_luong

    gio_hang.append({

        "mon": mon,

        "size": size,

        "so_luong": so_luong,

        "duong": duong,

        "da": da,

        "topping": topping,

        "gia": gia_1_ly,

        "thanh_tien": thanh_tien

    })

    st.caption(

        f"💰 {gia_1_ly:,} VNĐ/ly | "

        f"Thành tiền: **{thanh_tien:,} VNĐ**"

    )

    st.divider()

# =========================================================

# GIỎ HÀNG

# =========================================================

if gio_hang:

    st.subheader("🛒 Giỏ hàng")

    tong_tien = 0

    for item in gio_hang:

        st.write(

            f"**{item['mon']}** - "

            f"Size {item['size']} - "

            f"{item['so_luong']} ly - "

            f"Đường {item['duong']} - "

            f"Đá {item['da']} - "

            f"{item['topping']} - "

            f"**{item['thanh_tien']:,} VNĐ**"

        )

        tong_tien += item["thanh_tien"]

    st.divider()

    col1, col2 = st.columns(2)

    with col1:

        st.metric(

            "💰 Tổng tiền",

            f"{tong_tien:,} VNĐ"

        )

    with col2:

        diem_duoc_cong = tong_tien // 10000

        st.metric(

            "⭐ Điểm nhận được",

            f"{diem_duoc_cong} điểm"

        )

    # =====================================================

    # THANH TOÁN

    # =====================================================

    st.subheader("💳 Thanh toán")

    phuong_thuc = st.radio(

        "Chọn phương thức thanh toán:",

        [

            "Tiền mặt",

            "Chuyển khoản",

            "Ví điện tử"

        ],

        horizontal=True

    )

    if st.button(

        "💵 THANH TOÁN",

        use_container_width=True

    ):

        if not ten_khach.strip():

            st.error("⚠️ Vui lòng nhập tên khách hàng.")

        elif not so_dien_thoai_hop_le:

            st.error(

                "⚠️ Vui lòng nhập số điện thoại gồm đúng 10 số."

            )

        else:

            # Cộng điểm

            cap_nhat_diem(

                so_dien_thoai,

                ten_khach,

                diem_duoc_cong

            )

            thoi_gian = datetime.now().strftime(

                "%d/%m/%Y %H:%M:%S"

            )

            # =============================================

            # TẠO HÓA ĐƠN

            # =============================================

            hoa_don = ""

            hoa_don += "=" * 45 + "\n"

            hoa_don += f"{TEN_QUAN}\n"

            hoa_don += f"{DIA_CHI}\n"

            hoa_don += "=" * 45 + "\n"

            hoa_don += f"Khách hàng: {ten_khach}\n"

            hoa_don += f"Số điện thoại: {so_dien_thoai}\n"

            hoa_don += f"Thời gian: {thoi_gian}\n"

            hoa_don += "-" * 45 + "\n"

            for item in gio_hang:

                hoa_don += (

                    f"{item['mon']}\n"

                    f"  Size: {item['size']}\n"

                    f"  Số lượng: {item['so_luong']}\n"

                    f"  Đường: {item['duong']}\n"

                    f"  Đá: {item['da']}\n"

                    f"  Topping: {item['topping']}\n"

                    f"  Thành tiền: "

                    f"{item['thanh_tien']:,} VNĐ\n"

                )

            hoa_don += "-" * 45 + "\n"

            hoa_don += (

                f"TỔNG TIỀN: {tong_tien:,} VNĐ\n"

            )

            hoa_don += (

                f"Thanh toán: {phuong_thuc}\n"

            )

            hoa_don += (

                f"Điểm được cộng: {diem_duoc_cong}\n"

            )

            diem_moi = lay_diem(so_dien_thoai)

            hoa_don += (

                f"Tổng điểm hiện tại: {diem_moi}\n"

            )

            hoa_don += "=" * 45 + "\n"

            hoa_don += "Cảm ơn quý khách! ❤️\n"

            hoa_don += "=" * 45

            st.session_state.hoa_don = hoa_don

            st.session_state.da_thanh_toan = True

            st.success(

                "✅ Thanh toán thành công!"

            )

            st.balloons()

# =========================================================

# HÓA ĐƠN

# =========================================================

if st.session_state.hoa_don:

    st.divider()

    st.subheader("🧾 HÓA ĐƠN")

    st.code(

        st.session_state.hoa_don,

        language="text"

    )

    st.download_button(

        label="📥 TẢI HÓA ĐƠN",

        data=st.session_state.hoa_don,

        file_name="hoa_don_tra_sua.txt",

        mime="text/plain",

        use_container_width=True

    )

# =========================================================

# CHATBOT AI

# =========================================================

st.divider()

st.header("🤖 CHATBOT")

st.caption(

    "Bạn có thể hỏi chatbot về menu, giá món, size, "

    "topping và tích điểm."

)

# Hiển thị lịch sử

for message in st.session_state.lich_su_chat:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])

# Ô nhập chatbot

cau_hoi = st.chat_input(

    "Ví dụ: Trà sữa matcha size L bao nhiêu tiền?"

)

if cau_hoi:

    # Hiển thị câu hỏi

    st.session_state.lich_su_chat.append({

        "role": "user",

        "content": cau_hoi

    })

    with st.chat_message("user"):

        st.markdown(cau_hoi)

    # AI trả lời

    with st.chat_message("assistant"):

        with st.spinner("🤖 Chatbot đang trả lời..."):

            cau_tra_loi = tra_loi_chatbot(

                cau_hoi,

                st.session_state.lich_su_chat[:-1]

            )

        st.markdown(cau_tra_loi)

    st.session_state.lich_su_chat.append({

        "role": "assistant",

        "content": cau_tra_loi

    })

# =========================================================

# XÓA LỊCH SỬ CHAT

# =========================================================

if st.session_state.lich_su_chat:

    if st.button("🗑️ Xóa lịch sử chatbot"):

        st.session_state.lich_su_chat = []

        st.rerun()

# =========================================================

# TẠO HÓA ĐƠN MỚI

# =========================================================

st.divider()

if st.button(

    "🔄 TẠO HÓA ĐƠN MỚI",

    use_container_width=True

):

    st.session_state.hoa_don = ""

    st.session_state.da_thanh_toan = False

    st.session_state.lich_su_chat = []

    st.rerun()
