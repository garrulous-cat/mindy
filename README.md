# 💊 健保藥品給付規定查詢網站

不需要任何程式基礎，跟著步驟做就可以架好！

---

## 🚀 第一次設定（約 15 分鐘）

### 步驟 1：建立免費 GitHub 帳號

1. 打開瀏覽器，前往 [https://github.com](https://github.com)
2. 點右上角「Sign up」
3. 依照指示完成註冊（需要 email）

---

### 步驟 2：上傳這個專案到 GitHub

1. 登入 GitHub 後，點右上角「+」→「New repository」
2. Repository name 填入：`nhi-drug-search`
3. 選「Public」（公開，才能用免費的 Pages）
4. 點「Create repository」
5. 選擇「uploading an existing file」
6. 把這個資料夾裡的**所有檔案和資料夾**都拖進去上傳
7. 點「Commit changes」

---

### 步驟 3：開啟 GitHub Pages（讓網站可以公開瀏覽）

1. 進入你的 repository 頁面
2. 點上方「Settings」（齒輪圖示）
3. 左側選「Pages」
4. Source 選「Deploy from a branch」
5. Branch 選「main」，資料夾選「/ (root)」
6. 點「Save」

等 1~2 分鐘，你的網站就會在這個網址可以看：
```
https://你的帳號名.github.io/nhi-drug-search
```

---

### 步驟 4：設定每週自動更新

1. 進入 repository 頁面
2. 點上方「Actions」
3. 如果看到提示說「I understand my workflows, go ahead and enable them」→ 點它
4. 完成！之後每週一早上 10 點會自動執行

---

## 🔄 手動觸發更新

如果你知道健保署剛公告新版，不想等到週一：

1. 進入 repository → 點「Actions」
2. 左側點「每週自動更新藥品給付規定」
3. 右側點「Run workflow」→「Run workflow」

---

## 📁 專案結構說明

```
nhi-drug-search/
├── index.html              # 搜尋網站主頁面
├── data/
│   ├── drugs.json          # 解析好的給付規定資料
│   └── last_version.txt    # 記錄目前版本號
├── scripts/
│   ├── check_update.py     # 自動檢查更新腳本
│   └── parse_pdf.py        # PDF 解析腳本
├── .github/workflows/
│   └── update.yml          # GitHub Actions 自動排程設定
└── requirements.txt        # Python 套件清單
```

---

## ❓ 常見問題

**Q：網站多久更新一次？**
A：GitHub Actions 設定每週一早上 10 點自動執行，檢查健保署有沒有新 PDF，有才會更新。

**Q：GitHub Actions 免費嗎？**
A：Public repository 完全免費，每月有 2,000 分鐘額度（本專案每次執行約 2 分鐘）。

**Q：健保署更新格式怎麼辦？**
A：如果 `check_update.py` 找不到新的 PDF 連結，GitHub Actions 執行結果會顯示錯誤，你可以到 Actions 頁面查看，再手動下載 PDF 執行一次解析。

**Q：如何手動更新資料？**
A：從健保署下載新版 PDF，重命名為任意名稱，放到 `data/` 資料夾，再執行：
```
python scripts/parse_pdf.py data/你下載的檔案.pdf
```
然後把 `data/drugs.json` 上傳到 GitHub。

---

## ⚠️ 聲明

本網站資料來源為衛生福利部中央健康保險署，僅供查詢參考，
以健保署官方公告內容為準。本站不承擔任何因資料落差造成的責任。
