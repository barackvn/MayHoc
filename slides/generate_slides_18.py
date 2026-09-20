"""Tạo bộ slide 18 trang chuẩn Visual & Metric-First theo phong cách UIT cho Đồ Án Môn Học Máy Học:
Phân loại ảnh cháy rừng (DeepFire Dataset).
Bám sát 100% cấu trúc 10 mục của Thầy, chứa đầy đủ các bảng báo cáo (Classification Report,
Confusion Matrix, Overfitting, EDA, Error Analysis...).
"""

import os
import sys
from pathlib import Path

# Đảm bảo stdout UTF-8
sys.stdout.reconfigure(encoding='utf-8')

import pptx
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

# Đường dẫn thư mục
BASE_DIR = Path(__file__).resolve().parent.parent  # MayHoc folder
FIG_DIR = BASE_DIR / 'reports' / 'figures'
OUT_PPTX = BASE_DIR / 'slides' / 'Bao_cao_MayHoc_Chay_rung.pptx'

# =============================================================================
# BẢNG MÀU CHUẨN VISUAL & METRIC-FIRST (PHONG CÁCH UIT CHUẨN KHOA HỌC)
# =============================================================================
COLOR_PRIMARY_BLUE = RGBColor(0x15, 0x65, 0xC0)    # Xanh UIT #1565C0
COLOR_DARK_NAVY    = RGBColor(0x0D, 0x47, 0xA1)    # Xanh đậm #0D47A1
COLOR_CYAN_ACCENT  = RGBColor(0x00, 0x83, 0x8F)    # Xanh cổ vịt nhấn số #00838F
COLOR_LIGHT_BLUE   = RGBColor(0xBB, 0xDE, 0xFB)    # Viền xanh #BBDEFB
COLOR_BG_CARD      = RGBColor(0xF8, 0xFA, 0xFC)    # Nền xám nhẹ #F8FAFC
COLOR_CARD_BORDER  = RGBColor(0xCB, 0xD5, 0xE1)    # Viền thẻ #CBD5E1
COLOR_BG_METRIC    = RGBColor(0xEE, 0xF6, 0xFF)    # Nền khối số xanh nhạt #EEF6FF
COLOR_BORDER_METRIC= RGBColor(0x90, 0xCA, 0xF9)    # Viền khối số #90CAF9
COLOR_BG_ALERT     = RGBColor(0xFF, 0xEB, 0xEE)    # Nền cảnh báo đỏ nhạt #FFEBEE
COLOR_BORDER_ALERT = RGBColor(0xEF, 0x9A, 0x9A)    # Viền đỏ cảnh báo #EF9A9A
COLOR_CALLOUT_BG   = RGBColor(0xFF, 0xF8, 0xE1)    # Nền cam mềm #FFF8E1
COLOR_CALLOUT_LINE = RGBColor(0xFF, 0x6F, 0x00)    # Viền cam #FF6F00
COLOR_TEXT_MAIN    = RGBColor(0x0F, 0x17, 0x2A)    # Chữ than đậm
COLOR_TEXT_MUTED   = RGBColor(0x47, 0x55, 0x69)    # Chữ phụ
COLOR_WHITE        = RGBColor(0xFF, 0xFF, 0xFF)    # Trắng
COLOR_GREEN_SOTA   = RGBColor(0x2E, 0x7D, 0x32)    # Xanh lá điểm SOTA
COLOR_RED_ALERT    = RGBColor(0xC6, 0x28, 0x28)    # Đỏ cảnh báo

FONT_NAME = "Arial"

