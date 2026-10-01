# =====================================================

# CHATBOX TƯ VẤN KHÁCH HÀNG

# =====================================================

st.divider()

st.header("💬 CHATBOX TƯ VẤN")

# Lưu lịch sử chat

if "messages" not in st.session_state:

    st.session_state.messages = []

# Hiển thị tin nhắn cũ

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.write(message["content"])

# Hàm tạo câu trả lời

def tra_loi_chat(cau_hoi):

    cau_hoi = cau_hoi.lower()

    # -----------------------------

    # CHÀO HỎI

    # -----------------------------

    if any(

        tu in cau_hoi

        for tu in ["xin chào", "chào", "hello", "hi"]

    ):

        return (

            "👋 Xin chào! Mình là chatbot của "

            "🧋 Quán Trà Sữa. "

            "Mình có thể tư vấn về món, giá, size, "

            "topping, tích điểm và địa chỉ quán nhé!"

        )

    # -----------------------------

    # ĐỊA CHỈ

    # -----------------------------

    elif any(

        tu in cau_hoi

        for tu in ["địa chỉ", "ở đâu", "địa điểm"]

    ):

        return (

            f"📍 Quán mình ở: "

            f"{DIA_CHI.replace('📍 ', '')}"

        )

    # -----------------------------

    # MENU

    # -----------------------------

    elif any(

        tu in cau_hoi

        for tu in ["menu", "có món", "món gì", "thức uống"]

    ):

        danh_sach = "\n".join(

            [

                f"🥤 {mon}: {gia:,} VNĐ"

                for mon, gia in MENU.items()

            ]

        )

        return (

            "🧋 MENU CỦA QUÁN:\n\n"

            + danh_sach

        )

    # -----------------------------

    # SIZE

    # -----------------------------

    elif any(

        tu in cau_hoi

        for tu in ["size", "kích thước", "cỡ"]

    ):

        return (

            "🥤 Quán có 3 size:\n\n"

            "• Size S: giá gốc\n"

            "• Size M: +5.000 VNĐ\n"

            "• Size L: +10.000 VNĐ"

        )

    # -----------------------------

    # TOPPING

    # -----------------------------

    elif any(

        tu in cau_hoi

        for tu in ["topping", "trân châu", "pudding", "kem cheese"]

    ):

        danh_sach = "\n".join(

            [

                f"• {topping}: "

                f"{gia:,} VNĐ"

                for topping, gia in TOPPINGS.items()

            ]

        )

        return (

            "🍮 TOPPING:\n\n"

            + danh_sach

        )

    # -----------------------------

    # GIÁ

    # -----------------------------

    elif any(

        tu in cau_hoi

        for tu in ["giá", "bao nhiêu tiền", "bao nhiêu"]

    ):

        return (

            "💰 Giá trà sữa hiện tại từ "

            "25.000 - 38.000 VNĐ.\n\n"

            "Size M +5.000 VNĐ và Size L +10.000 VNĐ.\n"

            "Topping sẽ cộng thêm tùy loại."

        )

    # -----------------------------

    # TÍCH ĐIỂM

    # -----------------------------

    elif any(

        tu in cau_hoi

        for tu in ["tích điểm", "điểm", "thành viên"]

    ):

        return (

            "⭐ Chính sách tích điểm:\n\n"

            "Cứ 10.000 VNĐ = 1 điểm.\n"

            "Điểm được lưu theo số điện thoại "

            "của khách hàng."

        )

    # -----------------------------

    # ĐƯỜNG

    # -----------------------------

    elif any(

        tu in cau_hoi

        for tu in ["đường", "ngọt"]

    ):

        return (

            "🍬 Quán có 3 mức đường:\n\n"

            "• 100%: ngọt bình thường\n"

            "• 70%: ít ngọt\n"

            "• 0%: không đường"

        )

    # -----------------------------

    # ĐÁ

    # -----------------------------

    elif any(

        tu in cau_hoi

        for tu in ["đá", "lạnh"]

    ):

        return (

            "🧊 Quán có 3 mức đá:\n\n"

            "• 100%: đá bình thường\n"

            "• 70%: ít đá\n"

            "• 0%: không đá"

        )

    # -----------------------------

    # CẢM ƠN

    # -----------------------------

    elif any(

        tu in cau_hoi

        for tu in ["cảm ơn", "thanks", "thank"]

    ):

        return (

            "🥰 Cảm ơn bạn đã ủng hộ quán! "

            "Chúc bạn uống trà sữa thật ngon nhé! 🧋❤️"

        )

    # -----------------------------

    # KHÔNG HIỂU

    # -----------------------------

    else:

        return (

            "🤖 Mình chưa hiểu câu hỏi này.\n\n"

            "Bạn có thể hỏi mình:\n"

            "• Menu có món gì?\n"

            "• Giá bao nhiêu?\n"

            "• Có size S/M/L không?\n"

            "• Có topping gì?\n"

            "• Địa chỉ quán ở đâu?\n"

            "• Cách tích điểm như thế nào?"

        )

# Ô nhập câu hỏi

cau_hoi = st.chat_input(

    "💬 Nhập câu hỏi cho quán..."

)

if cau_hoi:

    # Tin nhắn khách hàng

    st.session_state.messages.append(

        {

            "role": "user",

            "content": cau_hoi

        }

    )

    # Chatbot trả lời

    cau_tra_loi = tra_loi_chat(cau_hoi)

    st.session_state.messages.append(

        {

            "role": "assistant",

            "content": cau_tra_loi

        }

    )

    st.rerun()
