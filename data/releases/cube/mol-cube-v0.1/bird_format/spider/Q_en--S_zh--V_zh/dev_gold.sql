SELECT count(*) FROM `演唱会` WHERE `年份`  =  2014 OR `年份`  =  2015	concert_singer
select t2.`名称` ,  t2.`容量` from `演唱会` as t1 join `体育场` as t2 on t1.`体育场编号`  =  t2.`体育场编号` where t1.`年份`  >  2013 group by t2.`体育场编号` order by count(*) desc limit 1	concert_singer
SELECT count(*) FROM `学生` AS T1 JOIN `拥有宠物` AS T2 ON T1.`学生编号`  =  T2.`学生编号` JOIN `宠物` AS T3 ON T2.`宠物编号`  =  T3.`宠物编号` WHERE T1.`性别`  =  'F' AND T3.`宠物类型`  =  '狗'	pets_1
SELECT DISTINCT T1.`名` FROM `学生` AS T1 JOIN `拥有宠物` AS T2 ON T1.`学生编号`  =  T2.`学生编号` JOIN `宠物` AS T3 ON T3.`宠物编号`  =  T2.`宠物编号` WHERE T3.`宠物类型`  =  '猫' OR T3.`宠物类型`  =  '狗'	pets_1
select t1.`名` from `学生` as t1 join `拥有宠物` as t2 on t1.`学生编号`  =  t2.`学生编号` join `宠物` as t3 on t3.`宠物编号`  =  t2.`宠物编号` where t3.`宠物类型`  =  '猫' intersect select t1.`名` from `学生` as t1 join `拥有宠物` as t2 on t1.`学生编号`  =  t2.`学生编号` join `宠物` as t3 on t3.`宠物编号`  =  t2.`宠物编号` where t3.`宠物类型`  =  '狗'	pets_1
SELECT `专业` ,  `年龄` FROM `学生` WHERE `学生编号` NOT IN (SELECT T1.`学生编号` FROM `学生` AS T1 JOIN `拥有宠物` AS T2 ON T1.`学生编号`  =  T2.`学生编号` JOIN `宠物` AS T3 ON T3.`宠物编号`  =  T2.`宠物编号` WHERE T3.`宠物类型`  =  '猫')	pets_1
SELECT `学生编号` FROM `学生` EXCEPT SELECT T1.`学生编号` FROM `学生` AS T1 JOIN `拥有宠物` AS T2 ON T1.`学生编号`  =  T2.`学生编号` JOIN `宠物` AS T3 ON T3.`宠物编号`  =  T2.`宠物编号` WHERE T3.`宠物类型`  =  '猫'	pets_1
SELECT T1.`名` ,  T1.`年龄` FROM `学生` AS T1 JOIN `拥有宠物` AS T2 ON T1.`学生编号`  =  T2.`学生编号` JOIN `宠物` AS T3 ON T3.`宠物编号`  =  T2.`宠物编号` WHERE T3.`宠物类型`  =  '狗' AND T1.`学生编号` NOT IN (SELECT T1.`学生编号` FROM `学生` AS T1 JOIN `拥有宠物` AS T2 ON T1.`学生编号`  =  T2.`学生编号` JOIN `宠物` AS T3 ON T3.`宠物编号`  =  T2.`宠物编号` WHERE T3.`宠物类型`  =  '猫')	pets_1
SELECT T1.`名` ,  T1.`年龄` FROM `学生` AS T1 JOIN `拥有宠物` AS T2 ON T1.`学生编号`  =  T2.`学生编号` JOIN `宠物` AS T3 ON T3.`宠物编号`  =  T2.`宠物编号` WHERE T3.`宠物类型`  =  '狗' AND T1.`学生编号` NOT IN (SELECT T1.`学生编号` FROM `学生` AS T1 JOIN `拥有宠物` AS T2 ON T1.`学生编号`  =  T2.`学生编号` JOIN `宠物` AS T3 ON T3.`宠物编号`  =  T2.`宠物编号` WHERE T3.`宠物类型`  =  '猫')	pets_1
SELECT T1.`姓` FROM `学生` AS T1 JOIN `拥有宠物` AS T2 ON T1.`学生编号`  =  T2.`学生编号` JOIN `宠物` AS T3 ON T3.`宠物编号`  =  T2.`宠物编号` WHERE T3.`宠物年龄`  =  3 AND T3.`宠物类型`  =  '猫'	pets_1
SELECT T1.`0–60英里/小时加速时间（秒）` FROM `汽车数据` AS T1 JOIN `汽车名称` AS T2 ON T1.`汽车编号`  =  T2.`品牌编号` WHERE T2.`品牌名称`  =  'AMC Hornet Sportabout（旅行版）';	car_1
SELECT T1.`国家名称` FROM `国家` AS T1 JOIN `大洲` AS T2 ON T1.`所属大洲`  =  T2.`大洲编号` JOIN `汽车制造商` AS T3 ON T1.`国家编号`  =  T3.`所属国家` WHERE T2.`大洲名称`  =  '欧洲' GROUP BY T1.`国家名称` HAVING count(*)  >=  3;	car_1
SELECT T1.`国家名称` FROM `国家` AS T1 JOIN `大洲` AS T2 ON T1.`所属大洲`  =  T2.`大洲编号` JOIN `汽车制造商` AS T3 ON T1.`国家编号`  =  T3.`所属国家` WHERE T2.`大洲名称`  =  '欧洲' GROUP BY T1.`国家名称` HAVING count(*)  >=  3;	car_1
SELECT avg(T2.`排量（升）`) FROM `汽车名称` AS T1 JOIN `汽车数据` AS T2 ON T1.`品牌编号`  =  T2.`汽车编号` WHERE T1.`车型名称`  =  '沃尔沃';	car_1
SELECT avg(T2.`排量（升）`) FROM `汽车名称` AS T1 JOIN `汽车数据` AS T2 ON T1.`品牌编号`  =  T2.`汽车编号` WHERE T1.`车型名称`  =  '沃尔沃';	car_1
SELECT T1.`气缸数` FROM `汽车数据` AS T1 JOIN `汽车名称` AS T2 ON T1.`汽车编号`  =  T2.`品牌编号` WHERE T2.`车型名称`  =  '沃尔沃' ORDER BY T1.`0–60英里/小时加速时间（秒）` ASC LIMIT 1;	car_1
SELECT T1.`国家编号` ,  T1.`国家名称` FROM `国家` AS T1 JOIN `汽车制造商` AS T2 ON T1.`国家编号`  =  T2.`所属国家` GROUP BY T1.`国家编号` HAVING count(*)  >  3 UNION SELECT T1.`国家编号` ,  T1.`国家名称` FROM `国家` AS T1 JOIN `汽车制造商` AS T2 ON T1.`国家编号`  =  T2.`所属国家` JOIN `车型列表` AS T3 ON T2.`制造商编号`  =  T3.`制造商简称` WHERE T3.`车型名称`  =  '菲亚特';	car_1
select t1.`国家编号` ,  t1.`国家名称` from `国家` as t1 join `汽车制造商` as t2 on t1.`国家编号`  =  t2.`所属国家` group by t1.`国家编号` having count(*)  >  3 union select t1.`国家编号` ,  t1.`国家名称` from `国家` as t1 join `汽车制造商` as t2 on t1.`国家编号`  =  t2.`所属国家` join `车型列表` as t3 on t2.`制造商编号`  =  t3.`制造商简称` where t3.`车型名称`  =  '菲亚特';	car_1
SELECT `所属国家` FROM `航空公司` WHERE `航空公司名称`  =  "捷蓝航空"	flight_2
SELECT `所属国家` FROM `航空公司` WHERE `航空公司名称`  =  "捷蓝航空"	flight_2
SELECT `缩写` FROM `航空公司` WHERE `航空公司名称`  =  "捷蓝航空"	flight_2
SELECT `缩写` FROM `航空公司` WHERE `航空公司名称`  =  "捷蓝航空"	flight_2
SELECT `航空公司名称` FROM `航空公司` WHERE `缩写`  =  "UAL（联合航空控股公司）"	flight_2
SELECT `航空公司名称` FROM `航空公司` WHERE `缩写`  =  "UAL（联合航空控股公司）"	flight_2
SELECT count(*) FROM `航空公司` AS T1 JOIN `航班` AS T2 ON T2.`航空公司名称`  =  T1.`唯一标识符` WHERE T1.`航空公司名称`  =  "联合航空" AND T2.`到达机场`  =  "ASY"	flight_2
SELECT count(*) FROM `航空公司` AS T1 JOIN `航班` AS T2 ON T2.`航空公司名称`  =  T1.`唯一标识符` WHERE T1.`航空公司名称`  =  "联合航空" AND T2.`出发机场`  =  "AHD"	flight_2
SELECT T1.`航班号` FROM `航班` AS T1 JOIN `航空公司` AS T2 ON T2.`唯一标识符`  =  T1.`航空公司名称` WHERE T2.`航空公司名称`  =  "联合航空"	flight_2
SELECT T1.`航班号` FROM `航班` AS T1 JOIN `航空公司` AS T2 ON T2.`唯一标识符`  =  T1.`航空公司名称` WHERE T2.`航空公司名称`  =  "联合航空"	flight_2
SELECT t1.`姓名` FROM `员工` AS t1 JOIN `绩效评估` AS t2 ON t1.`员工编号`  =  t2.`员工编号` GROUP BY t2.`员工编号` ORDER BY count(*) DESC LIMIT 1	employee_hire_evaluation
SELECT t2.`门店名称` FROM `聘用记录` AS t1 JOIN `门店` AS t2 ON t1.`门店编号`  =  t2.`门店编号` GROUP BY t1.`门店编号` ORDER BY count(*) DESC LIMIT 1	employee_hire_evaluation
SELECT `模板类型编码` FROM `模板类型参考表` WHERE `模板类型描述`  =  "图书"	cre_Doc_Template_Mgt
SELECT `模板类型编码` FROM `模板类型参考表` WHERE `模板类型描述`  =  "图书"	cre_Doc_Template_Mgt
SELECT T2.`模板编号` FROM `模板类型参考表` AS T1 JOIN `模板` AS T2 ON T1.`模板类型编码`  = T2.`模板类型编码` WHERE T1.`模板类型描述`  =  "演示文稿"	cre_Doc_Template_Mgt
SELECT T2.`模板编号` FROM `模板类型参考表` AS T1 JOIN `模板` AS T2 ON T1.`模板类型编码`  = T2.`模板类型编码` WHERE T1.`模板类型描述`  =  "演示文稿"	cre_Doc_Template_Mgt
select `其他详情` from `段落` where `段落文本` like '韩国'	cre_Doc_Template_Mgt
select `其他详情` from `段落` where `段落文本` like '韩国'	cre_Doc_Template_Mgt
SELECT `文档编号` FROM `段落` WHERE `段落文本`  =  '巴西' INTERSECT SELECT `文档编号` FROM `段落` WHERE `段落文本`  =  '爱尔兰'	cre_Doc_Template_Mgt
SELECT `文档编号` FROM `段落` WHERE `段落文本`  =  '巴西' INTERSECT SELECT `文档编号` FROM `段落` WHERE `段落文本`  =  '爱尔兰'	cre_Doc_Template_Mgt
SELECT count(*) FROM `教师`	course_teach
SELECT T3.`姓名` FROM `课程安排` AS T1 JOIN `课程` AS T2 ON T1.`课程编号`  =  T2.`课程编号` JOIN `教师` AS T3 ON T1.`教师编号`  =  T3.`教师编号` WHERE T2.`课程名称`  =  "数学"	course_teach
SELECT T3.`姓名` FROM `课程安排` AS T1 JOIN `课程` AS T2 ON T1.`课程编号`  =  T2.`课程编号` JOIN `教师` AS T3 ON T1.`教师编号`  =  T3.`教师编号` WHERE T2.`课程名称`  =  "数学"	course_teach
SELECT avg(`年龄`) FROM `访客` WHERE `会员等级`  <=  4	museum_visit
SELECT t1.`访客编号` ,  t1.`姓名` ,  t1.`年龄` FROM `访客` AS t1 JOIN `参观记录` AS t2 ON t1.`访客编号`  =  t2.`访客编号` GROUP BY t1.`访客编号` HAVING count(*)  >  1	museum_visit
SELECT `名` ,  `姓` FROM `球员` ORDER BY `出生日期`	wta_1
SELECT count(*) ,  `国家代码` FROM `球员` GROUP BY `国家代码`	wta_1
SELECT count(*) FROM `舰船` WHERE `舰船处置方式`  =  '被俘获'	battle_death
SELECT `名称` ,  `结果` FROM `战役` WHERE `保加利亚指挥官` != '博里尔'	battle_death
SELECT DISTINCT T1.`编号` ,  T1.`名称` FROM `战役` AS T1 JOIN `舰船` AS T2 ON T1.`编号`  =  T2.`战损状态` WHERE T2.`舰船类型`  =  '双桅横帆船'	battle_death
SELECT `名称` FROM `战役` WHERE `保加利亚指挥官`  =  '卡洛扬' AND `拉丁指挥官`  =  '鲍德温一世'	battle_death
SELECT `名称` ,  `结果` ,  `保加利亚指挥官` FROM `战役` EXCEPT SELECT T1.`名称` ,  T1.`结果` ,  T1.`保加利亚指挥官` FROM `战役` AS T1 JOIN `舰船` AS T2 ON T1.`编号`  =  T2.`战损状态` WHERE T2.`位置`  =  '英吉利海峡'	battle_death
SELECT `备注` FROM `伤亡` WHERE `备注` LIKE '%东%'	battle_death
SELECT T1.`学位项目编号` ,  T1.`学位简称` FROM `学位项目` AS T1 JOIN `学生注册` AS T2 ON T1.`学位项目编号`  =  T2.`学位项目编号` GROUP BY T1.`学位项目编号` ORDER BY count(*) DESC LIMIT 1	student_transcripts_tracking
SELECT T1.`学位项目编号` ,  T1.`学位简称` FROM `学位项目` AS T1 JOIN `学生注册` AS T2 ON T1.`学位项目编号`  =  T2.`学位项目编号` GROUP BY T1.`学位项目编号` ORDER BY count(*) DESC LIMIT 1	student_transcripts_tracking
SELECT `标题` FROM `动画片` WHERE `导演` = "本·琼斯";	tvshow
SELECT `标题` FROM `动画片` WHERE `导演` = "本·琼斯";	tvshow
SELECT count(*) FROM `动画片` WHERE `编剧` = "约瑟夫·库尔";	tvshow
SELECT count(*) FROM `动画片` WHERE `编剧` = "约瑟夫·库尔";	tvshow
SELECT `标题` FROM `动画片` WHERE `导演` = "本·琼斯" OR `导演` = "布兰登·维蒂";	tvshow
SELECT `标题` FROM `动画片` WHERE `导演` = "本·琼斯" OR `导演` = "布兰登·维蒂";	tvshow
SELECT count(*) FROM `电视频道` WHERE `语言` = "英语";	tvshow
SELECT count(*) FROM `电视频道` WHERE `语言` = "英语";	tvshow
SELECT `播出日期` FROM `电视剧` WHERE `集数` = "一生之爱";	tvshow
SELECT `播出日期` FROM `电视剧` WHERE `集数` = "一生之爱";	tvshow
SELECT `周排名` FROM `电视剧` WHERE `集数` = "一生之爱";	tvshow
SELECT `周排名` FROM `电视剧` WHERE `集数` = "一生之爱";	tvshow
SELECT `套餐选项` ,  `节目名称` FROM `电视频道` WHERE `高清电视`  =  "是"	tvshow
SELECT `套餐选项` ,  `节目名称` FROM `电视频道` WHERE `高清电视`  =  "是"	tvshow
SELECT `像素宽高比_PAR` ,  `国家` FROM `电视频道` WHERE `语言` != '英语'	tvshow
SELECT `编号` FROM `电视频道` EXCEPT SELECT `频道` FROM `动画片` WHERE `导演`  =  '本·琼斯'	tvshow
SELECT `套餐选项` FROM `电视频道` WHERE `编号` NOT IN (SELECT `频道` FROM `动画片` WHERE `导演`  =  '本·琼斯')	tvshow
SELECT `姓名` FROM `人员` WHERE `国籍` != "俄罗斯"	poker_player
SELECT `姓名` FROM `人员` WHERE `国籍` != "俄罗斯"	poker_player
SELECT `姓名` FROM `人员` WHERE `人员编号` NOT IN (SELECT `人员编号` FROM `扑克选手`)	poker_player
SELECT count(*) FROM `区号州信息`	voter_1
SELECT T1.`参赛者编号` , T1.`参赛者姓名` FROM `参赛者` AS T1 JOIN `投票记录` AS T2 ON T1.`参赛者编号`  =  T2.`参赛者编号` GROUP BY T1.`参赛者编号` ORDER BY count(*) ASC LIMIT 1	voter_1
SELECT count(*) FROM `国家` WHERE `政体`  =  "共和国"	world_1
SELECT `名称` FROM `国家` WHERE `洲`  =  "亚洲" ORDER BY `预期寿命` LIMIT 1	world_1
SELECT avg(`国民生产总值`) ,  sum(`人口`) FROM `国家` WHERE `政体`  =  "美国领土"	world_1
SELECT T2.`语言` FROM `国家` AS T1 JOIN `国家语言` AS T2 ON T1.`代码`  =  T2.`国家代码` WHERE T1.`政体`  =  "共和国" GROUP BY T2.`语言` HAVING COUNT(*)  =  1	world_1
SELECT `名称` FROM `国家` WHERE `洲`  =  "亚洲"  AND `人口`  >  (SELECT min(`人口`) FROM `国家` WHERE `洲`  =  "非洲")	world_1
SELECT DISTINCT T2.`名称` FROM `国家` AS T1 JOIN `城市` AS T2 ON T2.`国家代码`  =  T1.`代码` WHERE T1.`洲`  =  '欧洲' AND T1.`名称` NOT IN (SELECT T3.`名称` FROM `国家` AS T3 JOIN `国家语言` AS T4 ON T3.`代码`  =  T4.`国家代码` WHERE T4.`是否官方语言`  =  'T' AND T4.`语言`  =  'English')	world_1
SELECT DISTINCT T3.`名称` FROM `国家` AS T1 JOIN `国家语言` AS T2 ON T1.`代码`  =  T2.`国家代码` JOIN `城市` AS T3 ON T1.`代码`  =  T3.`国家代码` WHERE T2.`是否官方语言`  =  'T' AND T2.`语言`  =  'Chinese' AND T1.`洲`  =  "亚洲"	world_1
SELECT count(*) FROM `国家` WHERE `洲`  =  "亚洲"	world_1
SELECT count(*) FROM `国家` WHERE `洲`  =  "亚洲"	world_1
SELECT `姓名` FROM `指挥家` WHERE `国籍` != '美国'	orchestra
SELECT `姓名` FROM `指挥家` WHERE `国籍` != '美国'	orchestra
SELECT max(`收视份额`) ,  min(`收视份额`) FROM `演出` WHERE `类型` != "直播总决赛"	orchestra
SELECT max(`收视份额`) ,  min(`收视份额`) FROM `演出` WHERE `类型` != "直播总决赛"	orchestra
SELECT `年级` FROM `高中生` GROUP BY `年级` HAVING count(*)  >=  4	network_1
SELECT T2.`姓名` FROM `好友关系` AS T1 JOIN `高中生` AS T2 ON T1.`学生编号`  =  T2.`学生编号` GROUP BY T1.`学生编号` ORDER BY count(*) DESC LIMIT 1	network_1
SELECT T1.`专业人员编号` ,  T1.`手机号码` FROM `专业人员` AS T1 JOIN `治疗记录` AS T2 ON T1.`专业人员编号`  =  T2.`专业人员编号` GROUP BY T1.`专业人员编号` HAVING count(*)  >=  2	dog_kennels
SELECT T1.`犬只名称` ,  T2.`治疗日期` FROM `犬只` AS T1 JOIN `治疗记录` AS T2 ON T1.`犬只编号`  =  T2.`犬只编号` WHERE T1.`犬种编码`  =  ( SELECT `犬种编码` FROM `犬只` GROUP BY `犬种编码` ORDER BY count(*) ASC LIMIT 1 )	dog_kennels
SELECT count(*) FROM `歌手`	singer
SELECT `姓名` FROM `歌手` WHERE `国籍` != "法国"	singer
SELECT `姓名` FROM `歌手` WHERE `国籍` != "法国"	singer
SELECT count(*) FROM `其他可用设施`	real_estate_properties