def build_presentation():
    prs = Presentation()
    # Màn ảnh rộng 16:9 (21678900 x 12192000 EMU)
    prs.slide_width = 21678900
    prs.slide_height = 12192000
    blank_layout = prs.slide_layouts[6]

    CHAPTER_TABS = [
        "1. Mục Tiêu & Dữ Liệu",
        "2. EDA & Tiền Xử Lý",
        "3. Mô Hình & Tuning",
        "4. Kết Quả & Đánh Giá",
        "5. Phân Tích Lỗi & Kết Luận"
    ]

    def add_nav_bar(slide, active_idx):
        if active_idx is None:
            return
        bar_height = 720000
        tab_width = prs.slide_width // len(CHAPTER_TABS)
        
        base_bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, bar_height)
        base_bar.fill.solid()
        base_bar.fill.fore_color.rgb = RGBColor(0xEA, 0xEE, 0xF4)
        base_bar.line.fill.background()

        for i, title in enumerate(CHAPTER_TABS):
            x = i * tab_width
            tab = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, 0, tab_width, bar_height)
            tab.fill.solid()
            tf = tab.text_frame; tf.word_wrap = True
            p = tf.paragraphs[0]; p.text = title; p.alignment = PP_ALIGN.CENTER
            p.font.name = FONT_NAME; p.font.size = Pt(16); p.font.bold = True
            
            if i == active_idx:
                tab.fill.fore_color.rgb = COLOR_PRIMARY_BLUE
                tab.line.fill.background()
                p.font.color.rgb = COLOR_WHITE
            else:
                tab.fill.fore_color.rgb = RGBColor(0xF1, 0xF5, 0xF9)
                tab.line.color.rgb = RGBColor(0xCB, 0xD5, 0xE1)
                tab.line.width = Pt(1)
                p.font.color.rgb = RGBColor(0x33, 0x41, 0x55)

    def add_slide_header(slide, title_text, section_tag=None):
        title_box = slide.shapes.add_textbox(1016000, 850000, 16000000, 750000)
        tf = title_box.text_frame; tf.word_wrap = True
        p = tf.paragraphs[0]; p.text = title_text
        p.font.name = FONT_NAME; p.font.size = Pt(32); p.font.bold = True; p.font.color.rgb = COLOR_DARK_NAVY

        if section_tag:
            p2 = tf.add_paragraph()
            p2.text = f"Mục tiêu môn học: {section_tag}"
            p2.font.name = FONT_NAME; p2.font.size = Pt(16); p2.font.italic = True; p2.font.bold = True; p2.font.color.rgb = COLOR_PRIMARY_BLUE

        line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 1016000, 1850000, 19642709, 50000)
        line.fill.solid(); line.fill.fore_color.rgb = COLOR_PRIMARY_BLUE; line.line.fill.background()

    def add_footer(slide, page_num, total_pages=18):
        foot_left = slide.shapes.add_textbox(1016000, 11500000, 14000000, 450000)
        tf_l = foot_left.text_frame; p_l = tf_l.paragraphs[0]
        p_l.text = "Đồ án Môn học Máy học | Phân loại ảnh cháy rừng (DeepFire Dataset) | UIT"
        p_l.font.name = FONT_NAME; p_l.font.size = Pt(15); p_l.font.color.rgb = COLOR_TEXT_MUTED

        foot_right = slide.shapes.add_textbox(18500000, 11500000, 2150000, 450000)
        tf_r = foot_right.text_frame; p_r = tf_r.paragraphs[0]
        p_r.text = f"{page_num} / {total_pages}"
        p_r.alignment = PP_ALIGN.RIGHT; p_r.font.name = FONT_NAME; p_r.font.size = Pt(18); p_r.font.bold = True; p_r.font.color.rgb = COLOR_PRIMARY_BLUE

    def add_card(slide, left, top, width, height, bg_color=COLOR_BG_CARD, border_color=COLOR_CARD_BORDER):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        card.fill.solid(); card.fill.fore_color.rgb = bg_color
        if border_color:
            card.line.color.rgb = border_color
            card.line.width = Pt(1.5)
        else:
            card.line.fill.background()
        return card

    def add_stat_box(slide, left, top, width, height, big_num, label, sublabel=None, num_color=COLOR_PRIMARY_BLUE, bg_color=COLOR_BG_METRIC, border_color=COLOR_BORDER_METRIC):
        card = add_card(slide, left, top, width, height, bg_color=bg_color, border_color=border_color)
        tbox = slide.shapes.add_textbox(left + 150000, top + 150000, width - 300000, height - 300000)
        tf = tbox.text_frame; tf.word_wrap = True
        
        p = tf.paragraphs[0]; p.text = str(big_num); p.alignment = PP_ALIGN.CENTER
        p.font.name = FONT_NAME; p.font.size = Pt(44); p.font.bold = True; p.font.color.rgb = num_color
        
        p_l = tf.add_paragraph(); p_l.text = str(label); p_l.alignment = PP_ALIGN.CENTER
        p_l.font.name = FONT_NAME; p_l.font.size = Pt(17); p_l.font.bold = True; p_l.font.color.rgb = COLOR_TEXT_MAIN
        
        if sublabel:
            p_s = tf.add_paragraph(); p_s.text = str(sublabel); p_s.alignment = PP_ALIGN.CENTER
            p_s.font.name = FONT_NAME; p_s.font.size = Pt(14); p_s.font.color.rgb = COLOR_TEXT_MUTED
        return card

    def add_notes(slide, notes_text):
        slide.notes_slide.notes_text_frame.text = notes_text

    # =========================================================================
    # SLIDE 01: TRANG BÌA (Title Slide)
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    top_bar = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, 220000)
    top_bar.fill.solid(); top_bar.fill.fore_color.rgb = COLOR_PRIMARY_BLUE; top_bar.line.fill.background()

    head_box = s1.shapes.add_textbox(1016000, 600000, 19642709, 850000)
    p = head_box.text_frame.paragraphs[0]
    p.text = "ĐẠI HỌC QUỐC GIA TP. HỒ CHÍ MINH — TRƯỜNG ĐẠI HỌC CÔNG NGHỆ THÔNG TIN (UIT)"
    p.font.name = FONT_NAME; p.font.size = Pt(18); p.font.bold = True; p.font.color.rgb = COLOR_PRIMARY_BLUE
    p_sub = head_box.text_frame.add_paragraph()
    p_sub.text = "KHOA KHOA HỌC MÁY TÍNH | BÁO CÁO ĐỒ ÁN MÔN HỌC: MÁY HỌC (MACHINE LEARNING)"
    p_sub.font.name = FONT_NAME; p_sub.font.size = Pt(16); p_sub.font.color.rgb = COLOR_TEXT_MUTED

    sep = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, 1016000, 1550000, 19642709, 50000)
    sep.fill.solid(); sep.fill.fore_color.rgb = COLOR_PRIMARY_BLUE; sep.line.fill.background()

    tbox = s1.shapes.add_textbox(1016000, 1800000, 19642709, 2100000)
    tf = tbox.text_frame; tf.word_wrap = True
    p1 = tf.paragraphs[0]
    p1.text = "ỨNG DỤNG CÁC THUẬT TOÁN HỌC MÁY TRONG PHÂN LOẠI ẢNH CHÁY RỪNG"
    p1.font.name = FONT_NAME; p1.font.size = Pt(32); p1.font.bold = True; p1.font.color.rgb = COLOR_DARK_NAVY
    p2 = tf.add_paragraph()
    p2.text = "FOREST FIRE IMAGE CLASSIFICATION | BỘ DỮ LIỆU DEEPFIRE (1.900 ẢNH)"
    p2.font.name = FONT_NAME; p2.font.size = Pt(26); p2.font.bold = True; p2.font.color.rgb = COLOR_PRIMARY_BLUE

    # Khối giảng viên & nhóm thực hiện
    gv_card = add_card(s1, 1016000, 4100000, 19642709, 1300000, bg_color=COLOR_BG_METRIC, border_color=COLOR_LIGHT_BLUE)
    gv_box = s1.shapes.add_textbox(1200000, 4200000, 19000000, 1100000)
    p_gv = gv_box.text_frame.paragraphs[0]
    p_gv.text = "Giảng viên hướng dẫn môn học: Bộ môn Trí tuệ Nhân tạo & Khoa học Dữ liệu"
    p_gv.font.name = FONT_NAME; p_gv.font.size = Pt(19); p_gv.font.bold = True; p_gv.font.color.rgb = COLOR_DARK_NAVY
    p_gv2 = gv_box.text_frame.add_paragraph()
    p_gv2.text = "Sinh viên thực hiện | Học kỳ II — Năm học 2025–2026 | Thực nghiệm chuẩn xác ngày 17/09/2026"
    p_gv2.font.name = FONT_NAME; p_gv2.font.size = Pt(16); p_gv2.font.color.rgb = COLOR_TEXT_MAIN

    # 4 khối chỉ số thực nghiệm nổi bật ngay trang bìa
    add_stat_box(s1, 1016000, 5650000, 4600000, 3200000, "1.896", "Ảnh Sử Dụng", "1.900 ảnh gốc (loại 4 ảnh trùng/nhóm)", COLOR_PRIMARY_BLUE)
    add_stat_box(s1, 6020000, 5650000, 4600000, 3200000, "4", "Mô Hình Đối Chứng", "Logistic, KNN, SVM, Random Forest", COLOR_CYAN_ACCENT)
    add_stat_box(s1, 11024000, 5650000, 4600000, 3200000, "94,03%", "F1-Score Test (SVM)", "Chốt trên Validation trước khi Test", COLOR_GREEN_SOTA)
    add_stat_box(s1, 16028000, 5650000, 4630709, 3200000, "95,26%", "Recall Lớp Cháy", "Chỉ bỏ sót 9/190 vụ cháy", COLOR_GREEN_SOTA)

    # Card tóm tắt phương pháp luận
    method_card = add_card(s1, 1016000, 9150000, 19642709, 1950000, bg_color=COLOR_CALLOUT_BG, border_color=COLOR_CALLOUT_LINE)
    mb = s1.shapes.add_textbox(1200000, 9250000, 19200000, 1750000)
    p_m = mb.text_frame.paragraphs[0]
    p_m.text = "QUY TRÌNH KHOA HỌC & TÍNH LIÊM CHÍNH HỌC THUẬT CỦA ĐỒ ÁN:"
    p_m.font.name = FONT_NAME; p_m.font.size = Pt(18); p_m.font.bold = True; p_m.font.color.rgb = COLOR_CALLOUT_LINE
    p_m2 = mb.text_frame.add_paragraph()
    p_m2.text = "• Tiền xử lý chặt chẽ: Kiểm toán trùng lặp bằng SHA-256 và dHash khoảng cách <= 4, triệt tiêu nguy cơ rò rỉ dữ liệu giữa Train và Test."
    p_m2.font.name = FONT_NAME; p_m2.font.size = Pt(15); p_m2.font.color.rgb = COLOR_TEXT_MAIN
    p_m3 = mb.text_frame.add_paragraph()
    p_m3.text = "• Trích xuất đặc trưng kết hợp Color Histogram (HSV) + HOG Texture; chuẩn hóa và giảm chiều PCA khép kín trong Sklearn Pipeline."
    p_m3.font.name = FONT_NAME; p_m3.font.size = Pt(15); p_m3.font.color.rgb = COLOR_TEXT_MAIN
    p_m4 = mb.text_frame.add_paragraph()
    p_m4.text = "• Không dùng Test để chọn tham số; toàn bộ số liệu báo cáo, Word, Slide, Notebook đều tái lập 100% từ mã nguồn tự động hóa."
    p_m4.font.name = FONT_NAME; p_m4.font.size = Pt(15); p_m4.font.color.rgb = COLOR_TEXT_MAIN

    add_notes(s1, "Kính thưa quý Thầy Cô trong Hội đồng. Hôm nay em xin trình bày đồ án môn học Máy học với đề tài: Phân loại ảnh cháy rừng bằng các thuật toán học máy kinh điển.")

    # =========================================================================
    # SLIDE 02: MỤC TIÊU CỦA ĐỒ ÁN & BÀI TOÁN (Mục 1 & 2 của Thầy)
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    add_nav_bar(s2, 0)
    add_slide_header(s2, "Mục Tiêu Đồ Án & Định Nghĩa Bài Toán Phân Loại", section_tag="Mục tiêu 1-5 theo đề cương của Giảng viên")
    add_footer(s2, 2)

    # Cột trái: 5 mục tiêu cụ thể theo đề cương của Thầy
    c_left = add_card(s2, 1016000, 2150000, 9500000, 9000000)
    tb_left = s2.shapes.add_textbox(1200000, 2300000, 9100000, 8600000)
    tf_l = tb_left.text_frame; tf_l.word_wrap = True
    p = tf_l.paragraphs[0]; p.text = "5 MỤC TIÊU ĐỒ ÁN THEO YÊU CẦU CỦA THẦY"
    p.font.name = FONT_NAME; p.font.size = Pt(20); p.font.bold = True; p.font.color.rgb = COLOR_PRIMARY_BLUE

    goals = [
        ("1. Hiểu & phân tích dữ liệu:", "Kiểm tra toàn bộ 1.900 ảnh, phân bố 2 lớp, phát hiện ảnh lỗi và phân tích độ sáng, sắc nét, màu sắc."),
        ("2. Tiền xử lý dữ liệu chuẩn mực:", "Xử lý trùng lặp pixel SHA-256, nhóm gần trùng dHash, resize 96x96, trích xuất đặc trưng HSV + HOG, chuẩn hóa Z-score & PCA."),
        ("3. Áp dụng các thuật toán ML:", "Cài đặt và cấu hình 4 thuật toán học máy đại diện: Logistic Regression, KNN, SVM (RBF) và Random Forest."),
        ("4. So sánh & chọn mô hình tối ưu:", "Đánh giá công bằng qua 3-fold StratifiedGroupKFold, chọn mô hình theo F1 lớp cháy trên Validation trước khi đánh giá Test."),
        ("5. Phân tích kết quả thực nghiệm:", "Phân tích Confusion Matrix, hiện tượng Overfitting qua Train vs Val, phân tích thuộc tính ảnh lỗi (FN/FP) và bài học thực tiễn.")
    ]
    for title, desc in goals:
        p_t = tf_l.add_paragraph(); p_t.text = title; p_t.font.name = FONT_NAME; p_t.font.size = Pt(16); p_t.font.bold = True; p_t.font.color.rgb = COLOR_DARK_NAVY
        p_d = tf_l.add_paragraph(); p_d.text = desc; p_d.font.name = FONT_NAME; p_d.font.size = Pt(14); p_d.font.color.rgb = COLOR_TEXT_MAIN

    # Cột phải: Định nghĩa bài toán & Phạm vi ranh giới
    c_right = add_card(s2, 10900000, 2150000, 9758709, 5800000)
    tb_r = s2.shapes.add_textbox(11100000, 2300000, 9350000, 5400000)
    tf_r = tb_r.text_frame; tf_r.word_wrap = True
    p_r1 = tf_r.paragraphs[0]; p_r1.text = "ĐỊNH NGHĨA BÀI TOÁN & PHẠM VI ỨNG DỤNG"
    p_r1.font.name = FONT_NAME; p_r1.font.size = Pt(20); p_r1.font.bold = True; p_r1.font.color.rgb = COLOR_PRIMARY_BLUE

    p_r2 = tf_r.add_paragraph()
    p_r2.text = "• Đầu vào (Input): Một ảnh màu RGB kích thước bất kỳ chụp phong cảnh rừng."
    p_r2.font.name = FONT_NAME; p_r2.font.size = Pt(15); p_r2.font.bold = True; p_r2.font.color.rgb = COLOR_TEXT_MAIN
    p_r3 = tf_r.add_paragraph()
    p_r3.text = "• Đầu ra (Output): Nhãn nhị phân 0 (Không cháy / No Fire) hoặc 1 (Cháy / Fire)."
    p_r3.font.name = FONT_NAME; p_r3.font.size = Pt(15); p_r3.font.bold = True; p_r3.font.color.rgb = COLOR_TEXT_MAIN
    p_r4 = tf_r.add_paragraph()
    p_r4.text = "• Bản chất: Phân loại toàn ảnh (Whole-image classification), xác định sự hiện diện của đám cháy trong khung hình."
    p_r4.font.name = FONT_NAME; p_r4.font.size = Pt(15); p_r4.font.color.rgb = COLOR_TEXT_MAIN
    p_r5 = tf_r.add_paragraph()
    p_r5.text = "• Ý nghĩa thực tiễn: Hỗ trợ kiểm lâm tự động lọc hàng nghìn ảnh từ trạm quan trắc hoặc drone tuần tra để phát hiện sớm hiểm họa."
    p_r5.font.name = FONT_NAME; p_r5.font.size = Pt(15); p_r5.font.color.rgb = COLOR_TEXT_MAIN

    # Khối Callout: Ranh giới khoa học trung thực
    c_alert = add_card(s2, 10900000, 8150000, 9758709, 3000000, bg_color=COLOR_BG_ALERT, border_color=COLOR_BORDER_ALERT)
    tb_a = s2.shapes.add_textbox(11100000, 8250000, 9350000, 2800000)
    tf_a = tb_a.text_frame; tf_a.word_wrap = True
    p_a1 = tf_a.paragraphs[0]; p_a1.text = "LƯU Ý QUAN TRỌNG VỀ GIỚI HẠN PHẠM VI:"
    p_a1.font.name = FONT_NAME; p_a1.font.size = Pt(16); p_a1.font.bold = True; p_a1.font.color.rgb = COLOR_RED_ALERT
    p_a2 = tf_a.add_paragraph()
    p_a2.text = "1. Chưa khoanh vùng bounding box: Đây là bài toán Classification, chưa phải Object Detection (YOLO) hay Segmentation."
    p_a2.font.name = FONT_NAME; p_a2.font.size = Pt(14); p_a2.font.color.rgb = COLOR_TEXT_MAIN
    p_a3 = tf_a.add_paragraph()
    p_a3.text = "2. Chưa dự báo tương lai: Chỉ nhận diện sự cố đã xuất hiện trên ảnh, chưa mô hình hóa tốc độ lan truyền đám cháy theo thời gian."
    p_a3.font.name = FONT_NAME; p_a3.font.size = Pt(14); p_a3.font.color.rgb = COLOR_TEXT_MAIN

    add_notes(s2, "Slide 2 trình bày rõ ràng 5 mục tiêu theo đúng yêu cầu đề cương của Thầy, đồng thời phân định ranh giới bài toán classification.")

    # =========================================================================
    # SLIDE 03: MÔ TẢ BỘ DỮ LIỆU & KIỂM TOÁN CHỐNG RÒ RỈ (Mục 2 của Thầy)
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    add_nav_bar(s3, 0)
    add_slide_header(s3, "Mô Tả Bộ Dữ Liệu DeepFire & Quy Trình Kiểm Toán", section_tag="Mục 2: Số mẫu, số lớp, gán nhãn, chia tập Train/Val/Test")
    add_footer(s3, 3)

    # 3 Stat boxes
    add_stat_box(s3, 1016000, 2150000, 6200000, 2100000, "1.900", "Tổng Mẫu Dữ Liệu Nguồn", "950 Cháy (50%) | 950 Không cháy (50%)", COLOR_PRIMARY_BLUE)
    add_stat_box(s3, 7616000, 2150000, 6200000, 2100000, "4 Ảnh", "Bị Loại Qua Kiểm Toán", "2 ảnh trùng pixel + 2 ảnh Train dính Test", COLOR_RED_ALERT, bg_color=COLOR_BG_ALERT, border_color=COLOR_BORDER_ALERT)
    add_stat_box(s3, 14216000, 2150000, 6442709, 2100000, "1.896", "Số Ảnh Thực Nghiệm Chuẩn", "1.213 Train | 303 Validation | 380 Test", COLOR_GREEN_SOTA)

    # Bảng phân chia chi tiết các tập dữ liệu
    tb_shape = s3.shapes.add_table(5, 5, 1016000, 4500000, 19642709, 2800000)
    table = tb_shape.table
    table.columns[0].width = 3600000; table.columns[1].width = 4000000
    table.columns[2].width = 4000000; table.columns[3].width = 4000000; table.columns[4].width = 4042709

    headers = ["TẬP DỮ LIỆU", "KHÔNG CHÁY (LỚP 0)", "CHÁY (LỚP 1)", "TỔNG SỐ ẢNH", "TỶ LỆ PHÂN BỐ"]
    for j, h in enumerate(headers):
        c = table.cell(0, j); c.fill.solid(); c.fill.fore_color.rgb = COLOR_PRIMARY_BLUE
        p = c.text_frame.paragraphs[0]; p.text = h; p.font.name = FONT_NAME; p.font.size = Pt(16); p.font.bold = True; p.font.color.rgb = COLOR_WHITE; p.alignment = PP_ALIGN.CENTER

    split_rows = [
        ("Tập Huấn luyện (Train)", "609 ảnh (50.2%)", "604 ảnh (49.8%)", "1.213 ảnh", "Cân bằng gần 1:1 (~64%)"),
        ("Tập Thẩm định (Validation)", "151 ảnh (49.8%)", "152 ảnh (50.2%)", "303 ảnh", "Cân bằng 1:1 (~16%)"),
        ("Tập Kiểm thử (Test)", "190 ảnh (50.0%)", "190 ảnh (50.0%)", "380 ảnh", "Cân bằng tuyệt đối (20%)"),
        ("TỔNG CỘNG THỰC DÙNG", "950 ảnh", "946 ảnh", "1.896 ảnh", "Tỷ lệ lý tưởng cho Học máy")
    ]
    for i, row in enumerate(split_rows):
        for j, val in enumerate(row):
            c = table.cell(i+1, j); c.fill.solid()
            c.fill.fore_color.rgb = RGBColor(0xFF, 0xFF, 0xFF) if i % 2 == 0 else RGBColor(0xF1, 0xF5, 0xF9)
            if i == 3: c.fill.fore_color.rgb = COLOR_BG_METRIC
            p = c.text_frame.paragraphs[0]; p.text = val; p.font.name = FONT_NAME; p.font.size = Pt(15); p.font.color.rgb = COLOR_TEXT_MAIN
            if j == 0 or i == 3: p.font.bold = True
            if j > 0: p.alignment = PP_ALIGN.CENTER

    # 2 Khối phân tích: Cơ chế gán nhãn & Kỹ thuật chống rò rỉ dHash
    card_l = add_card(s3, 1016000, 7550000, 9500000, 3600000)
    tb_l = s3.shapes.add_textbox(1200000, 7700000, 9100000, 3300000)
    tf_l = tb_l.text_frame; tf_l.word_wrap = True
    p = tf_l.paragraphs[0]; p.text = "CƠ CHẾ THU THẬP & GÁN NHÃN NGUỒN"
    p.font.name = FONT_NAME; p.font.size = Pt(18); p.font.bold = True; p.font.color.rgb = COLOR_PRIMARY_BLUE
    p1 = tf_l.add_paragraph(); p1.text = "• Nguồn: Bộ dữ liệu DeepFire / Forest Fire Dataset của A. Khan và cộng sự (2022), phân phối trên Kaggle bởi tác giả alik05."
    p1.font.name = FONT_NAME; p1.font.size = Pt(14); p1.font.color.rgb = COLOR_TEXT_MAIN
    p2 = tf_l.add_paragraph(); p2.text = "• Cơ chế gán nhãn: Nhãn được gán chuẩn theo tiền tố file nofire_ (lớp 0) và fire_ (lớp 1) của tác giả, không phải tự động đoán."
    p2.font.name = FONT_NAME; p2.font.size = Pt(14); p2.font.color.rgb = COLOR_TEXT_MAIN
    p3 = tf_l.add_paragraph(); p3.text = "• Nhận định cân bằng: Cả lớp Cháy và Không cháy đều có 950 ảnh (1:1), do đó KHÔNG gặp hiện tượng mất cân bằng lớp và không cần SMOTE."
    p3.font.name = FONT_NAME; p3.font.size = Pt(14); p3.font.color.rgb = COLOR_TEXT_MAIN

    card_r = add_card(s3, 10900000, 7550000, 9758709, 3600000, bg_color=COLOR_CALLOUT_BG, border_color=COLOR_CALLOUT_LINE)
    tb_r = s3.shapes.add_textbox(11100000, 7700000, 9350000, 3300000)
    tf_r = tb_r.text_frame; tf_r.word_wrap = True
    p = tf_r.paragraphs[0]; p.text = "KỸ THUẬT KIỂM TOÁN CHỐNG RÒ RỈ DỮ LIỆU (DATA LEAKAGE)"
    p.font.name = FONT_NAME; p.font.size = Pt(18); p.font.bold = True; p.font.color.rgb = COLOR_CALLOUT_LINE
    p1 = tf_r.add_paragraph(); p1.text = "• Băm SHA-256: Phát hiện và loại bỏ chính xác 2 ảnh trùng pixel hoàn toàn."
    p1.font.name = FONT_NAME; p1.font.size = Pt(14); p1.font.color.rgb = COLOR_TEXT_MAIN
    p2 = tf_r.add_paragraph(); p2.text = "• 64-bit dHash (ngưỡng Hamming <= 4): Phát hiện các ảnh gần trùng (near-duplicates, chụp cùng cảnh chỉ đổi góc chụp hoặc độ sáng)."
    p2.font.name = FONT_NAME; p2.font.size = Pt(14); p2.font.color.rgb = COLOR_TEXT_MAIN
    p3 = tf_r.add_paragraph(); p3.text = "• Phân tách ranh giới: Loại bỏ 2 ảnh Train dính nhóm với Test; dùng StratifiedGroupKFold để các cụm dHash không bao giờ giao nhau giữa Train/Val/Test."
    p3.font.name = FONT_NAME; p3.font.size = Pt(14); p3.font.color.rgb = COLOR_TEXT_MAIN

    add_notes(s3, "Trả lời trực tiếp câu hỏi mục 2 của Thầy: số lượng mẫu, số lớp, có mất cân bằng không, gán nhãn thế nào, chia tập bao nhiêu.")

    # =========================================================================
    # SLIDE 04: EDA 1 - PHÂN BỐ LỚP & ẢNH MẪU THỰC TẾ (Mục 3.1 của Thầy)
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    add_nav_bar(s4, 1)
    add_slide_header(s4, "Phân Tích Dữ Liệu (EDA): Phân Bố & Đa Dạng Hình Ảnh", section_tag="Mục 3.1: EDA trực quan cho dữ liệu dạng Ảnh")
    add_footer(s4, 4)

    # Chèn hình 01_class_distribution.png
    fig1_path = FIG_DIR / '01_class_distribution.png'
    if fig1_path.exists():
        s4.shapes.add_picture(str(fig1_path), 1016000, 2150000, 9500000, 4800000)
    else:
        add_card(s4, 1016000, 2150000, 9500000, 4800000)

    # Chèn hình 02_samples.png
    fig2_path = FIG_DIR / '02_samples.png'
    if fig2_path.exists():
        s4.shapes.add_picture(str(fig2_path), 10900000, 2150000, 9758709, 4800000)
    else:
        add_card(s4, 10900000, 2150000, 9758709, 4800000)

    # Khối giải thích phân tích EDA dưới hình
    card_eda = add_card(s4, 1016000, 7200000, 19642709, 3950000)
    tb_eda = s4.shapes.add_textbox(1200000, 7350000, 19200000, 3650000)
    tf_e = tb_eda.text_frame; tf_e.word_wrap = True
    p = tf_e.paragraphs[0]; p.text = "NHẬN XÉT PHÂN TÍCH KHÁM PHÁ DỮ LIỆU ẢNH (EDA INSIGHTS):"
    p.font.name = FONT_NAME; p.font.size = Pt(18); p.font.bold = True; p.font.color.rgb = COLOR_PRIMARY_BLUE

    p1 = tf_e.add_paragraph()
    p1.text = "1. Tính cân bằng phân bố: Biểu đồ cột bên trái khẳng định tỉ lệ lớp 0 và lớp 1 được phân bố đồng đều hoàn hảo trên cả 3 tập Train (1.213), Validation (303) và Test (380). Không có tập nào bị lệch lớp."
    p1.font.name = FONT_NAME; p1.font.size = Pt(15); p1.font.color.rgb = COLOR_TEXT_MAIN

    p2 = tf_e.add_paragraph()
    p2.text = "2. Đa dạng hình thái lớp Cháy (Fire): Đám cháy trong thực tế không chỉ có một màu đỏ đồng nhất; có ảnh lửa bùng phát cao (cháy rừng ban đêm), có ảnh chỉ thấy cột khói trắng dày đặc che lấp tán cây, có ảnh lửa âm ỉ nền đất tối."
    p2.font.name = FONT_NAME; p2.font.size = Pt(15); p2.font.color.rgb = COLOR_TEXT_MAIN

    p3 = tf_e.add_paragraph()
    p3.text = "3. Thách thức phân loại từ lớp Không cháy (No Fire): Xuất hiện nhiều cảnh quan phức tạp như núi đá nắng gắt, rừng rậm rạp bóng râm, cây lá vàng/đỏ mùa thu rất dễ gây nhầm lẫn với màu ngọn lửa nếu chỉ dùng quy tắc lọc màu đơn giản."
    p3.font.name = FONT_NAME; p3.font.size = Pt(15); p3.font.color.rgb = COLOR_TEXT_MAIN

    p4 = tf_e.add_paragraph()
    p4.text = "👉 KẾT LUẬN EDA 1: Không thể áp dụng phương pháp ngưỡng màu đơn biến (Thresholding). Bắt buộc phải kết hợp cả thông tin Màu Sắc (Color Histogram) và Cấu Trúc Đường Nét Cạnh (HOG) để mô hình học máy phân biệt."
    p4.font.name = FONT_NAME; p4.font.size = Pt(15); p4.font.bold = True; p4.font.color.rgb = COLOR_DARK_NAVY

    add_notes(s4, "EDA hình ảnh chỉ ra tính chất phức tạp của bài toán: lá cây mùa thu và khói mù có thể gây báo nhầm.")

    # =========================================================================
    # SLIDE 05: EDA 2 - CHẤT LƯỢNG, MÀU SẮC & ẢNH TRUNG BÌNH (Mục 3.1 của Thầy)
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    add_nav_bar(s5, 1)
    add_slide_header(s5, "EDA Chất Lượng Ảnh, Sắc Độ Màu Sắc & Ảnh Trung Bình", section_tag="Mục 3.1: Kích thước, độ sáng, độ sắc nét Laplacian, phân bố Hue/RGB")
    add_footer(s5, 5)

    # 3 Hình ảnh EDA kỹ thuật
    f3 = FIG_DIR / '03_quality.png'
    f4 = FIG_DIR / '04_color.png'
    f5 = FIG_DIR / '05_mean_images.png'
    if f3.exists(): s5.shapes.add_picture(str(f3), 1016000, 2150000, 6200000, 4800000)
    if f4.exists(): s5.shapes.add_picture(str(f4), 7616000, 2150000, 6800000, 4800000)
    if f5.exists(): s5.shapes.add_picture(str(f5), 14816000, 2150000, 5842709, 4800000)

    # Khối giải thích chi tiết
    card_stat = add_card(s5, 1016000, 7200000, 19642709, 3950000)
    tb_s = s5.shapes.add_textbox(1200000, 7350000, 19200000, 3650000)
    tf_s = tb_s.text_frame; tf_s.word_wrap = True
    p = tf_s.paragraphs[0]; p.text = "PHÂN TÍCH ĐỊNH LƯỢNG CHỈ SỐ KỸ THUẬT CỦA ẢNH (QUANTITATIVE EDA):"
    p.font.name = FONT_NAME; p.font.size = Pt(18); p.font.bold = True; p.font.color.rgb = COLOR_PRIMARY_BLUE

    p1 = tf_s.add_paragraph()
    p1.text = "• Kích thước ảnh (Resolution): Trong 1.896 ảnh giữ lại, có 1.822 ảnh kích thước 250x250 (chiếm 96.1%), 1 ảnh 252x252 và 73 ảnh 256x256. Do đó, bước Resize về một kích thước chuẩn (96x96) là hoàn toàn bắt buộc."
    p1.font.name = FONT_NAME; p1.font.size = Pt(15); p1.font.color.rgb = COLOR_TEXT_MAIN

    p2 = tf_s.add_paragraph()
    p2.text = "• Độ sáng & Độ sắc nét (Laplacian Variance): Lớp Cháy có độ sáng trung bình 0.339 (tối hơn lớp Không cháy 0.401) do nhiều ảnh chụp lửa trong nền khói đặc hoặc ban đêm. Phương sai Laplacian đo độ sắc nét cho thấy phân bố chồng lấn lớn giữa 2 lớp."
    p2.font.name = FONT_NAME; p2.font.size = Pt(15); p2.font.color.rgb = COLOR_TEXT_MAIN

    p3 = tf_s.add_paragraph()
    p3.text = "• Phân bố màu sắc Hue & RGB: Lớp Cháy có đỉnh phân bố Hue tập trung rất mạnh ở vùng màu ấm (đỏ, cam, vàng). Cường độ kênh Red trung bình của lớp Cháy đạt 0.476, cao hơn hẳn mức 0.377 của lớp Không cháy."
    p3.font.name = FONT_NAME; p3.font.size = Pt(15); p3.font.color.rgb = COLOR_TEXT_MAIN

    p4 = tf_s.add_paragraph()
    p4.text = "• Ảnh trung bình (Mean Images): Ảnh trung bình lớp Không cháy có sắc xanh lá và xám tán xạ đồng đều; ảnh lớp Cháy ám sắc cam nâu rực rỡ ở vùng trung tâm. Tuy nhiên, vị trí đám cháy xuất hiện ngẫu nhiên nên không thể dùng mặt nạ vị trí cố định."
    p4.font.name = FONT_NAME; p4.font.size = Pt(15); p4.font.color.rgb = COLOR_TEXT_MAIN

    add_notes(s5, "Slide phân tích kỹ thuật: kích thước, độ sáng, độ sắc nét Laplacian, histogram màu Hue và ảnh trung bình.")

    # =========================================================================
    # SLIDE 06: TIỀN XỬ LÝ DỮ LIỆU & TRÍCH XUẤT ĐẶC TRƯNG (Mục 3.2 & 4 của Thầy)
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    add_nav_bar(s6, 1)
    add_slide_header(s6, "Quy Trình Tiền Xử Lý Dữ Liệu & Trích Xuất Đặc Trưng", section_tag="Mục 3.2 & 4: Tiền xử lý, chuẩn hóa, HSV Histogram, HOG, PCA Pipeline")
    add_footer(s6, 6)

    # 4 Khối biểu diễn các bước tiền xử lý
    steps = [
        ("Bước 1: Chuẩn Hóa Ảnh", "EXIF Transpose & RGB", "Resize cố định 96x96 px", "Chia 255 đưa pixel về [0, 1]"),
        ("Bước 2: Trích Màu Sắc", "Color Histogram HSV", "32 bins Hue (sắc thái)", "16 bins S + 16 bins V = 64 chiều"),
        ("Bước 3: Trích Cạnh & Cấu Trúc", "HOG Feature Extractor", "8 hướng gradients, cell 16x16", "Khối block 2x2 = 800 chiều"),
        ("Bước 4: Nén Chiều Pipeline", "StandardScaler + PCA", "Ghép vector: 864 đặc trưng", "PCA giữ 95% var = 231 chiều")
    ]
    for i, (st, t1, t2, t3) in enumerate(steps):
        x = 1016000 + i * 4950000
        card = add_card(s6, x, 2150000, 4700000, 3600000, bg_color=COLOR_BG_METRIC, border_color=COLOR_BORDER_METRIC)
        tb = s6.shapes.add_textbox(x + 150000, 2250000, 4400000, 3300000)
        tf = tb.text_frame; tf.word_wrap = True
        p = tf.paragraphs[0]; p.text = st; p.font.name = FONT_NAME; p.font.size = Pt(17); p.font.bold = True; p.font.color.rgb = COLOR_PRIMARY_BLUE
        p1 = tf.add_paragraph(); p1.text = f"• {t1}"; p1.font.name = FONT_NAME; p1.font.size = Pt(14); p1.font.color.rgb = COLOR_TEXT_MAIN
        p2 = tf.add_paragraph(); p2.text = f"• {t2}"; p2.font.name = FONT_NAME; p2.font.size = Pt(14); p2.font.color.rgb = COLOR_TEXT_MAIN
        p3 = tf.add_paragraph(); p3.text = f"• {t3}"; p3.font.name = FONT_NAME; p3.font.size = Pt(14); p3.font.color.rgb = COLOR_TEXT_MAIN

    # Bảng chi tiết tổng hợp tham số kỹ thuật tiền xử lý
    tb_shape = s6.shapes.add_table(5, 4, 1016000, 6000000, 19642709, 3000000)
    table = tb_shape.table
    table.columns[0].width = 3600000; table.columns[1].width = 5000000
    table.columns[2].width = 5000000; table.columns[3].width = 6042709

    headers = ["THÀNH PHẦN", "THÔNG SỐ CẤU HÌNH", "SỐ CHIỀU ĐẶC TRƯNG", "Ý NGHĨA ĐỐI VỚI BÀI TOÁN"]
    for j, h in enumerate(headers):
        c = table.cell(0, j); c.fill.solid(); c.fill.fore_color.rgb = COLOR_PRIMARY_BLUE
        p = c.text_frame.paragraphs[0]; p.text = h; p.font.name = FONT_NAME; p.font.size = Pt(15); p.font.bold = True; p.font.color.rgb = COLOR_WHITE; p.alignment = PP_ALIGN.CENTER

    prep_data = [
        ("Histogram màu HSV", "Hue: 32 bins, Sat: 16 bins, Val: 16 bins", "64 chiều", "Nắm bắt gam màu ấm (đỏ, vàng, cam) đặc trưng của lửa và khói"),
        ("HOG (Histogram Gradients)", "orientations=8, pixels_per_cell=(16,16)", "800 chiều", "Mô tả cấu trúc đường viền đám khói, tán cây và kết cấu mặt đất"),
        ("Ghép đặc trưng (Concat)", "Vector ghép trực tiếp HSV + HOG", "864 chiều", "Biểu diễn đầy đủ thông tin màu sắc và hình thái học của ảnh"),
        ("PCA Giữ 95% Phương Sai", "Incremental fit trong từng fold train", "231 chiều (fit toàn train)", "Loại bỏ đa cộng tuyến, giảm 73% số chiều, tăng tốc độ huấn luyện")
    ]
    for i, row in enumerate(prep_data):
        for j, val in enumerate(row):
            c = table.cell(i+1, j); c.fill.solid()
            c.fill.fore_color.rgb = RGBColor(0xFF, 0xFF, 0xFF) if i % 2 == 0 else RGBColor(0xF1, 0xF5, 0xF9)
            p = c.text_frame.paragraphs[0]; p.text = val; p.font.name = FONT_NAME; p.font.size = Pt(14); p.font.color.rgb = COLOR_TEXT_MAIN
            if j == 0: p.font.bold = True
            if j == 2: p.alignment = PP_ALIGN.CENTER; p.font.bold = True; p.font.color.rgb = COLOR_PRIMARY_BLUE

    # Card nhấn mạnh Pipeline khép kín
    pipe_card = add_card(s6, 1016000, 9250000, 19642709, 1900000, bg_color=COLOR_CALLOUT_BG, border_color=COLOR_CALLOUT_LINE)
    tb_p = s6.shapes.add_textbox(1200000, 9350000, 19200000, 1700000)
    tf_p = tb_p.text_frame; tf_p.word_wrap = True
    p = tf_p.paragraphs[0]; p.text = "NGUYÊN TẮC THIẾT KẾ PIPELINE CHỐNG RÒ RỈ THÔNG TIN (DATA LEAKAGE):"
    p.font.name = FONT_NAME; p.font.size = Pt(16); p.font.bold = True; p.font.color.rgb = COLOR_CALLOUT_LINE
    p1 = tf_p.add_paragraph()
    p1.text = "Cả StandardScaler và PCA đều được đóng gói bên trong sklearn.pipeline.Pipeline. Trong quá trình Cross-Validation, các bộ biến đổi này CHỈ ĐƯỢC FIT trên fold Train và chỉ transform sang fold Validation. Tập Test hoàn toàn giữ kín, chỉ transform ở bước cuối cùng."
    p1.font.name = FONT_NAME; p1.font.size = Pt(14); p1.font.color.rgb = COLOR_TEXT_MAIN

    add_notes(s6, "Chi tiết quy trình tiền xử lý: resize 96x96, HSV 64 bin + HOG 800 bin = 864 đặc trưng; PCA nén còn 231 đặc trưng trong Pipeline.")

    # =========================================================================
    # SLIDE 07: BỐN MÔ HÌNH MACHINE LEARNING & TUNING (Mục 3.3 & 5 của Thầy)
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    add_nav_bar(s7, 2)
    add_slide_header(s7, "Bốn Mô Hình Machine Learning & Không Gian Siêu Tham Số", section_tag="Mục 3.3 & 5: Cài đặt ít nhất 3 mô hình cơ bản và tìm thông số tối ưu")
    add_footer(s7, 7)

    # 4 Thẻ mô hình so sánh
    models_info = [
        ("1. Logistic Regression", "Mô hình phân loại tuyến tính đối chứng cơ sở (Baseline).", "C in {0.1, 1, 10}, solver='lbfgs', max_iter=3000", "Tối ưu hóa hàm mất mát log-loss, tìm tổ hợp trọng số tuyến tính các thành phần PCA."),
        ("2. K-Nearest Neighbors", "Mô hình học theo bộ nhớ (Instance-based learning).", "k in {3, 5, 9}, weights in {'uniform', 'distance'}", "Bỏ phiếu nhãn dựa trên khoảng cách Euclidean trong không gian đặc trưng sau PCA."),
        ("3. Support Vector Machine", "Mô hình tìm siêu phẳng phân cách với biên cực đại.", "C in {1, 10}, kernel in {'linear', 'rbf'}, gamma='scale'", "Kernel RBF ánh xạ đặc trưng sang không gian phi tuyến vô hạn chiều để phân tách lửa."),
        ("4. Random Forest", "Mô hình tập hợp đa cây quyết định (Bagging Ensemble).", "n_estimators=150, max_depth in {12, None}, min_samples_leaf in {1, 2}", "Kết hợp 150 cây học trên tập con dữ liệu để giảm phương sai và chống quá khớp.")
    ]
    for i, (name, role, grid, desc) in enumerate(models_info):
        x = 1016000 + (i % 2) * 9900000
        y = 2150000 + (i // 2) * 3600000
        card = add_card(s7, x, y, 9600000, 3400000)
        tb = s7.shapes.add_textbox(x + 150000, y + 150000, 9300000, 3100000)
        tf = tb.text_frame; tf.word_wrap = True
        p = tf.paragraphs[0]; p.text = name; p.font.name = FONT_NAME; p.font.size = Pt(18); p.font.bold = True; p.font.color.rgb = COLOR_PRIMARY_BLUE
        p1 = tf.add_paragraph(); p1.text = f"• Vai trò: {role}"; p1.font.name = FONT_NAME; p1.font.size = Pt(14); p1.font.color.rgb = COLOR_DARK_NAVY
        p2 = tf.add_paragraph(); p2.text = f"• Lưới tham số (Grid): {grid}"; p2.font.name = FONT_NAME; p2.font.size = Pt(14); p2.font.bold = True; p2.font.color.rgb = COLOR_TEXT_MAIN
        p3 = tf.add_paragraph(); p3.text = f"• Cơ chế: {desc}"; p3.font.name = FONT_NAME; p3.font.size = Pt(13); p3.font.color.rgb = COLOR_TEXT_MUTED

    # Khối quy trình Cross-Validation bên dưới
    card_cv = add_card(s7, 1016000, 9550000, 19642709, 1650000, bg_color=COLOR_BG_METRIC, border_color=COLOR_BORDER_METRIC)
    tb_cv = s7.shapes.add_textbox(1200000, 9650000, 19200000, 1450000)
    tf_c = tb_cv.text_frame; tf_c.word_wrap = True
    p = tf_c.paragraphs[0]; p.text = "CƠ CHẾ TÌM THAM SỐ (HYPERPARAMETER TUNING) BẰNG 3-FOLD STRATIFIED GROUP K-FOLD:"
    p.font.name = FONT_NAME; p.font.size = Pt(16); p.font.bold = True; p.font.color.rgb = COLOR_PRIMARY_BLUE
    p1 = tf_c.add_paragraph()
    p1.text = "Thực hiện tìm kiếm tham số bằng GridSearchCV trên 1.213 ảnh Train. Chia 3 folds đảm bảo phân bố nhãn cân bằng và các cụm ảnh gần trùng (dHash) không bị cắt đôi. Tiêu chí chọn tham số tối ưu là F1-Score trung bình của lớp Cháy qua 3 folds."
    p1.font.name = FONT_NAME; p1.font.size = Pt(14); p1.font.color.rgb = COLOR_TEXT_MAIN

    add_notes(s7, "Trình bày 4 mô hình học máy: Logistic Regression, KNN, SVM, Random Forest và không gian tìm kiếm tham số qua 3-fold CV.")

    # =========================================================================
    # SLIDE 08: KẾT QUẢ CROSS-VALIDATION & KHÓA LỰA CHỌN TRƯỚC TEST (Mục 5 & 3.4)
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    add_nav_bar(s8, 2)
    add_slide_header(s8, "Kết Quả Cross-Validation & Khóa Mô Hình Trên Validation", section_tag="Mục 5: So sánh kết quả CV và quyết định chọn mô hình tối ưu")
    add_footer(s8, 8)

    # Bảng kết quả 3-fold CV
    tb_shape = s8.shapes.add_table(5, 5, 1016000, 2150000, 19642709, 3200000)
    table = tb_shape.table
    table.columns[0].width = 4500000; table.columns[1].width = 4500000
    table.columns[2].width = 3500000; table.columns[3].width = 3500000; table.columns[4].width = 3642709

    headers = ["MÔ HÌNH", "THAM SỐ TỐI ƯU ĐƯỢC CHỌN", "F1 CV TRUNG BÌNH", "ĐỘ LỆCH CHUẨN (STD)", "THỜI GIAN TÌM KIẾM"]
    for j, h in enumerate(headers):
        c = table.cell(0, j); c.fill.solid(); c.fill.fore_color.rgb = COLOR_PRIMARY_BLUE
        p = c.text_frame.paragraphs[0]; p.text = h; p.font.name = FONT_NAME; p.font.size = Pt(15); p.font.bold = True; p.font.color.rgb = COLOR_WHITE; p.alignment = PP_ALIGN.CENTER

    cv_data = [
        ("Logistic Regression", "C = 1, solver='lbfgs'", "93,79%", "+/- 1,06%", "4.1 giây"),
        ("KNN", "k = 3, weights='uniform'", "75,05%", "+/- 2,93%", "5.7 giây"),
        ("SVM (Tối ưu)", "C = 10, kernel='rbf', gamma='scale'", "93,66%", "+/- 0,46% (Ổn định nhất)", "4.2 giây"),
        ("Random Forest", "n_estimators=150, max_depth=None", "88,36%", "+/- 1,57%", "21.3 giây")
    ]
    for i, row in enumerate(cv_data):
        for j, val in enumerate(row):
            c = table.cell(i+1, j); c.fill.solid()
            c.fill.fore_color.rgb = RGBColor(0xFF, 0xFF, 0xFF) if i % 2 == 0 else RGBColor(0xF1, 0xF5, 0xF9)
            if i == 2: c.fill.fore_color.rgb = COLOR_BG_METRIC
            p = c.text_frame.paragraphs[0]; p.text = val; p.font.name = FONT_NAME; p.font.size = Pt(15); p.font.color.rgb = COLOR_TEXT_MAIN
            if j == 0 or i == 2: p.font.bold = True
            if j >= 2: p.alignment = PP_ALIGN.CENTER
            if j == 2 and i == 2: p.font.color.rgb = COLOR_GREEN_SOTA

    # 2 Khối phân tích: Đánh giá Validation & Khóa lựa chọn
    card_v = add_card(s8, 1016000, 5600000, 9500000, 5500000)
    tb_v = s8.shapes.add_textbox(1200000, 5750000, 9100000, 5200000)
    tf_v = tb_v.text_frame; tf_v.word_wrap = True
    p = tf_v.paragraphs[0]; p.text = "KẾT QUẢ TRÊN TẬP VALIDATION (303 ẢNH)"
    p.font.name = FONT_NAME; p.font.size = Pt(18); p.font.bold = True; p.font.color.rgb = COLOR_PRIMARY_BLUE

    val_res = [
        ("SVM (Lựa chọn số 1):", "F1 Validation = 94,19% | Recall = 95,39%", "Đạt F1 cao nhất toàn diện, độ ổn định CV vượt trội."),
        ("Logistic Regression:", "F1 Validation = 93,42% | Recall = 93,42%", "Kém SVM 0.77 điểm phần trăm trên tập validation."),
        ("Random Forest:", "F1 Validation = 86,45% | Recall = 88,16%", "Kém SVM 7.74 điểm phần trăm, dấu hiệu giảm hiệu năng do PCA."),
        ("KNN:", "F1 Validation = 71,54% | Recall = 59,21%", "Hiệu năng thấp nhất, khoảng cách đa chiều bị nhiễu.")
    ]
    for m_name, score, comm in val_res:
        p_t = tf_v.add_paragraph(); p_t.text = m_name; p_t.font.name = FONT_NAME; p_t.font.size = Pt(15); p_t.font.bold = True; p_t.font.color.rgb = COLOR_DARK_NAVY
        p_s = tf_v.add_paragraph(); p_s.text = f"• {score} - {comm}"; p_s.font.name = FONT_NAME; p_s.font.size = Pt(13); p_s.font.color.rgb = COLOR_TEXT_MAIN

    card_lock = add_card(s8, 10900000, 5600000, 9758709, 5500000, bg_color=COLOR_CALLOUT_BG, border_color=COLOR_CALLOUT_LINE)
    tb_l = s8.shapes.add_textbox(11100000, 5750000, 9350000, 5200000)
    tf_l = tb_l.text_frame; tf_l.word_wrap = True
    p = tf_l.paragraphs[0]; p.text = "NGUYÊN TẮC KHÓA LỰA CHỌN (SELECTION BEFORE TEST)"
    p.font.name = FONT_NAME; p.font.size = Pt(18); p.font.bold = True; p.font.color.rgb = COLOR_CALLOUT_LINE

    p1 = tf_l.add_paragraph()
    p1.text = "• Tiêu chí tiên quyết: Chọn mô hình dựa hoàn toàn trên F1 lớp Cháy của tập Validation. Nếu hòa điểm F1 thì xét chỉ số Recall (ưu tiên cứu rừng)."
    p1.font.name = FONT_NAME; p1.font.size = Pt(15); p1.font.color.rgb = COLOR_TEXT_MAIN

    p2 = tf_l.add_paragraph()
    p2.text = "• Khóa quyết định vào file JSON: Quyết định chọn SVM được ghi nhận vào file results/selection_before_test.json TRƯỚC KHI nạp dữ liệu Test vào tính toán."
    p2.font.name = FONT_NAME; p2.font.size = Pt(15); p2.font.color.rgb = COLOR_TEXT_MAIN

    p3 = tf_l.add_paragraph()
    p3.text = "• Ý nghĩa học thuật: Tuyệt đối không dùng kết quả Test để quay ngược lại tinh chỉnh siêu tham số (Data snooping / Cherry-picking). Đảm bảo kết quả kiểm thử hoàn toàn khách quan và trung thực 100%."
    p3.font.name = FONT_NAME; p3.font.size = Pt(15); p3.font.bold = True; p3.font.color.rgb = COLOR_DARK_NAVY

    add_notes(s8, "Khẳng định phương pháp luận khoa học: SVM được chốt trên validation trước khi đánh giá test.")

    # =========================================================================
    # SLIDE 09: KẾT QUẢ ĐÁNH GIÁ TRÊN TẬP TEST (Mục 3.4 & 6 của Thầy)
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    add_nav_bar(s9, 3)
    add_slide_header(s9, "Đánh Giá Hiệu Năng 4 Mô Hình Trên Tập Test (380 Ảnh)", section_tag="Mục 3.4 & 6: Accuracy, Precision, Recall, F1-Score trên 380 ảnh Test độc lập")
    add_footer(s9, 9)

    # 4 Stat boxes chỉ số của SVM
    add_stat_box(s9, 1016000, 2150000, 4600000, 2000000, "93,95%", "Accuracy (Độ chính xác)", "SVM đúng 357/380 ảnh Test", COLOR_PRIMARY_BLUE)
    add_stat_box(s9, 6020000, 2150000, 4600000, 2000000, "92,82%", "Precision Lớp Cháy", "Báo 195 ảnh, đúng 181 ảnh", COLOR_PRIMARY_BLUE)
    add_stat_box(s9, 11024000, 2150000, 4600000, 2000000, "95,26%", "Recall Lớp Cháy", "Chỉ bỏ sót 9/190 vụ cháy thật", COLOR_GREEN_SOTA)
    add_stat_box(s9, 16028000, 2150000, 4630709, 2000000, "94,03%", "F1-Score Lớp Cháy", "Cân bằng hoàn hảo P & R", COLOR_GREEN_SOTA)

    # Bảng so sánh 4 mô hình trên tập Test
    tb_shape = s9.shapes.add_table(5, 5, 1016000, 4350000, 10500000, 3600000)
    table = tb_shape.table
    table.columns[0].width = 3300000; table.columns[1].width = 1800000
    table.columns[2].width = 1800000; table.columns[3].width = 1800000; table.columns[4].width = 1800000

    headers = ["MÔ HÌNH", "ACCURACY", "PRECISION", "RECALL", "F1-SCORE"]
    for j, h in enumerate(headers):
        c = table.cell(0, j); c.fill.solid(); c.fill.fore_color.rgb = COLOR_PRIMARY_BLUE
        p = c.text_frame.paragraphs[0]; p.text = h; p.font.name = FONT_NAME; p.font.size = Pt(15); p.font.bold = True; p.font.color.rgb = COLOR_WHITE; p.alignment = PP_ALIGN.CENTER

    test_metrics = [
        ("Logistic Regression", "92,63%", "92,19%", "93,16%", "92,67%"),
        ("KNN", "74,47%", "92,66%", "53,16%", "67,56%"),
        ("SVM (Tối ưu nhất)", "93,95%", "92,82%", "95,26%", "94,03%"),
        ("Random Forest", "87,63%", "88,65%", "86,32%", "87,47%")
    ]
    for i, row in enumerate(test_metrics):
        for j, val in enumerate(row):
            c = table.cell(i+1, j); c.fill.solid()
            c.fill.fore_color.rgb = RGBColor(0xFF, 0xFF, 0xFF) if i % 2 == 0 else RGBColor(0xF1, 0xF5, 0xF9)
            if i == 2: c.fill.fore_color.rgb = COLOR_BG_METRIC
            p = c.text_frame.paragraphs[0]; p.text = val; p.font.name = FONT_NAME; p.font.size = Pt(15); p.font.color.rgb = COLOR_TEXT_MAIN
            if j == 0 or i == 2: p.font.bold = True
            if j >= 1: p.alignment = PP_ALIGN.CENTER
            if j == 4 and i == 2: p.font.color.rgb = COLOR_GREEN_SOTA

    # Chèn hình 07_model_comparison.png bên phải
    f7 = FIG_DIR / '07_model_comparison.png'
    if f7.exists():
        s9.shapes.add_picture(str(f7), 11800000, 4350000, 8858709, 3600000)

    # Khối phân tích nhận xét kết quả
    card_eval = add_card(s9, 1016000, 8150000, 19642709, 3000000)
    tb_e = s9.shapes.add_textbox(1200000, 8250000, 19200000, 2800000)
    tf_e = tb_e.text_frame; tf_e.word_wrap = True
    p = tf_e.paragraphs[0]; p.text = "PHÂN TÍCH CHUYÊN SÂU CÁC METRICS TRÊN TẬP TEST ĐỘC LẬP:"
    p.font.name = FONT_NAME; p.font.size = Pt(17); p.font.bold = True; p.font.color.rgb = COLOR_PRIMARY_BLUE

    p1 = tf_e.add_paragraph()
    p1.text = "• SVM đạt quán quân toàn diện: Accuracy đạt 93.95% (357/380 ảnh đúng), F1 đạt 94.03%. Đặc biệt Recall lớp Cháy đạt 95.26%, chỉ để lọt 9 đám cháy trong tổng số 190 ảnh cháy thử nghiệm."
    p1.font.name = FONT_NAME; p1.font.size = Pt(14); p1.font.color.rgb = COLOR_TEXT_MAIN

    p2 = tf_e.add_paragraph()
    p2.text = "• Logistic Regression là đối chứng rất mạnh: Đạt F1 92.67%, chỉ kém SVM 1.36 điểm phần trăm. Điều này chứng minh không gian đặc trưng HSV + HOG sau PCA đã có độ phân tách tuyến tính rất tốt."
    p2.font.name = FONT_NAME; p2.font.size = Pt(14); p2.font.color.rgb = COLOR_TEXT_MAIN

    p3 = tf_e.add_paragraph()
    p3.text = "• Thất bại của KNN (Recall chỉ 53.16%): Mặc dù Precision cao (92.66%), nhưng KNN bỏ sót tới gần 47% số vụ cháy. Hiện tượng khoảng cách Euclidean bị bão hòa trong không gian 231 chiều khiến KNN không thể phát hiện hiệu quả."
    p3.font.name = FONT_NAME; p3.font.size = Pt(14); p3.font.color.rgb = COLOR_TEXT_MAIN

    add_notes(s9, "Bảng kết quả Test trên 380 ảnh. SVM dẫn đầu với Accuracy 93.95%, Recall 95.26%, F1 94.03%.")

    # =========================================================================
    # SLIDE 10: BÁO CÁO PHÂN LOẠI CHI TIẾT (Full Classification Report)
    # =========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    add_nav_bar(s10, 3)
    add_slide_header(s10, "Báo Cáo Phân Loại Chi Tiết Cả Hai Lớp (Classification Report)", section_tag="Mục 6: Bổ sung đầy đủ các Report theo yêu cầu của Thầy")
    add_footer(s10, 10)

    # Bảng Classification Report chi tiết 4 mô hình x 2 lớp
    tb_shape = s10.shapes.add_table(13, 6, 1016000, 2150000, 19642709, 6200000)
    table = tb_shape.table
    table.columns[0].width = 4600000; table.columns[1].width = 3000000
    table.columns[2].width = 3000000; table.columns[3].width = 3000000
    table.columns[4].width = 3000000; table.columns[5].width = 3042709

    headers = ["MÔ HÌNH", "LỚP DỰ ĐOÁN", "PRECISION", "RECALL", "F1-SCORE", "SUPPORT (MẪU)"]
    for j, h in enumerate(headers):
        c = table.cell(0, j); c.fill.solid(); c.fill.fore_color.rgb = COLOR_PRIMARY_BLUE
        p = c.text_frame.paragraphs[0]; p.text = h; p.font.name = FONT_NAME; p.font.size = Pt(15); p.font.bold = True; p.font.color.rgb = COLOR_WHITE; p.alignment = PP_ALIGN.CENTER

    report_rows = [
        ("SVM (Tối ưu)", "Không cháy (Lớp 0)", "95,14%", "92,63%", "93,87%", "190 ảnh"),
        ("SVM (Tối ưu)", "Cháy (Lớp 1)", "92,82%", "95,26%", "94,03%", "190 ảnh"),
        ("SVM (Tối ưu)", "Macro Avg / Weighted Avg", "93,98%", "93,95%", "93,95%", "380 ảnh"),
        ("Logistic Regression", "Không cháy (Lớp 0)", "93,09%", "92,11%", "92,59%", "190 ảnh"),
        ("Logistic Regression", "Cháy (Lớp 1)", "92,19%", "93,16%", "92,67%", "190 ảnh"),
        ("Logistic Regression", "Macro Avg / Weighted Avg", "92,64%", "92,63%", "92,63%", "380 ảnh"),
        ("Random Forest", "Không cháy (Lớp 0)", "86,67%", "88,95%", "87,79%", "190 ảnh"),
        ("Random Forest", "Cháy (Lớp 1)", "88,65%", "86,32%", "87,47%", "190 ảnh"),
        ("Random Forest", "Macro Avg / Weighted Avg", "87,66%", "87,63%", "87,63%", "380 ảnh"),
        ("KNN", "Không cháy (Lớp 0)", "67,16%", "95,79%", "78,96%", "190 ảnh"),
        ("KNN", "Cháy (Lớp 1)", "92,66%", "53,16%", "67,56%", "190 ảnh"),
        ("KNN", "Macro Avg / Weighted Avg", "79,91%", "74,47%", "73,26%", "380 ảnh")
    ]
    for i, row in enumerate(report_rows):
        for j, val in enumerate(row):
            c = table.cell(i+1, j); c.fill.solid()
            if i in [0, 1, 2]:
                c.fill.fore_color.rgb = COLOR_BG_METRIC
            elif i % 3 == 2:
                c.fill.fore_color.rgb = RGBColor(0xEA, 0xEE, 0xF4)
            else:
                c.fill.fore_color.rgb = RGBColor(0xFF, 0xFF, 0xFF) if (i // 3) % 2 == 0 else RGBColor(0xF8, 0xFA, 0xFC)
            p = c.text_frame.paragraphs[0]; p.text = val; p.font.name = FONT_NAME; p.font.size = Pt(14); p.font.color.rgb = COLOR_TEXT_MAIN
            if j == 0 or i in [2, 5, 8, 11]: p.font.bold = True
            if j >= 2: p.alignment = PP_ALIGN.CENTER
            if i in [0, 1, 2] and j == 4: p.font.color.rgb = COLOR_GREEN_SOTA; p.font.bold = True

    # Khối tóm tắt nhận xét Report
    card_rep = add_card(s10, 1016000, 8550000, 19642709, 2650000, bg_color=COLOR_CALLOUT_BG, border_color=COLOR_CALLOUT_LINE)
    tb_r = s10.shapes.add_textbox(1200000, 8650000, 19200000, 2450000)
    tf_r = tb_r.text_frame; tf_r.word_wrap = True
    p = tf_r.paragraphs[0]; p.text = "Ý NGHĨA KHOA HỌC TỪ BẢNG CLASSIFICATION REPORT:"
    p.font.name = FONT_NAME; p.font.size = Pt(17); p.font.bold = True; p.font.color.rgb = COLOR_CALLOUT_LINE

    p1 = tf_r.add_paragraph()
    p1.text = "• SVM đạt sự cân bằng tối ưu giữa 2 lớp: F1 lớp Không cháy đạt 93.87% và F1 lớp Cháy đạt 94.03%. Mô hình không bị thiên vị sang bất kỳ lớp nào (Macro Avg = Weighted Avg = 93.95%)."
    p1.font.name = FONT_NAME; p1.font.size = Pt(14); p1.font.color.rgb = COLOR_TEXT_MAIN

    p2 = tf_r.add_paragraph()
    p2.text = "• Sự mất cân bằng nghiêm trọng của KNN: F1 giữa 2 lớp chênh lệch tới 11.4 điểm phần trăm (78.96% vs 67.56%). KNN có xu hướng gán nhãn về lớp Không cháy để an toàn (Recall lớp 0 lên đến 95.79%), dẫn đến bỏ sót thảm họa cháy rừng."
    p2.font.name = FONT_NAME; p2.font.size = Pt(14); p2.font.color.rgb = COLOR_TEXT_MAIN

    add_notes(s10, "Báo cáo phân loại đầy đủ theo đúng yêu cầu bổ sung: Precision, Recall, F1, Support cho cả 2 lớp và Macro/Weighted Avg.")

    # =========================================================================
    # SLIDE 11: PHÂN TÍCH CONFUSION MATRIX (Mục 3.4 & 3.5 của Thầy)
    # =========================================================================
    s11 = prs.slides.add_slide(blank_layout)
    add_nav_bar(s11, 3)
    add_slide_header(s11, "Phân Tích Ma Trận Nhầm Lẫn (Confusion Matrix)", section_tag="Mục 3.4 & 3.5: Model hay nhầm class nào? Báo nhầm (FP) vs Bỏ sót (FN)")
    add_footer(s11, 11)

    # Chèn hình 06_confusion_matrices.png bên trái
    f6 = FIG_DIR / '06_confusion_matrices.png'
    if f6.exists():
        s11.shapes.add_picture(str(f6), 1016000, 2150000, 9500000, 5600000)

    # Bảng phân tích chi tiết các ca nhầm lẫn bên phải
    tb_shape = s11.shapes.add_table(5, 5, 10900000, 2150000, 9758709, 5600000)
    table = tb_shape.table
    table.columns[0].width = 2558709; table.columns[1].width = 1800000
    table.columns[2].width = 1800000; table.columns[3].width = 1800000; table.columns[4].width = 1800000

    headers = ["MÔ HÌNH", "ĐÚNG K.CHÁY (TN)", "BÁO NHẦM (FP)", "BỎ SÓT (FN)", "ĐÚNG CHÁY (TP)"]
    for j, h in enumerate(headers):
        c = table.cell(0, j); c.fill.solid(); c.fill.fore_color.rgb = COLOR_PRIMARY_BLUE
        p = c.text_frame.paragraphs[0]; p.text = h; p.font.name = FONT_NAME; p.font.size = Pt(13); p.font.bold = True; p.font.color.rgb = COLOR_WHITE; p.alignment = PP_ALIGN.CENTER

    cm_data = [
        ("SVM (Tối ưu)", "176 ảnh (92.6%)", "14 ảnh (7.4%)", "9 ảnh (4.7%)", "181 ảnh (95.3%)"),
        ("Logistic Reg.", "174 ảnh (91.6%)", "16 ảnh (8.4%)", "13 ảnh (6.8%)", "177 ảnh (93.2%)"),
        ("Random Forest", "169 ảnh (88.9%)", "21 ảnh (11.1%)", "26 ảnh (13.7%)", "164 ảnh (86.3%)"),
        ("KNN", "182 ảnh (95.8%)", "8 ảnh (4.2%)", "89 ảnh (46.8%)", "101 ảnh (53.2%)")
    ]
    for i, row in enumerate(cm_data):
        for j, val in enumerate(row):
            c = table.cell(i+1, j); c.fill.solid()
            c.fill.fore_color.rgb = RGBColor(0xFF, 0xFF, 0xFF) if i % 2 == 0 else RGBColor(0xF1, 0xF5, 0xF9)
            if i == 0: c.fill.fore_color.rgb = COLOR_BG_METRIC
            p = c.text_frame.paragraphs[0]; p.text = val; p.font.name = FONT_NAME; p.font.size = Pt(13); p.font.color.rgb = COLOR_TEXT_MAIN
            if j == 0: p.font.bold = True
            if j >= 1: p.alignment = PP_ALIGN.CENTER
            if j == 3 and i == 0: p.font.color.rgb = COLOR_GREEN_SOTA; p.font.bold = True
            if j == 3 and i == 3: p.font.color.rgb = COLOR_RED_ALERT; p.font.bold = True

    # Khối trả lời trực tiếp câu hỏi của Thầy
    card_ans = add_card(s11, 1016000, 7950000, 19642709, 3200000)
    tb_a = s11.shapes.add_textbox(1200000, 8050000, 19200000, 3000000)
    tf_a = tb_a.text_frame; tf_a.word_wrap = True
    p = tf_a.paragraphs[0]; p.text = "TRẢ LỜI CÂU HỎI MỤC 3.5 CỦA THẦY: MODEL HAY NHẦM CLASS NÀO?"
    p.font.name = FONT_NAME; p.font.size = Pt(17); p.font.bold = True; p.font.color.rgb = COLOR_PRIMARY_BLUE

    p1 = tf_a.add_paragraph()
    p1.text = "1. Đối với SVM: Tỉ lệ lỗi rất thấp trên cả 2 phía. Mô hình báo nhầm 14 ảnh Không cháy thành Cháy (FP = 7.37%) và chỉ bỏ sót 9 ảnh Cháy thành Không cháy (FN = 4.74%). Trong bài toán cháy rừng, lỗi bỏ sót (FN) nguy hiểm hơn nhiều so với báo nhầm, và SVM đã kiểm soát FN ở mức thấp nhất (9 ảnh)."
    p1.font.name = FONT_NAME; p1.font.size = Pt(14); p1.font.color.rgb = COLOR_TEXT_MAIN

    p2 = tf_a.add_paragraph()
    p2.text = "2. Đối với KNN: Model bị nhầm trầm trọng lớp Cháy thành Không cháy (FN = 89 ảnh, chiếm tới 46.84%). KNN hầu như bất lực trong việc phát hiện một nửa số đám cháy, cho thấy việc bỏ phiếu k lân cận trong không gian nén PCA là không đáng tin cậy."
    p2.font.name = FONT_NAME; p2.font.size = Pt(14); p2.font.color.rgb = COLOR_TEXT_MAIN

    add_notes(s11, "Phân tích Confusion Matrix trả lời câu hỏi model hay nhầm class nào: KNN bỏ sót 89 ảnh cháy; SVM chỉ bỏ sót 9 ảnh.")

    # =========================================================================
    # SLIDE 12: SO SÁNH TRAIN VS VALIDATION - OVERFITTING (Mục 3.5 & 7 của Thầy)
    # =========================================================================
    s12 = prs.slides.add_slide(blank_layout)
    add_nav_bar(s12, 4)
    add_slide_header(s12, "So Sánh Train vs Validation — Đánh Giá Học Quá Khớp", section_tag="Mục 3.5 & 7: Phân tích Overfitting / Underfitting giữa tập Train và Validation")
    add_footer(s12, 12)

    # Bảng so sánh F1 Train vs Validation
    tb_shape = s12.shapes.add_table(5, 4, 1016000, 2150000, 10500000, 4200000)
    table = tb_shape.table
    table.columns[0].width = 3300000; table.columns[1].width = 2400000
    table.columns[2].width = 2400000; table.columns[3].width = 2400000

    headers = ["MÔ HÌNH", "F1 TRAIN (%)", "F1 VALIDATION (%)", "KHOẢNG CHÊNH LỆCH"]
    for j, h in enumerate(headers):
        c = table.cell(0, j); c.fill.solid(); c.fill.fore_color.rgb = COLOR_PRIMARY_BLUE
        p = c.text_frame.paragraphs[0]; p.text = h; p.font.name = FONT_NAME; p.font.size = Pt(15); p.font.bold = True; p.font.color.rgb = COLOR_WHITE; p.alignment = PP_ALIGN.CENTER

    gap_data = [
        ("SVM (Kiểm soát tốt nhất)", "100,00%", "94,19%", "5,81 điểm phần trăm"),
        ("Logistic Regression", "100,00%", "93,42%", "6,58 điểm phần trăm"),
        ("Random Forest", "100,00%", "86,45%", "13,55 điểm phần trăm"),
        ("KNN", "86,06%", "71,54%", "14,51 điểm phần trăm")
    ]
    for i, row in enumerate(gap_data):
        for j, val in enumerate(row):
            c = table.cell(i+1, j); c.fill.solid()
            c.fill.fore_color.rgb = RGBColor(0xFF, 0xFF, 0xFF) if i % 2 == 0 else RGBColor(0xF1, 0xF5, 0xF9)
            if i == 0: c.fill.fore_color.rgb = COLOR_BG_METRIC
            p = c.text_frame.paragraphs[0]; p.text = val; p.font.name = FONT_NAME; p.font.size = Pt(15); p.font.color.rgb = COLOR_TEXT_MAIN
            if j == 0 or i == 0: p.font.bold = True
            if j >= 1: p.alignment = PP_ALIGN.CENTER
            if j == 3 and i == 0: p.font.color.rgb = COLOR_GREEN_SOTA; p.font.bold = True
            if j == 3 and i in [2, 3]: p.font.color.rgb = COLOR_RED_ALERT

    # Thẻ phân tích Overfitting bên phải
    card_gap = add_card(s12, 11800000, 2150000, 8858709, 4200000, bg_color=COLOR_BG_ALERT, border_color=COLOR_BORDER_ALERT)
    tb_g = s12.shapes.add_textbox(12000000, 2300000, 8450000, 3900000)
    tf_g = tb_g.text_frame; tf_g.word_wrap = True
    p = tf_g.paragraphs[0]; p.text = "DẤU HIỆU HỌC QUÁ KHỚP (OVERFITTING):"
    p.font.name = FONT_NAME; p.font.size = Pt(18); p.font.bold = True; p.font.color.rgb = COLOR_RED_ALERT

    p1 = tf_g.add_paragraph()
    p1.text = "• Điểm Train 100% không có nghĩa mô hình hoàn hảo: Cả SVM, Logistic Regression và Random Forest đều đạt F1 Train tuyệt đối 100%. Không gian 231 đặc trưng đủ phức tạp để phân tách trọn vẹn tập huấn luyện."
    p1.font.name = FONT_NAME; p1.font.size = Pt(14); p1.font.color.rgb = COLOR_TEXT_MAIN

    p2 = tf_g.add_paragraph()
    p2.text = "• Random Forest bị Overfit rõ nét nhất: Điểm train 100% nhưng Val chỉ đạt 86.45% (chênh tới 13.55%). Cây quyết định học vẹt các mẫu Train cụ thể mà không khái quát hóa tốt khi không gian bị xoay bởi PCA."
    p2.font.name = FONT_NAME; p2.font.size = Pt(14); p2.font.color.rgb = COLOR_TEXT_MAIN

    # Khối giải thích cơ chế kiểm soát overfitting của SVM
    card_svm_exp = add_card(s12, 1016000, 6600000, 19642709, 4550000)
    tb_se = s12.shapes.add_textbox(1200000, 6750000, 19200000, 4250000)
    tf_se = tb_se.text_frame; tf_se.word_wrap = True
    p = tf_se.paragraphs[0]; p.text = "TẠI SAO SVM KIỂM SOÁT HỌC QUÁ KHỚP TỐT NHẤT TRONG CẢ 4 MÔ HÌNH?"
    p.font.name = FONT_NAME; p.font.size = Pt(18); p.font.bold = True; p.font.color.rgb = COLOR_PRIMARY_BLUE

    p1 = tf_se.add_paragraph()
    p1.text = "1. Nguyên lý Biên Cực Đại (Maximum Margin): Không chỉ đơn thuần phân tách nhãn 0 và 1, SVM tối đa hóa khoảng cách giữa siêu phẳng phân cách và các Support Vectors gần nhất. Biên cực đại này đóng vai trò như một cơ chế điều hòa tự nhiên (Regularization) kiềm chế mô hình không bám theo nhiễu cục bộ."
    p1.font.name = FONT_NAME; p1.font.size = Pt(15); p1.font.color.rgb = COLOR_TEXT_MAIN

    p2 = tf_se.add_paragraph()
    p2.text = "2. Khoảng chênh lệch Train - Val nhỏ nhất (5.81%): Trên tập Test thực tế, SVM vẫn duy trì F1 94.03% (chỉ giảm 0.16% so với Validation). Điều này chứng minh SVM có khả năng tổng quát hóa (Generalization) vượt trội nhất trên dữ liệu ảnh thực nghiệm."
    p2.font.name = FONT_NAME; p2.font.size = Pt(15); p2.font.color.rgb = COLOR_TEXT_MAIN

    p3 = tf_se.add_paragraph()
    p3.text = "3. Thừa nhận trung thực: Báo cáo không tuyên bố 'xóa bỏ hoàn toàn overfitting'. Mọi mô hình có dung lượng lớn đều có xu hướng khớp sâu tập train. Để giảm thêm khoảng chênh 5.8%, giải pháp tối ưu là bổ sung ảnh thực địa đa dạng hơn."
    p3.font.name = FONT_NAME; p3.font.size = Pt(15); p3.font.bold = True; p3.font.color.rgb = COLOR_DARK_NAVY

    add_notes(s12, "Phân tích Train vs Val trả lời câu hỏi overfitting/underfitting: SVM chênh ít nhất (5.8%), RF chênh 13.5%.")

    # =========================================================================
    # SLIDE 13: ĐÁNH GIÁ ĐƯỜNG HỌC (Learning Curve của SVM) (Mục 3.5 & 7)
    # =========================================================================
    s13 = prs.slides.add_slide(blank_layout)
    add_nav_bar(s13, 4)
    add_slide_header(s13, "Phân Tích Đường Học (Learning Curve) Của Mô Hình SVM", section_tag="Mục 3.5 & 7: Xu hướng cải thiện hiệu năng khi gia tăng kích thước mẫu huấn luyện")
    add_footer(s13, 13)

    # Chèn hình 08_learning_curve.png bên trái
    f8 = FIG_DIR / '08_learning_curve.png'
    if f8.exists():
        s13.shapes.add_picture(str(f8), 1016000, 2150000, 9500000, 5600000)

    # Bảng số liệu Learning Curve bên phải
    tb_shape = s13.shapes.add_table(4, 4, 10900000, 2150000, 9758709, 5600000)
    table = tb_shape.table
    table.columns[0].width = 2558709; table.columns[1].width = 2400000
    table.columns[2].width = 2400000; table.columns[3].width = 2400000

    headers = ["KÍCH THƯỚC MẪU TRAIN", "F1 SCORE TRAIN", "F1 SCORE CV VALIDATION", "XU HƯỚNG TỔNG QUÁT HÓA"]
    for j, h in enumerate(headers):
        c = table.cell(0, j); c.fill.solid(); c.fill.fore_color.rgb = COLOR_PRIMARY_BLUE
        p = c.text_frame.paragraphs[0]; p.text = h; p.font.name = FONT_NAME; p.font.size = Pt(14); p.font.bold = True; p.font.color.rgb = COLOR_WHITE; p.alignment = PP_ALIGN.CENTER

    lc_data = [
        ("1. ~283 mẫu (35%)", "100,00%", "91,00%", "Mô hình mới học quy luật cơ bản"),
        ("2. ~525 mẫu (65%)", "100,00%", "92,62% (+1.62%)", "Khả năng khái quát hóa tăng rõ rệt"),
        ("3. ~809 mẫu (100%)", "100,00%", "93,66% (+1.04%)", "Đạt độ hội tụ tối ưu trên tập Train")
    ]
    for i, row in enumerate(lc_data):
        for j, val in enumerate(row):
            c = table.cell(i+1, j); c.fill.solid()
            c.fill.fore_color.rgb = RGBColor(0xFF, 0xFF, 0xFF) if i % 2 == 0 else RGBColor(0xF1, 0xF5, 0xF9)
            if i == 2: c.fill.fore_color.rgb = COLOR_BG_METRIC
            p = c.text_frame.paragraphs[0]; p.text = val; p.font.name = FONT_NAME; p.font.size = Pt(14); p.font.color.rgb = COLOR_TEXT_MAIN
            if j == 0: p.font.bold = True
            if j in [1, 2]: p.alignment = PP_ALIGN.CENTER
            if j == 2: p.font.bold = True; p.font.color.rgb = COLOR_GREEN_SOTA

    # Khối giải thích ý nghĩa đường học
    card_lc = add_card(s13, 1016000, 7950000, 19642709, 3200000)
    tb_l = s13.shapes.add_textbox(1200000, 8050000, 19200000, 3000000)
    tf_l = tb_l.text_frame; tf_l.word_wrap = True
    p = tf_l.paragraphs[0]; p.text = "Ý NGHĨA KHOA HỌC RÚT RA TỪ ĐƯỜNG HỌC (LEARNING CURVE):"
    p.font.name = FONT_NAME; p.font.size = Pt(17); p.font.bold = True; p.font.color.rgb = COLOR_PRIMARY_BLUE

    p1 = tf_l.add_paragraph()
    p1.text = "• Đường kiểm tra chéo (CV Score) liên tục đi lên: F1 CV tăng trưởng đều đặn từ 91.00% lên 92.62% rồi chạm 93.66% khi bổ sung số lượng ảnh học trong fold. Điều này khẳng định SVM học thực sự các đặc trưng bản chất của ảnh chứ không chỉ ghi nhớ ngẫu nhiên."
    p1.font.name = FONT_NAME; p1.font.size = Pt(14); p1.font.color.rgb = COLOR_TEXT_MAIN

    p2 = tf_l.add_paragraph()
    p2.text = "• Mô hình chưa chạm ngưỡng bão hòa dữ liệu: Độ dốc của đường validation vẫn có xu hướng hướng lên. Kết quả này gợi ý rằng nếu tiếp tục bổ sung thêm 1.000 - 2.000 ảnh phong cảnh rừng mới vào tập huấn luyện, F1 của SVM có thể tiếp tục tăng lên mức 96% - 97%."
    p2.font.name = FONT_NAME; p2.font.size = Pt(14); p2.font.color.rgb = COLOR_TEXT_MAIN

    add_notes(s13, "Đường học cho thấy F1 CV tăng dần khi thêm dữ liệu, chứng tỏ mô hình học tốt và có tiềm năng mở rộng.")

    # =========================================================================
    # SLIDE 14: PHÂN TÍCH LỖI THỰC TẾ (Error Analysis: FN & FP) (Mục 3.5 của Thầy)
    # =========================================================================
    s14 = prs.slides.add_slide(blank_layout)
    add_nav_bar(s14, 4)
    add_slide_header(s14, "Phân Tích Lỗi Thực Tế (Error Analysis: FN & FP)", section_tag="Mục 3.5: Ảnh mờ hay rõ? Thuộc tính độ sáng & nguyên nhân nhầm lẫn")
    add_footer(s14, 14)

    # Chèn hình 09_errors.png bên trái
    f9 = FIG_DIR / '09_errors.png'
    if f9.exists():
        s14.shapes.add_picture(str(f9), 1016000, 2150000, 9500000, 5600000)

    # Bảng số liệu định lượng độ sắc nét & độ sáng bên phải
    tb_shape = s14.shapes.add_table(4, 4, 10900000, 2150000, 9758709, 5600000)
    table = tb_shape.table
    table.columns[0].width = 2558709; table.columns[1].width = 2400000
    table.columns[2].width = 2400000; table.columns[3].width = 2400000

    headers = ["NHÓM DỰ ĐOÁN (SVM)", "SỐ LƯỢNG ẢNH", "ĐỘ SÁNG TRUNG BÌNH", "ĐỘ SẮC NÉT (LAPLACIAN)"]
    for j, h in enumerate(headers):
        c = table.cell(0, j); c.fill.solid(); c.fill.fore_color.rgb = COLOR_PRIMARY_BLUE
        p = c.text_frame.paragraphs[0]; p.text = h; p.font.name = FONT_NAME; p.font.size = Pt(13); p.font.bold = True; p.font.color.rgb = COLOR_WHITE; p.alignment = PP_ALIGN.CENTER

    err_stat = [
        ("Dự đoán Đúng", "357 ảnh (93.95%)", "0,371", "1.686,2 (Rõ nét)"),
        ("Bỏ sót (False Negative)", "9 ảnh (4.74%)", "0,322 (Tối hơn)", "559,2 (MỜ HƠN RÕ RỆT)"),
        ("Báo nhầm (False Positive)", "14 ảnh (7.37%)", "0,376", "1.573,2 (Sắc nét)")
    ]
    for i, row in enumerate(err_stat):
        for j, val in enumerate(row):
            c = table.cell(i+1, j); c.fill.solid()
            c.fill.fore_color.rgb = RGBColor(0xFF, 0xFF, 0xFF) if i % 2 == 0 else RGBColor(0xF1, 0xF5, 0xF9)
            p = c.text_frame.paragraphs[0]; p.text = val; p.font.name = FONT_NAME; p.font.size = Pt(13); p.font.color.rgb = COLOR_TEXT_MAIN
            if j == 0: p.font.bold = True
            if j in [1, 2, 3]: p.alignment = PP_ALIGN.CENTER
            if i == 1 and j == 3: p.font.color.rgb = COLOR_RED_ALERT; p.font.bold = True

    # Khối giải thích câu hỏi của Thầy
    card_err_ans = add_card(s14, 1016000, 7950000, 19642709, 3200000)
    tb_ea = s14.shapes.add_textbox(1200000, 8050000, 19200000, 3000000)
    tf_ea = tb_ea.text_frame; tf_ea.word_wrap = True
    p = tf_ea.paragraphs[0]; p.text = "TRẢ LỜI CÂU HỎI MỤC 3.5: ẢNH MỜ HAY RÕ? NGUYÊN NHÂN GÂY NHẦM LẪN?"
    p.font.name = FONT_NAME; p.font.size = Pt(17); p.font.bold = True; p.font.color.rgb = COLOR_PRIMARY_BLUE

    p1 = tf_ea.add_paragraph()
    p1.text = "• Bằng chứng số liệu về độ mờ: Nhóm ảnh bị BỎ SÓT (FN) có độ sắc nét Laplacian trung bình chỉ 559.2, thấp hơn gấp 3 LẦN so với nhóm ảnh dự đoán đúng (1.686.2). Điều này chứng minh trực tiếp câu hỏi của Thầy: Ảnh mờ và mất chi tiết viền (do khói dày che khuất hoặc lửa ở quá xa trong bóng tối) là nguyên nhân hàng đầu khiến bộ trích xuất HOG bị vô hiệu hóa."
    p1.font.name = FONT_NAME; p1.font.size = Pt(14); p1.font.color.rgb = COLOR_TEXT_MAIN

    p2 = tf_ea.add_paragraph()
    p2.text = "• Nguyên nhân Báo nhầm (FP = 14 ảnh): Xuất hiện các cảnh rừng có mây mù sương trắng dày trên ngọn cây (nofire_0400) tạo kết cấu giống khói lửa, hoặc tán cây đổi màu vàng cam mùa thu (nofire_0422) kích hoạt nhầm histogram màu Hue ấm."
    p2.font.name = FONT_NAME; p2.font.size = Pt(14); p2.font.color.rgb = COLOR_TEXT_MAIN

    add_notes(s14, "Phân tích lỗi định lượng trả lời câu hỏi ảnh mờ/rõ: nhóm FN có độ sắc nét chỉ 559 so với 1.686 của nhóm đúng.")

    # =========================================================================
    # SLIDE 15: TRẢ LỜI TOÀN DIỆN CÂU HỎI CỦA THẦY (Mục 3.5 của Thầy)
    # =========================================================================
    s15 = prs.slides.add_slide(blank_layout)
    add_nav_bar(s15, 4)
    add_slide_header(s15, "Tổng Kết Trả Lời Toàn Diện 8 Câu Hỏi Đề Cương Của Thầy", section_tag="Mục 3.5: Trả lời đẩy đủ 8 câu hỏi bắt buộc trong đề tài đồ án")
    add_footer(s15, 15)

    # 8 Câu hỏi & câu trả lời súc tích
    q_and_a = [
        ("1. Model nào tốt nhất?", "SVM (Kernel RBF, C=10) đạt điểm cao nhất trên cả Validation (F1 94.19%) và Test (F1 94.03%, Accuracy 93.95%)."),
        ("2. Chênh lệch nhau bao nhiêu?", "SVM vượt trội hơn Logistic Regression +1.36%, vượt Random Forest +6.56% và bỏ xa KNN tới +26.47% F1 Test."),
        ("3. Phân tích các metrics?", "SVM cân bằng lý tưởng: Recall 95.26% (ưu tiên hàng đầu để hạn chế sót cháy), Precision 92.82%, F1 94.03%."),
        ("4. Model hay nhầm class nào?", "KNN hay nhầm lớp Cháy thành Không cháy (bỏ sót 89 ảnh). SVM nhầm rất ít: chỉ 14 ảnh FP và 9 ảnh FN."),
        ("5. Ảnh mờ hay rõ ảnh hưởng thế nào?", "Ảnh bị bỏ sót (FN) có độ sắc nét trung bình chỉ 559 (mờ hơn gấp 3 lần so với 1.686 của ảnh đúng). Ảnh mờ làm hỏng HOG."),
        ("6. Train vs Val có Overfit không?", "Có overfit nhẹ ở SVM (chênh 5.81%) và LR (6.58%); Overfit nặng ở Random Forest (chênh 13.55%). SVM kiểm soát tốt nhất."),
        ("7. Model nào phù hợp với dữ liệu?", "SVM RBF phù hợp nhất nhờ năng lực ánh xạ phi tuyến trên không gian kết hợp màu sắc HSV + kết cấu viền HOG."),
        ("8. Điều gì ảnh hưởng đến kết quả?", "Chất lượng trích đặc trưng, kích thước resize 96x96, việc áp dụng PCA lên Random Forest, và điều kiện thời tiết (sương, lá vàng).")
    ]
    for i, (q, a) in enumerate(q_and_a):
        x = 1016000 + (i % 2) * 9900000
        y = 2150000 + (i // 2) * 2250000
        card = add_card(s15, x, y, 9600000, 2100000)
        tb = s15.shapes.add_textbox(x + 150000, y + 100000, 9300000, 1900000)
        tf = tb.text_frame; tf.word_wrap = True
        p = tf.paragraphs[0]; p.text = q; p.font.name = FONT_NAME; p.font.size = Pt(15); p.font.bold = True; p.font.color.rgb = COLOR_PRIMARY_BLUE
        p1 = tf.add_paragraph(); p1.text = f"👉 {a}"; p1.font.name = FONT_NAME; p1.font.size = Pt(13); p1.font.color.rgb = COLOR_TEXT_MAIN

    add_notes(s15, "Slide trả lời trực tiếp toàn bộ 8 câu hỏi cốt lõi của Thầy tại Mục 3.5 trong đề cương.")

    # =========================================================================
    # SLIDE 16: KẾT LUẬN & ĐỐI CHIẾU YÊU CẦU ĐỒ ÁN (Mục 8 & Bảng đối chiếu)
    # =========================================================================
    s16 = prs.slides.add_slide(blank_layout)
    add_nav_bar(s16, 4)
    add_slide_header(s16, "Kết Luận & Bảng Đối Chiếu Yêu Cầu Đề Cương", section_tag="Mục 8: Hoàn thành 100% các tiêu chí đánh giá môn học của Thầy")
    add_footer(s16, 16)

    # Bảng đối chiếu 10 mục của Thầy
    tb_shape = s16.shapes.add_table(6, 4, 1016000, 2150000, 19642709, 5200000)
    table = tb_shape.table
    table.columns[0].width = 3000000; table.columns[1].width = 6500000
    table.columns[2].width = 5000000; table.columns[3].width = 5142709

    headers = ["MỤC YÊU CẦU", "NỘI DUNG THỰC HIỆN TRONG ĐỒ ÁN", "VỊ TRÍ BÁO CÁO & SLIDE", "TRẠNG THÁI HOÀN THÀNH"]
    for j, h in enumerate(headers):
        c = table.cell(0, j); c.fill.solid(); c.fill.fore_color.rgb = COLOR_PRIMARY_BLUE
        p = c.text_frame.paragraphs[0]; p.text = h; p.font.name = FONT_NAME; p.font.size = Pt(15); p.font.bold = True; p.font.color.rgb = COLOR_WHITE; p.alignment = PP_ALIGN.CENTER

    audit_table = [
        ("1. Tóm tắt & Dataset", "1.896 ảnh DeepFire, kiểm toán SHA256 & dHash, chia Train/Val/Test cân bằng 50:50", "Báo cáo Mục 1-2; Slide 01-03", "Hoàn thành 100% (Passed)"),
        ("2. EDA & Tiền xử lý", "Phân tích 5 biểu đồ EDA ảnh; Tiền xử lý HSV 64 bin + HOG 800 bin, PCA 231 chiều", "Báo cáo Mục 3-4; Slide 04-06", "Hoàn thành 100% (Passed)"),
        ("3. Mô hình ML & Tham số", "4 mô hình: Logistic Regression, KNN, SVM, Random Forest; 3-fold Group CV", "Báo cáo Mục 5; Slide 07-08", "Hoàn thành 100% (Passed)"),
        ("4. Đánh giá & Metrics", "Accuracy, Precision, Recall, F1 cả 2 lớp, Confusion Matrix, Macro/Weighted Avg", "Báo cáo Mục 6; Slide 09-11", "Hoàn thành 100% (Passed)"),
        ("5. Phân tích kết quả & Lỗi", "So sánh Train vs Val (Overfitting), Learning Curve, phân tích định lượng ảnh FN/FP", "Báo cáo Mục 7; Slide 12-15", "Hoàn thành 100% (Passed)")
    ]
    for i, row in enumerate(audit_table):
        for j, val in enumerate(row):
            c = table.cell(i+1, j); c.fill.solid()
            c.fill.fore_color.rgb = RGBColor(0xFF, 0xFF, 0xFF) if i % 2 == 0 else RGBColor(0xF1, 0xF5, 0xF9)
            p = c.text_frame.paragraphs[0]; p.text = val; p.font.name = FONT_NAME; p.font.size = Pt(14); p.font.color.rgb = COLOR_TEXT_MAIN
            if j == 0: p.font.bold = True
            if j == 3: p.alignment = PP_ALIGN.CENTER; p.font.bold = True; p.font.color.rgb = COLOR_GREEN_SOTA

    # Khối kết luận giá trị cốt lõi
    card_sum = add_card(s16, 1016000, 7650000, 19642709, 3500000, bg_color=COLOR_BG_METRIC, border_color=COLOR_BORDER_METRIC)
    tb_sm = s16.shapes.add_textbox(1200000, 7800000, 19200000, 3200000)
    tf_sm = tb_sm.text_frame; tf_sm.word_wrap = True
    p = tf_sm.paragraphs[0]; p.text = "TỔNG KẾT THÀNH QUẢ ĐẠT ĐƯỢC CỦA ĐỒ ÁN MÔN HỌC MÁY HỌC:"
    p.font.name = FONT_NAME; p.font.size = Pt(18); p.font.bold = True; p.font.color.rgb = COLOR_PRIMARY_BLUE

    p1 = tf_sm.add_paragraph()
    p1.text = "1. Xây dựng hoàn chỉnh một quy trình Machine Learning thị giác máy tính chuẩn mực: Từ đọc dữ liệu thô, kiểm toán chống rò rỉ (dHash), trích xuất đặc trưng kết hợp (Màu sắc + Hình thái cạnh), tối ưu hóa siêu tham số đến kiểm thử khách quan."
    p1.font.name = FONT_NAME; p1.font.size = Pt(15); p1.font.color.rgb = COLOR_TEXT_MAIN

    p2 = tf_sm.add_paragraph()
    p2.text = "2. Mô hình SVM (RBF) chứng minh hiệu quả vượt trội: Đạt F1 Test 94.03% và Recall 95.26% trên 380 ảnh kiểm thử, vượt qua các mô hình khác nhờ năng lực phân ranh giới phi tuyến biên cực đại."
    p2.font.name = FONT_NAME; p2.font.size = Pt(15); p2.font.color.rgb = COLOR_TEXT_MAIN

    p3 = tf_sm.add_paragraph()
    p3.text = "3. Tính tái lập tuyệt đối (100% Reproducibility): Toàn bộ số liệu, hình ảnh và mô hình đều được tự động hóa bằng code Python độc lập, sẵn sàng chuyển giao và kiểm chứng."
    p3.font.name = FONT_NAME; p3.font.size = Pt(15); p3.font.color.rgb = COLOR_TEXT_MAIN

    add_notes(s16, "Kết luận đồ án và đối chiếu bảng 10 mục của Thầy: hoàn thành 100% với tính liêm chính học thuật cao.")

    # =========================================================================
    # SLIDE 17: HƯỚNG PHÁT TRIỂN & ỨNG DỤNG THỰC TẾ (Mục 9 của Thầy)
    # =========================================================================
    s17 = prs.slides.add_slide(blank_layout)
    add_nav_bar(s17, 4)
    add_slide_header(s17, "Hướng Phát Triển Đề Tài & Triển Khai Thực Địa", section_tag="Mục 9: Các giải pháp mở rộng thực tế trong tương lai")
    add_footer(s17, 17)

    # 4 Khối hướng phát triển
    future_directions = [
        ("1. Dữ Liệu Bất Cân Bằng Thực Địa", "Thu thập dữ liệu camera quan sát thực tế (nơi ảnh không cháy chiếm >99%). Áp dụng kỹ thuật Threshold Moving hoặc Cost-Sensitive Learning để tối ưu hóa chi phí bỏ sót cháy."),
        ("2. Phân Tích Chuỗi Video Thời Gian", "Không xử lý từng khung hình độc lập mà tích hợp Temporal Smoothing (lọc thời gian qua 10-30 khung hình liên tiếp) để loại bỏ hiện tượng nhấp nháy báo nhầm do sương gió."),
        ("3. Nâng Cấp Deep Learning (CNN / YOLO)", "Thử nghiệm các kiến trúc học sâu hiện đại (MobileNetV3, ResNet) và mô hình Object Detection (YOLOv8/v11) để không chỉ phân loại mà còn khoanh vùng tọa độ ngọn lửa (Bounding Box)."),
        ("4. Đóng Gói Nhúng Phần Cứng Biên (Edge AI)", "Tối ưu hóa mô hình qua ONNX Runtime / TensorRT để triển khai trực tiếp trên thiết bị nhúng công suất thấp (Raspberry Pi 5, Jetson Nano) gắn trên Drone tuần tra rừng.")
    ]
    for i, (title, desc) in enumerate(future_directions):
        x = 1016000 + (i % 2) * 9900000
        y = 2150000 + (i // 2) * 4400000
        card = add_card(s17, x, y, 9600000, 4100000)
        tb = s17.shapes.add_textbox(x + 200000, y + 200000, 9200000, 3700000)
        tf = tb.text_frame; tf.word_wrap = True
        p = tf.paragraphs[0]; p.text = title; p.font.name = FONT_NAME; p.font.size = Pt(18); p.font.bold = True; p.font.color.rgb = COLOR_PRIMARY_BLUE
        p_sub = tf.add_paragraph()
        p_sub.text = desc; p_sub.font.name = FONT_NAME; p_sub.font.size = Pt(15); p_sub.font.color.rgb = COLOR_TEXT_MAIN

    add_notes(s17, "Trình bày 4 hướng phát triển thực tiễn: dữ liệu thực tế bất cân bằng, video stream, deep learning và edge AI.")

    # =========================================================================
    # SLIDE 18: SẢN PHẨM NỘP, DEMO SUY LUẬN & CẢM ƠN (Mục 10 & 6 của Thầy)
    # =========================================================================
    s18 = prs.slides.add_slide(blank_layout)
    top_bar = s18.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, 220000)
    top_bar.fill.solid(); top_bar.fill.fore_color.rgb = COLOR_PRIMARY_BLUE; top_bar.line.fill.background()

    add_slide_header(s18, "Tổng Hợp Sản Phẩm Bàn Giao & Lời Cảm Ơn", section_tag="Mục 10 & 6: File Word, Notebook Colab, Script, Model đã train")
    add_footer(s18, 18)

    # Cột trái: 4 sản phẩm nộp hoàn chỉnh
    card_del = add_card(s18, 1016000, 2150000, 9500000, 5200000)
    tb_del = s18.shapes.add_textbox(1200000, 2300000, 9100000, 4900000)
    tf_d = tb_del.text_frame; tf_d.word_wrap = True
    p = tf_d.paragraphs[0]; p.text = "CÁC SẢN PHẨM NỘP ĐẦY ĐỦ THEO YÊU CẦU:"
    p.font.name = FONT_NAME; p.font.size = Pt(18); p.font.bold = True; p.font.color.rgb = COLOR_PRIMARY_BLUE

    dels = [
        ("1. Báo cáo Word hoàn chỉnh:", "reports/Bao_cao_MayHoc_Chay_rung.docx (3.3 MB, đúng 10 mục của Thầy)."),
        ("2. Slide báo cáo thuyết trình:", "slides/Bao_cao_MayHoc_Chay_rung.pptx (18 slide Visual chuẩn UIT)."),
        ("3. File Notebook tự chứa mã:", "notebooks/MayHoc_Chay_rung.ipynb (Chạy 1 click 'Run All' trên Google Colab)."),
        ("4. Toàn bộ mã nguồn & Model:", "src/experiment.py, src/predict.py và 4 file models/*.joblib đã train sẵn.")
    ]
    for t, d in dels:
        p_t = tf_d.add_paragraph(); p_t.text = t; p_t.font.name = FONT_NAME; p_t.font.size = Pt(15); p_t.font.bold = True; p_t.font.color.rgb = COLOR_DARK_NAVY
        p_d = tf_d.add_paragraph(); p_d.text = d; p_d.font.name = FONT_NAME; p_d.font.size = Pt(13); p_d.font.color.rgb = COLOR_TEXT_MAIN

    # Cột phải: Demo suy luận nhanh
    card_demo = add_card(s18, 10900000, 2150000, 9758709, 5200000, bg_color=COLOR_BG_METRIC, border_color=COLOR_BORDER_METRIC)
    tb_dm = s18.shapes.add_textbox(11100000, 2300000, 9350000, 4900000)
    tf_dm = tb_dm.text_frame; tf_dm.word_wrap = True
    p = tf_dm.paragraphs[0]; p.text = "DEMO SUY LUẬN NHANH TRÊN MÁY TÍNH (CLI):"
    p.font.name = FONT_NAME; p.font.size = Pt(18); p.font.bold = True; p.font.color.rgb = COLOR_PRIMARY_BLUE

    p1 = tf_dm.add_paragraph()
    p1.text = "• Câu lệnh kiểm tra dự đoán 1 ảnh bất kỳ bằng model SVM tối ưu:"
    p1.font.name = FONT_NAME; p1.font.size = Pt(14); p1.font.color.rgb = COLOR_TEXT_MAIN

    p_cmd = tf_dm.add_paragraph()
    p_cmd.text = "python src/predict.py duong_dan_anh.jpg"
    p_cmd.font.name = "Consolas"; p_cmd.font.size = Pt(15); p_cmd.font.bold = True; p_cmd.font.color.rgb = COLOR_DARK_NAVY

    p2 = tf_dm.add_paragraph()
    p2.text = "• Kết quả thực tế đã kiểm thử trực tiếp trên terminal:"
    p2.font.name = FONT_NAME; p2.font.size = Pt(14); p2.font.color.rgb = COLOR_TEXT_MAIN

    p_res1 = tf_dm.add_paragraph()
    p_res1.text = ">> fire_0002.jpg    -->  {'model': 'SVM', 'label': 1, 'class': 'Cháy'}"
    p_res1.font.name = "Consolas"; p_res1.font.size = Pt(13); p_res1.font.bold = True; p_res1.font.color.rgb = COLOR_GREEN_SOTA

    p_res2 = tf_dm.add_paragraph()
    p_res2.text = ">> nofire_0006.jpg  -->  {'model': 'SVM', 'label': 0, 'class': 'Không cháy'}"
    p_res2.font.name = "Consolas"; p_res2.font.size = Pt(13); p_res2.font.bold = True; p_res2.font.color.rgb = COLOR_PRIMARY_BLUE

    # Khối cảm ơn bên dưới
    card_thanks = add_card(s18, 1016000, 7650000, 19642709, 3500000, bg_color=COLOR_CALLOUT_BG, border_color=COLOR_CALLOUT_LINE)
    tb_th = s18.shapes.add_textbox(1200000, 7800000, 19200000, 3200000)
    tf_th = tb_th.text_frame; tf_th.word_wrap = True
    p = tf_th.paragraphs[0]; p.text = "XIN CHÂN THÀNH CẢM ƠN QUÝ THẦY CÔ VÀ HỘI ĐỒNG!"
    p.font.name = FONT_NAME; p.font.size = Pt(22); p.font.bold = True; p.font.color.rgb = COLOR_CALLOUT_LINE; p.alignment = PP_ALIGN.CENTER

    p_th1 = tf_th.add_paragraph()
    p_th1.text = "Nhóm chúng em rất mong nhận được những góp ý quý báu từ Quý Thầy Cô để tiếp tục hoàn thiện đồ án."
    p_th1.font.name = FONT_NAME; p_th1.font.size = Pt(16); p_th1.alignment = PP_ALIGN.CENTER; p_th1.font.color.rgb = COLOR_TEXT_MAIN

    p_th2 = tf_th.add_paragraph()
    p_th2.text = "Kính chúc Quý Thầy Cô dồi dào sức khỏe và công tác tốt!"
    p_th2.font.name = FONT_NAME; p_th2.font.size = Pt(16); p_th2.font.bold = True; p_th2.alignment = PP_ALIGN.CENTER; p_th2.font.color.rgb = COLOR_DARK_NAVY

    add_notes(s18, "Slide kết thúc: tổng kết sản phẩm nộp, demo CLI và lời cảm ơn Hội đồng.")

    # Lưu file
    OUT_PPTX.parent.mkdir(parents=True, exist_ok=True)
    prs.save(str(OUT_PPTX))
    print(f"Successfully generated 18-slide presentation at: {OUT_PPTX}")

if __name__ == '__main__':
    build_presentation()
