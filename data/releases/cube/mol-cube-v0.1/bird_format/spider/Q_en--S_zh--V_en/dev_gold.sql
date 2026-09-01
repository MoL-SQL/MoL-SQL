SELECT COUNT(*) AS _col_0 FROM "演唱会" AS concert WHERE concert."年份" = 2014 OR concert."年份" = 2015	concert_singer
SELECT t2."名称" AS name, t2."容量" AS capacity FROM "演唱会" AS t1 JOIN "体育场" AS t2 ON t1."体育场编号" = t2."体育场编号" WHERE t1."年份" > 2013 GROUP BY t2."体育场编号" ORDER BY COUNT(*) DESC LIMIT 1	concert_singer
SELECT COUNT(*) AS _col_0 FROM "学生" AS t1 JOIN "拥有宠物" AS t2 ON t1."学生编号" = t2."学生编号" JOIN "宠物" AS t3 ON t2."宠物编号" = t3."宠物编号" WHERE t1."性别" = 'F' AND t3."宠物类型" = 'dog'	pets_1
SELECT DISTINCT t1."名" AS fname FROM "学生" AS t1 JOIN "拥有宠物" AS t2 ON t1."学生编号" = t2."学生编号" JOIN "宠物" AS t3 ON t3."宠物编号" = t2."宠物编号" WHERE t3."宠物类型" = 'cat' OR t3."宠物类型" = 'dog'	pets_1
SELECT t1."名" AS fname FROM "学生" AS t1 JOIN "拥有宠物" AS t2 ON t1."学生编号" = t2."学生编号" JOIN "宠物" AS t3 ON t3."宠物编号" = t2."宠物编号" WHERE t3."宠物类型" = 'cat' INTERSECT SELECT t1."名" AS fname FROM "学生" AS t1 JOIN "拥有宠物" AS t2 ON t1."学生编号" = t2."学生编号" JOIN "宠物" AS t3 ON t3."宠物编号" = t2."宠物编号" WHERE t3."宠物类型" = 'dog'	pets_1
SELECT student."专业" AS major, student."年龄" AS age FROM "学生" AS student WHERE NOT student."学生编号" IN (SELECT t1."学生编号" AS stuid FROM "学生" AS t1 JOIN "拥有宠物" AS t2 ON t1."学生编号" = t2."学生编号" JOIN "宠物" AS t3 ON t3."宠物编号" = t2."宠物编号" WHERE t3."宠物类型" = 'cat')	pets_1
SELECT student."学生编号" AS stuid FROM "学生" AS student EXCEPT SELECT t1."学生编号" AS stuid FROM "学生" AS t1 JOIN "拥有宠物" AS t2 ON t1."学生编号" = t2."学生编号" JOIN "宠物" AS t3 ON t3."宠物编号" = t2."宠物编号" WHERE t3."宠物类型" = 'cat'	pets_1
SELECT t1."名" AS fname, t1."年龄" AS age FROM "学生" AS t1 JOIN "拥有宠物" AS t2 ON t1."学生编号" = t2."学生编号" JOIN "宠物" AS t3 ON t3."宠物编号" = t2."宠物编号" WHERE t3."宠物类型" = 'dog' AND NOT t1."学生编号" IN (SELECT t1."学生编号" AS stuid FROM "学生" AS t1 JOIN "拥有宠物" AS t2 ON t1."学生编号" = t2."学生编号" JOIN "宠物" AS t3 ON t3."宠物编号" = t2."宠物编号" WHERE t3."宠物类型" = 'cat')	pets_1
SELECT t1."名" AS fname, t1."年龄" AS age FROM "学生" AS t1 JOIN "拥有宠物" AS t2 ON t1."学生编号" = t2."学生编号" JOIN "宠物" AS t3 ON t3."宠物编号" = t2."宠物编号" WHERE t3."宠物类型" = 'dog' AND NOT t1."学生编号" IN (SELECT t1."学生编号" AS stuid FROM "学生" AS t1 JOIN "拥有宠物" AS t2 ON t1."学生编号" = t2."学生编号" JOIN "宠物" AS t3 ON t3."宠物编号" = t2."宠物编号" WHERE t3."宠物类型" = 'cat')	pets_1
SELECT t1."姓" AS lname FROM "学生" AS t1 JOIN "拥有宠物" AS t2 ON t1."学生编号" = t2."学生编号" JOIN "宠物" AS t3 ON t3."宠物编号" = t2."宠物编号" WHERE t3."宠物年龄" = 3 AND t3."宠物类型" = 'cat'	pets_1
SELECT t1."0–60英里/小时加速时间（秒）" AS accelerate FROM "汽车数据" AS t1 JOIN "汽车名称" AS t2 ON t1."汽车编号" = t2."品牌编号" WHERE t2."品牌名称" = 'amc hornet sportabout (sw)'	car_1
SELECT t1."国家名称" AS countryname FROM "国家" AS t1 JOIN "大洲" AS t2 ON t1."所属大洲" = t2."大洲编号" JOIN "汽车制造商" AS t3 ON t1."国家编号" = t3."所属国家" WHERE t2."大洲名称" = 'europe' GROUP BY t1."国家名称" HAVING COUNT(*) >= 3	car_1
SELECT t1."国家名称" AS countryname FROM "国家" AS t1 JOIN "大洲" AS t2 ON t1."所属大洲" = t2."大洲编号" JOIN "汽车制造商" AS t3 ON t1."国家编号" = t3."所属国家" WHERE t2."大洲名称" = 'europe' GROUP BY t1."国家名称" HAVING COUNT(*) >= 3	car_1
SELECT AVG(t2."排量（升）") AS _col_0 FROM "汽车名称" AS t1 JOIN "汽车数据" AS t2 ON t1."品牌编号" = t2."汽车编号" WHERE t1."车型名称" = 'volvo'	car_1
SELECT AVG(t2."排量（升）") AS _col_0 FROM "汽车名称" AS t1 JOIN "汽车数据" AS t2 ON t1."品牌编号" = t2."汽车编号" WHERE t1."车型名称" = 'volvo'	car_1
SELECT t1."气缸数" AS cylinders FROM "汽车数据" AS t1 JOIN "汽车名称" AS t2 ON t1."汽车编号" = t2."品牌编号" WHERE t2."车型名称" = 'volvo' ORDER BY t1."0–60英里/小时加速时间（秒）" ASC LIMIT 1	car_1
SELECT t1."国家编号" AS countryid, t1."国家名称" AS countryname FROM "国家" AS t1 JOIN "汽车制造商" AS t2 ON t1."国家编号" = t2."所属国家" GROUP BY t1."国家编号" HAVING COUNT(*) > 3 UNION SELECT t1."国家编号" AS countryid, t1."国家名称" AS countryname FROM "国家" AS t1 JOIN "汽车制造商" AS t2 ON t1."国家编号" = t2."所属国家" JOIN "车型列表" AS t3 ON t2."制造商编号" = t3."制造商简称" WHERE t3."车型名称" = 'fiat'	car_1
SELECT t1."国家编号" AS countryid, t1."国家名称" AS countryname FROM "国家" AS t1 JOIN "汽车制造商" AS t2 ON t1."国家编号" = t2."所属国家" GROUP BY t1."国家编号" HAVING COUNT(*) > 3 UNION SELECT t1."国家编号" AS countryid, t1."国家名称" AS countryname FROM "国家" AS t1 JOIN "汽车制造商" AS t2 ON t1."国家编号" = t2."所属国家" JOIN "车型列表" AS t3 ON t2."制造商编号" = t3."制造商简称" WHERE t3."车型名称" = 'fiat'	car_1
SELECT airlines."所属国家" AS country FROM "航空公司" AS airlines WHERE airlines."航空公司名称" = 'JetBlue Airways'	flight_2
SELECT airlines."所属国家" AS country FROM "航空公司" AS airlines WHERE airlines."航空公司名称" = 'JetBlue Airways'	flight_2
SELECT airlines."缩写" AS abbreviation FROM "航空公司" AS airlines WHERE airlines."航空公司名称" = 'JetBlue Airways'	flight_2
SELECT airlines."缩写" AS abbreviation FROM "航空公司" AS airlines WHERE airlines."航空公司名称" = 'JetBlue Airways'	flight_2
SELECT airlines."航空公司名称" AS airline FROM "航空公司" AS airlines WHERE airlines."缩写" = 'UAL'	flight_2
SELECT airlines."航空公司名称" AS airline FROM "航空公司" AS airlines WHERE airlines."缩写" = 'UAL'	flight_2
SELECT COUNT(*) AS _col_0 FROM "航空公司" AS t1 JOIN "航班" AS t2 ON t2."航空公司名称" = t1."唯一标识符" WHERE t1."航空公司名称" = 'United Airlines' AND t2."到达机场" = 'ASY'	flight_2
SELECT COUNT(*) AS _col_0 FROM "航空公司" AS t1 JOIN "航班" AS t2 ON t2."航空公司名称" = t1."唯一标识符" WHERE t1."航空公司名称" = 'United Airlines' AND t2."出发机场" = 'AHD'	flight_2
SELECT t1."航班号" AS flightno FROM "航班" AS t1 JOIN "航空公司" AS t2 ON t2."唯一标识符" = t1."航空公司名称" WHERE t2."航空公司名称" = 'United Airlines'	flight_2
SELECT t1."航班号" AS flightno FROM "航班" AS t1 JOIN "航空公司" AS t2 ON t2."唯一标识符" = t1."航空公司名称" WHERE t2."航空公司名称" = 'United Airlines'	flight_2
SELECT t1."姓名" AS name FROM "员工" AS t1 JOIN "绩效评估" AS t2 ON t1."员工编号" = t2."员工编号" GROUP BY t2."员工编号" ORDER BY COUNT(*) DESC LIMIT 1	employee_hire_evaluation
SELECT t2."门店名称" AS name FROM "聘用记录" AS t1 JOIN "门店" AS t2 ON t1."门店编号" = t2."门店编号" GROUP BY t1."门店编号" ORDER BY COUNT(*) DESC LIMIT 1	employee_hire_evaluation
SELECT ref_template_types."模板类型编码" AS template_type_code FROM "模板类型参考表" AS ref_template_types WHERE ref_template_types."模板类型描述" = 'Book'	cre_Doc_Template_Mgt
SELECT ref_template_types."模板类型编码" AS template_type_code FROM "模板类型参考表" AS ref_template_types WHERE ref_template_types."模板类型描述" = 'Book'	cre_Doc_Template_Mgt
SELECT t2."模板编号" AS template_id FROM "模板类型参考表" AS t1 JOIN "模板" AS t2 ON t1."模板类型编码" = t2."模板类型编码" WHERE t1."模板类型描述" = 'Presentation'	cre_Doc_Template_Mgt
SELECT t2."模板编号" AS template_id FROM "模板类型参考表" AS t1 JOIN "模板" AS t2 ON t1."模板类型编码" = t2."模板类型编码" WHERE t1."模板类型描述" = 'Presentation'	cre_Doc_Template_Mgt
SELECT paragraphs."其他详情" AS other_details FROM "段落" AS paragraphs WHERE paragraphs."段落文本" LIKE 'korea'	cre_Doc_Template_Mgt
SELECT paragraphs."其他详情" AS other_details FROM "段落" AS paragraphs WHERE paragraphs."段落文本" LIKE 'korea'	cre_Doc_Template_Mgt
SELECT paragraphs."文档编号" AS document_id FROM "段落" AS paragraphs WHERE paragraphs."段落文本" = 'Brazil' INTERSECT SELECT paragraphs."文档编号" AS document_id FROM "段落" AS paragraphs WHERE paragraphs."段落文本" = 'Ireland'	cre_Doc_Template_Mgt
SELECT paragraphs."文档编号" AS document_id FROM "段落" AS paragraphs WHERE paragraphs."段落文本" = 'Brazil' INTERSECT SELECT paragraphs."文档编号" AS document_id FROM "段落" AS paragraphs WHERE paragraphs."段落文本" = 'Ireland'	cre_Doc_Template_Mgt
SELECT COUNT(*) AS _col_0 FROM "教师" AS teacher	course_teach
SELECT t3."姓名" AS name FROM "课程安排" AS t1 JOIN "课程" AS t2 ON t1."课程编号" = t2."课程编号" JOIN "教师" AS t3 ON t1."教师编号" = t3."教师编号" WHERE t2."课程名称" = 'Math'	course_teach
SELECT t3."姓名" AS name FROM "课程安排" AS t1 JOIN "课程" AS t2 ON t1."课程编号" = t2."课程编号" JOIN "教师" AS t3 ON t1."教师编号" = t3."教师编号" WHERE t2."课程名称" = 'Math'	course_teach
SELECT AVG(visitor."年龄") AS _col_0 FROM "访客" AS visitor WHERE visitor."会员等级" <= 4	museum_visit
SELECT t1."访客编号" AS id, t1."姓名" AS name, t1."年龄" AS age FROM "访客" AS t1 JOIN "参观记录" AS t2 ON t1."访客编号" = t2."访客编号" GROUP BY t1."访客编号" HAVING COUNT(*) > 1	museum_visit
SELECT players."名" AS first_name, players."姓" AS last_name FROM "球员" AS players ORDER BY players."出生日期"	wta_1
SELECT COUNT(*) AS _col_0, players."国家代码" AS country_code FROM "球员" AS players GROUP BY players."国家代码"	wta_1
SELECT COUNT(*) AS _col_0 FROM "舰船" AS ship WHERE ship."舰船处置方式" = 'Captured'	battle_death
SELECT battle."名称" AS name, battle."结果" AS result FROM "战役" AS battle WHERE battle."保加利亚指挥官" <> 'Boril'	battle_death
SELECT DISTINCT t1."编号" AS id, t1."名称" AS name FROM "战役" AS t1 JOIN "舰船" AS t2 ON t1."编号" = t2."战损状态" WHERE t2."舰船类型" = 'Brig'	battle_death
SELECT battle."名称" AS name FROM "战役" AS battle WHERE battle."保加利亚指挥官" = 'Kaloyan' AND battle."拉丁指挥官" = 'Baldwin I'	battle_death
SELECT battle."名称" AS name, battle."结果" AS result, battle."保加利亚指挥官" AS bulgarian_commander FROM "战役" AS battle EXCEPT SELECT t1."名称" AS name, t1."结果" AS result, t1."保加利亚指挥官" AS bulgarian_commander FROM "战役" AS t1 JOIN "舰船" AS t2 ON t1."编号" = t2."战损状态" WHERE t2."位置" = 'English Channel'	battle_death
SELECT death."备注" AS note FROM "伤亡" AS death WHERE death."备注" LIKE '%East%'	battle_death
SELECT t1."学位项目编号" AS degree_program_id, t1."学位简称" AS degree_summary_name FROM "学位项目" AS t1 JOIN "学生注册" AS t2 ON t1."学位项目编号" = t2."学位项目编号" GROUP BY t1."学位项目编号" ORDER BY COUNT(*) DESC LIMIT 1	student_transcripts_tracking
SELECT t1."学位项目编号" AS degree_program_id, t1."学位简称" AS degree_summary_name FROM "学位项目" AS t1 JOIN "学生注册" AS t2 ON t1."学位项目编号" = t2."学位项目编号" GROUP BY t1."学位项目编号" ORDER BY COUNT(*) DESC LIMIT 1	student_transcripts_tracking
SELECT cartoon."标题" AS title FROM "动画片" AS cartoon WHERE cartoon."导演" = 'Ben Jones'	tvshow
SELECT cartoon."标题" AS title FROM "动画片" AS cartoon WHERE cartoon."导演" = 'Ben Jones'	tvshow
SELECT COUNT(*) AS _col_0 FROM "动画片" AS cartoon WHERE cartoon."编剧" = 'Joseph Kuhr'	tvshow
SELECT COUNT(*) AS _col_0 FROM "动画片" AS cartoon WHERE cartoon."编剧" = 'Joseph Kuhr'	tvshow
SELECT cartoon."标题" AS title FROM "动画片" AS cartoon WHERE cartoon."导演" = 'Ben Jones' OR cartoon."导演" = 'Brandon Vietti'	tvshow
SELECT cartoon."标题" AS title FROM "动画片" AS cartoon WHERE cartoon."导演" = 'Ben Jones' OR cartoon."导演" = 'Brandon Vietti'	tvshow
SELECT COUNT(*) AS _col_0 FROM "电视频道" AS tv_channel WHERE tv_channel."语言" = 'English'	tvshow
SELECT COUNT(*) AS _col_0 FROM "电视频道" AS tv_channel WHERE tv_channel."语言" = 'English'	tvshow
SELECT tv_series."播出日期" AS air_date FROM "电视剧" AS tv_series WHERE tv_series."集数" = 'A Love of a Lifetime'	tvshow
SELECT tv_series."播出日期" AS air_date FROM "电视剧" AS tv_series WHERE tv_series."集数" = 'A Love of a Lifetime'	tvshow
SELECT tv_series."周排名" AS weekly_rank FROM "电视剧" AS tv_series WHERE tv_series."集数" = 'A Love of a Lifetime'	tvshow
SELECT tv_series."周排名" AS weekly_rank FROM "电视剧" AS tv_series WHERE tv_series."集数" = 'A Love of a Lifetime'	tvshow
SELECT tv_channel."套餐选项" AS package_option, tv_channel."节目名称" AS series_name FROM "电视频道" AS tv_channel WHERE tv_channel."高清电视" = 'yes'	tvshow
SELECT tv_channel."套餐选项" AS package_option, tv_channel."节目名称" AS series_name FROM "电视频道" AS tv_channel WHERE tv_channel."高清电视" = 'yes'	tvshow
SELECT tv_channel."像素宽高比_PAR" AS pixel_aspect_ratio_par, tv_channel."国家" AS country FROM "电视频道" AS tv_channel WHERE tv_channel."语言" <> 'English'	tvshow
SELECT tv_channel."编号" AS id FROM "电视频道" AS tv_channel EXCEPT SELECT cartoon."频道" AS channel FROM "动画片" AS cartoon WHERE cartoon."导演" = 'Ben Jones'	tvshow
SELECT tv_channel."套餐选项" AS package_option FROM "电视频道" AS tv_channel WHERE NOT tv_channel."编号" IN (SELECT cartoon."频道" AS channel FROM "动画片" AS cartoon WHERE cartoon."导演" = 'Ben Jones')	tvshow
SELECT people."姓名" AS name FROM "人员" AS people WHERE people."国籍" <> 'Russia'	poker_player
SELECT people."姓名" AS name FROM "人员" AS people WHERE people."国籍" <> 'Russia'	poker_player
SELECT people."姓名" AS name FROM "人员" AS people WHERE NOT people."人员编号" IN (SELECT poker_player."人员编号" AS people_id FROM "扑克选手" AS poker_player)	poker_player
SELECT COUNT(*) AS _col_0 FROM "区号州信息" AS area_code_state	voter_1
SELECT t1."参赛者编号" AS contestant_number, t1."参赛者姓名" AS contestant_name FROM "参赛者" AS t1 JOIN "投票记录" AS t2 ON t1."参赛者编号" = t2."参赛者编号" GROUP BY t1."参赛者编号" ORDER BY COUNT(*) ASC LIMIT 1	voter_1
SELECT COUNT(*) AS _col_0 FROM "国家" AS country WHERE country."政体" = 'Republic'	world_1
SELECT country."名称" AS name FROM "国家" AS country WHERE country."洲" = 'Asia' ORDER BY country."预期寿命" LIMIT 1	world_1
SELECT AVG(country."国民生产总值") AS _col_0, SUM(country."人口") AS _col_1 FROM "国家" AS country WHERE country."政体" = 'US Territory'	world_1
SELECT t2."语言" AS language FROM "国家" AS t1 JOIN "国家语言" AS t2 ON t1."代码" = t2."国家代码" WHERE t1."政体" = 'Republic' GROUP BY t2."语言" HAVING COUNT(*) = 1	world_1
SELECT country."名称" AS name FROM "国家" AS country WHERE country."洲" = 'Asia' AND country."人口" > (SELECT MIN(country."人口") AS _col_0 FROM "国家" AS country WHERE country."洲" = 'Africa')	world_1
SELECT DISTINCT t2."名称" AS name FROM "国家" AS t1 JOIN "城市" AS t2 ON t2."国家代码" = t1."代码" WHERE t1."洲" = 'Europe' AND NOT t1."名称" IN (SELECT t3."名称" AS name FROM "国家" AS t3 JOIN "国家语言" AS t4 ON t3."代码" = t4."国家代码" WHERE t4."是否官方语言" = 'T' AND t4."语言" = 'English')	world_1
SELECT DISTINCT t3."名称" AS name FROM "国家" AS t1 JOIN "国家语言" AS t2 ON t1."代码" = t2."国家代码" JOIN "城市" AS t3 ON t1."代码" = t3."国家代码" WHERE t2."是否官方语言" = 'T' AND t2."语言" = 'Chinese' AND t1."洲" = 'Asia'	world_1
SELECT COUNT(*) AS _col_0 FROM "国家" AS country WHERE country."洲" = 'Asia'	world_1
SELECT COUNT(*) AS _col_0 FROM "国家" AS country WHERE country."洲" = 'Asia'	world_1
SELECT conductor."姓名" AS name FROM "指挥家" AS conductor WHERE conductor."国籍" <> 'USA'	orchestra
SELECT conductor."姓名" AS name FROM "指挥家" AS conductor WHERE conductor."国籍" <> 'USA'	orchestra
SELECT MAX(performance."收视份额") AS _col_0, MIN(performance."收视份额") AS _col_1 FROM "演出" AS performance WHERE performance."类型" <> 'Live final'	orchestra
SELECT MAX(performance."收视份额") AS _col_0, MIN(performance."收视份额") AS _col_1 FROM "演出" AS performance WHERE performance."类型" <> 'Live final'	orchestra
SELECT highschooler."年级" AS grade FROM "高中生" AS highschooler GROUP BY highschooler."年级" HAVING COUNT(*) >= 4	network_1
SELECT t2."姓名" AS name FROM "好友关系" AS t1 JOIN "高中生" AS t2 ON t1."学生编号" = t2."学生编号" GROUP BY t1."学生编号" ORDER BY COUNT(*) DESC LIMIT 1	network_1
SELECT t1."专业人员编号" AS professional_id, t1."手机号码" AS cell_number FROM "专业人员" AS t1 JOIN "治疗记录" AS t2 ON t1."专业人员编号" = t2."专业人员编号" GROUP BY t1."专业人员编号" HAVING COUNT(*) >= 2	dog_kennels
SELECT t1."犬只名称" AS name, t2."治疗日期" AS date_of_treatment FROM "犬只" AS t1 JOIN "治疗记录" AS t2 ON t1."犬只编号" = t2."犬只编号" WHERE t1."犬种编码" = (SELECT dogs."犬种编码" AS breed_code FROM "犬只" AS dogs GROUP BY dogs."犬种编码" ORDER BY COUNT(*) ASC LIMIT 1)	dog_kennels
SELECT COUNT(*) AS _col_0 FROM "歌手" AS singer	singer
SELECT singer."姓名" AS name FROM "歌手" AS singer WHERE singer."国籍" <> 'France'	singer
SELECT singer."姓名" AS name FROM "歌手" AS singer WHERE singer."国籍" <> 'France'	singer
SELECT COUNT(*) AS _col_0 FROM "其他可用设施" AS other_available_features	real_estate_properties
