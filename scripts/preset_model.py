# 個人職場數位化分析：範例資料（全虛構）＋獨立 Python 模型核對
import json, io, sys

def T(id, name, cat, freq, minutes, level, potential, difficulty, tool, toolCost, learnHours):
    return dict(id=id, name=name, categoryId=cat, freq=freq, minutes=minutes, level=level, potential=potential,
                difficulty=difficulty, tool=tool, toolCost=toolCost, learnHours=learnHours)

def C(id, name, target):
    return dict(id=id, name=name, targetPct=target)

PRESETS = [
  dict(id="admin", emoji="🗂️", label="行政助理", blurb="多數工作已上雲端，工具幾乎免費，示範健康的數位化基準。",
    overrides=dict(monthlySalary=38000, monthlyHours=176, weeklyStdHours=40, alertHours=3, capEnabled=True, toolBudget=600,
      skills=dict(cloud=4, collab=4, sheet=3, viz=3, auto=3, ai=3, security=4, meeting=4),
      categories=[C("cat1","溝通協作",70), C("cat2","文書報告",50), C("cat3","行政流程",50), C("cat4","資料整理",50)],
      tasks=[
        T("t1","回覆內部 Email 與訊息","cat1",40,8,3,30,1,"信件範本＋自動分類規則",0,1),
        T("t2","會議記錄與待辦追蹤","cat1",4,45,3,60,2,"會議逐字稿＋AI 摘要",300,2),
        T("t3","公文與簽呈撰寫","cat2",5,40,2,40,2,"Word 範本＋生成式 AI 草稿",0,3),
        T("t4","請購與報帳單據處理","cat3",10,20,2,50,2,"電子表單＋線上簽核",0,3),
        T("t5","會議室與行事曆安排","cat3",12,10,3,50,1,"共用行事曆預約頁",0,0.5),
        T("t6","每週出勤與加班彙整","cat4",1,150,2,70,3,"Excel Power Query 合併",0,8),
        T("t7","文件掃描歸檔","cat4",6,20,2,40,1,"掃描 OCR＋雲端資料夾規則",0,1),
        T("t8","訪客接待登記","cat3",10,12,1,40,2,"線上訪客登記表單",0,1),
      ])),
  dict(id="sales", emoji="🤝", label="業務專員", blurb="客戶資料、訂單、通話紀錄仍靠手寫與手打，手工警示多、速贏機會最多。",
    overrides=dict(monthlySalary=45000, monthlyHours=176, weeklyStdHours=40, alertHours=3, capEnabled=False, toolBudget=0,
      skills=dict(cloud=2, collab=3, sheet=2, viz=1, auto=1, ai=2, security=2, meeting=3),
      categories=[C("cat1","客戶開發",60), C("cat2","客戶服務",65), C("cat3","報價與訂單",70), C("cat4","業績報表",70)],
      tasks=[
        T("t1","名片與客戶資料建檔","cat1",20,10,0,80,1,"名片掃描 App 匯入 CRM",0,1),
        T("t2","電話追蹤紀錄（手寫）","cat1",25,8,0,60,1,"CRM 通話紀錄＋提醒",450,3),
        T("t3","報價單製作","cat3",8,35,1,65,2,"報價單範本＋自動編號",0,2),
        T("t4","訂單手動登打","cat3",12,20,0,75,2,"線上訂購表單串接試算表",0,4),
        T("t5","客戶 LINE 詢問回覆","cat2",60,4,1,40,2,"LINE 官方帳號快速回覆",0,2),
        T("t6","每週業績週報","cat4",1,180,1,75,3,"CRM 儀表板自動產出",0,10),
        T("t7","拜訪行程規劃","cat1",5,20,2,40,1,"地圖路線＋共用行事曆",0,0.5),
        T("t8","客訴紀錄整理","cat2",4,25,1,50,3,"客服表單＋分類標籤",0,3),
      ])),
  dict(id="marketing", emoji="📣", label="行銷企劃", blurb="AI 與設計工具用得最多，但訂閱費超過自訂的工具預算。",
    overrides=dict(monthlySalary=48000, monthlyHours=176, weeklyStdHours=40, alertHours=3, capEnabled=True, toolBudget=1500,
      skills=dict(cloud=4, collab=5, sheet=3, viz=4, auto=3, ai=5, security=3, meeting=4),
      categories=[C("cat1","內容產製",80), C("cat2","社群經營",75), C("cat3","數據分析",70), C("cat4","專案協作",70)],
      tasks=[
        T("t1","社群貼文文案","cat1",10,30,4,50,1,"生成式 AI 文案範本",650,4),
        T("t2","活動視覺素材","cat1",6,45,3,50,2,"線上設計平台品牌套件",400,6),
        T("t3","社群排程發布","cat2",12,10,3,70,1,"社群平台內建排程",0,1),
        T("t4","留言與私訊回覆","cat2",50,3,2,40,2,"自動回覆＋常見問答",0,2),
        T("t5","廣告成效月報","cat3",1,240,2,70,4,"Looker Studio 自動儀表板",0,16),
        T("t6","競品與市場資料蒐集","cat3",2,90,3,50,3,"AI 研究助理＋RSS 追蹤",700,5),
        T("t7","跨部門專案進度追蹤","cat4",5,30,2,50,3,"Notion 專案看板",380,6),
        T("t8","影片剪輯與字幕","cat1",2,120,3,50,3,"AI 自動字幕剪輯工具",500,8),
      ])),
  dict(id="finance", emoji="🧾", label="財會人員", blurb="對帳、催收、單據核對大量手工，示範高耗時手工警示與需要投資的自動化。",
    overrides=dict(monthlySalary=52000, monthlyHours=176, weeklyStdHours=40, alertHours=3, capEnabled=True, toolBudget=1000,
      skills=dict(cloud=3, collab=2, sheet=4, viz=2, auto=1, ai=2, security=4, meeting=2),
      categories=[C("cat1","帳務處理",70), C("cat2","對帳與稽核",70), C("cat3","報表編製",75), C("cat4","行政溝通",60)],
      tasks=[
        T("t1","銀行對帳（逐筆比對）","cat2",5,90,1,75,3,"Power Query＋比對公式",0,12),
        T("t2","應收帳款催收","cat1",15,12,0,60,2,"帳齡表＋自動提醒信",0,3),
        T("t3","傳票登打","cat1",40,6,1,50,4,"會計系統批次匯入範本",0,10),
        T("t4","發票與單據核對","cat2",30,8,0,55,3,"OCR 辨識＋規則比對",350,8),
        T("t5","月結管理報表","cat3",1,300,1,70,4,"Power BI 月結儀表板",0,24),
        T("t6","費用分攤計算","cat3",2,60,2,60,3,"Excel 分攤範本",0,4),
        T("t7","部門費用詢問回覆","cat4",20,5,2,40,1,"常見問答文件＋表單",0,1),
      ])),
  dict(id="consultant", emoji="🎤", label="講師／顧問", blurb="時薪高、要學的工具多，示範學習投入大、回本期拉長的情境。",
    overrides=dict(monthlySalary=120000, monthlyHours=160, weeklyStdHours=45, alertHours=3, capEnabled=True, toolBudget=3000,
      skills=dict(cloud=4, collab=3, sheet=3, viz=3, auto=2, ai=4, security=3, meeting=5),
      categories=[C("cat1","教材開發",70), C("cat2","客戶溝通",65), C("cat3","行政財務",60), C("cat4","行銷曝光",70)],
      tasks=[
        T("t1","簡報教材製作","cat1",2,240,2,50,4,"AI 簡報生成＋品牌範本",600,50),
        T("t2","課程影片錄製剪輯","cat1",1,300,2,50,5,"AI 剪輯＋聲音克隆配音",900,60),
        T("t3","提案書撰寫","cat2",2,150,2,50,3,"提案範本庫＋AI 草稿",0,20),
        T("t4","報名與學員通知","cat3",3,40,1,70,3,"線上報名表＋自動通知信",0,10),
        T("t5","開立發票與收款對帳","cat3",4,25,1,60,2,"雲端發票＋收款試算表",150,3),
        T("t6","課後問卷分析","cat1",2,60,1,70,3,"線上問卷＋自動圖表",0,6),
        T("t7","社群與電子報經營","cat4",3,60,2,50,3,"排程工具＋AI 文案",400,10),
        T("t8","客戶來信與行程協調","cat2",30,6,2,40,1,"預約連結＋信件範本",0,1),
      ])),
]

