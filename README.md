# 🎧 ePub 有聲書轉換器 (ePub to Audiobook Converter)

這是一個基於 Python 與 Streamlit 開發的輕量級 Web 應用程式。只要上傳 `.epub` 電子書檔案，就能自動為你解析完美章節、過濾多餘註解，並使用高自然度的 AI 語音將文字轉換為 MP3 有聲書！

##  核心特色 (Features)

* **精準目錄解析**：直接讀取 ePub 官方目錄（TOC）架構，完美還原書籍的章節順序與標題。
* **智慧內文清洗**：內建強大的 HTML 過濾器，自動剃除「上標字（註腳號碼）」、「電子書譯註區塊」以及「圖片說明」，確保朗讀過程流暢，不被雜訊干擾。
* **多種語音選擇**：整合 `edge-tts`，提供多款自然且富有情緒起伏的微軟 AI 語音（如：曉臻、雲哲等）供自由選擇。
* **線上試聽與下載**：轉換完成後可直接在網頁內播放試聽，並提供一鍵下載 MP3 檔案功能。

## 🚀 線上體驗 (Demo)

> **[點擊這裡前往使用網頁版 (Streamlit Cloud)](https://ebookreaderepub.streamlit.app/)** >

---

## 💻 本機端執行 (Local Installation)

如果你想要在自己的電腦上運行這個專案，請確保你已安裝 Python 3.8 或以上版本。

**1. 複製專案到本地**
```bash
git clone [https://github.com/你的帳號/你的專案名稱.git](https://github.com/你的帳號/你的專案名稱.git)
cd 你的專案名稱
2. 安裝必備套件

Bash
pip install -r requirements.txt
3. 啟動 Streamlit 伺服器

Bash
streamlit run app.py
執行後，瀏覽器將會自動開啟 http://localhost:8501。

🛠️ 技術棧 (Tech Stack)
前端介面：Streamlit

電子書解析：EbookLib, BeautifulSoup4

語音合成引擎：edge-tts

⚠️ 注意事項
本工具之語音轉換功能依賴網路連線至微軟伺服器，若轉換超長章節時遇到 Timeout 錯誤，建議分段處理或檢查網路連線。

本專案僅供個人學習與輔助閱讀使用，請尊重原作者版權，勿將轉換後的有聲書用於任何商業或侵權行為。
