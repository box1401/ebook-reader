import streamlit as st
import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup
import asyncio
import edge_tts
import os

# --- 1. 解析 ePub 取出章節 (讀取官方目錄版) ---
@st.cache_data 
def parse_epub(file_bytes):
    with open("temp.epub", "wb") as f:
        f.write(file_bytes)
    
    book = epub.read_epub("temp.epub")
    chapters = []
    
    def build_toc_map(toc_items):
        toc_map = {}
        for item in toc_items:
            if isinstance(item, ebooklib.epub.Link):
                href = item.href.split('#')[0] 
                if href not in toc_map:
                    toc_map[href] = item.title
            elif isinstance(item, tuple) and len(item) == 2:
                section, sub_items = item
                if isinstance(section, ebooklib.epub.Section) and section.href:
                    href = section.href.split('#')[0]
                    if href not in toc_map:
                        toc_map[href] = section.title
                toc_map.update(build_toc_map(sub_items))
        return toc_map

    toc_map = build_toc_map(book.toc)
    
    for item_id, _ in book.spine:
        item = book.get_item_with_id(item_id)
        if item and item.get_type() == ebooklib.ITEM_DOCUMENT:
            file_name = item.get_name() 
            soup = BeautifulSoup(item.get_content(), 'html.parser')
            
            # ✨ 必須先移除不要的標籤 ✨
            for tag in soup.find_all('sup'):
                tag.decompose()
            for tag in soup.find_all(attrs={"epub:type": ["noteref", "footnote"]}):
                tag.decompose()
            for tag in soup.find_all(lambda t: t.has_attr('class') and any('note' in c.lower() or 'footnote' in c.lower() for c in t.get('class', []))):
                tag.decompose()
            for tag in soup.find_all(['figure', 'figcaption']):
                tag.decompose()
                
            # ✨ 清洗乾淨後，再提取文字 ✨
            content = soup.get_text().strip()
            
            if len(content) > 50:
                if file_name in toc_map:
                    title = toc_map[file_name]
                else:
                    title_tag = soup.find(['title', 'h1', 'h2'])
                    title = title_tag.get_text().strip() if title_tag else f"未命名章節 {len(chapters)+1}"
                    
                chapters.append({"title": title, "content": content})
     
    if os.path.exists("temp.epub"):
        os.remove("temp.epub")
        
    return chapters
async def generate_audio(text, voice):
    communicate = edge_tts.Communicate(text, voice)
    audio_data = bytearray()
    
    # 流式獲取音訊，直接存入記憶體
    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            audio_data.extend(chunk["data"])
            
    return bytes(audio_data)

# --- 3. 網頁介面主程式 ---
st.set_page_config(page_title="電子書轉有聲書", page_icon="🎧", layout="centered")
st.title("🎧 電子書轉有聲書 ")
st.markdown("上傳書籍，選擇章節，一鍵轉成 MP3 聆聽與下載！")

# 檔案上傳區塊
uploaded_file = st.file_uploader("📂 請上傳電子書檔案", type="epub")

if uploaded_file:
    # 讀取並解析章節
    file_bytes = uploaded_file.getvalue()
    chapters = parse_epub(file_bytes)
    
    if not chapters:
        st.error("解析失敗：找不到有效的章節內容。")
    else:
        st.success(f"成功解析！共找到 {len(chapters)} 個章節。")
        
        # 建立兩欄式排版選擇器
        col1, col2 = st.columns([2, 1])
        
        with col1:
            chapter_titles = [f"{i+1}. {c['title']}" for i, c in enumerate(chapters)]
            selected_idx = st.selectbox("📖 選擇要聽的章節", range(len(chapter_titles)), format_func=lambda x: chapter_titles[x])
            selected_chapter = chapters[selected_idx]
            
        with col2:
            voice_option = st.selectbox(
                "🗣️ 選擇語音",
                ["zh-TW-HsiaoChenNeural", "zh-TW-YunJheNeural", "zh-CN-XiaoxiaoNeural"]
            )
            
        st.markdown("---")
        
        # 執行轉換
        if st.button("🚀 生成章節語音", use_container_width=True):
            with st.spinner("正在呼叫小幫手幫你念故事，請稍候..."):
                try:
                    # 轉換完整章節
                    text_to_process = selected_chapter['content']
                    
                    # 取得音檔二進位資料
                    audio_bytes = asyncio.run(generate_audio(text_to_process, voice_option))
                    
                    st.success("✨ 轉換完成！")
                    
                    # 使用 Streamlit 內建的乾淨播放器
                    st.audio(audio_bytes, format="audio/mp3")
                    
                    # 提供 MP3 下載按鈕
                    st.download_button(
                        label="📥 下載此章節 MP3",
                        data=audio_bytes,
                        file_name=f"{selected_chapter['title']}.mp3",
                        mime="audio/mp3"
                    )
                    
                except Exception as e:
                    st.error(f"發生錯誤：{e}")