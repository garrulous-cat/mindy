#!/usr/bin/env python3
"""
解析健保藥品給付規定 PDF → data/drugs.json
用法：python scripts/parse_pdf.py <pdf路徑>
"""

import sys
import json
import re
import pdfplumber
from pathlib import Path

def parse_drug_sections(pdf_path: str) -> list[dict]:
    print(f"📖 讀取 PDF：{pdf_path}")
    full_text = ""
    with pdfplumber.open(pdf_path) as pdf:
        total = len(pdf.pages)
        for i, page in enumerate(pdf.pages):
            t = page.extract_text()
            if t:
                full_text += t + "\n"
            if (i + 1) % 50 == 0:
                print(f"  已讀取 {i+1}/{total} 頁...")

    print(f"✅ 共讀取 {total} 頁，開始解析...")

    # 清理頁首頁尾
    full_text = re.sub(r'\(\d{3}\.\d+\.\d+更新\)', '', full_text)
    full_text = re.sub(r'\f', '\n', full_text)

    # 切割條目：形如 "1.2.3.藥名" 或 "1.2.3 藥名"
    pattern = re.compile(
        r'^(\d+\.\d+(?:\.\d+)?\.?\s{0,3}[A-Za-z\u4e00-\u9fff\(（][^\n]{2,120})$',
        re.MULTILINE
    )

    entries = []
    matches = list(pattern.finditer(full_text))

    for i, m in enumerate(matches):
        title = m.group(1).strip()
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(full_text)
        body = full_text[start:end].strip()

        if len(body) < 10:
            continue

        # 抽出英文藥名
        drug_names = re.findall(
            r'\b[A-Z][a-zA-Z]{3,}(?:\s+[a-zA-Z]{3,}){0,2}\b',
            title + ' ' + body[:500]
        )
        drug_names = list(dict.fromkeys(drug_names))[:8]  # 去重，最多8個

        # 抽出章節編號
        section_match = re.match(r'^(\d+\.\d+)', title)
        section = section_match.group(1) if section_match else ''

        entries.append({
            "id": i,
            "title": title,
            "drug_names": drug_names,
            "section": section,
            "content": body[:4000],  # 最多4000字
        })

    return entries


def main():
    # 決定 PDF 路徑
    if len(sys.argv) > 1:
        pdf_path = sys.argv[1]
    else:
        # 自動找最新的 PDF
        pdfs = sorted(Path('.').glob('*.pdf')) + sorted(Path('data').glob('*.pdf'))
        if not pdfs:
            print("❌ 找不到 PDF 檔案，請指定路徑：python scripts/parse_pdf.py 給付規定.pdf")
            sys.exit(1)
        pdf_path = str(pdfs[-1])
        print(f"自動選擇：{pdf_path}")

    entries = parse_drug_sections(pdf_path)
    print(f"✅ 解析完成，共 {len(entries)} 個條目")

    out = Path('data/drugs.json')
    out.parent.mkdir(exist_ok=True)
    with open(out, 'w', encoding='utf-8') as f:
        json.dump(entries, f, ensure_ascii=False, indent=2)

    print(f"💾 已儲存：{out}（{out.stat().st_size // 1024} KB）")


if __name__ == '__main__':
    main()
