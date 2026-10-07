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

PRESETS += [
  dict(id="hr", emoji="🧑‍💼", label="人資人員", blurb="招募、考勤、加退保仍有不少手工；履歷篩選與訓練報名是速贏，出勤核對值得投資。",
    overrides=dict(monthlySalary=46000, monthlyHours=176, weeklyStdHours=40, alertHours=3, capEnabled=True, toolBudget=800,
      skills=dict(cloud=3, collab=3, sheet=3, viz=2, auto=2, ai=2, security=4, meeting=3),
      categories=[C("cat1","招募任用",65), C("cat2","薪資考勤",70), C("cat3","訓練發展",60), C("cat4","員工關係",55)],
      tasks=[
        T("t1","履歷篩選與面試邀約","cat1",15,12,1,60,2,"招募平台篩選條件＋面試預約連結",0,3),
        T("t2","面試行程協調","cat1",8,15,2,50,1,"共用行事曆預約頁",0,1),
        T("t3","新人報到文件","cat1",3,40,1,60,2,"線上報到表單＋電子簽署",300,3),
        T("t4","出勤異常核對","cat2",1,180,1,70,3,"打卡系統異常報表＋Power Query",0,8),
        T("t5","薪資計算與核對","cat2",1,240,2,50,4,"薪資系統匯入範本",0,16),
        T("t6","勞健保加退保","cat2",4,30,0,50,2,"加退保清單範本＋線上申報",0,2),
        T("t7","教育訓練報名與簽到","cat3",3,45,1,70,2,"線上報名表＋QR 簽到",0,2),
        T("t8","員工請假與規章詢問","cat4",25,6,1,50,1,"內部常見問答＋AI 問答機器人",0,4),
      ])),
  dict(id="purchasing", emoji="📦", label="採購人員", blurb="詢價、催貨、轉單靠 Email 與手打，多數改善需要 ERP 配合。",
    overrides=dict(monthlySalary=44000, monthlyHours=176, weeklyStdHours=40, alertHours=3, capEnabled=False, toolBudget=0,
      skills=dict(cloud=2, collab=2, sheet=3, viz=2, auto=1, ai=1, security=3, meeting=2),
      categories=[C("cat1","詢比議價",60), C("cat2","訂單管理",70), C("cat3","供應商管理",60)],
      tasks=[
        T("t1","供應商詢價比價","cat1",6,40,1,50,3,"詢價範本＋比價試算表",0,4),
        T("t2","請購單轉採購單","cat2",25,8,1,70,3,"ERP 批次轉單",0,10),
        T("t3","交期追蹤催貨","cat2",30,6,0,60,2,"交期追蹤表＋自動提醒信",0,3),
        T("t4","進貨驗收對帳","cat2",10,15,1,50,3,"驗收單掃描＋對帳公式",0,6),
        T("t5","供應商評鑑","cat3",1,120,1,60,2,"線上評鑑表單＋自動計分",0,3),
        T("t6","採購月報","cat2",1,150,1,70,4,"ERP 報表＋Power BI",0,16),
      ])),
  dict(id="cs", emoji="🎧", label="客服專員", blurb="通話紀錄還靠手打、退換貨跑紙本，改成系統摘要與線上表單就是速贏。",
    overrides=dict(monthlySalary=36000, monthlyHours=176, weeklyStdHours=40, alertHours=3, capEnabled=True, toolBudget=500,
      skills=dict(cloud=2, collab=3, sheet=2, viz=1, auto=1, ai=3, security=3, meeting=2),
      categories=[C("cat1","顧客回覆",75), C("cat2","紀錄與追蹤",70), C("cat3","報表",65)],
      tasks=[
        T("t1","Email 客訴回覆","cat1",40,8,2,50,1,"回覆範本庫＋AI 草稿",0,2),
        T("t2","電話紀錄登打","cat2",60,3,0,70,1,"客服系統通話摘要",0,1),
        T("t3","LINE 常見問題回覆","cat1",120,2,2,60,2,"關鍵字自動回覆",0,3),
        T("t4","退換貨單據處理","cat2",20,10,1,60,2,"線上退貨申請表單",0,3),
        T("t5","每日客訴彙整報表","cat3",5,30,1,75,3,"表單資料自動彙整儀表板",0,8),
        T("t6","跨部門轉單追蹤","cat2",15,8,1,50,2,"共用工單看板",0,2),
      ])),
  dict(id="pm", emoji="📋", label="專案經理", blurb="協作工具成熟、職能分數高；看板更新是速贏，主管簡報值得用 AI 投資。",
    overrides=dict(monthlySalary=65000, monthlyHours=176, weeklyStdHours=45, alertHours=3, capEnabled=True, toolBudget=2000,
      skills=dict(cloud=4, collab=5, sheet=4, viz=4, auto=3, ai=4, security=3, meeting=5),
      categories=[C("cat1","進度管理",75), C("cat2","溝通協調",70), C("cat3","文件報告",65)],
      tasks=[
        T("t1","專案進度更新","cat1",5,30,2,60,2,"專案管理看板",380,6),
        T("t2","週會議程與紀錄","cat2",3,60,3,60,1,"AI 會議紀錄＋待辦自動指派",600,3),
        T("t3","跨部門協調 Email","cat2",40,6,2,30,1,"信件範本＋共用收件匣",0,1),
        T("t4","風險與議題追蹤","cat1",2,45,2,40,3,"議題清單看板＋自動提醒",0,4),
        T("t5","主管簡報製作","cat3",2,120,2,50,3,"簡報範本＋AI 生成大綱",500,8),
        T("t6","專案成本試算","cat3",1,90,2,50,4,"預算追蹤儀表板",0,12),
        T("t7","甘特圖更新","cat1",2,40,1,70,2,"專案管理工具自動甘特圖",0,4),
      ])),
  dict(id="engineer", emoji="💻", label="軟體工程師", blurb="已大量使用 AI 程式助理，手動測試是最值得投資自動化的一塊。",
    overrides=dict(monthlySalary=75000, monthlyHours=176, weeklyStdHours=45, alertHours=3, capEnabled=True, toolBudget=1500,
      skills=dict(cloud=5, collab=4, sheet=4, viz=3, auto=4, ai=5, security=4, meeting=4),
      categories=[C("cat1","程式開發",80), C("cat2","測試部署",75), C("cat3","文件溝通",65)],
      tasks=[
        T("t1","撰寫程式","cat1",10,90,3,40,1,"AI 程式助理",600,10),
        T("t2","程式碼審查","cat1",8,30,2,40,2,"AI 審查＋自動檢查規則",0,4),
        T("t3","手動測試","cat2",5,60,1,70,3,"自動化測試腳本",0,24),
        T("t4","部署上線","cat2",3,40,2,80,4,"CI/CD 流水線",0,30),
        T("t5","技術文件撰寫","cat3",2,60,2,50,2,"AI 文件生成＋範本",0,3),
        T("t6","工單與錯誤回報整理","cat3",15,8,2,50,1,"議題追蹤自動分類",0,2),
      ])),
  dict(id="store", emoji="🏪", label="門市店長", blurb="排班、日報、訂貨仍靠紙本與 Excel，POS 內建功能沒用到。",
    overrides=dict(monthlySalary=50000, monthlyHours=208, weeklyStdHours=48, alertHours=3, capEnabled=True, toolBudget=1000,
      skills=dict(cloud=2, collab=3, sheet=2, viz=2, auto=1, ai=2, security=2, meeting=2),
      categories=[C("cat1","營運管理",60), C("cat2","人員管理",65), C("cat3","業績銷售",65)],
      tasks=[
        T("t1","員工排班","cat2",1,180,1,70,2,"線上排班 App",300,4),
        T("t2","每日營收日報","cat3",6,30,1,70,2,"POS 自動日報",0,2),
        T("t3","訂貨與補貨","cat1",6,30,1,50,3,"POS 庫存預警＋建議訂量",0,6),
        T("t4","交接與公告","cat1",7,15,1,50,1,"群組記事本＋公告範本",0,1),
        T("t5","會員活動推播","cat3",2,60,2,50,2,"會員系統分眾推播",500,6),
        T("t6","衛生安全檢查表","cat1",7,15,0,60,1,"線上檢核表單",0,1),
        T("t7","員工訓練","cat2",2,60,1,40,3,"教學影片＋線上測驗",0,8),
      ])),
  dict(id="warehouse", emoji="🚚", label="倉管物流", blurb="點收、盤點、單號全靠紙本手打，成熟度最低、改善空間最大。",
    overrides=dict(monthlySalary=38000, monthlyHours=176, weeklyStdHours=40, alertHours=3, capEnabled=True, toolBudget=500,
      skills=dict(cloud=1, collab=2, sheet=2, viz=1, auto=1, ai=1, security=2, meeting=2),
      categories=[C("cat1","進出貨",60), C("cat2","庫存管理",60), C("cat3","單據報表",60)],
      tasks=[
        T("t1","進貨點收（紙本）","cat1",10,25,0,60,3,"手機掃碼點收",0,6),
        T("t2","出貨揀貨單","cat1",20,10,1,50,2,"系統列印揀貨單＋條碼",0,3),
        T("t3","庫存盤點","cat2",1,240,0,60,3,"條碼盤點機＋雲端庫存表",300,10),
        T("t4","庫存數量回報","cat2",10,10,1,70,2,"雲端庫存即時表",0,2),
        T("t5","物流單號登打","cat1",30,4,0,80,1,"物流平台批次匯入",0,1),
        T("t6","月底進銷存報表","cat3",1,180,1,70,3,"進銷存樞紐分析範本",0,8),
      ])),
]
# 顯示順序：依職能別排列，行政助理固定第一（「重設為範例一」用）
ORDER = ["admin","hr","finance","purchasing","sales","cs","marketing","pm","engineer","store","warehouse","consultant"]
PRESETS = sorted(PRESETS, key=lambda p: ORDER.index(p["id"]))
assert len(PRESETS) == 12 and len({p["id"] for p in PRESETS}) == 12

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
