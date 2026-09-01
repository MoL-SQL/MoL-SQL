SELECT count(*) FROM `核电站` WHERE `国家` = "Japan" AND `运行状态` = "建设中"	GeoNuclearData
SELECT count(`名称`) FROM `核电站` WHERE `运行状态` = "建设中"	GeoNuclearData
SELECT count(*) FROM `核电站` WHERE `国家` = "France" and `运行状态` = "运行中"	GeoNuclearData
SELECT `名称` FROM `核电站` where `运行状态` = "运行中" and `国家` = "Japan"	GeoNuclearData
SELECT max(`装机容量`) FROM `核电站` WHERE `反应堆类型` = "压水堆" and `运行状态` = "运行中"	GeoNuclearData
SELECT `名称` FROM `核电站` ORDER BY `装机容量` DESC LIMIT 1	GeoNuclearData
SELECT `经度`, `纬度` FROM `核电站` WHERE `反应堆类型` = "沸水堆" ORDER BY `开工日期` LIMIT 1	GeoNuclearData
SELECT `国家` FROM `核电站` GROUP BY `国家` ORDER BY sum(`装机容量`) DESC LIMIT 1	GeoNuclearData
SELECT `国家` FROM `核电站` WHERE `运行状态` = "建设中" GROUP BY `国家` ORDER BY count(*) DESC LIMIT 1	GeoNuclearData
SELECT `国家` FROM `核电站` GROUP BY `国家` ORDER BY sum(`装机容量`) DESC LIMIT 1	GeoNuclearData
SELECT `国家` FROM `核电站` WHERE `运行状态` = "已停运" GROUP BY `国家` ORDER BY count(`名称`) DESC LIMIT 1	GeoNuclearData
SELECT `国家` FROM `核电站` WHERE `运行状态` = "建设中" GROUP BY `国家` ORDER BY count(*) DESC LIMIT 1	GeoNuclearData
SELECT count(*) FROM `大曼彻斯特犯罪记录` WHERE `处理结果` LIke "%正在调查中%"	GreaterManchesterCrime
SELECT count(*) FROM `大曼彻斯特犯罪记录` WHERE `处理结果` = "正在调查中"	GreaterManchesterCrime
SELECT count(*) FROM `大曼彻斯特犯罪记录` WHERE `犯罪类型` LIKE "%毒品%"	GreaterManchesterCrime
SELECT `处理结果` FROM `大曼彻斯特犯罪记录` WHERE `犯罪编号` = "6B:E2:54:C6:58:D2"	GreaterManchesterCrime
SELECT `犯罪类型` FROM `大曼彻斯特犯罪记录` GROUP BY `犯罪类型` ORDER BY count(*) DESC LIMIT 1	GreaterManchesterCrime
SELECT `地点` FROM `大曼彻斯特犯罪记录` WHERE `犯罪类型` = "暴力及性犯罪" GROUP BY `地点` ORDER BY count(*) DESC LIMIT 1	GreaterManchesterCrime
SELECT `地点` FROM `大曼彻斯特犯罪记录` GROUP BY `地点` ORDER BY count(*) LIMIT 1	GreaterManchesterCrime
SELECT `地点` FROM `大曼彻斯特犯罪记录` WHERE `犯罪类型` LIke "%毒品%" GROUP BY `地点` ORDER BY count(*) DESC LIMIT 1	GreaterManchesterCrime
SELECT `犯罪类型` FROM `大曼彻斯特犯罪记录` WHERE `地方统计区` LIKE "%Salford%" GROUP BY `犯罪类型` ORDER BY count(*) DESC LIMIT 1	GreaterManchesterCrime
SELECT `犯罪类型` FROM `大曼彻斯特犯罪记录` WHERE `处理结果` LIKE "%调查已完成%" GROUP BY `犯罪类型` ORDER BY count(*) DESC LIMIT 1	GreaterManchesterCrime
SELECT `犯罪类型` FROM `大曼彻斯特犯罪记录` WHERE `处理结果` = "调查已完成；未确认嫌疑人" GROUP BY `犯罪类型` ORDER BY count(*) DESC LIMIT 1	GreaterManchesterCrime
SELECT `犯罪类型` FROM `大曼彻斯特犯罪记录` WHERE `处理结果` = "等待法院判决结果" GROUP BY `犯罪类型` ORDER BY count(*) DESC LIMIT 1	GreaterManchesterCrime
SELECT `国家` FROM `样本数据15` WHERE `样本主键` = 6480 AND `产地` = 2	Pesticide
SELECT `商品` FROM `样本数据15` WHERE `产地` = 2 AND `商品` not in (SELECT `商品` FROM `样本数据15` WHERE `产地` = 1)	Pesticide
SELECT `检测类别` FROM `检测结果数据15` WHERE `样本主键` = 7498	Pesticide
SELECT `均值` FROM `检测结果数据15` WHERE `商品` = "苹果"	Pesticide
SELECT `浓度单位` FROM `检测结果数据15` WHERE `商品` = "桃"	Pesticide
SELECT `实验室` FROM `检测结果数据15` GROUP BY `实验室` ORDER BY count(*) DESC LIMIT 1	Pesticide
SELECT `实验室` FROM `检测结果数据15` WHERE `商品` = "苹果"	Pesticide
SELECT `种植状态` FROM `样本数据15` WHERE `商品` = "苹果" GROUP BY `种植状态` ORDER BY count(*) DESC LIMIT 1	Pesticide
SELECT `分销状态` FROM `样本数据15` WHERE `商品` = "苹果" GROUP BY `分销状态` ORDER BY count(*) DESC LIMIT 1	Pesticide
SELECT `州/省` FROM `样本数据15` WHERE `声明` = "采购订单" GROUP BY `州/省` ORDER BY count(*) DESC LIMIT 1	Pesticide
SELECT T1.`品种` FROM `检测结果数据15` as T2 JOIN `样本数据15` as T1 ON T1.`样本主键` = T2.`样本主键` WHERE T2.`商品` = "苹果" GROUP BY T1.`品种` ORDER BY sum(T2.`浓度`) DESC LIMIT 1	Pesticide
SELECT DISTINCT `商品` FROM `样本数据15`	Pesticide
SELECT count(DISTINCT `学区`) FROM `联邦财政收入_2017` as T1 JOIN `联邦财政收入关键指标_2017` as T2 ON T1.`州代码` = T2.`州代码` WHERE T2.`州名称` = "Indiana"	StudentMathScore
SELECT sum(T1.`指标C14`), sum(T1.`指标C25`) FROM `联邦财政收入_2017` as T1 JOIN `联邦财政收入关键指标_2017` as T2 ON T1.`州代码` = T2.`州代码` WHERE T2.`州名称` = "Colorado"	StudentMathScore
SELECT T1.`学区`, max(T1.`联邦财政收入总额` / T3.`平均量表分`) FROM `联邦财政收入_2017` as T1 JOIN `联邦财政收入关键指标_2017` as T2 on T1.`州代码` = T2.`州代码` JOIN `NDE核心数学八年级成绩` as T3 ON T2.`州名称` = T3.`州`	StudentMathScore
SELECT T1.`学区`, min(T1.`联邦财政收入总额` / T3.`平均量表分`) FROM `联邦财政收入_2017` as T1 JOIN `联邦财政收入关键指标_2017` as T2 on T1.`州代码` = T2.`州代码` JOIN `NDE核心数学八年级成绩` as T3 ON T2.`州名称` = T3.`州`	StudentMathScore
SELECT `平均量表分` FROM `NDE核心数学八年级成绩` WHERE `州` = "North Carolina" UNION SELECT `平均量表分` FROM `NDE核心数学八年级成绩` WHERE `州` = "New York"	StudentMathScore
SELECT T1.`学区`, max(T1.`指标C14`), T3.`平均量表分` FROM `联邦财政收入_2017` as T1 JOIN `联邦财政收入关键指标_2017` as T2 ON T1.`州代码` = T2.`州代码` JOIN `NDE核心数学八年级成绩` as T3 ON T2.`州名称` = T3.`州` UNION SELECT T1.`学区`, max(T1.`指标C25`), T3.`平均量表分` FROM `联邦财政收入_2017` as T1 JOIN `联邦财政收入关键指标_2017` as T2 ON T1.`州代码` = T2.`州代码` JOIN `NDE核心数学八年级成绩` as T3 ON T2.`州名称` = T3.`州`	StudentMathScore
SELECT `平均量表分` FROM `NDE核心数学八年级成绩` WHERE `州` = "North Carolina" UNION SELECT `平均量表分` FROM `NDE核心数学八年级成绩` WHERE `州` = "South Carolina"	StudentMathScore
SELECT T2.`州名称`, sum(`指标C14`),sum(`指标C25`) FROM `联邦财政收入_2017` as T1 JOIN `联邦财政收入关键指标_2017` as T2 ON T1.`州代码` = T2.`州代码` JOIN `NDE核心数学八年级成绩` as T3 ON T2.`州名称` = T3.`州` GROUP BY T2.`州名称` ORDER BY T3.`平均量表分` DESC LIMIT 10	StudentMathScore
SELECT T1.`学区` FROM `联邦财政收入_2017` as T1 JOIN `联邦财政收入关键指标_2017` as T2 ON T1.`州代码` = T2.`州代码` WHERE T2.`州名称` = "Wisconsin" ORDER BY T1.`联邦财政收入总额` DESC LIMIT 1	StudentMathScore
SELECT T2.`州名称` FROM `联邦财政收入关键指标_2017` as T2 JOIN `联邦财政收入_2017` as T1 ON T1.`州代码` = T2.`州代码` GROUP BY T2.`州名称` ORDER BY sum(`联邦财政收入总额`) DESC LIMIT 1	StudentMathScore
SELECT T2.`州名称`, T3.`平均量表分` FROM `联邦财政收入关键指标_2017` as T2 JOIN `联邦财政收入_2017` as T1 ON T1.`州代码` = T2.`州代码` JOIN `NDE核心数学八年级成绩` as T3 ON T2.`州名称` = T3.`州` GROUP BY T2.`州名称` ORDER BY sum(T1.`联邦财政收入总额`) LIMIT 1	StudentMathScore
SELECT T2.`州名称`, T3.`平均量表分` FROM `联邦财政收入关键指标_2017` as T2 JOIN `联邦财政收入_2017` as T1 ON T1.`州代码` = T2.`州代码` JOIN `NDE核心数学八年级成绩` as T3 ON T2.`州名称` = T3.`州` GROUP BY T2.`州名称` ORDER BY sum(T1.`联邦财政收入总额`) DESC LIMIT 1	StudentMathScore
SELECT avg(T1.`体重`) FROM `球员` as T1 JOIN `球员奖项` as T2 ON T1.`球员编号` = T2.`球员编号` GROUP BY `备注`	TheHistoryofBaseball
SELECT count(*) FROM (SELECT `球员编号` FROM `球员奖项` GROUP BY `球员编号` HAVING count(*) > 10)	TheHistoryofBaseball
SELECT T1.`出生国家` FROM `球员` as T1 JOIN `名人堂` as T2 ON T1.`球员编号` = T2.`球员编号` WHERE T2.`是否入选` = "Y" GROUP BY T1.`出生国家` ORDER BY count(*) DESC, MIN(T1.`球员编号`) ASC LIMIT 10	TheHistoryofBaseball
SELECT T2.`球队编号` FROM `名人堂` as T1 JOIN `薪资` as T2 ON T1.`球员编号` = T2.`球员编号` AND T1.`入选年份` = T2.`年份` WHERE T1.`是否入选` = "Y" GROUP BY T2.`球队编号` ORDER BY count(*) DESC LIMIT 10	TheHistoryofBaseball
SELECT T1.`出生国家` FROM `名人堂` as T2 JOIN `球员` as T1 ON T1.`球员编号` = T2.`球员编号` WHERE T2.`是否入选` = "Y" AND T2.`入选年份` >= 1871	TheHistoryofBaseball
SELECT `薪资` FROM `薪资` WHERE `联盟编号` = "美国联盟"	TheHistoryofBaseball
SELECT `薪资` FROM `薪资` WHERE `联盟编号` = "国家联盟"	TheHistoryofBaseball
SELECT avg(T1.`体重`) FROM `球员` as T1 JOIN `球员奖项` as T2 ON T1.`球员编号` = T2.`球员编号` WHERE T2.`奖项编号` = "《The Sporting News》全明星" AND `备注` = "三垒手"	TheHistoryofBaseball
SELECT `出生国家` FROM `球员` as T1 JOIN `球员奖项` as T2 ON T1.`球员编号` = T2.`球员编号` GROUP BY T1.`出生国家` ORDER BY count(*) DESC LIMIT 1	TheHistoryofBaseball
SELECT `联盟编号` FROM `球员奖项` WHERE `获奖年份` = "2006" GROUP BY `联盟编号` ORDER BY count(*) DESC LIMIT 1	TheHistoryofBaseball
SELECT `球员编号` FROM `薪资` WHERE `年份` >= 2010 ORDER BY `薪资` DESC LIMIT 1	TheHistoryofBaseball
SELECT `球员编号` FROM `球员奖项` WHERE `获奖年份` = 2010 AND `奖项编号` = "年度最佳新秀"	TheHistoryofBaseball
SELECT count(*) FROM `火灾` WHERE `火灾年份` = 2010 AND `统计起因描述` LIKE "%纵火%"	USWildFires
SELECT count(*) FROM `火灾` WHERE `权属描述` = "缺失/未指定"	USWildFires
SELECT count(*) FROM `火灾` WHERE `权属描述` = "缺失/未指定"	USWildFires
SELECT count(*) FROM `火灾` WHERE `县` = "Gloucester" AND `过火面积` > 10	USWildFires
SELECT count(*) FROM `火灾` WHERE `统计起因描述` LIKE "%营火%" AND `火灾年份` = 2014	USWildFires
SELECT `权属描述` FROM `火灾` GROUP BY `权属描述` ORDER BY count(*) DESC LIMIT 1	USWildFires
SELECT * FROM `火灾` WHERE `州` = "TX" AND `统计起因描述` LIKE "营火"	USWildFires
SELECT `统计起因描述` FROM `火灾` GROUP BY `统计起因描述` ORDER BY count(*) DESC LIMIT 1	USWildFires
SELECT `统计起因描述` FROM `火灾` GROUP BY `统计起因描述` ORDER BY count(*) DESC LIMIT 1	USWildFires
SELECT sum(`过火面积`) FROM `火灾`	USWildFires
SELECT `县` FROM `火灾` WHERE `州` = "WA" AND `火灾年份` = 2012	USWildFires
SELECT `州` FROM `火灾` GROUP BY `州` ORDER BY count(*) DESC LIMIT 1	USWildFires
SELECT count(*) FROM ( SELECT `组名` FROM `种子` GROUP BY `组名` HAVING count(*) > 1 )	WhatCDHipHop
SELECT `组名` FROM `种子` WHERE `艺术家` = "lasean camry" AND `总下载次数` = (SELECT max(`总下载次数`) FROM `种子` WHERE `艺术家` = "lasean camry") UNION SELECT `组名` FROM `种子` WHERE `艺术家` = "lasean camry" AND `总下载次数` = (SELECT min(`总下载次数`) FROM `种子` WHERE `艺术家` = "lasean camry")	WhatCDHipHop
SELECT T2.`组名` FROM `种子` as T2 JOIN `标签` as T1 ON T1.`标签编号` = T2.`种子编号` WHERE T1.`标签名称` = "houston" ORDER BY `总下载次数` DESC LIMIT 1	WhatCDHipHop
SELECT `艺术家` FROM `种子` WHERE `发行年份` > 2010 GROUP BY `艺术家`	WhatCDHipHop
SELECT sum(`总下载次数`), `发行类型` FROM `种子` GROUP BY `发行类型`	WhatCDHipHop
SELECT sum(`总下载次数`) FROM `种子` WHERE `发行年份` BETWEEN 2000 AND 2010 UNION SELECT sum(`总下载次数`) FROM `种子` WHERE `发行年份` < 2000	WhatCDHipHop
SELECT DISTINCT `组名` FROM `种子` WHERE `总下载次数` > 100 AND `发行类型` = "album"	WhatCDHipHop
SELECT `艺术家` FROM `种子` GROUP BY `艺术家` ORDER BY count(`组名`) DESC LIMIT 1	WhatCDHipHop
SELECT `发行类型` FROM `种子` GROUP BY `发行类型` ORDER BY sum(`总下载次数`) DESC LIMIT 1	WhatCDHipHop
SELECT `发行年份` FROM `种子` GROUP BY `发行年份` ORDER BY count(`组名`) LIMIT 1	WhatCDHipHop
SELECT `发行年份` FROM `种子` GROUP BY `发行年份` ORDER BY count(`组名`) DESC LIMIT 1	WhatCDHipHop
SELECT `艺术家` FROM `种子` WHERE `发行年份` = 2015 GROUP BY `艺术家` ORDER BY `总下载次数` DESC LIMIT 1	WhatCDHipHop
SELECT count(`联赛`) FROM `足球数据` WHERE `国家` != "Scotland" and `国家` != "England" and `裁判` != ""	WorldSoccerDataBase
SELECT count(*) FROM `足球数据` WHERE `全场主队进球数` + `全场客队进球数` > 5	WorldSoccerDataBase
SELECT count(`联赛代码`) FROM `足球数据`	WorldSoccerDataBase
SELECT count(*) FROM `足球数据` WHERE B365H > `PS主胜赔率`	WorldSoccerDataBase
SELECT count(*) FROM `足球数据` WHERE `PS主胜赔率` != "" AND `PS平局赔率` != "" AND `PS客胜赔率` != ""	WorldSoccerDataBase
SELECT count(*) FROM `足球数据` WHERE `赛季` LIKE "%2010%" AND `国家` = "Spain"	WorldSoccerDataBase
SELECT count(*) FROM `足球数据` WHERE `全场主队进球数` = 0 AND `全场客队进球数` = 0	WorldSoccerDataBase
SELECT `客队` FROM `足球数据` WHERE `主队` = "Omiya Ardija" AND `赛季` LIKE "%2018%"	WorldSoccerDataBase
SELECT max(B365A) FROM `足球数据`	WorldSoccerDataBase
SELECT B365D FROM `足球数据` WHERE `主队` = "Swindon" and `客队` = "Millwall" and `赛季` = "2016/2017"	WorldSoccerDataBase
SELECT `比赛` FROM `博彩前端` ORDER BY `平局初盘赔率` DESC LIMIT 1	WorldSoccerDataBase
SELECT `年份` FROM `博彩前端` GROUP BY `年份` ORDER BY count(*) DESC LIMIT 1	WorldSoccerDataBase
