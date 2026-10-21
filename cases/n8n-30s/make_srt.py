import re, textwrap

# VO script cac cau (khop voi vo_fast.wav = 28.92s)
lines = [
    "Bất kỳ công việc nào làm đi làm lại — giờ có thể tự động hóa.",
    "n8n là nền tảng tự động hóa quy trình làm việc,",
    "và nó đã có trí tuệ nhân tạo tích hợp sẵn.",
    "Hơn hai trăm nghìn lập trình viên trên thế giới đang dùng công cụ này mỗi ngày.",
    "Kéo và thả. Kết nối bất kỳ ứng dụng nào —",
    "từ Gmail, Slack, đến cơ sở dữ liệu. Thêm trí tuệ nhân tạo vào bất kỳ bước nào — không cần viết code.",
    "Công việc tám tiếng — giảm xuống còn hai mươi phút.",
    "Mã nguồn mở. Tự cài đặt trên máy chủ của bạn. Không phụ thuộc vào nhà cung cấp nào.",
    "n8n.io — thử ngay, miễn phí.",
]

# Chia deu 28.92s cho cac cau (estimate)
# Timestamps: du tinh theo do dai text
total_dur = 28.5
char_counts = [len(l) for l in lines]
total_chars = sum(char_counts)

srt = []
t = 0.5  # start 0.5s vao
idx = 1

def fmt_time(sec):
    h = int(sec//3600)
    m = int((sec%3600)//60)
    s = sec % 60
    return f"{h:02d}:{m:02d}:{s:06.3f}".replace('.', ',')

for i, line in enumerate(lines):
    dur = (char_counts[i] / total_chars) * total_dur
    dur = max(dur, 1.5)
    end = min(t + dur, 29.5)
    
    # Wrap long lines
    wrapped = textwrap.wrap(line, width=34)
    text = "\n".join(wrapped[:2])
    
    srt.append(f"{idx}")
    srt.append(f"{fmt_time(t)} --> {fmt_time(end)}")
    srt.append(text)
    srt.append("")
    idx += 1
    t = end + 0.05

with open("subtitles.srt", "w", encoding="utf-8") as f:
    f.write("\n".join(srt))
print("subtitles.srt written")