SKILL_IDS = ["cloud","collab","sheet","viz","auto","ai","security","meeting"]

def model(o):
    rate = o["monthlySalary"]/o["monthlyHours"]
    rows = []
    for t in o["tasks"]:
        wh = t["freq"]*t["minutes"]/60
        saved = wh*t["potential"]/100*(1-t["level"]/4)
        mval = saved*52/12*rate
        net = mval - t["toolCost"]
        learn = t["learnHours"]*rate
        pay = (0 if learn == 0 else learn/net) if net > 0 else None
        alert = "urgent" if (t["level"] == 0 and wh >= o["alertHours"]) else ("watch" if (t["level"] <= 1 and wh >= o["alertHours"]) else None)
        rows.append(dict(name=t["name"], wh=wh, saved=saved, mval=mval, net=net, pay=pay, alert=alert, diff=t["difficulty"], level=t["level"], cost=t["toolCost"], learn=learn))
    n = len(rows)
    avg = sum(r["saved"] for r in rows)/n
    for r in rows:
        hi = r["saved"] > 0 and r["saved"] >= avg
        easy = r["diff"] <= 2
        r["q"] = "later" if r["saved"] <= 0 else (("quick" if easy else "invest") if hi else ("tidy" if easy else "later"))
    tw = sum(r["wh"] for r in rows); sv = sum(r["saved"] for r in rows)
    taskPct = sum(r["wh"]*r["level"]/4 for r in rows)/tw*100
    sk = o["skills"]; skillPct = (sum(sk[k] for k in SKILL_IDS)/8 - 1)/4*100
    mat = taskPct*0.6 + skillPct*0.4
    val = sum(r["mval"] for r in rows); cost = sum(r["cost"] for r in rows); learn = sum(r["learn"] for r in rows)
    net = val - cost
    manual = sum(r["wh"] for r in rows if r["level"] <= 1)/tw*100
    return dict(rate=rate, tw=tw, saved=sv, savedPct=sv/tw*100, val=val, cost=cost, net=net, learn=learn,
                payback=(learn/net if net > 0 else None), taskPct=taskPct, skillPct=skillPct, mat=mat, manual=manual,
                urgent=sum(r["alert"]=="urgent" for r in rows), watch=sum(r["alert"]=="watch" for r in rows),
                quads={q: [r["name"] for r in rows if r["q"]==q] for q in ["quick","invest","tidy","later"]},
                negNet=[r["name"] for r in rows if r["cost"] > 0 and r["net"] < 0], avg=avg)

if __name__ == "__main__":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", line_buffering=True)
    for p in PRESETS:
        m = model(p["overrides"])
        print(p["label"], {k: (round(v, 2) if isinstance(v, float) else v) for k, v in m.items()})
    if len(sys.argv) > 1:
        json.dump(PRESETS, open(sys.argv[1], "w", encoding="utf-8"), ensure_ascii=False)
