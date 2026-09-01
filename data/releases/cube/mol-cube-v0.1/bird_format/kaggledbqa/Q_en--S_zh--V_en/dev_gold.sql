SELECT COUNT(*) AS _col_0 FROM "核电站" AS nuclear_power_plants WHERE nuclear_power_plants."国家" = 'Japan' AND nuclear_power_plants."运行状态" = 'Under Construction'	GeoNuclearData
SELECT COUNT(nuclear_power_plants."名称") AS _col_0 FROM "核电站" AS nuclear_power_plants WHERE nuclear_power_plants."运行状态" = 'Under Construction'	GeoNuclearData
SELECT COUNT(*) AS _col_0 FROM "核电站" AS nuclear_power_plants WHERE nuclear_power_plants."国家" = 'France' AND nuclear_power_plants."运行状态" = 'Operational'	GeoNuclearData
SELECT nuclear_power_plants."名称" AS name FROM "核电站" AS nuclear_power_plants WHERE nuclear_power_plants."运行状态" = 'Operational' AND nuclear_power_plants."国家" = 'Japan'	GeoNuclearData
SELECT MAX(nuclear_power_plants."装机容量") AS _col_0 FROM "核电站" AS nuclear_power_plants WHERE nuclear_power_plants."反应堆类型" = 'PWR' AND nuclear_power_plants."运行状态" = 'Operational'	GeoNuclearData
SELECT nuclear_power_plants."名称" AS name FROM "核电站" AS nuclear_power_plants ORDER BY nuclear_power_plants."装机容量" DESC LIMIT 1	GeoNuclearData
SELECT nuclear_power_plants."经度" AS longitude, nuclear_power_plants."纬度" AS latitude FROM "核电站" AS nuclear_power_plants WHERE nuclear_power_plants."反应堆类型" = 'BWR' ORDER BY nuclear_power_plants."开工日期" LIMIT 1	GeoNuclearData
SELECT nuclear_power_plants."国家" AS country FROM "核电站" AS nuclear_power_plants GROUP BY nuclear_power_plants."国家" ORDER BY SUM(nuclear_power_plants."装机容量") DESC LIMIT 1	GeoNuclearData
SELECT nuclear_power_plants."国家" AS country FROM "核电站" AS nuclear_power_plants WHERE nuclear_power_plants."运行状态" = 'Under Construction' GROUP BY nuclear_power_plants."国家" ORDER BY COUNT(*) DESC LIMIT 1	GeoNuclearData
SELECT nuclear_power_plants."国家" AS country FROM "核电站" AS nuclear_power_plants GROUP BY nuclear_power_plants."国家" ORDER BY SUM(nuclear_power_plants."装机容量") DESC LIMIT 1	GeoNuclearData
SELECT nuclear_power_plants."国家" AS country FROM "核电站" AS nuclear_power_plants WHERE nuclear_power_plants."运行状态" = 'Shutdown' GROUP BY nuclear_power_plants."国家" ORDER BY COUNT(nuclear_power_plants."名称") DESC LIMIT 1	GeoNuclearData
SELECT nuclear_power_plants."国家" AS country FROM "核电站" AS nuclear_power_plants WHERE nuclear_power_plants."运行状态" = 'Under Construction' GROUP BY nuclear_power_plants."国家" ORDER BY COUNT(*) DESC LIMIT 1	GeoNuclearData
SELECT COUNT(*) AS _col_0 FROM "大曼彻斯特犯罪记录" AS greatermanchestercrime WHERE greatermanchestercrime."处理结果" LIKE '%Under investigation%'	GreaterManchesterCrime
SELECT COUNT(*) AS _col_0 FROM "大曼彻斯特犯罪记录" AS greatermanchestercrime WHERE greatermanchestercrime."处理结果" = 'Under investigation'	GreaterManchesterCrime
SELECT COUNT(*) AS _col_0 FROM "大曼彻斯特犯罪记录" AS greatermanchestercrime WHERE greatermanchestercrime."犯罪类型" LIKE '%Drug%'	GreaterManchesterCrime
SELECT greatermanchestercrime."处理结果" AS outcome FROM "大曼彻斯特犯罪记录" AS greatermanchestercrime WHERE greatermanchestercrime."犯罪编号" = '6B:E2:54:C6:58:D2'	GreaterManchesterCrime
SELECT greatermanchestercrime."犯罪类型" AS type FROM "大曼彻斯特犯罪记录" AS greatermanchestercrime GROUP BY greatermanchestercrime."犯罪类型" ORDER BY COUNT(*) DESC LIMIT 1	GreaterManchesterCrime
SELECT greatermanchestercrime."地点" AS location FROM "大曼彻斯特犯罪记录" AS greatermanchestercrime WHERE greatermanchestercrime."犯罪类型" = 'Violence and sexual offences' GROUP BY greatermanchestercrime."地点" ORDER BY COUNT(*) DESC LIMIT 1	GreaterManchesterCrime
SELECT greatermanchestercrime."地点" AS location FROM "大曼彻斯特犯罪记录" AS greatermanchestercrime GROUP BY greatermanchestercrime."地点" ORDER BY COUNT(*) LIMIT 1	GreaterManchesterCrime
SELECT greatermanchestercrime."地点" AS location FROM "大曼彻斯特犯罪记录" AS greatermanchestercrime WHERE greatermanchestercrime."犯罪类型" LIKE '%Drug%' GROUP BY greatermanchestercrime."地点" ORDER BY COUNT(*) DESC LIMIT 1	GreaterManchesterCrime
SELECT greatermanchestercrime."犯罪类型" AS type FROM "大曼彻斯特犯罪记录" AS greatermanchestercrime WHERE greatermanchestercrime."地方统计区" LIKE '%Salford%' GROUP BY greatermanchestercrime."犯罪类型" ORDER BY COUNT(*) DESC LIMIT 1	GreaterManchesterCrime
SELECT greatermanchestercrime."犯罪类型" AS type FROM "大曼彻斯特犯罪记录" AS greatermanchestercrime WHERE greatermanchestercrime."处理结果" LIKE '%Investigation complete%' GROUP BY greatermanchestercrime."犯罪类型" ORDER BY COUNT(*) DESC LIMIT 1	GreaterManchesterCrime
SELECT greatermanchestercrime."犯罪类型" AS type FROM "大曼彻斯特犯罪记录" AS greatermanchestercrime WHERE greatermanchestercrime."处理结果" = 'Investigation complete; no suspect identified' GROUP BY greatermanchestercrime."犯罪类型" ORDER BY COUNT(*) DESC LIMIT 1	GreaterManchesterCrime
SELECT greatermanchestercrime."犯罪类型" AS type FROM "大曼彻斯特犯罪记录" AS greatermanchestercrime WHERE greatermanchestercrime."处理结果" = 'Awaiting court outcome' GROUP BY greatermanchestercrime."犯罪类型" ORDER BY COUNT(*) DESC LIMIT 1	GreaterManchesterCrime
SELECT sampledata15."国家" AS country FROM "样本数据15" AS sampledata15 WHERE sampledata15."样本主键" = 6480 AND sampledata15."产地" = 2	Pesticide
SELECT sampledata15."商品" AS commod FROM "样本数据15" AS sampledata15 WHERE sampledata15."产地" = 2 AND NOT sampledata15."商品" IN (SELECT sampledata15."商品" AS commod FROM "样本数据15" AS sampledata15 WHERE sampledata15."产地" = 1)	Pesticide
SELECT resultsdata15."检测类别" AS testclass FROM "检测结果数据15" AS resultsdata15 WHERE resultsdata15."样本主键" = 7498	Pesticide
SELECT resultsdata15."均值" AS mean FROM "检测结果数据15" AS resultsdata15 WHERE resultsdata15."商品" = 'AP'	Pesticide
SELECT resultsdata15."浓度单位" AS conunit FROM "检测结果数据15" AS resultsdata15 WHERE resultsdata15."商品" = 'PO'	Pesticide
SELECT resultsdata15."实验室" AS lab FROM "检测结果数据15" AS resultsdata15 GROUP BY resultsdata15."实验室" ORDER BY COUNT(*) DESC LIMIT 1	Pesticide
SELECT resultsdata15."实验室" AS lab FROM "检测结果数据15" AS resultsdata15 WHERE resultsdata15."商品" = 'AP'	Pesticide
SELECT sampledata15."种植状态" AS growst FROM "样本数据15" AS sampledata15 WHERE sampledata15."商品" = 'AP' GROUP BY sampledata15."种植状态" ORDER BY COUNT(*) DESC LIMIT 1	Pesticide
SELECT sampledata15."分销状态" AS distst FROM "样本数据15" AS sampledata15 WHERE sampledata15."商品" = 'AP' GROUP BY sampledata15."分销状态" ORDER BY COUNT(*) DESC LIMIT 1	Pesticide
SELECT sampledata15."州/省" AS state FROM "样本数据15" AS sampledata15 WHERE sampledata15."声明" = 'PO' GROUP BY sampledata15."州/省" ORDER BY COUNT(*) DESC LIMIT 1	Pesticide
SELECT t1."品种" AS variety FROM "检测结果数据15" AS t2 JOIN "样本数据15" AS t1 ON t1."样本主键" = t2."样本主键" WHERE t2."商品" = 'AP' GROUP BY t1."品种" ORDER BY SUM(t2."浓度") DESC LIMIT 1	Pesticide
SELECT DISTINCT sampledata15."商品" AS commod FROM "样本数据15" AS sampledata15	Pesticide
SELECT COUNT(DISTINCT t1."学区") AS _col_0 FROM "联邦财政收入_2017" AS t1 JOIN "联邦财政收入关键指标_2017" AS t2 ON t1."州代码" = t2."州代码" WHERE t2."州名称" = 'Indiana'	StudentMathScore
SELECT SUM(t1."指标C14") AS _col_0, SUM(t1."指标C25") AS _col_1 FROM "联邦财政收入_2017" AS t1 JOIN "联邦财政收入关键指标_2017" AS t2 ON t1."州代码" = t2."州代码" WHERE t2."州名称" = 'Colorado'	StudentMathScore
SELECT t1."学区" AS school_district, MAX(t1."联邦财政收入总额" / t3."平均量表分") AS _col_1 FROM "联邦财政收入_2017" AS t1 JOIN "联邦财政收入关键指标_2017" AS t2 ON t1."州代码" = t2."州代码" JOIN "NDE核心数学八年级成绩" AS t3 ON t2."州名称" = t3."州"	StudentMathScore
SELECT t1."学区" AS school_district, MIN(t1."联邦财政收入总额" / t3."平均量表分") AS _col_1 FROM "联邦财政收入_2017" AS t1 JOIN "联邦财政收入关键指标_2017" AS t2 ON t1."州代码" = t2."州代码" JOIN "NDE核心数学八年级成绩" AS t3 ON t2."州名称" = t3."州"	StudentMathScore
SELECT ndecoreexcel_math_grade8."平均量表分" AS average_scale_score FROM "NDE核心数学八年级成绩" AS ndecoreexcel_math_grade8 WHERE ndecoreexcel_math_grade8."州" = 'North Carolina' UNION SELECT ndecoreexcel_math_grade8."平均量表分" AS average_scale_score FROM "NDE核心数学八年级成绩" AS ndecoreexcel_math_grade8 WHERE ndecoreexcel_math_grade8."州" = 'New York'	StudentMathScore
SELECT t1."学区" AS school_district, MAX(t1."指标C14") AS _col_1, t3."平均量表分" AS average_scale_score FROM "联邦财政收入_2017" AS t1 JOIN "联邦财政收入关键指标_2017" AS t2 ON t1."州代码" = t2."州代码" JOIN "NDE核心数学八年级成绩" AS t3 ON t2."州名称" = t3."州" UNION SELECT t1."学区" AS school_district, MAX(t1."指标C25") AS _col_1, t3."平均量表分" AS average_scale_score FROM "联邦财政收入_2017" AS t1 JOIN "联邦财政收入关键指标_2017" AS t2 ON t1."州代码" = t2."州代码" JOIN "NDE核心数学八年级成绩" AS t3 ON t2."州名称" = t3."州"	StudentMathScore
SELECT ndecoreexcel_math_grade8."平均量表分" AS average_scale_score FROM "NDE核心数学八年级成绩" AS ndecoreexcel_math_grade8 WHERE ndecoreexcel_math_grade8."州" = 'North Carolina' UNION SELECT ndecoreexcel_math_grade8."平均量表分" AS average_scale_score FROM "NDE核心数学八年级成绩" AS ndecoreexcel_math_grade8 WHERE ndecoreexcel_math_grade8."州" = 'South Carolina'	StudentMathScore
SELECT t2."州名称" AS state, SUM(t1."指标C14") AS _col_1, SUM(t1."指标C25") AS _col_2 FROM "联邦财政收入_2017" AS t1 JOIN "联邦财政收入关键指标_2017" AS t2 ON t1."州代码" = t2."州代码" JOIN "NDE核心数学八年级成绩" AS t3 ON t2."州名称" = t3."州" GROUP BY t2."州名称" ORDER BY t3."平均量表分" DESC LIMIT 10	StudentMathScore
SELECT t1."学区" AS school_district FROM "联邦财政收入_2017" AS t1 JOIN "联邦财政收入关键指标_2017" AS t2 ON t1."州代码" = t2."州代码" WHERE t2."州名称" = 'Wisconsin' ORDER BY t1."联邦财政收入总额" DESC LIMIT 1	StudentMathScore
SELECT t2."州名称" AS state FROM "联邦财政收入关键指标_2017" AS t2 JOIN "联邦财政收入_2017" AS t1 ON t1."州代码" = t2."州代码" GROUP BY t2."州名称" ORDER BY SUM(t1."联邦财政收入总额") DESC LIMIT 1	StudentMathScore
SELECT t2."州名称" AS state, t3."平均量表分" AS average_scale_score FROM "联邦财政收入关键指标_2017" AS t2 JOIN "联邦财政收入_2017" AS t1 ON t1."州代码" = t2."州代码" JOIN "NDE核心数学八年级成绩" AS t3 ON t2."州名称" = t3."州" GROUP BY t2."州名称" ORDER BY SUM(t1."联邦财政收入总额") LIMIT 1	StudentMathScore
SELECT t2."州名称" AS state, t3."平均量表分" AS average_scale_score FROM "联邦财政收入关键指标_2017" AS t2 JOIN "联邦财政收入_2017" AS t1 ON t1."州代码" = t2."州代码" JOIN "NDE核心数学八年级成绩" AS t3 ON t2."州名称" = t3."州" GROUP BY t2."州名称" ORDER BY SUM(t1."联邦财政收入总额") DESC LIMIT 1	StudentMathScore
SELECT AVG(t1."体重") AS _col_0 FROM "球员" AS t1 JOIN "球员奖项" AS t2 ON t1."球员编号" = t2."球员编号" GROUP BY t2."备注"	TheHistoryofBaseball
SELECT COUNT(*) AS _col_0 FROM (SELECT player_award."球员编号" AS player_id FROM "球员奖项" AS player_award GROUP BY player_award."球员编号" HAVING COUNT(*) > 10) AS _0	TheHistoryofBaseball
SELECT t1."出生国家" AS birth_country FROM "球员" AS t1 JOIN "名人堂" AS t2 ON t1."球员编号" = t2."球员编号" WHERE t2."是否入选" = 'Y' GROUP BY t1."出生国家" ORDER BY COUNT(*) DESC, MIN(t1."球员编号") ASC LIMIT 10	TheHistoryofBaseball
SELECT t2."球队编号" AS team_id FROM "名人堂" AS t1 JOIN "薪资" AS t2 ON t1."球员编号" = t2."球员编号" AND t1."入选年份" = t2."年份" WHERE t1."是否入选" = 'Y' GROUP BY t2."球队编号" ORDER BY COUNT(*) DESC LIMIT 10	TheHistoryofBaseball
SELECT t1."出生国家" AS birth_country FROM "名人堂" AS t2 JOIN "球员" AS t1 ON t1."球员编号" = t2."球员编号" WHERE t2."是否入选" = 'Y' AND t2."入选年份" >= 1871	TheHistoryofBaseball
SELECT salary."薪资" AS salary FROM "薪资" AS salary WHERE salary."联盟编号" = 'AL'	TheHistoryofBaseball
SELECT salary."薪资" AS salary FROM "薪资" AS salary WHERE salary."联盟编号" = 'NL'	TheHistoryofBaseball
SELECT AVG(t1."体重") AS _col_0 FROM "球员" AS t1 JOIN "球员奖项" AS t2 ON t1."球员编号" = t2."球员编号" WHERE t2."奖项编号" = 'TSN All-Star' AND t2."备注" = '3B'	TheHistoryofBaseball
SELECT t1."出生国家" AS birth_country FROM "球员" AS t1 JOIN "球员奖项" AS t2 ON t1."球员编号" = t2."球员编号" GROUP BY t1."出生国家" ORDER BY COUNT(*) DESC LIMIT 1	TheHistoryofBaseball
SELECT player_award."联盟编号" AS league_id FROM "球员奖项" AS player_award WHERE player_award."获奖年份" = '2006' GROUP BY player_award."联盟编号" ORDER BY COUNT(*) DESC LIMIT 1	TheHistoryofBaseball
SELECT salary."球员编号" AS player_id FROM "薪资" AS salary WHERE salary."年份" >= 2010 ORDER BY salary."薪资" DESC LIMIT 1	TheHistoryofBaseball
SELECT player_award."球员编号" AS player_id FROM "球员奖项" AS player_award WHERE player_award."获奖年份" = 2010 AND player_award."奖项编号" = 'Rookie of the Year'	TheHistoryofBaseball
SELECT COUNT(*) AS _col_0 FROM "火灾" AS fires WHERE fires."火灾年份" = 2010 AND fires."统计起因描述" LIKE '%Arson%'	USWildFires
SELECT COUNT(*) AS _col_0 FROM "火灾" AS fires WHERE fires."权属描述" = 'MISSING/NOT SPECIFIED'	USWildFires
SELECT COUNT(*) AS _col_0 FROM "火灾" AS fires WHERE fires."权属描述" = 'MISSING/NOT SPECIFIED'	USWildFires
SELECT COUNT(*) AS _col_0 FROM "火灾" AS fires WHERE fires."县" = 'Gloucester' AND fires."过火面积" > 10	USWildFires
SELECT COUNT(*) AS _col_0 FROM "火灾" AS fires WHERE fires."统计起因描述" LIKE '%Campfire%' AND fires."火灾年份" = 2014	USWildFires
SELECT fires."权属描述" AS owner_descr FROM "火灾" AS fires GROUP BY fires."权属描述" ORDER BY COUNT(*) DESC LIMIT 1	USWildFires
SELECT fires."火灾年份" AS fire_year, fires."发现日期" AS discovery_date, fires."发现年积日" AS discovery_doy, fires."发现时间" AS discovery_time, fires."统计起因编码" AS stat_cause_code, fires."统计起因描述" AS stat_cause_descr, fires."扑灭日期" AS cont_date, fires."扑灭年积日" AS cont_doy, fires."扑灭时间" AS cont_time, fires."过火面积" AS fire_size, fires."过火面积等级" AS fire_size_class, fires."纬度" AS latitude, fires."经度" AS longitude, fires."权属编码" AS owner_code, fires."权属描述" AS owner_descr, fires."州" AS state, fires."县" AS county, fires."联邦信息处理标准编码" AS fips_code, fires."联邦信息处理标准名称" AS fips_name FROM "火灾" AS fires WHERE fires."州" = 'TX' AND fires."统计起因描述" LIKE 'Campfire'	USWildFires
SELECT fires."统计起因描述" AS stat_cause_descr FROM "火灾" AS fires GROUP BY fires."统计起因描述" ORDER BY COUNT(*) DESC LIMIT 1	USWildFires
SELECT fires."统计起因描述" AS stat_cause_descr FROM "火灾" AS fires GROUP BY fires."统计起因描述" ORDER BY COUNT(*) DESC LIMIT 1	USWildFires
SELECT SUM(fires."过火面积") AS _col_0 FROM "火灾" AS fires	USWildFires
SELECT fires."县" AS county FROM "火灾" AS fires WHERE fires."州" = 'WA' AND fires."火灾年份" = 2012	USWildFires
SELECT fires."州" AS state FROM "火灾" AS fires GROUP BY fires."州" ORDER BY COUNT(*) DESC LIMIT 1	USWildFires
SELECT COUNT(*) AS _col_0 FROM (SELECT torrents."组名" AS groupname FROM "种子" AS torrents GROUP BY torrents."组名" HAVING COUNT(*) > 1) AS _0	WhatCDHipHop
SELECT torrents."组名" AS groupname FROM "种子" AS torrents WHERE torrents."艺术家" = 'lasean camry' AND torrents."总下载次数" = (SELECT MAX(torrents."总下载次数") AS _col_0 FROM "种子" AS torrents WHERE torrents."艺术家" = 'lasean camry') UNION SELECT torrents."组名" AS groupname FROM "种子" AS torrents WHERE torrents."艺术家" = 'lasean camry' AND torrents."总下载次数" = (SELECT MIN(torrents."总下载次数") AS _col_0 FROM "种子" AS torrents WHERE torrents."艺术家" = 'lasean camry')	WhatCDHipHop
SELECT t2."组名" AS groupname FROM "种子" AS t2 JOIN "标签" AS t1 ON t1."标签编号" = t2."种子编号" WHERE t1."标签名称" = 'houston' ORDER BY t2."总下载次数" DESC LIMIT 1	WhatCDHipHop
SELECT torrents."艺术家" AS artist FROM "种子" AS torrents WHERE torrents."发行年份" > 2010 GROUP BY torrents."艺术家"	WhatCDHipHop
SELECT SUM(torrents."总下载次数") AS _col_0, torrents."发行类型" AS releasetype FROM "种子" AS torrents GROUP BY torrents."发行类型"	WhatCDHipHop
SELECT SUM(torrents."总下载次数") AS _col_0 FROM "种子" AS torrents WHERE torrents."发行年份" BETWEEN 2000 AND 2010 UNION SELECT SUM(torrents."总下载次数") AS _col_0 FROM "种子" AS torrents WHERE torrents."发行年份" < 2000	WhatCDHipHop
SELECT DISTINCT torrents."组名" AS groupname FROM "种子" AS torrents WHERE torrents."总下载次数" > 100 AND torrents."发行类型" = 'album'	WhatCDHipHop
SELECT torrents."艺术家" AS artist FROM "种子" AS torrents GROUP BY torrents."艺术家" ORDER BY COUNT(torrents."组名") DESC LIMIT 1	WhatCDHipHop
SELECT torrents."发行类型" AS releasetype FROM "种子" AS torrents GROUP BY torrents."发行类型" ORDER BY SUM(torrents."总下载次数") DESC LIMIT 1	WhatCDHipHop
SELECT torrents."发行年份" AS groupyear FROM "种子" AS torrents GROUP BY torrents."发行年份" ORDER BY COUNT(torrents."组名") LIMIT 1	WhatCDHipHop
SELECT torrents."发行年份" AS groupyear FROM "种子" AS torrents GROUP BY torrents."发行年份" ORDER BY COUNT(torrents."组名") DESC LIMIT 1	WhatCDHipHop
SELECT torrents."艺术家" AS artist FROM "种子" AS torrents WHERE torrents."发行年份" = 2015 GROUP BY torrents."艺术家" ORDER BY torrents."总下载次数" DESC LIMIT 1	WhatCDHipHop
SELECT COUNT(football_data."联赛") AS _col_0 FROM "足球数据" AS football_data WHERE football_data."国家" <> 'Scotland' AND football_data."国家" <> 'England' AND football_data."裁判" <> ''	WorldSoccerDataBase
SELECT COUNT(*) AS _col_0 FROM "足球数据" AS football_data WHERE football_data."全场主队进球数" + football_data."全场客队进球数" > 5	WorldSoccerDataBase
SELECT COUNT(football_data."联赛代码") AS _col_0 FROM "足球数据" AS football_data	WorldSoccerDataBase
SELECT COUNT(*) AS _col_0 FROM "足球数据" AS football_data WHERE football_data.B365H > football_data."PS主胜赔率"	WorldSoccerDataBase
SELECT COUNT(*) AS _col_0 FROM "足球数据" AS football_data WHERE football_data."PS主胜赔率" <> '' AND football_data."PS平局赔率" <> '' AND football_data."PS客胜赔率" <> ''	WorldSoccerDataBase
SELECT COUNT(*) AS _col_0 FROM "足球数据" AS football_data WHERE football_data."赛季" LIKE '%2010%' AND football_data."国家" = 'Spain'	WorldSoccerDataBase
SELECT COUNT(*) AS _col_0 FROM "足球数据" AS football_data WHERE football_data."全场主队进球数" = 0 AND football_data."全场客队进球数" = 0	WorldSoccerDataBase
SELECT football_data."客队" AS awayteam FROM "足球数据" AS football_data WHERE football_data."主队" = 'Omiya Ardija' AND football_data."赛季" LIKE '%2018%'	WorldSoccerDataBase
SELECT MAX(football_data.B365A) AS _col_0 FROM "足球数据" AS football_data	WorldSoccerDataBase
SELECT football_data.B365D AS b365d FROM "足球数据" AS football_data WHERE football_data."主队" = 'Swindon' AND football_data."客队" = 'Millwall' AND football_data."赛季" = '2016/2017'	WorldSoccerDataBase
SELECT betfront."比赛" AS match FROM "博彩前端" AS betfront ORDER BY betfront."平局初盘赔率" DESC LIMIT 1	WorldSoccerDataBase
SELECT betfront."年份" AS year FROM "博彩前端" AS betfront GROUP BY betfront."年份" ORDER BY COUNT(*) DESC LIMIT 1	WorldSoccerDataBase
