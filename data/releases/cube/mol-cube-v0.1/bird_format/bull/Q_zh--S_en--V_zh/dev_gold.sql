SELECT fundmanager AS fundmanager, fund AS fund FROM mf_awards AS mf_awards WHERE mf_awards.appraisalorg = '证券时报'	ccks_fund
SELECT b.type AS type, COUNT(*) AS _col_1 FROM mf_fundreturnrank AS a JOIN mf_fundarchives AS b ON a.innercode = b.innercode WHERE a.indexcycle = '成立以来' AND a.fundreturnmean > 0 GROUP BY b.type	ccks_fund
SELECT a.secuabbr AS secuabbr, b.secretarybd AS secretarybd, b.secretarybdtel AS secretarybdtel FROM lc_coconcept AS a JOIN lc_stockarchives AS b ON a.companycode = b.companycode WHERE a.conceptname = '3D玻璃'	ccks_stock
SELECT a.name AS name FROM mf_fundmanagernew AS a JOIN mf_fundrisklevel AS b ON a.innercode = b.innercode WHERE b.risklevel = '中低' GROUP BY a.name HAVING COUNT(a.secuabbr) > 5	ccks_fund
SELECT COUNT(*) AS _col_0 FROM mf_fmretscaleanalysis AS a JOIN mf_personalinfo AS b ON a.personalcode = b.personalcode WHERE a.totalaum > 100 AND b.education = '本科'	ccks_fund
SELECT a.secuabbr AS secuabbr, b.secretarybd AS secretarybd FROM lc_coconcept AS a JOIN lc_stockarchives AS b ON a.companycode = b.companycode WHERE a.conceptname = '大飞机'	ccks_stock
SELECT a.chinesename AS chinesename, b.education AS education FROM mf_fmretscaleanalysis AS a JOIN mf_personalinfo AS b ON a.personalcode = b.personalcode WHERE a.timeinterval = '今年以来' ORDER BY a.avgaum DESC LIMIT 3	ccks_fund
SELECT COUNT(*) AS _col_0 FROM mf_fundrisklevel AS a JOIN mf_fundarchives AS b ON a.innercode = b.innercode WHERE a.risklevel = '中' AND b.investmenttype = '综合型'	ccks_fund
SELECT b.secuabbr AS secuabbr, b.manager AS manager, b.riskreturncharacter AS riskreturncharacter FROM mf_benchmarkgrowthrate AS a JOIN mf_fundarchives AS b ON a.innercode = b.innercode ORDER BY a.benchgrforthisweek DESC LIMIT 10	ccks_fund
SELECT b.type AS type, COUNT(*) AS _col_1 FROM mf_fundreturnrank AS a JOIN mf_fundarchives AS b ON a.innercode = b.innercode WHERE a.indexcycle = '六个月' AND a.fundreturnmean < 0 GROUP BY b.type	ccks_fund
SELECT secuabbr AS secuabbr FROM mf_fundreturnrank AS mf_fundreturnrank WHERE mf_fundreturnrank.indexcycle = '六个月' ORDER BY fundreturn DESC LIMIT 1	ccks_fund
SELECT a.chinesename AS chinesename, b.education AS education, b.experiencetime AS experiencetime FROM mf_fmretscaleanalysis AS a JOIN mf_personalinfo AS b ON a.personalcode = b.personalcode WHERE a.weightedavgmonreturn > 0	ccks_fund
SELECT secuabbr AS secuabbr, manager AS manager FROM mf_fundarchives AS mf_fundarchives WHERE investadvisorname = '合煦智远基金管理有限公司' AND mf_fundarchives.fundtype = '债券型'	ccks_fund
SELECT a.totalaumtypeavg AS totalaumtypeavg FROM mf_fmretandscalerank AS a JOIN mf_personalinfo AS b ON a.personalcode = b.personalcode WHERE b.education = '本科'	ccks_fund
SELECT secuabbr AS secuabbr FROM mf_fundarchives AS mf_fundarchives WHERE mf_fundarchives.fundtype = '其他型' AND mf_fundarchives.investstyle = '配置型'	ccks_fund
SELECT a.chinameabbr AS chinameabbr, a.generalmanager AS generalmanager, a.legalrepr AS legalrepr FROM lc_stockarchives AS a JOIN lc_actualcontroller AS b ON a.companycode = b.companycode WHERE b.nationalitydesc = '美国'	ccks_stock
SELECT shname AS shname, actualshares AS actualshares FROM lc_largeshsubscription AS lc_largeshsubscription WHERE secucode = '600110'	ccks_stock
SELECT indexvalue AS indexvalue FROM ed_producerpiformp AS ed_producerpiformp WHERE ed_producerpiformp.indexname = '金属制品业' AND ed_producerpiformp.reportperiod = '上年同期' AND STRFTIME('%Y', enddate) = STRFTIME('%Y', DATE('now', '-1 year'))	ccks_macro
SELECT ratioceiling AS ratioceiling FROM ed_taxrate AS ed_taxrate WHERE ed_taxrate.typename = '农村信用社' AND ed_taxrate.itemname = '超额存款准备金率'	ccks_macro
SELECT b.chinameabbr AS chinameabbr, a.firstindustryname AS firstindustryname FROM lc_exgindustry AS a JOIN lc_sharestru AS b ON a.companycode = b.companycode WHERE b.totalshares > 10000000000	ccks_stock
SELECT gdp AS gdp, primaryindustrygdp AS primaryindustrygdp, secondindustrygdp AS secondindustrygdp, thirdindustrygdp AS thirdindustrygdp FROM ed_grossdomesticproduct AS ed_grossdomesticproduct	ccks_macro
SELECT a.chinameabbr AS chinameabbr, b.state AS state, b.city AS city FROM lc_business AS a JOIN lc_stockarchives AS b ON a.companycode = b.companycode WHERE a.industryname = '资本市场服务'	ccks_stock
SELECT a.chinameabbr AS chinameabbr FROM lc_stockarchives AS a JOIN lc_exgindustry AS b ON a.companycode = b.companycode WHERE a.state = '广东省' AND b.firstindustryname = '房地产业'	ccks_stock
SELECT leadername AS leadername, chinameabbr AS chinameabbr FROM lc_executivesholdings AS lc_executivesholdings WHERE lc_executivesholdings.positiondescription LIKE '%董事长%' OR lc_executivesholdings.positiondescription LIKE '%副董事长%'	ccks_stock
SELECT a.chinesename AS chinesename, b.education AS education FROM mf_fmretandscalerank AS a JOIN mf_personalinfo AS b ON a.personalcode = b.personalcode WHERE a.timeinterval = '近1年' ORDER BY a.returntypeavg DESC LIMIT 5	ccks_fund
SELECT stateownedunits AS stateownedunits, collectiveunits AS collectiveunits, jointventures AS jointventures FROM ed_retailvalueofscgoods AS ed_retailvalueofscgoods	ccks_macro
SELECT enddate AS enddate, subjectsum AS subjectsum FROM ed_newincreasingloan AS ed_newincreasingloan WHERE ed_newincreasingloan.reportperiod = '期末累计'	ccks_macro
SELECT COUNT(*) AS _col_0 FROM lc_coconcept AS a JOIN lc_stockarchives AS b ON a.companycode = b.companycode WHERE a.conceptname = '互联网金融' AND b.city = '杭州市'	ccks_stock
SELECT indexvalue AS indexvalue FROM ed_producerpiformp AS ed_producerpiformp WHERE ed_producerpiformp.reportperiod = '上年同期' AND ed_producerpiformp.indextype = '工业结构分类指数' AND ed_producerpiformp.indexname = '生产资料-加工'	ccks_macro
SELECT indexvalue AS indexvalue FROM ed_producerpiformp AS ed_producerpiformp WHERE ed_producerpiformp.indexname = '医药制造业' AND ed_producerpiformp.reportperiod = '上年同月' AND STRFTIME('%Y', enddate) = STRFTIME('%Y', DATE('now', '-1 year')) AND ROUND(STRFTIME('%m', enddate) / 3.0 + 0.495) = 1	ccks_macro
SELECT b.chinesename AS chinesename FROM mf_managerexperience AS a JOIN mf_personalinfo AS b ON a.personalcode = b.personalcode GROUP BY b.chinesename ORDER BY COUNT(*) DESC LIMIT 1	ccks_fund
SELECT secuabbr AS secuabbr, manager AS manager FROM mf_fundarchives AS mf_fundarchives WHERE mf_fundarchives.investstyle = '大盘价值股票'	ccks_fund
SELECT chinameabbr AS chinameabbr FROM lc_exgindustry AS lc_exgindustry WHERE lc_exgindustry.firstindustryname = '建筑业'	ccks_stock
SELECT secuabbr AS secuabbr FROM mf_fundrisklevel AS mf_fundrisklevel WHERE mf_fundrisklevel.risklevel = '中高'	ccks_fund
SELECT chinameabbr AS chinameabbr, AVG(actualshares) AS _col_1 FROM lc_largeshsubscription AS lc_largeshsubscription GROUP BY chinameabbr	ccks_stock
SELECT investadvisorname AS investadvisorname FROM mf_fundarchives AS mf_fundarchives GROUP BY investadvisorname ORDER BY COUNT(*) DESC LIMIT 1	ccks_fund
SELECT shname AS shname, oughtshares AS oughtshares FROM lc_largeshsubscription AS lc_largeshsubscription WHERE chinameabbr = '天山股份'	ccks_stock
SELECT collectiveunits AS collectiveunits, selfemployed AS selfemployed FROM ed_retailvalueofscgoods AS ed_retailvalueofscgoods WHERE ed_retailvalueofscgoods.reportarea = '省市' AND ed_retailvalueofscgoods.reportperiod = '期末累计' AND STRFTIME('%Y', enddate) = STRFTIME('%Y', DATE('now', '-1 year'))	ccks_macro
SELECT retailvalueofscgoods AS retailvalueofscgoods FROM ed_retailvalueofscgoods AS ed_retailvalueofscgoods WHERE province = '北京'	ccks_macro
SELECT retailvalueofscgoods AS retailvalueofscgoods FROM ed_retailvalueofscgoods AS ed_retailvalueofscgoods WHERE province = '北京' AND ed_retailvalueofscgoods.reportperiod = '期末累计'	ccks_macro
SELECT a.chinameabbr AS chinameabbr, a.fpshname AS fpshname FROM lc_sharefpsta AS a JOIN lc_exgindustry AS b ON a.companycode = b.companycode WHERE b.firstindustryname = '建筑业' ORDER BY a.accuproportion DESC	ccks_stock
SELECT primaryindustrygdp AS primaryindustrygdp, secondindustrygdp AS secondindustrygdp, thirdindustrygdp AS thirdindustrygdp FROM ed_grossdomesticproduct AS ed_grossdomesticproduct	ccks_macro
SELECT basiscode AS basiscode, ratiofloor AS ratiofloor, ratioceiling AS ratioceiling FROM ed_taxrate AS ed_taxrate WHERE ed_taxrate.typename = '企债质押式回购' AND ed_taxrate.itemname = '经手费'	ccks_macro
SELECT MAX(indexvalue) AS _col_0 FROM ed_producerpiformp AS ed_producerpiformp WHERE ed_producerpiformp.indexname = '纺织业' AND ed_producerpiformp.reportperiod = '上年同期' AND STRFTIME('%Y', enddate) = STRFTIME('%Y', DATE('now', '-1 year'))	ccks_macro
SELECT b.secuabbr AS secuabbr, a.rrinsingleyear AS rrinsingleyear, a.rrintwoyear AS rrintwoyear FROM mf_netvalueperformancehis AS a JOIN mf_fundarchives AS b ON a.innercode = b.innercode WHERE b.fundtype = '债券型'	ccks_fund
SELECT enddate AS enddate, retailvalueofscgoods AS retailvalueofscgoods FROM ed_retailvalueofscgoods AS ed_retailvalueofscgoods WHERE province = '上海' AND ed_retailvalueofscgoods.reportperiod = '年度' AND STRFTIME('%Y', enddate) < '2010'	ccks_macro
SELECT enddate AS enddate, industrialvalueadded AS industrialvalueadded FROM ed_industryproduction AS ed_industryproduction WHERE ed_industryproduction.reportarea = '全国' AND ed_industryproduction.statstandard = '国有及规模以上工业企业' AND ed_industryproduction.reportperiod = '期末累计'	ccks_macro
SELECT ratioceiling AS ratioceiling FROM ed_taxrate AS ed_taxrate WHERE ed_taxrate.typename = 'A股' AND ed_taxrate.itemname = '证券交易印花税' AND ed_taxrate.secumarket = '深圳证券交易所'	ccks_macro
SELECT MAX(indexvalue) AS _col_0, MIN(indexvalue) AS _col_1 FROM ed_producerpiformp AS ed_producerpiformp WHERE ed_producerpiformp.indexname = '食品制造业' AND ed_producerpiformp.reportperiod = '上年同期' AND STRFTIME('%Y', enddate) = '2008'	ccks_macro
SELECT lc_exgindustry.secondindustryname AS secondindustryname FROM lc_exgindustry AS lc_exgindustry WHERE lc_exgindustry.firstindustryname = '信息传输、软件和信息技术服务业' GROUP BY lc_exgindustry.secondindustryname ORDER BY COUNT(*) DESC LIMIT 2	ccks_stock
SELECT enddate AS enddate, province AS province, industrialvalueadded AS industrialvalueadded FROM ed_industryproduction AS ed_industryproduction WHERE ed_industryproduction.reportarea = '省市' AND ed_industryproduction.statstandard = '国有及规模以上工业企业' AND ed_industryproduction.reportperiod = '年度'	ccks_macro
SELECT secuabbr AS secuabbr, riskreturncharacter AS riskreturncharacter FROM mf_fundarchives AS mf_fundarchives WHERE mf_fundarchives.investstyle = '行业股票-医药'	ccks_fund
SELECT enddate AS enddate, subjectsum AS subjectsum FROM ed_newincreasingloan AS ed_newincreasingloan WHERE ed_newincreasingloan.reportperiod = '期末累计' AND subjectsum > 150000 AND STRFTIME('%Y', enddate) >= '2000'	ccks_macro
SELECT ratioceiling AS ratioceiling FROM ed_taxrate AS ed_taxrate WHERE ed_taxrate.typename = '中资大型银行' AND ed_taxrate.itemname = '超额存款准备金率'	ccks_macro
SELECT domesticloans AS domesticloans, fcdeposits AS fcdeposits FROM ed_chinamoneyandbanking AS ed_chinamoneyandbanking WHERE STRFTIME('%Y', enddate) >= '2005'	ccks_macro
SELECT a.avgaumtyperank AS avgaumtyperank FROM mf_fmretandscalerank AS a JOIN mf_personalinfo AS b ON a.personalcode = b.personalcode WHERE b.education = '本科'	ccks_fund
SELECT a.chinameabbr AS chinameabbr, b.leadername AS leadername, b.positiondescription AS positiondescription FROM lc_sharetransfer AS a JOIN lc_executivesholdings AS b ON a.companycode = b.companycode ORDER BY a.pctbeforetran DESC LIMIT 5	ccks_stock
SELECT b.type AS type, COUNT(*) AS _col_1 FROM mf_fundreturnrank AS a JOIN mf_fundarchives AS b ON a.innercode = b.innercode WHERE a.indexcycle = '六个月' AND a.fundreturnmean < 0 GROUP BY b.type	ccks_fund
SELECT b.chinesename AS chinesename, b.birthdate AS birthdate FROM mf_fmscaleanalysisn AS a JOIN mf_personalinfo AS b ON a.personalcode = b.personalcode ORDER BY a.bondfundnv DESC LIMIT 10	ccks_fund
SELECT otherforeignassets AS otherforeignassets, otherliability AS otherliability FROM ed_moneyauthoritybs AS ed_moneyauthoritybs	ccks_macro
SELECT a.returntyperank AS returntyperank FROM mf_fmretandscalerank AS a JOIN mf_personalinfo AS b ON a.personalcode = b.personalcode WHERE b.experiencetime > 10	ccks_fund
SELECT enddate AS enddate, netabroadassets AS netabroadassets FROM ed_chinamoneyandbanking AS ed_chinamoneyandbanking WHERE netabroadassets > 1000000	ccks_macro
SELECT enddate AS enddate, subjectsum AS subjectsum, yoy AS yoy FROM ed_newincreasingloan AS ed_newincreasingloan WHERE ed_newincreasingloan.reportperiod = '月份' AND subjectsum > 100000 AND STRFTIME('%Y', enddate) = STRFTIME('%Y', DATE('now', '-2 year'))	ccks_macro
SELECT chinameabbr AS chinameabbr FROM lc_sharesfloatingschedule AS lc_sharesfloatingschedule WHERE newmarketableashares <= 1000	ccks_stock
SELECT COUNT(*) AS _col_0 FROM lc_business AS a JOIN lc_stockarchives AS b ON a.companycode = b.companycode WHERE b.state = '江苏省' AND a.industryname = '农副食品加工业'	ccks_stock
SELECT industrialvalueadded AS industrialvalueadded FROM ed_industryproduction AS ed_industryproduction WHERE province = '上海' AND ed_industryproduction.statstandard = '全部工业企业' AND ed_industryproduction.reportperiod = '年度' AND STRFTIME('%Y', enddate) = '2000'	ccks_macro
SELECT a.chinameabbr AS chinameabbr FROM lc_sharesfloatingschedule AS a JOIN lc_exgindustry AS b ON a.companycode = b.companycode WHERE b.firstindustryname = '制造业' ORDER BY a.proportion1 DESC LIMIT 1	ccks_stock
SELECT fund AS fund FROM mf_awards AS mf_awards WHERE mf_awards.awardname = '中国股票型对冲基金奖提名' AND mf_awards.appraisalorg = '晨星资讯'	ccks_fund
SELECT enddate AS enddate, retailvalueofscgoods AS retailvalueofscgoods FROM ed_retailvalueofscgoods AS ed_retailvalueofscgoods WHERE ed_retailvalueofscgoods.reportarea = '全国' AND ed_retailvalueofscgoods.reportperiod = '年度' AND STRFTIME('%Y', enddate) > STRFTIME('%Y', DATE('now', '-3 year'))	ccks_macro
SELECT COUNT(*) AS _col_0 FROM mf_fmretscaleanalysis AS a JOIN mf_personalinfo AS b ON a.personalcode = b.personalcode WHERE a.totalaum > 100 AND b.education = '本科'	ccks_fund
SELECT b.type AS type, COUNT(*) AS _col_1 FROM mf_fundreturnrank AS a JOIN mf_fundarchives AS b ON a.innercode = b.innercode WHERE a.indexcycle = '一个月' AND a.fundreturn > 0 GROUP BY b.type	ccks_fund
SELECT b.education AS education, COUNT(*) AS _col_1 FROM mf_managerexperience AS a JOIN mf_personalinfo AS b ON a.personalcode = b.personalcode WHERE a.investadvisorname LIKE '富国基金%' AND a.incumbent = '是' GROUP BY b.education	ccks_fund
SELECT a.state AS state, COUNT(*) AS _col_1 FROM lc_stockarchives AS a JOIN lc_coconcept AS b ON a.companycode = b.companycode WHERE b.conceptname = '大飞机' GROUP BY a.state	ccks_stock
SELECT b.chinesename AS chinesename, b.totalfundnv AS totalfundnv, b.equityfundnv AS equityfundnv, b.hybridfundnv AS hybridfundnv FROM mf_personalinfo AS a JOIN mf_fmscaleanalysisn AS b ON a.personalcode = b.personalcode WHERE a.nationality <> '中国'	ccks_fund
SELECT fundmanager AS fundmanager, mf_awards.awardname AS awardname FROM mf_awards AS mf_awards WHERE mf_awards.appraisalorg = '证券时报'	ccks_fund
SELECT gdppercapita AS gdppercapita FROM ed_grossdomesticproduct AS ed_grossdomesticproduct	ccks_macro
SELECT enddate AS enddate, depositswithcentralbank AS depositswithcentralbank, cashinvault AS cashinvault FROM ed_otherdepositorycorpbs AS ed_otherdepositorycorpbs WHERE STRFTIME('%Y', enddate) >= '2008'	ccks_macro
SELECT a.chinameabbr AS chinameabbr FROM lc_stockarchives AS a JOIN lc_exgindustry AS b ON a.companycode = b.companycode WHERE a.state = '浙江省' AND b.firstindustryname = '科学研究和技术服务业'	ccks_stock
SELECT secucode AS secucode, chinameabbr AS chinameabbr FROM lc_coconcept AS lc_coconcept WHERE lc_coconcept.conceptname LIKE '%新能源%'	ccks_stock
SELECT a.secucode AS secucode, b.officeaddr AS officeaddr FROM lc_business AS a JOIN lc_stockarchives AS b ON a.companycode = b.companycode WHERE a.industryname = '零售业'	ccks_stock
SELECT chinameabbr AS chinameabbr FROM lc_sharesfloatingschedule AS lc_sharesfloatingschedule ORDER BY totalashares DESC LIMIT 10	ccks_stock
SELECT a.secucode AS secucode, a.chinameabbr AS chinameabbr FROM lc_coconcept AS a JOIN lc_stockarchives AS b ON a.companycode = b.companycode WHERE b.state = '安徽省' AND a.conceptname = '无人驾驶'	ccks_stock
SELECT ratioceiling AS ratioceiling FROM ed_taxrate AS ed_taxrate WHERE ed_taxrate.typename = '中资大型银行' AND ed_taxrate.itemname = '超额存款准备金率'	ccks_macro
SELECT a.secucode AS secucode, b.state AS state FROM lc_coconcept AS a JOIN lc_stockarchives AS b ON a.companycode = b.companycode WHERE a.conceptname = '元宇宙'	ccks_stock
SELECT ed_producerpiformp.reportperiod AS reportperiod, ed_producerpiformp.indextype AS indextype, indexvalue AS indexvalue FROM ed_producerpiformp AS ed_producerpiformp WHERE ed_producerpiformp.indexname = '冶金工业'	ccks_macro
SELECT enddate AS enddate, industrialoutputvalueap AS industrialoutputvalueap FROM ed_industryproduction AS ed_industryproduction WHERE ed_industryproduction.reportarea = '全国' AND ed_industryproduction.statstandard = '全部工业企业' AND ed_industryproduction.reportperiod = '期末累计'	ccks_macro
SELECT leadername AS leadername, shareamount AS shareamount FROM lc_executivesholdings AS lc_executivesholdings WHERE lc_executivesholdings.positiondescription LIKE '%副总裁%'	ccks_stock
SELECT b.secuabbr AS secuabbr, b.investfield AS investfield FROM mf_benchmarkgrowthrate AS a JOIN mf_fundarchives AS b ON a.innercode = b.innercode WHERE a.benchgrforthismonth < 0	ccks_fund
SELECT COUNT(*) AS _col_0 FROM lc_ipodeclaration AS lc_ipodeclaration WHERE lc_ipodeclaration.csrcindustryname = '银行业'	ccks_stock
SELECT a.firstindustryname AS firstindustryname FROM lc_exgindustry AS a JOIN lc_sharestru AS b ON a.companycode = b.companycode WHERE b.nonlistedshares > 200000000 GROUP BY a.firstindustryname HAVING COUNT(*) > 50	ccks_stock
SELECT a.state AS state, COUNT(*) AS _col_1 FROM lc_stockarchives AS a JOIN lc_coconcept AS b ON a.companycode = b.companycode WHERE b.conceptname = '石墨烯' GROUP BY a.state HAVING COUNT(*) > 1	ccks_stock
SELECT b.chinameabbr AS chinameabbr FROM lc_exgindustry AS a JOIN lc_sharestru AS b ON a.companycode = b.companycode WHERE a.firstindustryname = '建筑业' AND b.totalshares > 10000000000	ccks_stock
SELECT indexvalue AS indexvalue FROM ed_producerpiformp AS ed_producerpiformp WHERE ed_producerpiformp.indexname = '饮料制造业' AND ed_producerpiformp.reportperiod = '上年同期' AND STRFTIME('%Y', enddate) = STRFTIME('%Y', DATE('now', '-1 year'))	ccks_macro
SELECT lc_exgindustry.secondindustryname AS secondindustryname FROM lc_exgindustry AS lc_exgindustry WHERE lc_exgindustry.firstindustryname = '制造业' GROUP BY lc_exgindustry.secondindustryname ORDER BY COUNT(*) DESC LIMIT 1	ccks_stock
SELECT b.secondindustryname AS secondindustryname, COUNT(*) AS _col_1 FROM lc_sharesfloatingschedule AS a JOIN lc_exgindustry AS b ON a.companycode = b.companycode WHERE a.accumarketableashares > 5000 GROUP BY b.secondindustryname	ccks_stock
SELECT chinesename AS chinesename FROM mf_personalinfo AS mf_personalinfo WHERE mf_personalinfo.nationality <> '中国'	ccks_fund
