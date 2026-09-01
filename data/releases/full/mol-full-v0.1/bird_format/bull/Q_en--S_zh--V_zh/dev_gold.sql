select `基金类别描述`, count(*) from `公募基金最新收益率排名` where `指标周期` = '一个月' and `基金收益率(%)` > 0 group by `基金类别描述`	ccks_fund
select b.`证券简称`,b.`基金投资方向` from `公募基金最新基准收益率` as a join `公募基金概况` as b on a.`基金内部编码`=b.`基金内部编码`   where a.`本周以来基金基准增长率(%)`>0;	ccks_fund
select `股东名称` from `配股大股东认配状况`  where strftime('%Y', `首次信息发布时间`)='2017' group by  `股东名称` order by max(`实配股数(股)`) desc limit 1;	ccks_stock
select `股东名称` from `配股大股东认配状况` where `实配股数(股)`>500000 and `应配股数(股)`>500000;	ccks_stock
select a.`中文名称缩写`, a.`领导姓名`, a.`职位描述` from `公司报告期管理层持股` as a join `股东股权变动` as b on a.`公司代码` = b.`公司代码` order by b.`出让前持股比例` desc limit 5	ccks_stock
select `户均持股比例半年增长率(%)` from `股东户数` where `中文名称缩写`='兴业证券';	ccks_stock
select `毛利率` from `公司主营业务构成` where `中文名称缩写` ='西藏发展';	ccks_stock
select a.`中文名称缩写`, a.`股权被冻结质押股东名称`, a.`累计占冻结质押方持股数比例` from `股东股权冻结和质押统计` as a join `公司行业划分表` as b on a.`公司代码` = b.`公司代码` where b.`一级行业名称` = '房地产业'	ccks_stock
select a.`证券简称` from `公募基金经理(新)` as a join `公募基金经理基本资料` as b on a.`所属人员代码` = b.`所属人员编码` where b.`最高学历` = '本科'	ccks_fund
select b.`基金经理姓名`,b.`最高学历` from `基金经理规模统计(新)` as a join `公募基金经理基本资料` as b on a.`基金经理代码`=b.`所属人员编码` where a.`QDII管理规模(亿元)`>200;	ccks_fund
select `中文名称缩写` from `公司概况` where `总经理`='孙健';	ccks_stock
select `基金经理` , `基金名称` from `公募基金获奖情况` where `评奖单位` = '证券时报';	ccks_fund
select b.`证券简称`,b.`基金经理` from `公募基金债券组合明细` as a join `公募基金概况` as b on a.`基金内部编码`=b.`基金内部编码` where a.`债券简称`='兴业转债';	ccks_fund
select `中文名称缩写`, `实际控制人` from `公司实际控制人` where `所属基金/股票代码` like '00%';	ccks_stock
select b.`基金经理姓名`, a.`最大盈利(未填充)` from `基金经理历任收益风险指标(全)` as a join `公募基金经理基本资料` as b on a.`基金经理代码` = b.`所属人员编码` where b.`最高学历` = '博士' and a.`指标周期` = '一年';	ccks_fund
select b.`证券简称`,b.`基金经理` from `公募基金债券组合明细` as a join `公募基金概况` as b on a.`基金内部编码`=b.`基金内部编码` group by b.`证券简称` order by count(*) desc limit 10;	ccks_fund
select b.`中文名称缩写`,a.`研发投入合计(元)` from `公司研发投入与产出` as a join `公司概况` as b on a.`公司代码`=b.`公司代码`   where b.`省份`='浙江省' and strftime('%Y', a.`截止日期`)='2018';	ccks_stock
select b.`基金运作方式`, count(*) from `公募基金最新收益率排名` as a join `公募基金概况` as b on a.`基金内部编码` = b.`基金内部编码` where a.`指标周期` = '成立以来' and a.`同类基金收益率均值(%)` > 0 group by b.`基金运作方式`	ccks_fund
select a.`机构全称`,b.`股东名称` from `发行与上市中介机构` as a join `配股大股东认配状况` as b on a.`公司代码`=b.`公司代码` where a.`中文名称缩写`='天健集团';	ccks_stock
select count(*) from `公司主营业务构成` where `主营业务成本(元)` < 100000000;	ccks_stock
select a.`所属基金/股票代码` , b.`董事会秘书` , b.`董秘电话` from `概念所属公司表` as a join `公司概况` as b on a.`公司代码` = b.`公司代码` where a.`概念名称` ='东数西算' ;	ccks_stock
select `基金投资类型`, avg(`基金设立规模(份)`) from `公募基金概况` group by `基金投资类型`;	ccks_fund
select `中文名称缩写` from `公司实际控制人` where `实际控制人` = '赵马克';	ccks_stock
select `成交笔数(笔)` from `日行情表` where `所属基金/股票代码` = '601908';	ccks_stock
select a.`所属基金/股票简称` , b.`董事会秘书` , b.`董秘电话` from `概念所属公司表` as a join `公司概况` as b on a.`公司代码` = b.`公司代码` where a.`概念名称` ='3D玻璃' ;	ccks_stock
select `单位累计净值(元)` , `开放式基金单位基金净值日增长率` from  `公募基金净值` ;	ccks_fund
select distinct a.`中文名称缩写` from `公司分红` as a join `公司概况` as b on a.`公司代码` = b.`公司代码` where strftime('%Y', b.`公司成立日期`)>'2010' ;	ccks_stock
select count(*) from `公募基金最新收益率排名` where `基金收益率(%)` < 0 and `基金年化收益率(%)` < 0	ccks_fund
select a.`姓名` from `公募基金经理(新)` as a join `公募基金风险等级表` as b on a.`基金内部编码` = b.`基金内部代码` where b.`风险等级` = '中低' group by a.`姓名` having count(a.`证券简称`) > 5	ccks_fund
select `基金简称` from `公募基金最新基准收益率` where `三年基金基准增长率(%)`>0;	ccks_fund
select `中文名称缩写`, `日期` from `股票月度行情数据` where `市净率` < 5 and `市盈率TTM` > 200;	ccks_stock
select count(*) from `公募基金衍生指标_基金经理收益与规模同类分析` as a join `公募基金经理基本资料` as b on a.`基金经理代码` = b.`所属人员编码` where a.`总规模(亿元)` > 100 and b.`最高学历` = '本科'	ccks_fund
select count(*) from `公司主营业务构成`  where strftime('%Y', `截止日期`)='2020' and `毛利率` > 1	ccks_stock
select `基金管理人简称` from `公募基金管理人概况` where strftime('%Y', `成立日期`)>'2010';	ccks_fund
select a.`所属基金/股票简称` , b.`董事会秘书` from `概念所属公司表` as a join `公司概况` as b on a.`公司代码` = b.`公司代码` where a.`概念名称` ='大飞机' ;	ccks_stock
select b.`最高学历` from `基金经理历任收益风险指标(全)` as a join `公募基金经理基本资料` as b on a.`基金经理代码` = b.`所属人员编码` where a.`年化阿尔法(未填充)` > 0.2 group by b.`最高学历` having count(*) > 5	ccks_fund
select `基金管理人简称` from `公募基金管理人概况` where `法人代表` like '周%';	ccks_fund
select a.`证券简称` from `公募基金风险等级表` as a join `公募基金概况` as b on a.`基金内部代码` = b.`基金内部编码` where a.`风险等级` = '中低' and b.`基金运作方式` = '开放式'	ccks_fund
select b.`基金经理姓名`,b.`背景介绍` from `基金经理规模统计(新)` as a join `公募基金经理基本资料` as b on a.`基金经理代码`=b.`所属人员编码` where a.`股票型基金数量(只)`>5;	ccks_fund
select `主营业务收入(元)` , `主营业务收入同比` from `公司主营业务构成` where `主营业务收入同比` > 0 and `中文名称缩写` ='古井贡酒';	ccks_stock
select a.`基金经理姓名`, b.`最高学历` from `公募基金衍生指标_基金经理收益与规模同类分析` as a join `公募基金经理基本资料` as b on a.`基金经理代码` = b.`所属人员编码` where a.`时间区间` = '今年以来' order by a.`平均规模(亿元)` desc limit 3	ccks_fund
select `公司中文名称` from `公司主营业务构成`  where strftime('%Y', `截止日期`)='2020' and `毛利率` > 1	ccks_stock
select `中文名称缩写`, `送股比例(10送X)` from `公司分红` where `中文名称缩写` = '京基智农' or `中文名称缩写` = '天健集团';	ccks_stock
select `股东名称` from `配股大股东认配状况` where `应配股数(股)`>2000000;	ccks_stock
select `股东名称`,`实配股数(股)` from `配股大股东认配状况` where `中文名称缩写`='同济科技';	ccks_stock
select `组织形式`, count(*) from `公募基金管理人概况` group by `组织形式` order by count(*) asc;	ccks_fund
select `实配股数(股)` from `配股大股东认配状况` where `股东名称`='杉杉集团';	ccks_stock
select `基金管理人简称` from `公募基金管理人概况` order by `注册资本(元)` desc limit 1;	ccks_fund
select a.`证券简称` from `公募基金风险等级表` as a join `公募基金概况` as b on a.`基金内部代码` = b.`基金内部编码` where a.`风险等级` = '中低' and b.`基金投资类型`= '成长型—稳健成长型'	ccks_fund
select `公司中文名称`, `股东投资金额` from `企业之间参股情况`  where `中文名称缩写` = '航天发展' and strftime('%Y', `截止日期`)='2019' and strftime('%m', `截止日期` )='5'	ccks_stock
select a.`机构全称`,a.`法人代表`,b.`股东名称`,b.`实配股数(股)` from `发行与上市中介机构` as a join `配股大股东认配状况` as b on a.`公司代码`=b.`公司代码` where a.`中文名称缩写`='东阿阿胶';	ccks_stock
select `户均持股数半年增长率(%)` from `股东户数` where `中文名称缩写`='工商银行';	ccks_stock
select count(*) from `公募基金风险等级表` as a join `公募基金概况` as b on a.`基金内部代码` = b.`基金内部编码` where a.`风险等级` = '中' and b.`基金投资类型`= '综合型'	ccks_fund
select b.`证券简称`,b.`基金经理` from `公募基金债券组合明细` as a join `公募基金概况` as b on a.`基金内部编码`=b.`基金内部编码` where a.`债券简称`='21国债01' order by a.`持有数量(张)` desc limit 1;	ccks_fund
select `省份`,`所属城市`,`A股证券代码` from `公司概况` where `中文名称缩写`='天娱数科';	ccks_stock
select b.`证券简称`,b.`基金经理`,b.`风险收益特征` from `公募基金最新基准收益率` as a join `公募基金概况` as b on a.`基金内部编码`=b.`基金内部编码` order by a.`本周以来基金基准增长率(%)` desc limit 10;	ccks_fund
select `基金简称` from `公募基金最新基准收益率` where `两年基金基准增长率(%)`<0;	ccks_fund
select `主营业务利润(元)`, `主营业务成本(元)` from `公司主营业务构成`  where strftime('%Y', `截止日期`) = strftime('%Y', DATE('now', '-1 year')) and `所属基金/股票代码` ='000822';	ccks_stock
select `基金管理人` from `公募基金概况` where `基金托管人`='中信银行股份有限公司' group by `基金管理人` order by count(*) desc limit 1;	ccks_fund
select `主营业务收入同比` from `公司主营业务构成` where `主营业务收入同比` < 0 and `所属基金/股票代码` ='000822' and strftime('%Y', `截止日期`)>'2020'	ccks_stock
select b.`中文名称缩写`, a.`总经理` from `公司概况` as a join `自由流通股本` as b on a.`公司代码` = b.`公司代码` where b.`A股总股本(股)` > 10000000000	ccks_stock
select `单位净值(元)` , `单位基金净值周增长率` from  `公募基金净值` ;	ccks_fund
select b.`风险等级`, count(a.`证券简称`) from `公募基金经理(新)` as a join `公募基金风险等级表` as b on a.`基金内部编码` = b.`基金内部代码` where a.`任职期间基金净值增长率` > 0 group by b.`风险等级`	ccks_fund
select `债券型基金数量(只)`,`债券型管理规模(亿元)` from `基金经理规模统计(新)` where `基金经理姓名`='陈龙';	ccks_fund
select `基金简称` from `公募基金最新基准收益率` where `本周以来基金基准增长率(%)`>5;	ccks_fund
select `户均持股比例季度增长率(%)` from `股东户数`  where strftime('%Y', `截止日期`)='2020' and `中文名称缩写`='金禾实业';	ccks_stock
select a.`证券简称`, a.`风险收益特征` from `公募基金概况` as a join `公募基金风险等级表` as b on a.`基金内部编码` = b.`基金内部代码` where b.`风险等级` = '中'	ccks_fund
select  `所属基金/股票代码`  from `公司主营业务构成`  where strftime('%Y', `截止日期`) > strftime('%Y', DATE('now', '-3 year')) and `毛利率` >1;	ccks_stock
select `基金简称` from `公募基金最新基准收益率` where `十年基金基准增长率(%)`>200;	ccks_fund
select `基金管理人`,count(*) from `公募基金概况` where `基金类别`='混合型' group by `基金管理人` order by count(*) desc limit 1;	ccks_fund
select `基金管理人简称` from `公募基金管理人概况` where `注册资本(元)` > 200000000 and strftime('%Y', `成立日期`)>'2015';	ccks_fund
select count(*) from `股东股权冻结和质押` where `接受股权质押方` ='中国进出口银行';	ccks_stock
select `法人代表` from `公募基金管理人概况` where `基金管理人简称` = '中银基金';	ccks_fund
select `主要业务` from `公司经营范围与行业变更` where `中文名称缩写` ='深科技'	ccks_stock
select a.`所属基金/股票代码`, b.`法人代表` , b.`公司办公地址` from `概念所属公司表` as a join `公司概况` as b on a.`公司代码` = b.`公司代码` where a.`概念名称` ='边缘计算' ;	ccks_stock
select `中文名称缩写`,`A股证券代码` from `公司概况` where `省份`='新疆维吾尔自治区';	ccks_stock
select a.`机构全称`,b.`A股证券简称` from `发行与上市中介机构` as a join `公司概况` as b on a.`公司代码`=b.`公司代码`  where b.`中文名称缩写`='武汉控股';	ccks_stock
select b.`基金运作方式`, count(*) from `公募基金最新收益率排名` as a join `公募基金概况` as b on a.`基金内部编码` = b.`基金内部编码` where a.`指标周期` = '六个月' and a.`同类基金收益率均值(%)` < 0 group by b.`基金运作方式`	ccks_fund
select a.`证券简称` from `公募基金风险等级表` as a join `公募基金概况` as b on a.`基金内部代码` = b.`基金内部编码` where a.`风险等级` = '中高' and b.`基金运作方式` = '开放式'	ccks_fund
select `发行量下限(不少于)(股)`, `发行量上限(不超过)(股)` from `A股增发` where `所属基金/股票代码` = '002305';	ccks_stock
select `基金简称` from `公募基金最新收益率排名` where `指标周期` = '六个月' order by `基金收益率(%)` desc limit 1	ccks_fund
select `利息净支出` from `利润分配表附注_财务费用` where strftime('%Y', `截止日期`)<'2017' and `中文名称缩写` = '八方股份';	ccks_stock
select `中文名称缩写`, `送股比例(10送X)` from `公司分红` order by `送股比例(10送X)` desc limit 1;	ccks_stock
select `中文名称缩写` from `公司分红` order by `送股比例(10送X)` desc limit 1;	ccks_stock
select `股东名称` from `配股大股东认配状况` where `中文名称缩写`='广州浪奇';	ccks_stock
select a.`姓名`, a.`任职期间基金净值增长率` from `公募基金经理(新)` as a join `公募基金概况` as b on a.`基金内部编码` = b.`基金内部编码` where b.`证券市场` = '上海期货交易所'	ccks_fund
select `中文名称缩写`, `实际控制人` from `公司实际控制人` where `所属基金/股票代码` like '6%';	ccks_stock
select `股东名称`, `股东持股数量` from `企业之间参股情况` where `中文名称缩写` ='农发种业' and strftime('%Y', `截止日期`)<'2019';	ccks_stock
select count(*)  from `公司主营业务构成`  where strftime('%Y', `截止日期`) > strftime('%Y', DATE('now', '-3 year')) and `毛利率` >1;	ccks_stock
select b.`背景介绍` from `公募基金经理(新)` as a join `公募基金经理基本资料` as b on a.`所属人员代码` = b.`所属人员编码` where `任职期间基金净值增长率` < 0 and `任职天数` > 200	ccks_fund
select a.`基金经理姓名`, b.`最高学历`, b.`证券从业经历(年)` from `公募基金衍生指标_基金经理收益与规模同类分析` as a join `公募基金经理基本资料` as b on a.`基金经理代码` = b.`所属人员编码` where a.`月平均收益率(%)` > 0	ccks_fund
select `风险等级` from `公募基金风险等级表` where `证券简称` = '国金50'	ccks_fund
select `基金管理人简称`, `成立日期` from `公募基金管理人概况` where `基金管理人简称` = '大成基金' or `基金管理人简称` = '兴银基金';	ccks_fund
select `省份`,`所属城市`,`公司成立日期` from `公司概况` where `中文名称缩写`='同仁堂';	ccks_stock
select b.`基金经理`,a.`市值(元)` from `公募基金债券组合明细` as a join `公募基金概况` as b on a.`基金内部编码`=b.`基金内部编码` where a.`债券简称`='博世转债';	ccks_fund
select `户均持股比例季度增长率(%)` from `股东户数`  where strftime('%Y', `截止日期`)='2020' and round(strftime('%m',`截止日期`)/3.0 + 0.495)=2 and `中文名称缩写`='京基智农';	ccks_stock
select `中文名称缩写` from `股票月度行情数据`  where `市净率` < 1 and strftime('%Y', `日期`) = strftime('%Y', date()) and strftime('%m', `日期`)='1';	ccks_stock
select `六个月基金基准增长率(%)` from `公募基金最新基准收益率` where `基金简称`='易方达中盘ETF';	ccks_fund
select b.`基金经理姓名`,b.`出生日期` from `基金经理规模统计(新)` as a join `公募基金经理基本资料` as b on a.`基金经理代码`=b.`所属人员编码` order by a.`债券型管理规模(亿元)` desc limit 10;	ccks_fund
select a.`中文名称缩写` from `公司研发投入与产出` as a join  `公司概况` as b on a.`公司代码`=b.`公司代码`  where strftime('%Y', a.`截止日期`)=strftime('%Y', DATE('now', '-1 year')) and b.`省份`='浙江省' and `研发投入合计(元)`>100000000;	ccks_stock
select `基金管理人` from `公募基金概况` where `基金托管人`='北京银行股份有限公司';	ccks_fund
select `证券简称`,`基金经理` from `公募基金概况` where `基金管理人`='合煦智远基金管理有限公司' and `基金类别`='债券型';	ccks_fund
select b.`证券简称`,b.`基金经理` from `公募基金最新基准收益率` as a join `公募基金概况` as b on a.`基金内部编码`=b.`基金内部编码` order by a.`一年基金基准增长率(%)` desc limit 10	ccks_fund
select `公司中文名称`,`A股证券代码` from `公司概况` where `中文名称缩写`='德美化工';	ccks_stock
select a.`基金简称`,b.`基金投资范围` from `公募基金最新基准收益率` as a join `公募基金概况` as b on a.`基金内部编码`=b.`基金内部编码`   where a.`本日基金基准增长率(%)`>0;	ccks_fund
select count(*) from `限售股票解禁时间表` where `本次新增可售A股占上期末已流通A股比例(%)` < 20	ccks_stock
select `基金简称` from `公募基金最新基准收益率` order by `三个月基金基准增长率(%)` desc limit 10;	ccks_fund
select a.`基金经理姓名`, b.`最高学历` from `公募基金衍生指标_基金经理收益与规模同类分析` as a join `公募基金经理基本资料` as b on a.`基金经理代码` = b.`所属人员编码` where a.`平均规模(亿元)` < 20 and a.`基金类别描述` = '股票型'	ccks_fund
select `户均持股比例季度增长率(%)` from `股东户数`  where strftime('%Y', `截止日期`)='2020' and round(strftime('%m',`截止日期`)/3.0 + 0.495)=4 and `中文名称缩写`='京基智农';	ccks_stock
select `最高学历`, `性别`, count(*) from `公募基金经理基本资料` group by `最高学历`, `性别`;	ccks_fund
select `基金管理人`,count(*) from `公募基金概况` where `基金投资风格`='行业股票-金融地产' group by `基金管理人`;	ccks_fund
select `股东名称`, `所属基金/股票代码` from `企业之间参股情况`  where `股东投资金额` > 10000000 and strftime('%Y', `截止日期`) > strftime('%Y', DATE('now', '-2 year')) ;	ccks_stock
select a.`基金简称`,a.`本日基金基准增长率(%)` from `公募基金最新基准收益率` as a join `公募基金概况` as b on a.`基金内部编码`=b.`基金内部编码`  where b.`基金运作方式`='LOF';	ccks_fund
select `公司中文名称` from `企业之间参股情况`  where strftime('%Y', `截止日期`)='2010' and strftime('%m', `截止日期` )='5' and `股东投资金额` > 100000000	ccks_stock
select `股东名称` from `配股大股东认配状况` where `所属基金/股票代码`='000686';	ccks_stock
select b.`证券简称`,b.`基金经理` from `公募基金债券组合明细` as a join `公募基金概况` as b on a.`基金内部编码`=b.`基金内部编码` where a.`债券简称`='百润转债' order by a.`市值(元)` desc limit 1;	ccks_fund
select b.`最高学历` from `基金经理历任收益风险指标(全)` as a join `公募基金经理基本资料` as b on a.`基金经理代码` = b.`所属人员编码` where a.`年化索提诺比率(未填充)` > 2 group by b.`最高学历` having count(*) > 10	ccks_fund
select a.`总管理规模同类均值(亿元)` from `公募基金衍生指标_基金经理最新收益与规模排名` as a join `公募基金经理基本资料` as b on a.`基金经理代码` = b.`所属人员编码` where b.`最高学历` = '本科'	ccks_fund
select `中文名称缩写` from `股东户数` where `户均持股数季度增长率(%)`>5;	ccks_stock
select `主要业务` , `行业名称` from `公司经营范围与行业变更` where `中文名称缩写` ='浙大网新'	ccks_stock
select `股东名称` from `配股大股东认配状况` where `所属基金/股票代码`='600165';	ccks_stock
select a.`姓名`, a.`任职期间基金净值增长率` from `公募基金经理(新)` as a join `公募基金风险等级表` as b on a.`基金内部编码` = b.`基金内部代码` where b.`风险等级` = '中高'	ccks_fund
select `送股比例(10送X)`, `派现(含税/人民币元)` from `公司分红` where `所属基金/股票代码` ='000552';	ccks_stock
select b.`基金运作方式`, count(*) from `公募基金净值最新区间表现` as a join `公募基金概况` as b on a.`证券内部编码` = b.`基金内部编码` where a.`一年回报率(%)` > 20 group by b.`基金运作方式`;	ccks_fund
select a.`机构全称`,b.`股东名称` from `发行与上市中介机构` as a join `配股大股东认配状况` as b on a.`公司代码`=b.`公司代码` where a.`中文名称缩写`='天健集团';	ccks_stock
select `基金简称` from `公募基金最新基准收益率` where `七年基金基准增长率(%)`>200;	ccks_fund
select b.`证券简称`,b.`基金经理`,a.`六个月基金基准增长率(%)` from `公募基金最新基准收益率` as a join `公募基金概况` as b on a.`基金内部编码`=b.`基金内部编码` where a.`六个月基金基准增长率(%)`>0;	ccks_fund
select count(*) from `公司主营业务构成` where `中文名称缩写`='中国石化' and `主营业务收入(元)` > 200000000000 ;	ccks_stock
select count(*) from `企业之间参股情况`  where strftime('%Y', `截止日期`)='2020' and strftime('%m', `截止日期` )='3' and `股东投资金额` > 100000000	ccks_stock
select count(*) from `公募基金概况`  where strftime('%Y', `存续期起始日`)='2021' and strftime('%m', `存续期起始日`)='5' and `基金类别`='基础设施证券投资基金';	ccks_fund
select b.`基金经理`,b.`基金管理人`,a.`股票型管理规模(亿元)` from `基金经理规模统计(新)` as a join `公募基金概况` as b on a.`基金经理姓名`=b.`基金经理` where a.`股票型管理规模(亿元)`>50;	ccks_fund
select b.`证券简称`,b.`基金经理`,b.`收益分配原则` from `公募基金最新基准收益率` as a join `公募基金概况` as b on a.`基金内部编码`=b.`基金内部编码` order by a.`一周基金基准增长率(%)` desc limit 10;	ccks_fund
select `基金管理人`,count(*) from `公募基金概况` where `基金性质`='QDII基金' and `基金投资类型`='优化指数型' group by `基金管理人` order by count(*) desc limit 1;	ccks_fund
select b.`证券简称`,b.`基金投资目标` from `公募基金最新基准收益率` as a join `公募基金概况` as b on a.`基金内部编码`=b.`基金内部编码`   order by a.`本周以来基金基准增长率(%)` desc limit 10;	ccks_fund
select a.`中文名称缩写` from `公司主营业务构成` as a join `公司概况` as b on a.`公司代码` = b.`公司代码`  where b.`省份` ='浙江省' and strftime('%Y', `截止日期`)='2020' order by  a.`主营业务成本(元)` limit 1;	ccks_stock
select `基金简称` from `公募基金最新基准收益率` order by `本季度以来基金基准增长率(%)` desc limit 10;	ccks_fund
select b.`基金经理姓名`,b.`性别`,b.`最高学历` from `基金经理规模统计(新)` as a join `公募基金经理基本资料` as b on a.`基金经理代码`=b.`所属人员编码` where a.`股票型管理规模(亿元)`>100;	ccks_fund
select `中文名称缩写`, `主要业务` from `公司经营范围与行业变更` where `中文名称缩写` ='南华生物' or `中文名称缩写` ='浙大网新'	ccks_stock
select `本月以来回报率(%)`, `一个月回报率(%)` from `公募基金净值最新区间表现` where `基金简称` = '天弘恒享';	ccks_fund
select `法人代表`,`总经理` from `公司概况` where `A股证券代码`='600135';	ccks_stock
select a.`中文名称缩写`, a.`所属城市`, a.`总经理` from `公司概况` as a join `公司行业划分表` as b on a.`公司代码` = b.`公司代码` where b.`一级行业名称` = '制造业'	ccks_stock
select `公司中文名称`, `中文名称缩写` from `股份回购`  where strftime('%Y', `预案公布日`) > strftime('%Y', DATE('now', '-2 year'));	ccks_stock
select b.`基金经理`,b.`基金管理人` from `公募基金债券组合明细` as a join `公募基金概况` as b on a.`基金内部编码`=b.`基金内部编码` where a.`债券简称`='20国开08' order by a.`市值(元)` desc limit 1;	ccks_fund
select `中文名称缩写` from `公司概况` where `总经理` like '刘%';	ccks_stock
select `主营业务收入(元)`, `主营业务利润(元)` from `公司主营业务构成`  where strftime('%Y', `截止日期`) = strftime('%Y', DATE('now', '-1 year')) and `所属基金/股票代码` ='000752';	ccks_stock
select a.`基金简称`,b.`基金经理` from `公募基金最新基准收益率` as a  join `公募基金概况` as b on a.`基金内部编码`=b.`基金内部编码`  where a.`本日基金基准增长率(%)`<0;	ccks_fund
select `法人代表`,`总经理` from `公司概况` where `中文名称缩写`='维宏股份';	ccks_stock
select `基金简称`,`一年基金基准增长率(%)` from `公募基金最新基准收益率`;	ccks_fund
select `证券简称`,`证券代码`,`基金管理人` from `公募基金概况` where `基金经理`='张坤';	ccks_fund
select `中文名称缩写`, `实际控制人` from `公司实际控制人` where `所属基金/股票代码` like '300%' order by `所属基金/股票代码`;	ccks_stock
select a.`最高学历`, count(*) from `公募基金经理基本资料` as a join `基金经理规模统计(新)` as b on a.`所属人员编码` = b.`基金经理代码` where b.`总管理规模(亿元)` > 100 group by a.`最高学历`;	ccks_fund
select `股东名称`, `所属基金/股票代码`, `股东投资金额` from `企业之间参股情况`  where `股东投资金额` > 10000000 and strftime('%Y', `截止日期`) = strftime('%Y', DATE('now', '-2 year')) ;	ccks_stock
select `中文名称缩写` from `股东户数` where `户均持股比例(%)`<10;	ccks_stock
select b.`证券简称`,b.`基金运作方式` from `公募基金最新基准收益率` as a join `公募基金概况` as b on a.`基金内部编码`=b.`基金内部编码`  where a.`一个月基金基准增长率(%)`<0;	ccks_fund
select b.`最高学历`, count(*) from `基金经理历任收益风险指标(全)` as a join `公募基金经理基本资料` as b on a.`基金经理代码` = b.`所属人员编码` where a.`年化阿尔法(未填充)` > 0.5 group by b.`最高学历`	ccks_fund
select b.`证券简称`,b.`基金管理人` from `公募基金最新基准收益率` as a join `公募基金概况` as b on a.`基金内部编码`=b.`基金内部编码`  where a.`一个月基金基准增长率(%)`>8;	ccks_fund
select `客服热线` from `公募基金管理人概况` where `基金管理人简称` = '方正富邦基金';	ccks_fund
select b.`基金经理`,b.`基金管理人` from `基金经理规模统计(新)` as a join `公募基金概况` as b on a.`基金经理姓名`=b.`基金经理` order by a.`旗下基金总数(只)` desc limit 1;	ccks_fund
select `股东名称`, `股东持股数量` from `企业之间参股情况`  where `所属基金/股票代码` ='000948' and strftime('%Y', `截止日期`) > strftime('%Y', DATE('now', '-3 year'));	ccks_stock
select a.`所属基金/股票代码` , b.`法人代表` , b.`董事会秘书` from `概念所属公司表` as a join `公司概况` as b on a.`公司代码` = b.`公司代码` where a.`概念名称` ='工业互联网' ;	ccks_stock
select `基金经理姓名` from `公募基金经理基本资料`  where `国籍` = '缅甸' and strftime('%Y', `证券从业日期`)='2015';	ccks_fund
select `中文名称缩写` from `公司主营业务构成`  where strftime('%Y', `截止日期`) = strftime('%Y', DATE('now', '-1 year')) order by  `主营业务收入(元)` desc limit 1;	ccks_stock
select b.`基金经理姓名`, b.`总管理规模(亿元)`, b.`股票型管理规模(亿元)`, b.`混合型管理规模(亿元)` from `公募基金经理基本资料` as a join `基金经理规模统计(新)` as b on a.`所属人员编码` = b.`基金经理代码` where a.`国籍` != '关岛';	ccks_fund
select `股东名称`,`应配股数(股)`,`实配股数(股)` from `配股大股东认配状况` where `中文名称缩写`='双节电气';	ccks_stock
select b.`证券简称`,b.`基金投资目标` from `公募基金最新基准收益率` as a join `公募基金概况` as b on a.`基金内部编码`=b.`基金内部编码`  order by a.`一个月基金基准增长率(%)` desc limit 10;	ccks_fund
select `证券简称` from `公募基金概况` where `基金类别`='其他型' and `基金投资风格`='配置型';	ccks_fund
select `基金管理人简称` from `公募基金管理人概况` where `注册资本(元)` < 1000000000;	ccks_fund
select `所属基金/股票代码`, `实际控制人` from `公司实际控制人` where `所属基金/股票代码` = '600881' or `所属基金/股票代码` = '601158';	ccks_stock
select `基金简称`,`本日基金基准增长率(%)` from `公募基金最新基准收益率` where `本日基金基准增长率(%)`>0 order by `本日基金基准增长率(%)` desc;	ccks_fund
select b.`中文名称缩写`, b.`实际控制人` from `公司概况` as a join `公司实际控制人` as b on a.`公司代码` = b.`公司代码` where a.`所属城市` = '杭州市';	ccks_stock
select count(*) from `公募基金概况`  where `证券市场`='上海黄金交易所' and `基金运作方式`='开放式' and strftime('%Y', `上市日期`)='2021';	ccks_fund
select b.`基金经理`,a.`债券简称` from `公募基金债券组合明细` as a join `公募基金概况` as b on a.`基金内部编码`=b.`基金内部编码` where a.`基金简称`='富国天丰';	ccks_fund
select `经营范围-兼营` from `公司经营范围与行业变更` lb where `中文名称缩写` ='深科技'	ccks_stock
select `证券代码` from `公募基金概况` where `证券简称`='易方达人工智能ETF';	ccks_fund
select b.`基金运作方式`, count(*) from `公募基金最新收益率排名` as a join `公募基金概况` as b on a.`基金内部编码` = b.`基金内部编码` where a.`指标周期` = '一年' and a.`基金收益率(%)` < 0 group by b.`基金运作方式`	ccks_fund
select `股权被冻结质押股东名称`, `累计冻结质押股数(股)` from `股东股权冻结和质押统计` where `中文名称缩写` = '新天然气' and `累计占冻结质押方持股数比例` > 0.8	ccks_stock
select count(*) from `公司概况` as a join `自由流通股本` as b on a.`公司代码` = b.`公司代码` where a.`省份` = '江苏省' and b.`自由流通比例(归档后)(%)` = 100	ccks_stock
select `股东名称`, `股东持股比例` from `企业之间参股情况` where `中文名称缩写` = '诺德股份';	ccks_stock
select `中文名称缩写` from `利润分配表附注_财务费用` order by `利息净支出` asc	ccks_stock
select `股东名称`,`应配股数(股)` from `配股大股东认配状况` where `中文名称缩写`='天山股份';	ccks_stock
select `股东名称` from `配股大股东认配状况` where `所属基金/股票代码`='600797';	ccks_stock
select `主营业务收入(元)` , `主营业务成本(元)`, `主营业务利润(元)` from `公司主营业务构成`  where strftime('%Y', `截止日期`) = strftime('%Y', DATE('now', '-1 year')) and `所属基金/股票代码` ='000822';	ccks_stock
select `A股证券简称`,`A股证券代码` from `公司概况` where `A股证券代码`='600190';	ccks_stock
select `主要业务`, `行业名称` from `公司经营范围与行业变更` where `中文名称缩写` = '精研科技'	ccks_stock
select b.`中文名称缩写` from `公司研发投入与产出` as a join `公司概况` as b on a.`公司代码`=b.`公司代码`  where b.`省份`='广东省' order by a.`研发人员数量` desc limit 50;	ccks_stock
select `基金简称`,`本周以来基金基准增长率(%)` from `公募基金最新基准收益率` where `本周以来基金基准增长率(%)`<0 order by `本周以来基金基准增长率(%)`;	ccks_fund
select a.`基金简称` from `公募基金最新收益率排名` as a join `公募基金概况` as b on a.`基金内部编码` = b.`基金内部编码` where b.`基金类别` = '债券型' and a.`同类基金收益率均值(%)` > 0	ccks_fund
select b.`证券简称`,b.`基金经理` from `公募基金债券组合明细` as a join `公募基金概况` as b on a.`基金内部编码`=b.`基金内部编码` group by b.`证券简称` order by count(*) desc limit 1;	ccks_fund
select b.`基金经理`,a.`债券简称`,a.`市值(元)` from `公募基金债券组合明细` as a join `公募基金概况` as b on a.`基金内部编码`=b.`基金内部编码` where a.`基金简称`='富国天丰';	ccks_fund
select b.`证券简称`,b.`基金经理` from `公募基金债券组合明细` as a join `公募基金概况` as b on a.`基金内部编码`=b.`基金内部编码` where a.`债券简称`='南银转债';	ccks_fund
select `承销数量(股)` from `发行与上市中介机构` where `中文名称缩写`='天健集团';	ccks_stock
select `中文名称缩写` from `股东户数` where `户均持股数季度增长率(%)`<5;	ccks_stock
select b.`证券简称`,b.`基金经理` from `公募基金债券组合明细` as a join `公募基金概况` as b on a.`基金内部编码`=b.`基金内部编码` where a.`债券简称`='杭银转债';	ccks_fund
select a.`证券简称` from `公募基金风险等级表` as a join `公募基金概况` as b on a.`基金内部代码` = b.`基金内部编码` where a.`风险等级` = '中' and b.`基金类别`= '债券型'	ccks_fund
select `中文名称缩写`,`所属区县` from `公司概况` where `所属城市`='长春市';	ccks_stock
select a.`姓名`, b.`最高学历` from `公募基金经理(新)` as a join `公募基金经理基本资料` as b on a.`所属人员代码` = b.`所属人员编码` order by a.`任职天数` desc limit 1	ccks_fund
select a.`中文名称缩写`, a.`总经理`, a.`法人代表` from `公司概况` as a join `公司实际控制人` as b on a.`公司代码` = b.`公司代码` where b.`国籍描述` = '美国';	ccks_stock
select `股东名称`,`实配股数(股)` from `配股大股东认配状况` where `所属基金/股票代码`='600110';	ccks_stock
select `组织形式`, count(*) from `公募基金管理人概况` group by `组织形式`;	ccks_fund
select a.`机构全称`,a.`承销金额(元)`,b.`股东名称`,b.`实配股数(股)` from `发行与上市中介机构` as a join `配股大股东认配状况` as b on a.`公司代码`=b.`公司代码` where a.`中文名称缩写`='天健集团';	ccks_stock
select `股东名称` from `企业之间参股情况`  where `股东持股数量` > 10000000 and strftime('%Y', `截止日期`)='2020' ;	ccks_stock
select `基金简称` from `公募基金最新收益率排名` where `指标周期` = '今年以来' and `基金收益率(%)` < 0	ccks_fund
select `准备金存款`  from `其他存款性公司资产负债表` ;	ccks_macro
select `股权被冻结质押股东名称` from `股东股权冻结和质押统计` where `中文名称缩写` = '哈尔斯' or `中文名称缩写` = '京运通'	ccks_stock
select `截止日期`, `对政府债权(净)` , `对中央银行债权` from `其他存款性公司资产负债表`  where strftime('%Y', `截止日期`) = strftime('%Y', DATE('now', '-1 year')) and round(strftime('%m',`截止日期`)/3.0 + 0.495) = 4;	ccks_macro
select count(*) from `公募基金最新收益率排名` where `基金代码` like '16%' and `基金收益率(%)` > 0	ccks_fund
select `基金经理姓名` from `基金经理规模统计(新)` where `股票型管理规模(亿元)` > 200;	ccks_fund
select `基金管理人` from `公募基金概况` where `基金投资类型`='指数型' group by `基金管理人` order by count(*) desc limit 1;	ccks_fund
select `成交量(股)`, `成交金额(元)` from `日行情表` where `中文名称缩写` = '科思股份';	ccks_stock
select `基金经理姓名` from `公募基金经理基本资料` where `基金经理姓名` like '王%' and `证券从业经历(年)` > 10;	ccks_fund
select `所属基金/股票代码`, `中文名称缩写` from `公司分红` where `送股比例(10送X)` is not null;	ccks_stock
select `配股年度`, `每股配股价格(元)`, `募集资金总额(元)` from `A股配股` where `中文名称缩写` = '四川美丰';	ccks_stock
select `基金名称` from `公募基金获奖情况` where `基金公司名称` ='鹏华基金管理有限公司';	ccks_fund
select count(*) from `公募基金费率(新)` where `适用客户类型` ='养老金客户';	ccks_fund
select b.`基金运作方式` from `公募基金净值最新区间表现` as a join `公募基金概况` as b on a.`证券内部编码` = b.`基金内部编码` group by b.`基金运作方式` order by avg(a.`日回报率(%)`) desc limit 1;	ccks_fund
select `单位累计净值(元)` from `公募基金净值`  where `基金简称` = '国投瑞盈' and strftime('%Y', `截止日期`) = strftime('%Y', date());	ccks_fund
select `保荐机构` from `A股发行申报企业信息` where `中文名称缩写`='红塔证券';	ccks_stock
select `所属行业/领域` from `A股发行申报企业信息` where strftime('%Y', `截止日期`)>'2017' group by `所属行业/领域` order by count(*) desc limit 1;	ccks_stock
select `指数` from `工业品出厂价格指数`  where `指数名称` ='金属制品业' and `数据统计期间` ='上年同期' and strftime('%Y', `截止日期`) = strftime('%Y', DATE('now', '-1 year')) ;	ccks_macro
select `五年回报率(%)` from `公募基金净值最新区间表现` ;	ccks_fund
select `最高比率(%)` from `税率表` where `税率类别` ='农村信用社' and `税率项目` ='超额存款准备金率';	ccks_macro
select b.`中文名称缩写`, a.`一级行业名称` from `公司行业划分表` as a join `公司股本结构变动` as b on a.`公司代码` = b.`公司代码` where b.`总股本(股)` > 10000000000	ccks_stock
select `国内生产总值(百万元)`, `第一产业(百万元)`, `第二产业(百万元)`, `第三产业(百万元)` from `国内生产总值` ;	ccks_macro
select `证券从业日期` from `公募基金经理基本资料` where `基金经理姓名` = '柳军';	ccks_fund
select b.`领导姓名`, b.`中文名称缩写` from `公司概况` as a join `公司报告期管理层持股` as b on a.`公司代码` = b.`公司代码` where a.`省份` = '浙江省' and b.`职位描述` like '%副总经理%'	ccks_stock
select `概念名称` from `概念所属公司表` where `所属基金/股票代码` ='002354';	ccks_stock
select a.`中文名称缩写` , b.`省份`, b.`所属城市` from `公司经营范围与行业变更` as a join `公司概况` as b on a.`公司代码` = b.`公司代码` where a.`行业名称` ='资本市场服务';	ccks_stock
select `国籍描述`, count(`中文名称缩写`) from `公司实际控制人` group by `国籍描述`;	ccks_stock
select `基金简称`,`基金代码` from `公募基金债券组合明细` where `债券代码`='128125'	ccks_fund
select `中文名称缩写` from `股东持股统计`  where strftime('%Y', `截止日期`)='2021' order by  `信托公司持有A股比例(%)` desc limit 10;	ccks_stock
select `债券`, `央行债券` from `中国货币与银行概览`  where strftime('%Y', `截止日期`) = strftime('%Y', DATE('now', '-1 year')) ;	ccks_macro
select a.`中文名称缩写` from `公司概况` as a join `公司行业划分表` as b on a.`公司代码` = b.`公司代码` where a.`省份` = '广东省' and b.`一级行业名称` = '房地产业'	ccks_stock
select b.`中文名称缩写`,a.`股东名称` from `配股大股东认配状况` as a join `公司概况` as b on a.`公司代码`=b.`公司代码`  where b.`所属城市`='广州市';	ccks_stock
select `领导姓名`, `中文名称缩写` from `公司报告期管理层持股` where `职位描述` like '%董事长%' or `职位描述` like '%副董事长%'	ccks_stock
select b.`中文名称缩写`, b.`A股(股)` from `公司行业划分表` as a join `公司股本结构变动` as b on a.`公司代码` = b.`公司代码` where a.`一级行业名称` = '制造业' order by b.`A股(股)` desc	ccks_stock
select `回购期限`, `最低比率(%)`, `最高比率(%)` from `税率表` where `税率类别` ='国债买断式回购' and `税率项目` ='经手费';	ccks_macro
select `地方财政收入(百万元)`, `地方财政支出(百万元)` from `财政收支`  where strftime('%Y', `截止日期`)='2010' ;	ccks_macro
select count(*) from `公募基金获奖情况` where `奖项名称` = '三年持续回报明星基金公司奖';	ccks_fund
select `截止日期`, `总资产`, `总负债` from `其他存款性公司资产负债表` where `总负债` < 5000000 and `总资产` > 50000000;	ccks_macro
select a.`姓名`, b.`最高学历` from `公募基金衍生指标_基金经理最新收益与规模排名` as a join `公募基金经理基本资料` as b on a.`基金经理代码` = b.`所属人员编码` where a.`时间区间` = '近1年' order by a.`同类经理收益率均值(%)` desc limit 5	ccks_fund
select b.`中文名称缩写` from `公司概况` as a join `自由流通股本` as b on a.`公司代码` = b.`公司代码` where a.`省份` = '广东省' and b.`A股总股本(股)` > 100000000	ccks_stock
select `基金公司名称` from `公募基金获奖情况` where `评奖单位代码` ='14561';	ccks_fund
select `国内生产总值(百万元)`, `人均国内生产总值(元/人)` from `国内生产总值` where `省市` ='浙江';	ccks_macro
select  `基金代码`, `基金简称` from `公募基金净值最新区间表现` where `设立以来年化回报率(%)` > 30;	ccks_fund
select `基金简称` from `公募基金最新基准收益率` where `本日基金基准增长率(%)`>0 order by `本日基金基准增长率(%)` desc	ccks_fund
select `国有单位`, `集体单位`, `合营单位` from `社会消费品零售总额` ;	ccks_macro
select `所属基金/股票代码` , `主营业务利润(元)` from `公司主营业务构成` where `主营业务利润(元)` > 100000000;	ccks_stock
select `机构全称` from `发行与上市中介机构` where `中文名称缩写`='天健集团';	ccks_stock
select `截止日期`, `省市`, `第一产业(百万元)`, `第二产业(百万元)`, `第三产业(百万元)` from `国内生产总值`  where strftime('%Y', `截止日期`) > strftime('%Y', DATE('now', '-5 year') ) ;	ccks_macro
select a.`省份`, count(*) from `公司概况` as a join `公司经营范围与行业变更` as b on a.`公司代码` = b.`公司代码` where b.`行业名称` ='医药制造业' group by a.`省份` ;	ccks_stock
select `机构全称`,`承销金额(元)` from `发行与上市中介机构` where `所属基金/股票代码`='000401';	ccks_stock
select `中文名称缩写`, `所属基金/股票代码` from `法人配售与战略投资者`  where strftime('%Y', `信息发布日期`) = strftime('%Y', DATE('now', '-1 year'));	ccks_stock
select `进口商品总额(百万美元)` , `出口商品总额(百万美元)` from `海关进出口`  where `出口同比增减` > 0 and `进口同比增减` < 0 and strftime('%Y', `截止日期`)='2000';	ccks_macro
select `派现(含税/人民币元)` from `公司分红` where `所属基金/股票代码` ='000021';	ccks_stock
select `二年回报率(%)` from `公募基金净值最新区间表现` ;	ccks_fund
select count(*) from `A股增发`  where strftime('%Y', `预案公布日期`)='2020';	ccks_stock
select `股东名称`,`实配股数(股)` from `配股大股东认配状况` where `所属基金/股票代码`='600110';	ccks_stock
select `证券简称` from `公募基金概况` order by `设立日期` asc limit 1	ccks_fund
select `基金简称`,`市值(元)` from `公募基金债券组合明细` where `债券代码`='128125'	ccks_fund
select b.`基金经理姓名` from `基金经理任职及管理年限统计` a join `公募基金经理基本资料` b on a.`基金经理代码` = b.`所属人员编码` order by a.`本公司管理年限(月)` desc limit 1	ccks_fund
select `十年年化回报率(%)` from `公募基金净值最新区间表现` ;	ccks_fund
select `基金中文名称` from `公募基金概况` where `证券代码`='160215';	ccks_fund
select a.`所属城市` , count(*)  from `公司概况` as a join `概念所属公司表` as b on a.`公司代码` = b.`公司代码` where b.`概念名称` ='国产软件' group by a.`所属城市`;	ccks_stock
select b.`基金运作方式`, count(*) from `公募基金净值最新区间表现` as a join `公募基金概况` as b on a.`证券内部编码` = b.`基金内部编码` where a.`一年回报率(%)` > 20 group by b.`基金运作方式`;	ccks_fund
select `派现(含税/人民币元)` from `公司分红` where `所属基金/股票代码` ='000040';	ccks_stock
select `费率划分区间描述`, `费率描述` from `公募基金费率(新)` where `基金简称` ='富国创新药ETF';	ccks_fund
select count(*) from `A股配股` where `募集资金总额(元)` > 10000000000;	ccks_stock
select `其他国外资产(百万元)`, `国外负债(百万元)` from `货币当局资产负债表` ;	ccks_macro
select `领导姓名`, `中文名称缩写` from `公司报告期管理层持股` where `职位描述` like '%董事长%' and `职位描述` like '%总经理%'	ccks_stock
select `行业名称` from `公司经营范围与行业变更` where `中文名称缩写` ='精研科技'	ccks_stock
select `三年回报率(%)` from `公募基金净值最新区间表现` ;	ccks_fund
select `会计师事务所`,`签字会计师` from `A股发行申报企业信息` where `中文名称缩写`='大业股份';	ccks_stock
select `实配股数(股)` from `配股大股东认配状况` where `中文名称缩写`='深科技';	ccks_stock
select `中文名称缩写` from `公司行业划分表` where `二级行业名称` = '资本市场服务'	ccks_stock
select b.`研发投入合计(元)` from `A股发行申报企业信息` as a join `公司研发投入与产出` as b on a.`申报企业编号`=b.`公司代码`  where strftime('%Y', a.`截止日期`)>'2018' and a.`保荐机构`='广发证券';	ccks_stock
select `第三产业(百万元)` from `国内生产总值` ;	ccks_macro
select `省份`,`法人代表` from `公司概况` where `中文名称缩写`='五粮液';	ccks_stock
select `其它机构持有A股比例(%)` from `股东持股统计`  where strftime('%Y', `截止日期`)='2020' and round(strftime('%m',`截止日期`)/3.0 + 0.495)=1 and `中文名称缩写`='步步高';	ccks_stock
select `总资产(百万元)` from `货币当局资产负债表` ;	ccks_macro
select `股权授权方` from `股东股权托管`  where strftime('%Y', `信息发布日期`)='2018' and `中文名称缩写`='新日恒力' order by  `占股权授权方持股数比例` desc limit 1;	ccks_stock
select `进出口商品总额(百万美元)`, `进口商品总额(百万美元)`, `出口商品总额(百万美元)` from `海关进出口` ;	ccks_macro
select a.`最高学历`, max(b.`总管理规模(亿元)`) from `公募基金经理基本资料` as a join `基金经理规模统计(新)` as b on a.`所属人员编码` = b.`基金经理代码` group by a.`最高学历`;	ccks_fund
select `所属基金/股票代码` from `公司主营业务构成` where `主营业务收入同比` < 0 and strftime('%Y', `截止日期`)<'2019';	ccks_stock
select `领导姓名`, `职位描述`, `中文名称缩写` from `公司报告期管理层持股`  where strftime('%Y', `截止日期`)='2020' order by  `期末持股数(股)` desc limit 5	ccks_stock
select avg(`占资产净值比例`)  from `公募基金重仓股票组合` where `基金简称` = '富国天惠A'	ccks_fund
select `截止日期`,  `金额(亿元)` from `金融机构新增贷款` where `统计区间` ='期末累计' ;	ccks_macro
select b.`基金经理`,a.`债券简称` from `公募基金债券组合明细` as a join `公募基金概况` as b on a.`基金内部编码`=b.`基金内部编码` where a.`基金代码`='160615';	ccks_fund
select `机构全称`,`地址` from `发行与上市中介机构` where `中文名称缩写`='湖北宜化';	ccks_stock
select `各项存款` , `各项贷款` from `中国金融机构人民币信贷收支表`;	ccks_macro
select `中文名称缩写`,`QFII持有A股比例(%)` from `股东持股统计`  where strftime('%Y', `截止日期`)='2020';	ccks_stock
select b.`基金经理姓名` from `基金经理任职及管理年限统计` a join `公募基金经理基本资料` b on a.`基金经理代码` = b.`所属人员编码` order by a.`本公司管理年限(月)` asc  limit 1	ccks_fund
select `总股本(股)`, `流通股本(股)` from `股票月度行情数据` where `中文名称缩写` = '东方电子';	ccks_stock
select `社会消费品零售总额(百万元)` from `社会消费品零售总额` where `省市` ='北京' and `数据统计期间` ='期末累计' and strftime('%Y', `截止日期`)>='2000';	ccks_macro
select `收盘价(元)`, `流通股本(股)` from `股票月度行情数据` where `所属基金/股票代码` = '000822';	ccks_stock
select `基金经理姓名` from `基金经理规模统计(新)` order by `旗下基金总数(只)` desc limit 1;	ccks_fund
select b.`证券简称` from `公募基金净值最新区间表现` as a join `公募基金概况` as b on a.`证券内部编码` = b.`基金内部编码` where b.`基金类别` = '股票型' and a.`一周回报率(%)` > 5;	ccks_fund
select `证券简称` from `公募基金概况`  where strftime('%Y', `设立日期`)=strftime('%Y', DATE('now', '-1 year')) and round(strftime('%m',`设立日期`)/3.0 + 0.495)=1	ccks_fund
select `所属城市` from `公司概况` where `省份`='广东省' group by `所属城市` order by count(*) desc limit 1;	ccks_stock
select `中文名称缩写` from `公司实际控制人` where `国籍描述` = '美国';	ccks_stock
select `股东名称`, `所属基金/股票代码`, `股东持股数量` from `企业之间参股情况`  where `股东持股数量` > 10000000  and strftime('%Y', `截止日期`) >= strftime('%Y', DATE('now', '-2 year'));	ccks_stock
select  `基金名称` from  `公募基金获奖情况`  where strftime('%Y', `获奖年度`) >=2010 and `评奖单位` ='中国证券报' ;	ccks_fund
select `主营业务收入(元)`, `主营业务成本(元)`, `主营业务利润(元)` from `公司主营业务构成`  where strftime('%Y', `截止日期`) = strftime('%Y', DATE('now', '-1 year')) and `中文名称缩写` ='古井贡酒';	ccks_stock
select `股东名称`, `股东持股比例` from `企业之间参股情况` where `中文名称缩写` = '诺德股份';	ccks_stock
select a.`中文名称缩写`, b.`一级行业名称` from `股东股权变动` as a join `公司行业划分表` as b on a.`公司代码` = b.`公司代码` where a.`出让后持股比例` > 0.5	ccks_stock
select a.`基金简称` from `公募基金净值最新区间表现` as a join `公募基金概况` as b on a.`证券内部编码` = b.`基金内部编码` and b.`基金类别` ='股票型' where a.`设立以来年化回报率(%)` > 50;	ccks_fund
select b.`证券简称` from `公募基金最新基准收益率` as a join `公募基金概况` as b on a.`基金内部编码`=b.`基金内部编码` where a.`六个月基金基准增长率(%)`>5 and b.`基金投资类型`='指数型';	ccks_fund
select  `基金代码`, `基金简称`  from `公募基金净值最新区间表现` where `设立以来回报率(%)` < -30;	ccks_fund
select a.`基金简称`, b.`基金设立规模(份)`, b.`基金类别` from `公募基金净值最新区间表现` as a join `公募基金概况` as b on a.`证券内部编码` = b.`基金内部编码` order by a.`日回报率(%)` desc limit 3;	ccks_fund
select `主要业务` from `公司经营范围与行业变更` where `中文名称缩写` ='深科技'	ccks_stock
select `截止日期`, `国有及其控股企业(百万元)`, `集体企业(百万元)` from `工业生产` where `省市` ='上海' and `统计口径` ='全部工业企业' and `数据统计区间` ='期末累计' ;	ccks_macro
select `基金代码` , `单位净值(元)` from  `公募基金净值` ;	ccks_fund
select `托管涉及股数(股)` from `股东股权托管`  where strftime('%Y', `信息发布日期`)='2016' and `中文名称缩写`='澳柯玛';	ccks_stock
select a.`基金简称`, a.`基金代码` from `公募基金净值最新区间表现` as a join `公募基金概况` as b on a.`证券内部编码` = b.`基金内部编码` and b.`基金类别` ='混合型' where a.`设立以来年化回报率(%)` > 30;	ccks_fund
select `分红股本基数(股)`, `送股比例(10送X)`, `转增股比例(10转增X)` from `公司分红`  where `所属基金/股票代码` ='000728' and strftime('%Y', `分红实施公告日`) > strftime('%Y', DATE('now', '-2 year'));	ccks_stock
select `基金简称`, `日回报率(%)`, `一周回报率(%)` from `公募基金净值最新区间表现` where `一个月回报率(%)` > 5;	ccks_fund
select b.`证券简称`, b.`风险等级` from `公募基金经理(新)` as a join `公募基金风险等级表` as b on a.`基金内部编码` = b.`基金内部代码` where strftime('%Y', a.`到任日期`)>'2021'	ccks_fund
select `主要业务` from `公司经营范围与行业变更` where `中文名称缩写` ='浙大网新'	ccks_stock
select `一个月基金基准增长率(%)` from `公募基金最新基准收益率` where `基金简称`='华夏行业';	ccks_fund
select count(*) from `公司概况` where `所属城市`='厦门市';	ccks_stock
select b.`证券简称`,b.`基金经理`,b.`基金投资目标` from `公募基金最新基准收益率` as a join `公募基金概况` as b on a.`基金内部编码`=b.`基金内部编码` where a.`五年基金基准增长率(%)`>20;	ccks_fund
select b.`证券简称`,b.`基金经理` from `公募基金债券组合明细` as a join `公募基金概况` as b on a.`基金内部编码`=b.`基金内部编码` where a.`债券简称`='海亮转债';	ccks_fund
select `平均管理规模同类均值(亿元)` from `公募基金衍生指标_基金经理最新收益与规模排名` where `姓名` = '贾成东';	ccks_fund
select a.`所属城市` , count(*)  from `公司概况` as a join `概念所属公司表` as b on a.`公司代码` = b.`公司代码` where b.`概念名称` ='云计算'group by a.`所属城市` order by count(*) desc limit 1 ;	ccks_stock
select `国有单位` from `社会消费品零售总额` ;	ccks_macro
select `回购股数(股)`, `回购总金额(元)` from `股份回购` where `所属基金/股票代码` = '300011';	ccks_stock
select `设立以来回报率(%)` from `公募基金净值最新区间表现` ;	ccks_fund
select `三个月回报率(%)`, `六个月回报率(%)`, `一年回报率(%)` from `公募基金净值最新区间表现` where `基金简称` = '博时策略';	ccks_fund
select `股权被冻结质押股东名称`, sum(`累计冻结质押股数(股)`) from `股东股权冻结和质押统计` where `中文名称缩写` = '完美世界' group by `股权被冻结质押股东名称`	ccks_stock
select `回购股数(股)`, `占总股本比例` from `股份回购` where `中文名称缩写` = '南都电源' order by `预案公布日` desc limit 1	ccks_stock
select count(*) from `公司主营业务构成`  where strftime('%Y', `截止日期`) = strftime('%Y', DATE('now', '-1 year')) and `主营业务收入(元)` > 100000000;	ccks_stock
select b.`股东名称`,a.`机构全称` from `发行与上市中介机构` as a join `配股大股东认配状况` as b on a.`公司代码`=b.`公司代码` where a.`中文名称缩写`='东旭蓝天';	ccks_stock
select `其他资产`, `其他负债` from `其他存款性公司资产负债表` ;	ccks_macro
select `基金经理姓名` from `基金经理规模统计(新)` order by `股票型基金数量(只)` desc limit 1;	ccks_fund
select b.`一级行业名称`, count(*) from `限售股票解禁时间表` as a join `公司行业划分表` as b on a.`公司代码` = b.`公司代码` where a.`本次新增可售A股(万股)` > 100 group by b.`一级行业名称`	ccks_stock
select a.`概念名称`, count(*) from `概念所属公司表` as a join `公司概况` as b on a.`公司代码` = b.`公司代码` where b.`省份` ='海南省' group by a.`概念名称` ;	ccks_stock
select `债券简称` from `公募基金债券组合明细` where `基金简称`='鹏华价值' order by `市值(元)` desc limit 1;	ccks_fund
select `所属城市`,`所属区县` from `公司概况` where `A股证券代码`='600165';	ccks_stock
select `证券简称` from `公募基金概况` where `基金经理` = '王帅'	ccks_fund
select `收盘价(元)`, `流通股本(股)`, `总股本(股)` from `股票月度行情数据`  where `所属基金/股票代码` = '600649' and strftime('%Y', `日期`)='2021' and round(strftime('%m',`日期`)/3.0 + 0.495) = 3;	ccks_stock
select `回购股数(股)`, `占总股本比例` from `股份回购`  where `中文名称缩写` = '江苏租赁' and strftime('%Y', `预案公布日`)='2019' ;	ccks_stock
select `交易日`, `今开盘(元)`, `收盘价(元)` from `日行情表` where `中文名称缩写` = '山煤国际' and strftime('%Y', `交易日`)>='2018';	ccks_stock
select `领导姓名` from `公司报告期管理层持股` where `所属基金/股票代码` = '000430'	ccks_stock
select `公司中文名称` from `公司概况` where strftime('%Y', `公司成立日期`)>'2001';	ccks_stock
select `出让前持股数量(股)(份)`, `出让前持股比例` from `股东股权变动` where `所属基金/股票代码` = '300707'	ccks_stock
select `送股比例(10送X)`, `派现(含税/人民币元)` from `公司分红` where `中文名称缩写` ='东北证券';	ccks_stock
select `三年年化回报率(%)` from `公募基金净值最新区间表现` ;	ccks_fund
select b.`基金运作方式`, avg(a.`一年回报率(%)`) from `公募基金净值最新区间表现` as a join `公募基金概况` as b on a.`证券内部编码` = b.`基金内部编码` group by b.`基金运作方式`;	ccks_fund
select `增发目的` from `A股增发` where `所属基金/股票代码` = '300391';	ccks_stock
select `截止日期`,  `金额(亿元)` from `金融机构新增贷款`  where `统计区间` ='月份' and strftime('%Y', `截止日期`) = strftime('%Y', DATE('now', '-2 year'));	ccks_macro
select count(*) from `公司概况` where `省份`='北京市';	ccks_stock
select `主营业务收入(元)`, `主营业务利润(元)` from `公司主营业务构成`  where strftime('%Y', `截止日期`) = strftime('%Y', DATE('now', '-1 year')) and `所属基金/股票代码` ='000752';	ccks_stock
select `户均持股比例半年增长率(%)` from `股东户数`  where strftime('%Y', `截止日期`)='2020' and `中文名称缩写`='京基智农';	ccks_stock
select `基金简称` from `公募基金债券组合明细` where `债券代码`='128125' order by `持有数量(张)` desc limit 1;	ccks_fund
select `单位累计净值(元)` , `开放式基金单位基金净值日增长率`,`单位基金净值周增长率` from  `公募基金净值` where `基金简称` = '华安180ETF';	ccks_fund
select count(*)  from `概念所属公司表` as a join `公司概况` as b on a.`公司代码` = b.`公司代码` where a.`概念名称` ='互联网金融' and b.`所属城市` ='杭州市';	ccks_stock
select `公司网址` from `公募基金管理人概况` where `基金管理人简称` = '浦银安盛基金';	ccks_fund
select `基金名称` from  `公募基金获奖情况`  where strftime('%Y', `获奖年度`) = strftime('%Y', DATE('now', '-2 year'));	ccks_fund
select `送股比例(10送X)`, `派现(含税/人民币元)` from `公司分红` where `中文名称缩写` ='古井贡酒';	ccks_stock
select `中文名称缩写` from `发行与上市中介机构` where `承销数量(股)`>50000000;	ccks_stock
select `中文名称缩写` from `公司概况` where `A股证券代码` like '600%';	ccks_stock
select `二年年化回报率(%)` from `公募基金净值最新区间表现` ;	ccks_fund
select `国外净资产`, `国内信贷` from `中国货币与银行概览` where strftime('%Y', `截止日期`)<'2000';	ccks_macro
select `费率划分区间描述`, `费率描述` from `公募基金费率(新)` where `基金代码` ='159748';	ccks_fund
select `股东名称` from `配股大股东认配状况` where `中文名称缩写`='恒生电子' order by `实配股数(股)` desc limit 1;	ccks_stock
select `十年回报率(%)` , `十年年化回报率(%)` from `公募基金净值最新区间表现` ;	ccks_fund
select `指数名称`, `指数` from `工业品出厂价格指数` where `指数类别` ='工业结构分类指数' and `数据统计期间` ='上年同月' and strftime('%Y', `截止日期`)>='2010';	ccks_macro
select `股东名称`, `所属基金/股票代码`, `股东投资金额` from `企业之间参股情况`  where `股东投资金额` > 10000000 and strftime('%Y', `截止日期`) = strftime('%Y', DATE('now', '-2 year')) ;	ccks_stock
select `基金类别描述`, count(*) from `公募基金最新收益率排名` where `指标周期` = '成立以来' and `同类基金收益率均值(%)` > 0 group by `基金类别描述`	ccks_fund
select `保荐机构` from `A股发行申报企业信息` where `会计师事务所`='立信会计事务所' order by `截止日期` desc limit 1;	ccks_stock
select `指数` from `工业品出厂价格指数` where `数据统计期间` ='上年同期' and `指数类别` ='工业结构分类指数' and `指数名称` ='生产资料-加工';	ccks_macro
select `发行量下限(不少于)(股)`, `发行量上限(不超过)(股)` from `A股增发` where `中文名称缩写` = '吉峰科技';	ccks_stock
select `配售股数(股/份/张)`, `获配金额(元)` from `法人配售与战略投资者`  where `获配企业名称(披露)` ='邱丕云' and strftime('%Y', `信息发布日期`) > strftime('%Y', DATE('now', '-3 year')) order by  `获配金额(元)` desc ;	ccks_stock
select `配售总股数(股/份/张)`, `获配企业名称(披露)`, `配售股数(股/份/张)` from `法人配售与战略投资者` where `所属基金/股票代码` ='600517' ;	ccks_stock
select `基金简称` from `公募基金净值最新区间表现` order by `设立以来回报率(%)` desc limit 1;	ccks_fund
select `基金管理人简称` from `公募基金管理人概况` order by `成立日期` desc limit 1;	ccks_fund
select `指数` from `工业品出厂价格指数`  where `指数名称` ='医药制造业' and `数据统计期间` ='上年同月' and strftime('%Y', `截止日期`) = strftime('%Y', DATE('now', '-1 year')) and round(strftime('%m',`截止日期`)/3.0 + 0.495) = 1 ;	ccks_macro
select `股东名称`,`实配股数(股)`,`应配股数(股)` from `配股大股东认配状况` where `所属基金/股票代码`='000423';	ccks_stock
select `股东名称` from `配股大股东认配状况` where `应配股数(股)`>2000000;	ccks_stock
select max(`市盈率TTM`) from `股票月度行情数据`  where `所属基金/股票代码`  = '600352' and strftime('%Y', `日期`)='2022';	ccks_stock
select `总负债` from `其他存款性公司资产负债表` ;	ccks_macro
select a.`姓名`, b.`背景介绍` from `基金经理历任收益风险指标(全)` as a join `公募基金经理基本资料` as b on a.`基金经理代码` = b.`所属人员编码` where a.`最大盈利(未填充)` > 2	ccks_fund
select `费率划分标准Ⅰ` , `费率划分标准范围Ⅰ起始数值`, `费率划分标准范围Ⅰ截止数值` from `公募基金费率(新)` where `基金代码` ='501065';	ccks_fund
select `所属基金/股票代码`, `回购总金额(元)` from `股份回购` where strftime('%Y', `预案公布日`) >= '2019' ;	ccks_stock
select `对其他存款性公司债权`, `对其他居民部门债权` from `其他存款性公司资产负债表` where `总资产` > 50000000;	ccks_macro
select b.`基金经理姓名` from `基金经理任职及管理年限统计` a join `公募基金经理基本资料` b on a.`基金经理代码` = b.`所属人员编码` group by b.`基金经理姓名` order by count(*) desc limit 1	ccks_fund
select `证券简称`,`基金经理` from `公募基金概况` where `基金投资风格`='大盘价值股票';	ccks_fund
select a.`证券简称`, a.`风险收益特征` from `公募基金概况` as a join `公募基金风险等级表` as b on a.`基金内部编码` = b.`基金内部代码` where b.`风险等级` = '中'	ccks_fund
select `组织形式`, count(*) from `公募基金管理人概况` group by `组织形式`;	ccks_fund
select b.`领导姓名`, b.`职位描述` from `公司概况` as a join `公司报告期管理层持股` as b on a.`公司代码` = b.`公司代码` where a.`省份` = '浙江省' and b.`所属基金/股票代码` like '300%'	ccks_stock
select `地方财政收入(百万元)`, `地方财政支出(百万元)` from `财政收支` where `省市` ='上海';	ccks_macro
select `基金简称` from `公募基金主要财务指标(季报)`  where strftime('%Y', `截止日期`)='2020' and round(strftime('%m',`截止日期`)/3.0 + 0.495) = 4 and `期末基金资产净值` > 10000000000	ccks_fund
select count(*) from `公司概况` where `省份`='山西省';	ccks_stock
select `中文名称缩写` from `A股增发`  where strftime('%Y', `预案公布日期`)='2022';	ccks_stock
select `中文名称缩写` from `公司行业划分表` where `一级行业名称` = '建筑业'	ccks_stock
select `证券简称` from `公募基金风险等级表` where `风险等级` = '中高'	ccks_fund
select `基金本期利润` from `公募基金主要财务指标(季报)`  where `基金简称` = '华夏50ETF' and strftime('%Y', `截止日期`)='2021' and round(strftime('%m',`截止日期`)/3.0 + 0.495) = 1	ccks_fund
select `经营范围-主营` from `公司经营范围与行业变更` lb where `中文名称缩写` ='南华生物'	ccks_stock
select `十年回报率(%)` from `公募基金净值最新区间表现` ;	ccks_fund
select `股东名称` from `配股大股东认配状况` where `中文名称缩写`='亚泰集团' order by `实配股数(股)` desc limit 1;	ccks_stock
select `省份`, `所属城市` from `公司概况` where `省份`='湖南省' and `所属城市`='长沙市';	ccks_stock
select `中文名称缩写`,avg(`实配股数(股)`) from `配股大股东认配状况` group by `中文名称缩写`;	ccks_stock
select `基金经理姓名` from `基金经理规模统计(新)` where `总管理规模(亿元)` < 1;	ccks_fund
select `中文名称缩写` from `限售股票解禁时间表` where `所属基金/股票代码` like '6%' order by `A股总数(万股)` desc limit 1	ccks_stock
select `主营业务收入(元)` from `公司主营业务构成`  where `中文名称缩写` ='冰山冷热' and strftime('%Y', `截止日期`)='2020'	ccks_stock
select `基金管理人` from `公募基金概况` group by `基金管理人` order by count(*) desc limit 1;	ccks_fund
select `股东名称`,`应配股数(股)` from `配股大股东认配状况` where `中文名称缩写`='天山股份';	ccks_stock
select b.`基金经理` from `公募基金最新基准收益率` as a join `公募基金概况` as b on a.`基金内部编码`=b.`基金内部编码` order by a.`三个月基金基准增长率(%)` desc limit 10;	ccks_fund
select `股东名称`, `股东持股数量` from `企业之间参股情况` where `中文名称缩写` ='力源信息' ;	ccks_stock
select count(*) from `公司概况` where `所属城市`='武汉市';	ccks_stock
select `集体单位`, `个体单位` from `社会消费品零售总额`  where `统计区域类别` ='省市' and `数据统计期间` ='期末累计' and strftime('%Y', `截止日期`) = strftime('%Y', DATE('now', '-1 year')) ;	ccks_macro
select `债券简称` from `公募基金债券组合明细` where `基金简称`='鹏华价值' and `持有数量(张)`>50000;	ccks_fund
select `社会消费品零售总额(百万元)` from `社会消费品零售总额` where `省市` ='北京';	ccks_macro
select `社会消费品零售总额(百万元)` from `社会消费品零售总额` where `省市` ='北京' and `数据统计期间` ='期末累计';	ccks_macro
select `利息支出(元)`, `汇兑损益` from `利润分配表附注_财务费用`  where `中文名称缩写` = '万达信息' and strftime('%Y', `截止日期`)>'2016'	ccks_stock
select `截止日期`,  `金额(亿元)` from `金融机构新增贷款` where `统计区间` ='月份' and `金额(亿元)` > 150000;	ccks_macro
select `公司中文名称`, `股东投资金额` from `企业之间参股情况`  where `中文名称缩写` = '常山北明' and strftime('%Y', `截止日期`)='2020' and strftime('%m', `截止日期` )='3'	ccks_stock
select `农业存款`, `储蓄存款` from `中国金融机构人民币信贷收支表`;	ccks_macro
select a.`中文名称缩写`, a.`股权被冻结质押股东名称` from `股东股权冻结和质押统计` as a join `公司行业划分表` as b on a.`公司代码` = b.`公司代码` where b.`一级行业名称` = '建筑业' order by a.`累计占总股本比例` desc	ccks_stock
select `基金简称`,`本月以来基金基准增长率(%)` from `公募基金最新基准收益率` where `本月以来基金基准增长率(%)`>5;	ccks_fund
select count(*) from `公司主营业务构成`  where strftime('%Y', `截止日期`)='2020' and `毛利率` > 1	ccks_stock
select `本月以来回报率(%)` from  `公募基金净值最新区间表现` ;	ccks_fund
select `基金简称` from `公募基金债券组合明细` where `债券简称`='华海转债' and `持有数量(张)`>1000000;	ccks_fund
select a.`中文名称缩写` from `公司主营业务构成` as a join `公司概况` as b on a.`公司代码` = b.`公司代码`   where strftime('%Y', a.`截止日期`)='2020' and b.`省份` = '浙江省' order by  a.`主营业务收入(元)` desc limit 1;	ccks_stock
select count(distinct `中文名称缩写`) from `股票月度行情数据` where strftime('%Y', `日期`)='2022' and round(strftime('%m',`日期`)/3.0 + 0.495)=1 and `收盘价(元)`<2;	ccks_stock
select `公司中文名称`, count(*) from `股东股权冻结和质押`  where strftime('%Y', `冻结质押期限截止日`)='2020' and strftime('%m', `冻结质押期限截止日`)='3' group by  `公司中文名称`	ccks_stock
select `承销金额(元)` from `发行与上市中介机构` where `中文名称缩写`='常山北明';	ccks_stock
select `办公地址` from `公募基金管理人概况` where `基金管理人简称` = '建信基金';	ccks_fund
select max(`社会消费品零售总额(百万元)`) from `社会消费品零售总额` where `省市`='上海' and `数据统计期间` ='期末累计' ;	ccks_macro
select `基金简称` from `公募基金净值最新区间表现` where `一个月回报率(%)` > 5 and `一周回报率(%)` > 3;	ccks_fund
select `总管理规模同类排名` from `公募基金衍生指标_基金公司收益与规模同类均值与排名` where `基金公司中文简称`='中信证券';	ccks_fund
select `股权授权方`,`接受股权授权方` from `股东股权托管`  where strftime('%Y', `信息发布日期`)='2019' and `中文名称缩写`='诺德股份';	ccks_stock
select `储备资产`  from `其他存款性公司资产负债表` ;	ccks_macro
select `期末基金资产净值` from `公募基金主要财务指标(季报)` where `基金简称` = '南方积配' order by `截止日期` desc limit 1	ccks_fund
select `基金经理姓名` from `公募基金经理基本资料` where `最高学历` = '博士'  and `性别` = '男' and `基金经理姓名` like '李%'	ccks_fund
select `债券型基金数量(只)`,`债券型管理规模(亿元)` from `基金经理规模统计(新)` where `基金经理姓名`='陈龙';	ccks_fund
select `第一产业(百万元)`, `第二产业(百万元)`, `第三产业(百万元)` from `国内生产总值` ;	ccks_macro
select `基金公司中文简称`,`平均管理规模同类均值(亿元)` from `公募基金衍生指标_基金公司收益与规模同类均值与排名` order by `平均管理规模排名` limit 1;	ccks_fund
select max(`收盘价(元)`) from `股票月度行情数据` where `中文名称缩写` = '东方电子'	ccks_stock
select `城市维护建设费(百万元)` from `财政收支`  where `省市` ='北京' and strftime('%Y', `截止日期`) = strftime('%Y', DATE('now', '-2 year')) ;	ccks_macro
select `基金持有A股比例(%)` from `股东持股统计`  where strftime('%Y', `截止日期`)='2020' and strftime('%m', `截止日期`)='6' and `中文名称缩写`='中航重机';	ccks_stock
select `A股证券代码` from `公司概况` where `中文名称缩写`='康盛股份';	ccks_stock
select `基金简称` from `公募基金最新基准收益率` where `十年基金基准增长率(%)`>200;	ccks_fund
select `配售股数(股/份/张)` , `获配金额(元)` from `法人配售与战略投资者` where `获配企业名称(披露)` ='林泗华' ;	ccks_stock
select `户均持股比例(%)` from `股东户数`  where strftime('%Y', `截止日期`)='2019' and round(strftime('%m',`截止日期`)/3.0 + 0.495)=1 and `中文名称缩写`='东旭蓝天';	ccks_stock
select avg(a.`设立以来年化回报率(%)`) from `公募基金净值最新区间表现` as a join `公募基金概况` as b on a.`证券内部编码` = b.`基金内部编码` and b.`基金类别` ='股票型' ;	ccks_fund
select `联系人` from `公募基金管理人概况` where `基金管理人简称` = '南方基金';	ccks_fund
select `经营范围-兼营` from `公司经营范围与行业变更` lb where `中文名称缩写` ='深科技'	ccks_stock
select a.`姓名` from `公募基金经理(新)` as a join `公募基金经理基本资料` as b on a.`所属人员代码` = b.`所属人员编码` where a.`任职期间基金净值增长率` > 0 and b.`证券从业经历(年)` < 2	ccks_fund
select `计费基准` , `最低比率(%)`, `最高比率(%)` from `税率表` where `税率类别` ='企债质押式回购' and `税率项目` = '经手费' ;	ccks_macro
select a.`省份` , count(*) from `公司概况` as a join `公司经营范围与行业变更` as b on a.`公司代码` = b.`公司代码` where b.`行业名称` ='专业技术服务业' group by a.`省份` order by count(*) desc limit 1 ;	ccks_stock
select `社保基金持有A股比例(%)` from `股东持股统计`  where strftime('%Y', `截止日期`)='2020' and strftime('%m', `截止日期`)='5' and `中文名称缩写`='奥普光电';	ccks_stock
select `保荐机构`,`律师事务所`,`会计师事务所` from `A股发行申报企业信息` where `所属基金/股票代码`='300278';	ccks_stock
select `领导姓名` from `公司报告期管理层持股` where `中文名称缩写` = '越剑智能' and `期初持股数(股)` > 10000000	ccks_stock
select `评估机构` from `A股发行申报企业信息` where `中文名称缩写`='福斯特';	ccks_stock
select count(*) from `公募基金经理(新)` where `任职期间基金净值增长率` < 0	ccks_fund
select a.`中文名称缩写`, b.`法人代表` from `限售股票解禁时间表` as a join `公司概况` as b on a.`公司代码` = b.`公司代码` where a.`已流通A股占A股总数比例(%)` > 20	ccks_stock
select `基金经理姓名`, `QDII基金数量(只)`, `QDII管理规模(亿元)` from `基金经理规模统计(新)` where `基金经理姓名` = '徐猛' or `基金经理姓名` = '范冰';	ccks_fund
select max(`指数`) from `工业品出厂价格指数`  where `指数名称` ='纺织业' and `数据统计期间` ='上年同期' and strftime('%Y', `截止日期`) = strftime('%Y', DATE('now', '-1 year'));	ccks_macro
select `实配股数(股)` from `配股大股东认配状况` where `股东名称`='杉杉集团';	ccks_stock
select `机构全称`,`法人代表` from `发行与上市中介机构` where `中文名称缩写`='东阿阿胶';	ccks_stock
select b.`证券简称`, a.`一年回报率(%)`, a.`二年回报率(%)` from `公募基金净值最新区间表现` as a join `公募基金概况` as b on a.`证券内部编码` = b.`基金内部编码` where b.`基金类别` = '债券型';	ccks_fund
select `财政性存款` from `中国金融机构人民币信贷收支表`;	ccks_macro
select `基金简称` from `公募基金最新收益率排名` where `指标周期` = '六个月' order by `基金收益率(%)` desc limit 1	ccks_fund
select a.`同类基金年化收益率均值(%)` from `公募基金最新收益率排名` as a join `公募基金概况` as b on a.`基金内部编码` = b.`基金内部编码` where b.`基金运作方式` = 'LOF'	ccks_fund
select a.`中文名称缩写` from `公司股本结构变动` as a join `公司行业划分表` as b on a.`公司代码` = b.`公司代码` where b.`一级行业名称` = '制造业' order by a.`流通A股(股)` desc limit 20	ccks_stock
select `债券简称` from `公募基金债券组合明细` where `基金代码`='166001';	ccks_fund
select count(*) from `股份回购`  where strftime('%Y', `预案公布日`)='2021' ;	ccks_stock
select `基金管理人简称` from `公募基金管理人概况` where `法人代表` like '周%';	ccks_fund
select `最高学历`, `性别`, count(*) from `公募基金经理基本资料` group by `最高学历`, `性别`;	ccks_fund
select `股东名称`, max(`实配股数(股)`) from `配股大股东认配状况` where strftime('%Y', `首次信息发布时间`)>'2018' group by `股东名称`;	ccks_stock
select `外币存款` , `国外净资产` from `中国货币与银行概览`  where strftime('%Y', `截止日期`) = strftime('%Y', DATE('now', '-2 year')) ;	ccks_macro
select `二年年化回报率(%)` , `十年年化回报率(%)` from `公募基金净值最新区间表现` ;	ccks_fund
select `股权授权方` from `股东股权托管`  where strftime('%Y', `信息发布日期`)='2014' order by  `托管涉及股数(股)` desc limit 1;	ccks_stock
select `费率类别描述` , `费率描述` from `公募基金费率(新)` where `基金代码` ='501065';	ccks_fund
select max(`总资产`), min(`总资产`) , max(`总负债`), min(`总负债`)  from `其他存款性公司资产负债表`;	ccks_macro
select b.`一级行业名称`, count(*) from `限售股票解禁时间表` as a join `公司行业划分表` as b on a.`公司代码` = b.`公司代码` where a.`已流通A股占A股总数比例(%)` > 60 group by b.`一级行业名称`	ccks_stock
select  `获配企业名称(披露)` from `法人配售与战略投资者`  where `配售股数(股/份/张)` > 10000 and strftime('%Y', `信息发布日期`) = strftime('%Y', DATE('now', '-1 year'));	ccks_stock
select  `回购期限`,  `最低比率(%)`, `最高比率(%)` from `税率表` where `税率类别` ='国债买断式回购' and `税率项目` ='经手费' ;	ccks_macro
select `截止日期`, `重工业(百万元)` from `工业生产` where `统计区域类别` ='全国' and `统计口径` ='国有及规模以上工业企业' and `数据统计区间` ='月度';	ccks_macro
select `保险公司持有A股比例(%)` from `股东持股统计` where `中文名称缩写`='恒生电子';	ccks_stock
select `成交笔数(笔)` from `日行情表` where `所属基金/股票代码` = '601908';	ccks_stock
select a.`姓名` from `公募基金经理(新)` as a join `公募基金概况` as b on a.`基金内部编码` = b.`基金内部编码` where b.`基金类别` = '股票型'	ccks_fund
select `今年以来回报率(%)` from `公募基金净值最新区间表现` ;	ccks_fund
select count(*) from `法人配售与战略投资者`  where `配售股数(股/份/张)` > 10000 and strftime('%Y', `信息发布日期`) = strftime('%Y', DATE('now', '-1 year'));	ccks_stock
select b.`所属城市`, count(*) from `概念所属公司表` as a join `公司概况` as b on a.`公司代码` = b.`公司代码` where a.`概念名称` ='OLED' group by b.`所属城市` ;	ccks_stock
select `所属基金/股票代码`, `中文名称缩写` from `股份回购`  where `回购股数(股)` > 100000 and strftime('%Y', `预案公布日`) > strftime('%Y', DATE('now', '-2 year'));	ccks_stock
select `日回报率(%)`, `本周以来回报率(%)`, `一周回报率(%)` from `公募基金净值最新区间表现` where `基金简称` = '华宝宝盛';	ccks_fund
select `截止日期`, `社会消费品零售总额(百万元)` from `社会消费品零售总额` where `省市` ='上海' and `数据统计期间` ='年度' and strftime('%Y', `截止日期`)<'2010';	ccks_macro
select b.`证券简称`,b.`基金类别` from `公募基金债券组合明细` as a join `公募基金概况` as b on a.`基金内部编码`=b.`基金内部编码` where a.`债券简称`='海亮转债';	ccks_fund
select `截止日期`, `工业增加值(百万元)` from `工业生产` where `统计区域类别` ='全国' and `统计口径` ='国有及规模以上工业企业' and `数据统计区间` ='期末累计';	ccks_macro
select count(*) from `A股增发`  where strftime('%Y', `预案公布日期`) > strftime('%Y', DATE('now', '-5 year'));	ccks_stock
select `基金中文名称` from `公募基金概况` where `证券简称`='博时主题';	ccks_fund
select `批发零售贸易业` , `餐饮业` from `社会消费品零售总额` ;	ccks_macro
select `储备货币(百万元)` , `自有资金(百万元)` from `货币当局资产负债表`  where strftime('%Y', `截止日期`) = strftime('%Y', DATE('now', '-2 year')) ;	ccks_macro
select `公司中文名称`, `股东持股数量` from `企业之间参股情况`  where `中文名称缩写` = '航天发展' and strftime('%Y', `截止日期`)='2020' and strftime('%m', `截止日期` )='3'	ccks_stock
select `股权授权方` from `股东股权托管`  where strftime('%Y', `信息发布日期`)='2018' and `中文名称缩写`='新北洋';	ccks_stock
select a.`省份`, count(*) from `公司概况` as a join `公司股本结构变动` as b on a.`公司代码` = b.`公司代码` where b.`未流通A股(股)` > 200000000 group by a.`省份`	ccks_stock
select a.`行业名称` , count(*) from `公司经营范围与行业变更` as a join `公司概况` as b on a.`公司代码` = b.`公司代码`  where strftime('%Y', b.`公司成立日期`)='2010' group by  a.`行业名称` having count(*)>10;	ccks_stock
select avg(b.`总管理规模(亿元)`) from `公募基金经理基本资料` as a join `基金经理规模统计(新)` as b on a.`所属人员编码` = b.`基金经理代码` where a.`证券从业经历(年)` < 5;	ccks_fund
select `费率计算方式` , `费率划分区间描述`  from `公募基金费率(新)` where `基金简称` ='富国创新药ETF';	ccks_fund
select `最高比率(%)` from `税率表` where `税率类别` ='A股' and `税率项目` = '证券交易印花税' and `证券市场` ='深圳证券交易所' ;	ccks_macro
select `国籍`, count(*) from `公募基金经理基本资料` group by `国籍`	ccks_fund
select count(*) from `法人配售与战略投资者`  where strftime('%Y', `信息发布日期`)='2021';	ccks_stock
select b.`国籍` from `基金经理历任收益风险指标(全)` as a join `公募基金经理基本资料` as b on a.`基金经理代码` = b.`所属人员编码` where a.`年化夏普比率(未填充)` > 2 group by b.`国籍` having count(*) > 20	ccks_fund
select count(*) from `自由流通股本`  where `A股总股本(股)` > 10000000000 and strftime('%Y', `股本变动日期`)='2021'	ccks_stock
select `基金经理` , `基金名称` from `公募基金获奖情况` where `评奖单位代码` = '40981';	ccks_fund
select  `所属基金/股票代码` from `企业之间参股情况`  where `股东名称` ='顾瑜' and `股东投资金额` > 1000000 and strftime('%Y', `截止日期`) = strftime('%Y', DATE('now', '-1 year'));	ccks_stock
select a.`省份` , count(*) from `公司概况` as a join `公司经营范围与行业变更` as b on a.`公司代码` = b.`公司代码` where b.`行业名称` ='农业' group by a.`省份` ;	ccks_stock
select count(*) from `公募基金债券组合明细` where `基金简称`='博时主题';	ccks_fund
select a.`所属基金/股票代码`, a.`中文名称缩写` from `概念所属公司表` as a join `公司概况` as b on a.`公司代码` = b.`公司代码` where a.`概念名称` ='集成电路' and b.`所属城市` ='西安市';	ccks_stock
select `社保基金持有A股比例(%)` from `股东持股统计`  where strftime('%Y', `截止日期`)='2019' and strftime('%m', `截止日期`)='2' and `中文名称缩写`='中航重机';	ccks_stock
select `基金经理姓名` from `公募基金经理基本资料` where strftime('%Y', `出生日期`)>'1990';	ccks_fund
select `在任基金数(只)` from `公募基金衍生指标_基金经理收益与规模同类分析` where `基金经理姓名` = '付浩';	ccks_fund
select max(`指数`), min(`指数`) from `工业品出厂价格指数`  where `指数名称` ='食品制造业' and `数据统计期间` ='上年同期' and strftime('%Y', `截止日期`)='2008' ;	ccks_macro
select `回购股数(股)`, `占总股本比例`, `回购总金额(元)` from `股份回购` where `中文名称缩写` = '浙江龙盛' ;	ccks_stock
select `五年回报率(%)` from `公募基金净值最新区间表现` ;	ccks_fund
select `对政府债权(净)`, `对非金融部门债权`, `对特定存款机构的债权` from `中国货币与银行概览` ;	ccks_macro
select `指数名称`, `指数` from `工业品出厂价格指数` where `数据统计期间` ='上年同月' and `指数类别` ='工业结构分类指数';	ccks_macro
select `一级行业名称` from `公司行业划分表` where `中文名称缩写` = '普路通'	ccks_stock
select `基金简称` from `公募基金债券组合明细` where `债券代码`='200203';	ccks_fund
select `省市`, `第一产业(百万元)`, `第二产业(百万元)`, `第三产业(百万元)` from `国内生产总值`  where strftime('%Y', `截止日期`) = strftime('%Y', DATE('now', '-2 year') ) ;	ccks_macro
select `开放式基金单位基金净值日增长率` from `公募基金净值` where `基金简称` = '华安石油A';	ccks_fund
select  `所属基金/股票代码` from `股东股权冻结和质押`  where strftime('%Y', `冻结质押期限截止日`) > strftime('%Y', DATE('now', '-2 year'));	ccks_stock
select `截止日期`, `对政府债权(净)`, `对中央银行债权` from `其他存款性公司资产负债表` where `总资产` > 30000000;	ccks_macro
select `债券简称`,`市值(元)`,`占资产净值比例` from `公募基金债券组合明细` where `基金代码`='161010';	ccks_fund
select `获配企业名称(披露)` from `法人配售与战略投资者` where `所属基金/股票代码` = '002981';	ccks_stock
select `基金经理姓名` from `基金经理规模统计(新)` where `债券型基金数量(只)`>3;	ccks_fund
select  `中文名称缩写` from `法人配售与战略投资者`  where strftime('%Y', `信息发布日期`) = strftime('%Y', DATE('now', '-1 year')) ;	ccks_stock
select `二级行业名称` from `公司行业划分表` where `一级行业名称` = '信息传输、软件和信息技术服务业' group by `二级行业名称` order by count(*) desc limit 2	ccks_stock
select `省份`, `所属城市` from `公司概况` where `中文名称缩写`='华昌达';	ccks_stock
select  `获配企业名称(披露)` from `法人配售与战略投资者`  where strftime('%Y', `信息发布日期`)='2020'	ccks_stock
select `截止日期`, `单位基金净值周增长率` from  `公募基金净值`  where strftime('%Y', `截止日期`) > strftime('%Y', DATE('now', '-2 year')) and `基金代码` ='160416' ;	ccks_fund
select b.`基金类别` from `公募基金净值最新区间表现` as a join `公募基金概况` as b on a.`证券内部编码` = b.`基金内部编码` group by b.`基金类别` order by avg(a.`一个月回报率(%)`) desc limit 1;	ccks_fund
select `二年年化回报率(%)` from `公募基金净值最新区间表现` ;	ccks_fund
select a.`债券简称`,a.`市值(元)`, b.`基金经理` from `公募基金债券组合明细` as a join `公募基金概况` as b on a.`基金内部编码`=b.`基金内部编码` where a.`基金代码`='510130';	ccks_fund
select `基金公司中文简称` from `公募基金衍生指标_基金公司收益与规模同类均值与排名` where `基金类别描述`='债券型' order by `总规模管理规模同类均值(亿元)` desc limit 10;	ccks_fund
select a.`证券简称`, a.`基金简介` from `公募基金概况` as a join `公募基金风险等级表` as b on a.`基金内部编码` = b.`基金内部代码` where b.`风险等级` = '中高'	ccks_fund
select b.`证券简称`,b.`基金经理`,a.`六个月基金基准增长率(%)` from `公募基金最新基准收益率` as a join `公募基金概况` as b on a.`基金内部编码`=b.`基金内部编码` where a.`六个月基金基准增长率(%)`>0;	ccks_fund
select b.`省份` from `公司主营业务构成` as a join `公司概况` as b on a.`公司代码` = b.`公司代码` where a.`主营业务收入(元)` > 100000000000;	ccks_stock
select `所属行业/领域`,count(*) from `A股发行申报企业信息`  where strftime('%Y', `截止日期`)='2012' group by  `所属行业/领域`;	ccks_stock
select a.`姓名`, b.`最高学历` from `公募基金经理(新)` as a join `公募基金经理基本资料` as b on a.`所属人员代码` = b.`所属人员编码` where a.`任职期间基金净值增长率` < 0.1	ccks_fund
select `截止日期`, `省市`, `工业增加值(百万元)` from `工业生产` where `统计区域类别` = '省市' and `统计口径` ='国有及规模以上工业企业' and `数据统计区间` ='年度' ;	ccks_macro
select `保荐机构`, `律师事务所` from `A股发行申报企业信息` where `中文名称缩写`='红塔证券' order by `截止日期` desc limit 1;	ccks_stock
select `股权被冻结质押股东名称` from `股东股权冻结和质押` where `中文名称缩写` = '瑞茂通' and `涉及股数(股)` > 1000000 ;	ccks_stock
select `股票简称` from `公募基金重仓股票组合` where `股票简称` is not null group by  `股票简称` order by count(*) desc limit 1	ccks_fund
select `设立以来回报率(%)` from `公募基金净值最新区间表现` ;	ccks_fund
select `证券简称`,`风险收益特征` from `公募基金概况` where `基金投资风格`='行业股票-医药';	ccks_fund
select `企业收入(百万元)`, `企业所得税(百万元)` from `财政收支`  where `企业收入增速` > 5 and `省市` ='北京' and strftime('%Y', `截止日期`) > strftime('%Y', DATE('now', '-5 year')) ;	ccks_macro
select `十年年化回报率(%)` , `设立以来年化回报率(%)`  from `公募基金净值最新区间表现` ;	ccks_fund
select a.`最高学历`, avg(b.`总管理规模(亿元)`) from `公募基金经理基本资料` as a join `基金经理规模统计(新)` as b on a.`所属人员编码` = b.`基金经理代码` group by a.`最高学历`;	ccks_fund
select b.`最高学历`, count(*) from `基金经理历任收益风险指标(全)` as a join `公募基金经理基本资料` as b on a.`基金经理代码` = b.`所属人员编码` where a.`年化阿尔法(未填充)` > 0.5 group by b.`最高学历`	ccks_fund
select `省市` from `国内生产总值`  where strftime('%Y', `截止日期`) = strftime('%Y', DATE('now', '-1 year')) and `国内生产总值同比` > 0.5;	ccks_macro
select `主营业务收入(元)` from `公司主营业务构成`  where `中文名称缩写`='中国石化' and strftime('%Y', `截止日期`) = strftime('%Y', DATE('now', '-1 year')) and round(strftime('%m',`截止日期`)/3.0 + 0.495) = 1 ;	ccks_stock
select `截止日期`, `轻工业(百万元)` from `工业生产` where `统计区域类别` ='全国' and `统计口径` ='全部工业企业' and `数据统计区间` ='期末累计';	ccks_macro
select `单位净值(元)` , `单位基金净值周增长率` from  `公募基金净值` ;	ccks_fund
select `基金经理姓名` from `基金经理规模统计(新)` order by `QDII管理规模(亿元)` desc limit 1;	ccks_fund
select count(*) from `股份回购`  where strftime('%Y', `预案公布日`)='2021' ;	ccks_stock
select `中文名称缩写` from `股票月度行情数据`  where strftime('%Y', `日期`)='2020' group by  `中文名称缩写` order by max(`总股本(股)`) desc limit 10;	ccks_stock
select `基金经理姓名`, `股票型基金数量(只)`, `股票型管理规模(亿元)` from `基金经理规模统计(新)` where `股票型基金数量(只)` > 5;	ccks_fund
select `日回报率(%)` from  `公募基金净值最新区间表现` ;	ccks_fund
select `中文名称缩写` from `公司实际控制人` where `国籍描述` != '中国';	ccks_stock
select `户均持股比例半年增长率(%)` from `股东户数` where `中文名称缩写`='兴业证券';	ccks_stock
select `主营业务成本(元)`, `主营业务利润(元)` from `公司主营业务构成`  where `中文名称缩写` ='古井贡酒' and strftime('%Y', `截止日期`)='2018';	ccks_stock
select count(`交易日`) from `日行情表` where `中文名称缩写` = '科思股份' and `成交金额(元)` > 100000000;	ccks_stock
select a.`基金简称`, a.`设立以来回报率(%)` from `公募基金净值最新区间表现` as a join `公募基金概况` as b on a.`证券内部编码` = b.`基金内部编码` and b.`基金类别` ='债券型' ;	ccks_fund
select `分红股本基数(股)`, `派现(含税/人民币元)` from `公司分红`  where `中文名称缩写` ='深科技' and strftime('%Y', `分红实施公告日`) > strftime('%Y', DATE('now', '-3 year'));	ccks_stock
select `基金简称` from `公募基金重仓股票组合` where `股票简称` = '海康威视'	ccks_fund
select `截止日期`,  `金额(亿元)` from `金融机构新增贷款`  where `统计区间` ='期末累计' and `金额(亿元)` > 150000 and strftime('%Y', `截止日期`)>='2000';	ccks_macro
select  `所属基金/股票代码` from `公司分红`  where `送股比例(10送X)` > 0.5 and strftime('%Y', `分红实施公告日`) = strftime('%Y', DATE('now', '-1 year'));	ccks_stock
select `中文名称缩写` from `利润分配表附注_财务费用` order by `手续费(元)` desc limit 1	ccks_stock
select `截止日期`, `总资产`  from `其他存款性公司资产负债表` order by `总资产` desc limit 1;	ccks_macro
select b.`证券简称`,a.`本周以来基金基准增长率(%)` from `公募基金最新基准收益率` as a join `公募基金概况` as b on a.`基金内部编码`=b.`基金内部编码`   where b.`基金运作方式`='LOF';	ccks_fund
select  `最高比率(%)` from `税率表` where `税率类别` ='中资大型银行' and `税率项目` = '超额存款准备金率'  ;	ccks_macro
select `单位存款/企业存款` from `中国金融机构人民币信贷收支表`;	ccks_macro
select b.`证券简称` from `公募基金最新基准收益率` as a join `公募基金概况` as b on a.`基金内部编码`=b.`基金内部编码`  where b.`基金运作方式`='LOF' and a.`本月以来基金基准增长率(%)`>0;	ccks_fund
select `进口商品总额(百万美元)` , `出口商品总额(百万美元)` from `海关进出口`  where `进口商品总额(百万美元)` < 20 and `出口商品总额(百万美元)` > 40 and strftime('%Y', `截止日期`) > strftime('%Y', DATE('now', '-3 year'));	ccks_macro
select b.`中文名称缩写` from `配股大股东认配状况` as a join `公司概况` as b on a.`公司代码`=b.`公司代码`  where b.`省份`='福建省' and a.`应配股数(股)`>1000000;	ccks_stock
select `国内信贷`, `外币存款` from `中国货币与银行概览` where strftime('%Y', `截止日期`)>='2005';	ccks_macro
select `股东名称` from `配股大股东认配状况` where `中文名称缩写`='浙大网新' order by `实配股数(股)` desc limit 1;	ccks_stock
select a.`平均管理规模同类排名` from `公募基金衍生指标_基金经理最新收益与规模排名` as a join `公募基金经理基本资料` as b on a.`基金经理代码` = b.`所属人员编码` where b.`最高学历` = '本科'	ccks_fund
select `费率类别描述`, `费率描述` from `公募基金费率(新)` where `基金简称` ='南方天元' ;	ccks_fund
select `股权登记日` , `派现(含税/人民币元)` from `公司分红` where `派现(含税/人民币元)` > 5 and `中文名称缩写` = '古井贡酒';	ccks_stock
select a.`姓名` from `公募基金经理(新)` as a join `公募基金经理基本资料` as b on a.`所属人员代码` = b.`所属人员编码` where a.`任职天数` > 200 and b.`最高学历` = '博士'	ccks_fund
select a.`中文名称缩写`, b.`领导姓名`, b.`职位描述` from `股东股权变动` as a join `公司报告期管理层持股` as b on a.`公司代码` = b.`公司代码` order by a.`出让前持股比例` desc limit 5	ccks_stock
select a.`姓名`, b.`证券从业日期` from `基金经理历任收益风险指标(全)` as a join `公募基金经理基本资料` as b on a.`基金经理代码` = b.`所属人员编码` where a.`指标周期` = '三年' order by a.`卡玛比率(未填充)` desc limit 10	ccks_fund
select `一级行业名称`, `二级行业名称` from `公司行业划分表` where `中文名称缩写` = '西藏发展'	ccks_stock
select b.`基金运作方式`, count(*) from `公募基金最新收益率排名` as a join `公募基金概况` as b on a.`基金内部编码` = b.`基金内部编码` where a.`指标周期` = '六个月' and a.`同类基金收益率均值(%)` < 0 group by b.`基金运作方式`	ccks_fund
select `中文名称缩写`, avg(`成交金额(元)`) from `日行情表`  where strftime('%Y', `交易日`)='2021' and round(strftime('%m',`交易日`)/3.0 + 0.495) = 4 group by  `中文名称缩写`;	ccks_stock
select `本月以来基金基准增长率(%)` from `公募基金最新基准收益率` where `基金简称`='交银治理ETF';	ccks_fund
select `单位净值(元)`, `单位累计净值(元)`, `基金升贴水率` from `公募基金净值` where `基金简称` = '华安180ETF' ;	ccks_fund
select `货币和准货币(广义货币M2)`, `货币(狭义货币M1)`, `准货币` from `中国货币与银行概览`  where strftime('%Y', `截止日期`) > strftime('%Y', DATE('now', '-2 year')) ;	ccks_macro
select b.`基金经理姓名`,b.`出生日期` from `基金经理规模统计(新)` as a join `公募基金经理基本资料` as b on a.`基金经理代码`=b.`所属人员编码` order by a.`债券型管理规模(亿元)` desc limit 10;	ccks_fund
select `基金简称` from `公募基金主要财务指标(季报)`  where strftime('%Y', `截止日期`)='2021' and round(strftime('%m',`截止日期`)/3.0 + 0.495) = 1 and `期末基金资产净值` > 10000000000	ccks_fund
select a.`二级行业名称`, count(*) from `公司行业划分表` as a join `自由流通股本` as b on a.`公司代码` = b.`公司代码`  where b.`流通A股(股)` > 10000000000 and strftime('%Y', `股本变动日期`)='2019' group by  a.`二级行业名称`	ccks_stock
select b.`国籍`, count(*) from `公募基金衍生指标_基金经理收益与规模同类分析` as a join `公募基金经理基本资料` as b on a.`基金经理代码` = b.`所属人员编码` where a.`平均规模(亿元)` > 500 group by b.`国籍`	ccks_fund
select `货币和准货币(广义货币M2)`, `货币(狭义货币M1)`, `准货币` from `中国货币与银行概览`  where strftime('%Y', `截止日期`)<'1995';	ccks_macro
select `中文名称缩写`, `交易日` from `日行情表` where `成交金额(元)` > 1000000000;	ccks_stock
select `中文名称缩写` from `公司概况` where `法人代表`='张利忠';	ccks_stock
select `其他国外资产(百万元)`, `其他负债(百万元)` from `货币当局资产负债表` ;	ccks_macro
select `单位净值(元)`, `开放式基金单位基金净值日增长率` from  `公募基金净值`  where round(strftime('%m',`截止日期`)/3.0 + 0.495) = round(strftime('%m',date()) / 3.0 + 0.495) and `基金简称` ='华安石油A' ;	ccks_fund
select `所属城市`,count(*) from `公司概况` where `省份`='陕西省' group by `所属城市` order by count(*) desc limit 1;	ccks_stock
select `基金简称`,`持有数量(张)` from `公募基金债券组合明细` where `债券简称`='温氏转债';	ccks_fund
select `领导姓名`, `职位描述` from `公司报告期管理层持股` where `中文名称缩写` = '依米康'	ccks_stock
select `公司中文名称` from `企业之间参股情况`  where `中文名称缩写` = '航天发展' and strftime('%Y', `截止日期`)='2020' and strftime('%m', `截止日期` )='8'	ccks_stock
select `申赎确认日` from `公募基金概况` where `证券简称` = '招商成长'	ccks_fund
select a.`同类经理收益率排名` from `公募基金衍生指标_基金经理最新收益与规模排名` as a join `公募基金经理基本资料` as b on a.`基金经理代码` = b.`所属人员编码` where b.`证券从业经历(年)` > 10	ccks_fund
select `截止日期`, `国外净资产` from `中国货币与银行概览` where `国外净资产` > 1000000;	ccks_macro
select `基金经理姓名`,`总管理基金规模排名` from `基金经理规模统计(新)`;	ccks_fund
select `保荐机构` from `A股发行申报企业信息` where `会计师事务所`='立信会计事务所';	ccks_stock
select avg(`一年回报率(%)`) from `公募基金净值最新区间表现`;	ccks_fund
select `外汇(百万元)`, `货币黄金(百万元)`, `其他国外资产(百万元)` from `货币当局资产负债表` where `总资产(百万元)` > 10;	ccks_macro
select `领导姓名`, `职位描述` from `公司报告期管理层持股` where `中文名称缩写` = '福星股份' and `领导姓名` like '%谭%'	ccks_stock
select `财政借款`, `财政性存款` from `中国金融机构人民币信贷收支表`  where strftime('%Y', `截止日期`) > strftime('%Y', DATE('now', '-2 year')) ;	ccks_macro
select b.`证券简称`, b.`风险等级` from `公募基金经理(新)` as a join `公募基金风险等级表` as b on a.`基金内部编码` = b.`基金内部代码` where strftime('%Y', a.`离职日期`)<'2020'	ccks_fund
select a.`所属基金/股票代码`, b.`省份`, b.`所属城市` from `公司经营范围与行业变更` as a join `公司概况` as b on a.`公司代码` = b.`公司代码` where a.`行业名称` ='专业技术服务业';	ccks_stock
select `股东总户数(户)`,`户均持股数(股/户)` from `股东户数`  where `中文名称缩写`='新天然气' and strftime('%Y', `截止日期`)='2016';	ccks_stock
select `截止日期`,  `金额(亿元)`, `同比增减(%)` from `金融机构新增贷款`  where `统计区间` ='月份' and `金额(亿元)` > 100000 and strftime('%Y', `截止日期`) = strftime('%Y', DATE('now', '-2 year'));	ccks_macro
select b.`中文名称缩写` from `公司概况` as a join `公司股本结构变动` as b on a.`公司代码` = b.`公司代码` where a.`省份` = '上海市' and b.`流通A股(股)` > 10000000	ccks_stock
select `中文名称缩写`, `获配金额(元)` from `法人配售与战略投资者`  where `获配企业名称(披露)` ='广发估值优势混合型证券投资基金' and strftime('%Y', `信息发布日期`) = strftime('%Y', DATE('now', '-1 year')) ;	ccks_stock
select `国籍描述` from `公司实际控制人` group by `国籍描述` order by count(*) desc limit 3;	ccks_stock
select `基金公司中文简称` from `公募基金衍生指标_基金公司收益与规模同类均值与排名` where `基金类别描述`='债券型' order by `总管理规模同类排名` limit 10;	ccks_fund
select a.`姓名`, b.`证券从业日期` from `公募基金衍生指标_基金经理最新收益与规模排名` as a join `公募基金经理基本资料` as b on a.`基金经理代码` = b.`所属人员编码` where a.`时间区间` = '近1天' order by a.`平均管理规模同类均值(亿元)` desc limit 1	ccks_fund
select `基金经理姓名`, `债券型基金数量(只)`, `债券型管理规模(亿元)` from `基金经理规模统计(新)` order by `债券型管理规模(亿元)` desc limit 1;	ccks_fund
select `单位基金净值周增长率` from  `公募基金净值` where `基金代码` = '510220';	ccks_fund
select `截止日期`, `单位净值(元)` from `公募基金净值` where `基金简称` = '泰达效率';	ccks_fund
select b.`基金类别`, count(*) from `公募基金净值最新区间表现` as a join `公募基金概况` as b on a.`证券内部编码` = b.`基金内部编码` where a.`设立以来年化回报率(%)` > 10 group by b.`基金类别`;	ccks_fund
select `领导姓名`, `中文名称缩写` from `公司报告期管理层持股` where `职位描述` like '%董事长%' and `职位描述` like '%总裁%'	ccks_stock
select `中文名称缩写`, `所属基金/股票代码` from `法人配售与战略投资者`  where strftime('%Y', `信息发布日期`) = strftime('%Y', DATE('now', '-1 year')) ;	ccks_stock
select `中文名称缩写` from `限售股票解禁时间表` where `本次新增可售A股(万股)` <= 1000	ccks_stock
select count(distinct `基金公司代码`) from `公募基金获奖情况` ;	ccks_fund
select `截止日期`, `工业增加值(百万元)` from `工业生产` where `统计区域类别` ='全国' and `统计口径` ='全部工业企业' and `数据统计区间` ='月度';	ccks_macro
select `截止日期`, `工业总产值(现价)(百万元)` from `工业生产` where `统计区域类别` ='全国' and `统计口径` ='全部工业企业' and `数据统计区间` ='月度';	ccks_macro
select count(*) from `公司经营范围与行业变更` as a join `公司概况` as b on a.`公司代码` = b.`公司代码` where b.`省份` = '江苏省' and a.`行业名称` ='农副食品加工业';	ccks_stock
select `截止日期`, `外汇(百万元)`, `货币黄金(百万元)`, `其他国外资产(百万元)` from `货币当局资产负债表` where `总资产(百万元)` < 10;	ccks_macro
select `批发零售贸易业`, `餐饮业` from `社会消费品零售总额`  where `省市`='上海' and `数据统计期间` ='年度' and strftime('%Y', `截止日期`)='2004';	ccks_macro
select a.`一级行业名称`, count(*) from `公司行业划分表` as a join `公司股本结构变动` as b on a.`公司代码` = b.`公司代码` where b.`无限售条件流通A股(股)(披露)`  > 10000000000 group by a.`一级行业名称`	ccks_stock
select a.`所属城市` , count(*)  from `公司概况` as a join `概念所属公司表` as b on a.`公司代码` = b.`公司代码` where b.`概念名称` ='大数据' group by a.`所属城市` ;	ccks_stock
select `省份` from `公司概况`  where strftime('%Y', `公司成立日期`)='2000' group by  `省份` order by count(*) desc limit 1;	ccks_stock
select a.`行业名称`, count(*) from `公司经营范围与行业变更` as a join `公司概况` as b on a.`公司代码` = b.`公司代码` where b.`省份` = '江苏省' group by a.`行业名称` ;	ccks_stock
select `基金简称` from `公募基金债券组合明细` where `债券代码`='200203' order by `持有数量(张)` limit 1;	ccks_fund
select `中文名称缩写` from `公司概况` where `省份`='山东省';	ccks_stock
select `公司中文名称` from `股东户数`  where strftime('%Y', `截止日期`)='2016' order by  `股东总户数(户)` desc limit 1;	ccks_stock
select `本月以来回报率(%)`, `一个月回报率(%)` from `公募基金净值最新区间表现` where `基金简称` = '天弘恒享';	ccks_fund
select `数据统计期间`,  `指数` from `工业品出厂价格指数` where  `指数类别` ='国民经济行业指数' and `指数名称` ='金属制品业';	ccks_macro
select `工业增加值(百万元)` from `工业生产`  where `省市` ='上海' and `统计口径` ='全部工业企业' and `数据统计区间` ='年度' and strftime('%Y', `截止日期`)='2000';	ccks_macro
select count(*) from `股份回购`  where `回购总金额(元)` >= 100000000 and strftime('%Y', `预案公布日`) = strftime('%Y', DATE('now', '-1 year'));	ccks_stock
select count(*) from `股东股权变动` where `出让前持股比例` > 0.2	ccks_stock
select b.`中文名称缩写`, b.`实际控制人` from `公司概况` as a join `公司实际控制人` as b on a.`公司代码` = b.`公司代码` where a.`所属城市` = '杭州市';	ccks_stock
select `六个月回报率(%)` from  `公募基金净值最新区间表现` ;	ccks_fund
select `实收资本` from `其他存款性公司资产负债表` ;	ccks_macro
select `中文名称缩写` from `限售股票解禁时间表` where `已流通A股占A股总数比例(%)` > 50	ccks_stock
select `债券简称` from `公募基金债券组合明细` where `基金简称`='中银中国A';	ccks_fund
select a.`中文名称缩写` from `限售股票解禁时间表` as a join `公司行业划分表` as b on a.`公司代码` = b.`公司代码` where b.`一级行业名称` = '制造业' order by a.`本次新增可售A股占上期末已流通A股比例(%)` desc limit 1	ccks_stock
select count(*) from `公募基金获奖情况` ;	ccks_fund
select `中文名称缩写`, `增发目的` from `A股增发`  where strftime('%Y', `预案公布日期`)='2021';	ccks_stock
select `国内生产总值(百万元)` from `国内生产总值` ;	ccks_macro
select count(*) from `基金经理规模统计(新)` where `总管理规模(亿元)` > 500;	ccks_fund
select count(*) from `法人配售与战略投资者`  where strftime('%Y', `信息发布日期`) = strftime('%Y', DATE('now', '-1 year'));	ccks_stock
select `基金名称` from `公募基金获奖情况` where `奖项名称` = '中国股票型对冲基金奖提名' and `评奖单位` ='晨星资讯';	ccks_fund
select `所属行业/领域` from `A股发行申报企业信息` where `中文名称缩写`='红塔证券';	ccks_stock
select b.`基金运作方式`, count(*) from `公募基金最新收益率排名` as a join `公募基金概况` as b on a.`基金内部编码` = b.`基金内部编码` where a.`指标周期` = '一年' and a.`基金收益率(%)` < 0 group by b.`基金运作方式`	ccks_fund
select `截止日期`, `社会消费品零售总额(百万元)` from `社会消费品零售总额`  where `统计区域类别` ='全国' and `数据统计期间` ='年度' and strftime('%Y', `截止日期`) > strftime('%Y', DATE('now', '-3 year')) ;	ccks_macro
select a.`概念名称`, count(*) from `概念所属公司表` as a join `公司概况` as b on a.`公司代码` = b.`公司代码` where b.`省份` ='广东省' group by a.`概念名称` having count(*)>4  ;	ccks_stock
select `债券简称` from `公募基金债券组合明细` where `基金代码`='160611';	ccks_fund
select `基金投资风格`,count(*) from `公募基金概况` group by `基金投资风格`;	ccks_fund
select `股东名称`, `股东持股比例` from `企业之间参股情况`  where `中文名称缩写` = '农发种业' and strftime('%Y', `截止日期`)='2019' ;	ccks_stock
select  `所属基金/股票代码` from `企业之间参股情况`  where `股东名称` ='万安集团有限公司' and strftime('%Y', `截止日期`) = strftime('%Y', DATE('now', '-1 year'));	ccks_stock
select b.`证券简称`,b.`基金管理人` from `公募基金债券组合明细` as a join `公募基金概况` as b on a.`基金内部编码`=b.`基金内部编码` where a.`债券简称`='21国债06' order by a.`占资产净值比例` desc limit 1;	ccks_fund
select `基金管理人简称` from `公募基金管理人概况` order by `注册资本(元)` desc limit 3;	ccks_fund
select a.`省份` , count(*)  from `公司概况` as a join `概念所属公司表` as b on a.`公司代码` = b.`公司代码` where b.`概念名称` ='芯片概念' group by a.`省份` having count(*)>5;	ccks_stock
select count(*) from `公司经营范围与行业变更` where `行业名称` like '%计算机%' or `行业名称` like '%通信%' or `行业名称` like '%电信%'	ccks_stock
select b.`基金投资类型`,count(*) from `公募基金最新基准收益率` as a join `公募基金概况` as b on a.`基金内部编码`=b.`基金内部编码` where a.`今年以来基金基准增长率(%)`<0 group by b.`基金投资类型`;	ccks_fund
select count(*) from `公募基金衍生指标_基金经理收益与规模同类分析` as a join `公募基金经理基本资料` as b on a.`基金经理代码` = b.`所属人员编码` where a.`总规模(亿元)` > 100 and b.`最高学历` = '本科'	ccks_fund
select avg(b.`总管理规模(亿元)`) from `公募基金经理基本资料` as a join `基金经理规模统计(新)` as b on a.`所属人员编码` = b.`基金经理代码` where a.`证券从业经历(年)` > 15;	ccks_fund
select `截止日期`, `省市`, `工业总产值(现价)(百万元)` from `工业生产` where `统计区域类别` ='省市' and `统计口径` ='全部工业企业' and `数据统计区间` ='期末累计'  ;	ccks_macro
select `费率最高值`, `费率最低值` from `公募基金费率(新)` where `基金简称` ='南方天元';	ccks_fund
select b.`基金运作方式`, count(*) from `公募基金最新收益率排名` as a join `公募基金概况` as b on a.`基金内部编码` = b.`基金内部编码` where a.`指标周期` = '一个月' and a.`基金收益率(%)` > 0 group by b.`基金运作方式`	ccks_fund
select a.`配售总股数(股/份/张)` from `法人配售与战略投资者` as a  where strftime('%Y', a.`信息发布日期`)='2020' and strftime('%m', a.`信息发布日期`)='3' and a.`中文名称缩写` ='国网英大'	ccks_stock
select `第三产业(百万元)` from `国内生产总值` ;	ccks_macro
select `费用化研发投入(元)`,`资本化研发投入(元)` from `公司研发投入与产出`  where strftime('%Y', `截止日期`)=strftime('%Y', DATE('now', '-1 year')) and `中文名称缩写`='深科技';	ccks_stock
select count(*) from `公司报告期管理层持股` where  `中文名称缩写` = '拓维信息' and `职位描述` like '%董事%'	ccks_stock
select a.`姓名`, a.`证券简称` from `公募基金经理(新)` as a join `公募基金经理基本资料` as b on a.`所属人员代码` = b.`所属人员编码` where b.`最高学历` = '本科'	ccks_fund
select count(*) from `限售股票解禁时间表` where `已流通A股(万股)` > 1000	ccks_stock
select a.`发行对象`, b.`总经理`, b.`法人代表` from `A股增发` as a join `公司概况` as b on a.`公司代码` = b.`公司代码` where a.`中文名称缩写` = '晶盛机电';	ccks_stock
select b.`基金经理姓名`,b.`出生日期` from `基金经理规模统计(新)` as a join `公募基金经理基本资料` as b on a.`基金经理代码`=b.`所属人员编码` where a.`债券型基金数量(只)`>3;	ccks_fund
select count(*) from `公司主营业务构成`  where `主营业务收入(元)` > 100000000 and strftime('%Y', `截止日期`)>='2019';	ccks_stock
select `风险等级` from `公募基金风险等级表` where `证券简称` = '国金50'	ccks_fund
select `中文名称缩写` from `公司实际控制人` where `实际控制人` = '中国烟草总公司';	ccks_stock
select `领导姓名` from `公司报告期管理层持股` where `中文名称缩写` = '恒宝股份' and `职位描述` like '%副总裁%'	ccks_stock
select a.`行业名称` , count(*) from `公司经营范围与行业变更` as a join `公司概况` as b on a.`公司代码` = b.`公司代码`  where strftime('%Y', b.`公司成立日期`)='2020' group by  a.`行业名称` ;	ccks_stock
select `中文名称缩写` from `自由流通股本` order by `流通A股(股)` desc limit 5	ccks_stock
select `基金简称`, `基金代码`  from `公募基金主要财务指标(季报)`  where strftime('%Y', `截止日期`)='2021' group by  `基金简称` order by sum(`基金本期利润`) desc limit 10	ccks_fund
select `所属行业/领域` from `A股发行申报企业信息` group by `所属行业/领域` order by count(*) asc, min(`序号`) asc limit 10;	ccks_stock
select a.`省份` from `公司概况` as a join `公司股本结构变动` as b on a.`公司代码` = b.`公司代码` where b.`未流通A股(股)` > 200000000 group by a.`省份` having count(*) > 10	ccks_stock
select b.`所属城市`, count(*) from `限售股票解禁时间表` as a join `公司概况` as b on a.`公司代码` = b.`公司代码` where a.`本次新增可售A股(万股)` > 100 group by b.`所属城市`	ccks_stock
select `基金简称` from `公募基金最新基准收益率` where `本周以来基金基准增长率(%)`<0 order by `本周以来基金基准增长率(%)` limit 10;	ccks_fund
select a.`姓名` from `公募基金经理(新)` as a join `公募基金风险等级表` as b on a.`基金内部编码` = b.`基金内部代码` where b.`风险等级` = '中低' group by a.`姓名` having count(a.`证券简称`) > 5	ccks_fund
select `一周回报率(%)` from  `公募基金净值最新区间表现` ;	ccks_fund
select `进口同比增减`, `出口同比增减` from `海关进出口` ;	ccks_macro
select `券商持有A股比例(%)` from `股东持股统计`  where strftime('%Y', `截止日期`)='2020' and strftime('%m', `截止日期`)='2' and `中文名称缩写`='重庆建工';	ccks_stock
select `截止日期`, `单位净值(元)` from  `公募基金净值`  where strftime('%Y', `截止日期`) > strftime('%Y', DATE('now', '-2 year')) and `基金简称` ='华安石油A' ;	ccks_fund
select `中文名称缩写` from `自由流通股本` where `A股总股本(股)` > 1000000000 order by `自由流通比例(归档后)(%)` desc	ccks_stock
select avg(`旗下基金总数(只)`) from `基金经理规模统计(新)`;	ccks_fund
select a.`省份` from `公司概况` as a join `公司行业划分表` as b on a.`公司代码` = b.`公司代码` where b.`一级行业名称` = '批发和零售业' group by a.`省份` having count(*) > 3	ccks_stock
select `中文名称缩写` from `公司概况` where `董事会秘书`='冯莉';	ccks_stock
select `已流通A股(万股)`, `待流通A股(万股)` from `限售股票解禁时间表` where `中文名称缩写` = '通富微电' or `中文名称缩写` = '海亮股份'	ccks_stock
select `增发目的` from `A股增发` where `中文名称缩写` = '京能置业';	ccks_stock
select a.`基金简称`,a.`本日基金基准增长率(%)` from `公募基金最新基准收益率` as a join `公募基金概况` as b on a.`基金内部编码`=b.`基金内部编码`   where b.`基金类别`='股票型';	ccks_fund
select `证券从业经历(年)` from `公募基金经理基本资料` where `基金经理姓名` = '蒋一茜';	ccks_fund
select `国内生产总值(百万元)`, `人均国内生产总值(元/人)` from `国内生产总值` ;	ccks_macro
select `债券简称`,`市值(元)`,`占资产净值比例` from `公募基金债券组合明细` where `基金代码`='159901';	ccks_fund
select `毛利率` from `公司主营业务构成`  where strftime('%Y', `截止日期`) = strftime('%Y', DATE('now', '-1 year')) and `中文名称缩写` ='冰山冷热';	ccks_stock
select b.`最高学历`, count(*) from `基金经理任职及管理年限统计` a join `公募基金经理基本资料` b on a.`基金经理代码` = b.`所属人员编码` where a.`基金管理人名称` like '富国基金%' and a.`是否在任` = '是'  group by b.`最高学历`	ccks_fund
select `一年回报率(%)` from `公募基金净值最新区间表现` ;	ccks_fund
select `本周以来回报率(%)`, `一周回报率(%)` from `公募基金净值最新区间表现` where `基金简称` = '银华纯债';	ccks_fund
select count(*) from `公募基金最新基准收益率` as a join `公募基金概况` as b on a.`基金内部编码`=b.`基金内部编码` where a.`本月以来基金基准增长率(%)`>3 and b.`基金运作方式`='ETF';	ccks_fund
select `机构全称`,`承销金额(元)` from `发行与上市中介机构` where `中文名称缩写`='南华生物';	ccks_stock
select `截止日期`, `金额(亿元)` from `金融机构新增贷款`;	ccks_macro
select `送股比例(10送X)`, `派现(含税/人民币元)` from `公司分红`  where `所属基金/股票代码` ='000752' and strftime('%Y', `分红实施公告日`) = strftime('%Y', DATE('now', '-1 year')) ;	ccks_stock
select `股权被冻结质押股东名称`, `占冻结质押方持股数比例` from `股东股权冻结和质押`  where strftime('%Y', `冻结质押期限截止日`) = strftime('%Y', DATE('now', '-1 year'));	ccks_stock
select `本日基金基准增长率(%)` from `公募基金最新基准收益率` where `基金代码`='512500';	ccks_fund
select `设立以来回报率(%)`, `设立以来年化回报率(%)` from `公募基金净值最新区间表现` ;	ccks_fund
select `今年以来回报率(%)` from `公募基金净值最新区间表现` ;	ccks_fund
select `中文名称缩写` from `A股增发` order by `预计募集资金总额(元)` desc limit 1;	ccks_stock
select b.`中文名称缩写` from `发行与上市中介机构` as a join `公司概况` as b on a.`公司代码`=b.`公司代码`  where b.`省份`='辽宁省' and a.`承销数量(股)`>1000000 and a.`承销金额(元)`>10000000;	ccks_stock
select `领导姓名` from `公司报告期管理层持股`  where `中文名称缩写` = '科拓生物' and strftime('%Y', `截止日期`)='2020'	ccks_stock
select `获配企业名称(披露)` from `法人配售与战略投资者`  where `所属基金/股票代码` = '603059' and strftime('%Y', `信息发布日期`) = strftime('%Y', DATE('now', '-1 year')) and strftime('%m', `信息发布日期`)='4' order by  `获配金额(元)` desc limit 10 ;	ccks_stock
select a.`概念名称`, count(*) from `概念所属公司表` as a join `公司概况` as b on a.`公司代码` = b.`公司代码` where b.`所属城市` ='南京市' group by a.`概念名称` ;	ccks_stock
select `城市维护建设费(百万元)`, `文教科学卫生事业费(百万元)` from `财政收支` where `省市` ='四川';	ccks_macro
select `截止日期`, `进口商品总额(百万美元)` , `出口商品总额(百万美元)` from `海关进出口`  where `出口同比增减` > 0 and `出口商品总额(百万美元)` > 40 and strftime('%Y', `截止日期`) > strftime('%Y', DATE('now', '-10 year'));	ccks_macro
select `省市` from `国内生产总值`  where strftime('%Y', `截止日期`) = strftime('%Y', DATE('now', '-1 year')) order by  `第一产业(百万元)` desc limit 10;	ccks_macro
select `股东名称` from `企业之间参股情况`  where `股东持股数量` > 10000000 and `所属基金/股票代码` ='600110' and strftime('%Y', `截止日期`) = strftime('%Y', DATE('now', '-1 year'));	ccks_stock
select `所属基金/股票代码`, `股东持股数量`, `股东投资金额` from `企业之间参股情况` where `股东名称` ='顾瑜';	ccks_stock
select `三年年化回报率(%)` from `公募基金净值最新区间表现` ;	ccks_fund
select `基金简称` from `公募基金债券组合明细` where `债券简称`='20国债10';	ccks_fund
select `证券简称` from `公募基金概况`  where `基金管理人`='易方达基金管理有限公司' and `基金类别`='股票型' and strftime('%Y', `设立日期`)='2021';	ccks_fund
select `截止日期`, `总负债(百万元)` from `货币当局资产负债表`  order by `总负债(百万元)`  desc ;	ccks_macro
select `证券简称`, `基金管理人` from `公募基金概况` order by `设立日期` asc limit 1	ccks_fund
select `派现(含税/人民币元)`, `实派(税后/人民币元)` from `公司分红`  where `中文名称缩写` ='古井贡酒' and strftime('%Y', `分红实施公告日`) = strftime('%Y', DATE('now', '-1 year')) ;	ccks_stock
select a.`所属城市`, count(*) from `公司概况` as a join `公司股本结构变动` as b on a.`公司代码` = b.`公司代码` where b.`无限售条件流通A股(股)(披露)` > 10000000000 group by a.`所属城市`	ccks_stock
select `三年年化回报率(%)` from `公募基金净值最新区间表现` ;	ccks_fund
select a.`实配股数(股)`,a.`应配股数(股)` from `配股大股东认配状况` as a join `公司概况` as b on a.`公司代码`=b.`公司代码`  where b.`省份`='广西省';	ccks_stock
select `金融债券`, `股权及其他投资` from `中国金融机构人民币信贷收支表`;	ccks_macro
select `国内生产总值(百万元)`, `人均国内生产总值(元/人)` from `国内生产总值` where `省市` ='山东' ;	ccks_macro
select b.`中文名称缩写` from `公司研发投入与产出` as a join `公司概况` as b on a.`公司代码`=b.`公司代码`  where b.`省份`='广东省' order by a.`研发人员数量占比(%)` desc, a.`研发投入占营业收入比例(%)` desc limit 10;	ccks_stock
select `利息支出(元)` from `利润分配表附注_财务费用`  where `中文名称缩写` = '再升科技' or `中文名称缩写` = '蓝思科技' and strftime('%Y', `截止日期`)='2017'	ccks_stock
select `债券简称` from `公募基金债券组合明细` where `基金简称`='易方达中盘ETF' order by `占资产净值比例` desc limit 1;	ccks_fund
select a.`省份` , count(*)  from `公司概况` as a join `概念所属公司表` as b on a.`公司代码` = b.`公司代码` where b.`概念名称` ='大飞机' group by a.`省份` ;	ccks_stock
select `三个月回报率(%)` from `公募基金净值最新区间表现` where `基金简称` = '诺德债券';	ccks_fund
select `公司成立日期` from `公司概况` where `中文名称缩写`='华昌达';	ccks_stock
select `所属基金/股票代码` , `股东投资金额` from `企业之间参股情况`  where `股东名称` ='万安集团有限公司' and strftime('%Y', `截止日期`) = strftime('%Y', DATE('now', '-2 year'));	ccks_stock
select `中文名称缩写` from `A股增发`  where strftime('%Y', `预案公布日期`)='2022';	ccks_stock
select `总股本(股)`, `A股(股)` from `公司股本结构变动` where `所属基金/股票代码` = '600371'	ccks_stock
select `截止日期`, `轻工业(百万元)` from `工业生产` where `统计区域类别` ='全国' and `统计口径` ='国有及规模以上工业企业' and `数据统计区间` ='期末累计';	ccks_macro
select count(a.`姓名`) from `公募基金经理(新)` as a join `公募基金经理基本资料` as b on a.`所属人员代码` = b.`所属人员编码` where b.`最高学历` = '博士' and b.`性别` = '男'	ccks_fund
select `预案公布日期`, `增发目的`, `发行对象` from `A股增发` where `中文名称缩写` = '大业股份';	ccks_stock
select `基金简称` from `公募基金最新收益率排名` where `基金类别描述` = '股票型' and `基金年化收益率(%)` > 0	ccks_fund
select `签字会计师`,`签字律师` from `A股发行申报企业信息` where `中文名称缩写`='华纳百录';	ccks_stock
select `中文名称缩写` , `回购总金额(元)` from `股份回购`  where (`中文名称缩写` = '会稽山' or `中文名称缩写` = '宝钢股份') and strftime('%Y', `预案公布日`)='2020' ;	ccks_stock
select `中文名称缩写` from `利润分配表附注_财务费用` order by `汇兑损益` desc limit 20	ccks_stock
select `基金类别描述` from `公募基金衍生指标_基金公司收益与规模同类均值与排名` where `基金公司中文简称`='中信证券' order by `总管理规模同类排名` desc limit 1;	ccks_fund
select b.`证券简称`,b.`基金经理` from `公募基金债券组合明细` as a join `公募基金概况` as b on a.`基金内部编码`=b.`基金内部编码` where a.`债券简称`='百润转债' order by a.`市值(元)` desc limit 1;	ccks_fund
select count(*) from `法人配售与战略投资者`  where `配售股数(股/份/张)` < 10000 and strftime('%Y', `信息发布日期`) = strftime('%Y', DATE('now', '-1 year'));	ccks_stock
select `基金简称` from `公募基金最新基准收益率` where `七年基金基准增长率(%)`>200;	ccks_fund
select `费率划分标准范围Ⅰ起始数值`, `费率划分标准范围Ⅰ截止数值` from `公募基金费率(新)` where `费率类别描述` ='指数许可费';	ccks_fund
select `股票简称`, count(*) from `公募基金重仓股票组合` where `股票简称` = '宁德时代' or `股票简称` = '贵州茅台' group by `股票简称`	ccks_fund
select b.`证券简称`, b.`风险等级` from `公募基金经理(新)` as a join `公募基金风险等级表` as b on a.`基金内部编码` = b.`基金内部代码` where a.`任职天数` > 1000	ccks_fund
select `合营单位`, `个体单位` from `社会消费品零售总额` where `省市` ='浙江' and `数据统计期间` ='年度';	ccks_macro
select b.`证券简称`,b.`基金类别`,b.`基金经理` from `公募基金最新基准收益率` as a join `公募基金概况` as b on a.`基金内部编码`=b.`基金内部编码` where a.`十年基金基准增长率(%)`>50;	ccks_fund
select `公司中文名称` from `股东股权冻结和质押`  where strftime('%Y', `冻结质押期限截止日`)='2018' and strftime('%m', `冻结质押期限截止日`)='5' order by  `涉及股数(股)` desc limit 10	ccks_stock
select count(*) from `公募基金债券组合明细` where `基金简称`='华夏50ETF';	ccks_fund
select  `股权被冻结质押股东名称` from `股东股权冻结和质押`  where strftime('%Y', `冻结质押期限截止日`) > strftime('%Y', DATE('now', '-3 year'));	ccks_stock
select count(*) from `公募基金经理(新)` where `在任与否` = '在任' and `职位名称` = '基金经理助理'	ccks_fund
select b.`基金经理姓名`, b.`总管理规模(亿元)`, b.`股票型管理规模(亿元)`, b.`混合型管理规模(亿元)` from `公募基金经理基本资料` as a join `基金经理规模统计(新)` as b on a.`所属人员编码` = b.`基金经理代码` where a.`国籍` != '中国';	ccks_fund
select `增发目的` from `A股增发` where `中文名称缩写` = '京能置业';	ccks_stock
select b.`基金类别` from `公募基金净值最新区间表现` as a join `公募基金概况` as b on a.`证券内部编码` = b.`基金内部编码` group by b.`基金类别` having avg(a.`一年回报率(%)`) > 1;	ccks_fund
select `所属基金/股票代码`, `流通股本(股)` from `股票月度行情数据` where `所属基金/股票代码` = '600168' or `所属基金/股票代码` = '000422';	ccks_stock
select `公司网址` from `公司概况` where `中文名称缩写`='万科';	ccks_stock
select `基金经理` , `奖项名称` from `公募基金获奖情况` where `评奖单位` = '证券时报';	ccks_fund
select b.`基金经理`,b.`基金管理人` from `基金经理规模统计(新)` as a join `公募基金概况` as b on a.`基金经理姓名`=b.`基金经理` order by a.`旗下基金总数(只)` desc limit 1;	ccks_fund
select `回购价格(元/股)`, `回购股数(股)` from `股份回购`  where `中文名称缩写` = '南都电源' and strftime('%Y', `预案公布日`)='2021'	ccks_stock
select `总股本(股)`, `市净率`, `市盈率TTM` from `股票月度行情数据` where `所属基金/股票代码` = '000935';	ccks_stock
select a.`基金经理姓名`, b.`背景介绍` from `公募基金衍生指标_基金经理收益与规模同类分析` as a join `公募基金经理基本资料` as b on a.`基金经理代码` = b.`所属人员编码` where a.`收益率(%)` > 0 and a.`时间区间` = '近10年'	ccks_fund
select `基金名称` from `公募基金获奖情况` where strftime('%Y', `获奖年度`) >=2015 and `奖项名称` ='投资基金';	ccks_fund
select  `适用客户类型` from `公募基金费率(新)` where `基金代码` ='160133';	ccks_fund
select `出口商品总额(百万美元)`, `出口同比增减` from `海关进出口`  where strftime('%Y', `截止日期`) = strftime('%Y', DATE('now', '-1 year')) ;	ccks_macro
select `中文名称缩写` from `公司股本结构变动` where `有限售条件的流通A股(股)(披露)` > 100000000	ccks_stock
select `基金代码` from `公募基金最新基准收益率` where `五年基金基准增长率(%)`>50;	ccks_fund
select `人均国内生产总值(元/人)` from `国内生产总值` ;	ccks_macro
select `股权被冻结质押股东名称`, `涉及股数(股)` from `股东股权冻结和质押` where `中文名称缩写` = '瑞茂通';	ccks_stock
select `基金经理姓名`,`混合型管理规模(亿元)` from `基金经理规模统计(新)` order by `混合型管理规模(亿元)` desc limit 10;	ccks_fund
select `截止日期`,  `准备金存款` , `库存现金` from `其他存款性公司资产负债表`  where strftime('%Y', `截止日期`)>='2008';	ccks_macro
select `中文名称缩写` from `公司概况` where `省份`='湖北省' and `所属城市`='武汉市';	ccks_stock
select a.`中文名称缩写` from `公司概况` as a join `公司行业划分表` as b on a.`公司代码` = b.`公司代码` where a.`省份` = '浙江省' and b.`一级行业名称` = '科学研究和技术服务业'	ccks_stock
select `户均持股数半年增长率(%)` from `股东户数`  where strftime('%Y', `截止日期`)='2020' and `中文名称缩写`='京基智农';	ccks_stock
select `批发零售贸易业` from `社会消费品零售总额` ;	ccks_macro
select `经营范围-主营` from `公司经营范围与行业变更` lb where `中文名称缩写` ='天齐锂业'	ccks_stock
select `法人代表` from `公司概况` where `中文名称缩写`='药明康德';	ccks_stock
select `费率类别描述` , `费率划分标准Ⅰ`  from `公募基金费率(新)` where `基金简称` ='汇添富经典';	ccks_fund
select `中文名称缩写`, `实际控制人` from `公司实际控制人` where `所属基金/股票代码` like '00%';	ccks_stock
select count(*) from `股东股权冻结和质押` where `涉及股数(股)` > 10000000;	ccks_stock
select `基金简称` from `公募基金最新基准收益率` order by `三年基金基准增长率(%)` desc limit 1;	ccks_fund
select `基金简称` from `公募基金最新基准收益率` where `三年基金基准增长率(%)`>0;	ccks_fund
select `基金简称`,`基金成立以来基准年化增长率(%)` from `公募基金最新基准收益率` order by `基金成立以来基准年化增长率(%)` desc limit 10;	ccks_fund
select `五年回报率(%)` from `公募基金净值最新区间表现` ;	ccks_fund
select `所属基金/股票代码`, `中文名称缩写` from `概念所属公司表` where `概念名称` like '%新能源%';	ccks_stock
select `中文名称缩写` from `利润分配表附注_财务费用` order by `手续费(元)` desc limit 5	ccks_stock
select `中文名称缩写`,`A股证券代码` from `公司概况` where `省份`='新疆维吾尔自治区';	ccks_stock
select `一年回报率(%)` , `三年回报率(%)`, `五年回报率(%)` from `公募基金净值最新区间表现` ;	ccks_fund
select count(*) from `公募基金概况`  where `证券市场`='上海证券交易所' and `基金运作方式`='LOF' and strftime('%Y', `上市日期`)='2021';	ccks_fund
select `基金经理姓名` from `公募基金经理基本资料`  where strftime('%Y', `证券从业日期`) = strftime('%Y', date())	ccks_fund
select a.`省份` from `公司概况` as a join `公司股本结构变动` as b on a.`公司代码` = b.`公司代码` where b.`无限售条件流通A股(股)(披露)` > 10000000000 group by a.`省份` having count(*) > 10	ccks_stock
select `加权平均基金份额本期利润` from `公募基金主要财务指标(季报)`  where `基金简称` = '招商成长' and strftime('%Y', `截止日期`)='2021' and round(strftime('%m',`截止日期`)/3.0 + 0.495) = 3	ccks_fund
select * from `公募基金净值最新区间表现` where `一年回报率(%)` > 50 and `二年回报率(%)` > 50;	ccks_fund
select count(*)  from `概念所属公司表` as a join `公司概况` as b on a.`公司代码` = b.`公司代码` where a.`概念名称` ='电商概念' and b.`所属城市` ='杭州市';	ccks_stock
select a.`所属基金/股票代码` , b.`公司办公地址` from `公司经营范围与行业变更` as a join `公司概况` as b on a.`公司代码` = b.`公司代码` where a.`行业名称` ='零售业';	ccks_stock
select `所属基金/股票代码` from `概念所属公司表` where `概念名称` like '%百度概念%' and `概念名称` like '%阿里概念%';	ccks_stock
select `国内生产总值(百万元)`, `人均国内生产总值(元/人)` from `国内生产总值`  where `省市` ='山东' and  strftime('%Y', `截止日期`) > strftime('%Y', DATE('now', '-5 year') ) ;	ccks_macro
select `最高学历` from `公募基金经理基本资料` group by `最高学历` having avg(`证券从业经历(年)`) > 10;	ccks_fund
select `纳入广义货币的存款` from `其他存款性公司资产负债表` ;	ccks_macro
select count(*) from `基金经理规模统计(新)` where `QDII管理规模(亿元)` > 200;	ccks_fund
select count(*) from `公司经营范围与行业变更` as a join `公司经营范围与行业变更` as b on  a.`行业名称` = b.`行业名称` where b.`中文名称缩写` = '深科技'	ccks_stock
select count(*) from `A股增发`  where strftime('%Y', `预案公布日期`)='2022';	ccks_stock
select `期初持股数(股)`, `期末持股数(股)` from `公司报告期管理层持股` where `中文名称缩写` = '顺网科技' and `职位描述` like '%董事长%'	ccks_stock
select `截止日期`, `轻工业(百万元)` from `工业生产` where `统计区域类别` ='全国' and `统计口径` ='国有及规模以上工业企业' and `数据统计区间` ='年度';	ccks_macro
select b.`证券简称`,b.`基金经理` from `公募基金债券组合明细` as a join `公募基金概况` as b on a.`基金内部编码`=b.`基金内部编码` order by a.`持有数量(张)` desc limit 10;	ccks_fund
select a.`基金简称` from `公募基金最新收益率排名` as a join `公募基金概况` as b on a.`基金内部编码` = b.`基金内部编码` where b.`基金类别` = '股票型' order by `基金年化收益率(%)` desc limit 10	ccks_fund
select `指数` from `工业品出厂价格指数` where `数据统计期间` ='上年同期' and `指数类别` ='工业结构分类指数' and `指数名称` ='生活资料-耐用消费品';	ccks_macro
select a.`年化收益标准差(未填充)`, a.`年化下行风险(未填充)` from `基金经理历任收益风险指标(全)` as a join `公募基金经理基本资料` as b on a.`基金经理代码` = b.`所属人员编码` where b.`证券从业经历(年)` < 5	ccks_fund
select count(*) from `公募基金净值最新区间表现` where `一年回报率(%)` > 30 and `二年回报率(%)` > 30 and `三年回报率(%)` > 30;	ccks_fund
select count(*) from `公司报告期管理层持股` where  `所属基金/股票代码` = '002104' and  `职位描述` like '%副总裁%'	ccks_stock
select b.`证券简称` ,b.`基金经理` from `公募基金最新基准收益率` as a join `公募基金概况` as b on a.`基金内部编码`=b.`基金内部编码`  where a.`本月以来基金基准增长率(%)`>5;	ccks_fund
select `截止日期`, `社会消费品零售总额(百万元)` from `社会消费品零售总额`  where `统计区域类别` ='省市' and `数据统计期间` ='期末累计' and strftime('%Y', `截止日期`) > strftime('%Y', DATE('now', '-3 year')) ;	ccks_macro
select `性别`, count(*) from `公募基金经理基本资料` group by `性别`;	ccks_fund
select `基金经理` from `公募基金获奖情况` where `评奖单位` = '中国基金报社';	ccks_fund
select `收盘价(元)` from `日行情表`  where strftime('%Y', `交易日`)='2021' and strftime('%m', `交易日`)='1' and strftime('%d', `交易日`)='21' and `所属基金/股票代码` = '002153';	ccks_stock
select `获配企业名称(披露)`, `获配金额(元)` from `法人配售与战略投资者`  where `所属基金/股票代码` = '603059' and strftime('%Y', `信息发布日期`)='2020' order by  `获配金额(元)` desc ;	ccks_stock
select `中文名称缩写` from `公司分红`  where strftime('%Y', `分红实施公告日`) > strftime('%Y', DATE('now', '-10 year')) group by  `中文名称缩写` order by count(*) desc limit 1;	ccks_stock
select `出让前持股比例`, `出让后持股比例` from `股东股权变动`  where `中文名称缩写` = '朗新科技' and strftime('%Y', `股权正式变动日期/过户日期`)='2019'	ccks_stock
select b.`中文名称缩写`, a.`一级行业名称` from `公司行业划分表` as a join `公司股本结构变动` as b on a.`公司代码` = b.`公司代码` order by `未流通A股(股)` desc limit 5	ccks_stock
select count(distinct `奖项名称`) from `公募基金获奖情况` ;	ccks_fund
select `董秘电话` from `公司概况` where `中文名称缩写`='万科';	ccks_stock
select `中文名称缩写` from `限售股票解禁时间表` order by `A股总数(万股)` desc limit 10	ccks_stock
select a.`所属基金/股票代码`, a.`中文名称缩写` from `概念所属公司表` as a join `公司概况` as b on a.`公司代码` = b.`公司代码` where b.`省份` ='安徽省' and a.`概念名称` ='无人驾驶';	ccks_stock
select count(*) from `公司主营业务构成` where `中文名称缩写`='中国石化' and `主营业务收入(元)` > 200000000000 ;	ccks_stock
select `公司中文名称`, `股东持股比例` from `企业之间参股情况`  where `中文名称缩写` = '航天发展' and strftime('%Y', `截止日期`)='2020' and strftime('%m', `截止日期` )='3'	ccks_stock
select `基金简称` from `公募基金主要财务指标(季报)`  where strftime('%Y', `截止日期`)='2020' group by  `基金简称` having sum(`基金本期利润`) > 1000000000	ccks_fund
select  `最高比率(%)` from `税率表` where `税率类别` ='中资大型银行' and `税率项目` = '超额存款准备金率'  ;	ccks_macro
select `A股证券代码`,`A股证券简称` from `公司概况` where `中文名称缩写`='科大讯飞';	ccks_stock
select a.`所属基金/股票代码` , b.`董事会秘书` , b.`公司办公地址` from `概念所属公司表` as a join `公司概况` as b on a.`公司代码` = b.`公司代码` where a.`概念名称` ='共享经济' ;	ccks_stock
select `中文名称缩写`, `配股年度`, `募集资金总额(元)` from `A股配股` where `募集资金总额(元)` < 100000000;	ccks_stock
select `中文名称缩写`,`公司注册地址` from `公司概况` where `所属城市`='银川市';	ccks_stock
select `中文名称缩写` from `公司实际控制人` where `实际控制人` = '福建省财政厅';	ccks_stock
select `日回报率(%)` from  `公募基金净值最新区间表现` ;	ccks_fund
select a.`所属基金/股票代码` , b.`省份`  from `概念所属公司表` as a join `公司概况` as b on a.`公司代码` = b.`公司代码` where a.`概念名称` ='元宇宙' ;	ccks_stock
select `基金经理姓名` from `基金经理规模统计(新)` where `股票型管理规模(亿元)` > 100 and `混合型管理规模(亿元)` > 50;	ccks_fund
select `中文名称缩写` from `利润分配表附注_财务费用` order by `利息支出(元)` desc limit 10	ccks_stock
select `数据统计期间`, `指数类别`, `指数` from `工业品出厂价格指数` where  `指数名称` ='冶金工业';	ccks_macro
select `基金简称` from `公募基金最新收益率排名` where `基金收益率(%)` > 0 and `基金年化收益率(%)` > 0	ccks_fund
select `二年回报率(%)` from `公募基金净值最新区间表现` ;	ccks_fund
select b.`中文名称缩写` from `发行与上市中介机构` as a join `公司概况` as b on a.`公司代码`=b.`公司代码`  where b.`省份`='上海市' and a.`承销数量(股)`>1000000;	ccks_stock
select `中文名称缩写` from `利润分配表附注_财务费用` order by `手续费(元)` desc	ccks_stock
select `费率描述` from  `公募基金费率(新)` where `基金简称` ='富国300ESGETF';	ccks_fund
select `股权被冻结质押股东名称`, `涉及股数(股)` from `股东股权冻结和质押` where `所属基金/股票代码` = '600180' and `占总股本比例` >=0.05 ;	ccks_stock
select `机构全称` from `发行与上市中介机构` order by `承销数量(股)` desc limit 100;	ccks_stock
select `中文名称缩写` from `自由流通股本` where `自由流通比例(归档后)(%)` = 100	ccks_stock
select `中文名称缩写` from `A股配股`  where strftime('%Y', `配股年度`) = strftime('%Y', DATE('now', '-2 year'));	ccks_stock
select a.`股权出让方名称`, a.`出让前持股数量(股)(份)`, a.`出让前持股比例` from `股东股权变动` as a join `公司概况` as b on a.`公司代码` = b.`公司代码` where b.`省份` = '江苏省'	ccks_stock
select count(*) from `公司经营范围与行业变更` where `行业名称` like '%计算机%'	ccks_stock
select `截止日期`, `工业总产值(现价)(百万元)` from `工业生产` where `统计区域类别` ='全国' and `统计口径` ='全部工业企业' and `数据统计区间` ='期末累计';	ccks_macro
select `中文名称缩写` from `公司主营业务构成`  where strftime('%Y', `截止日期`)='2021' order by  `主营业务收入(元)` desc limit 5;	ccks_stock
select `证券简称`, `姓名` from `公募基金经理(新)` order by `任职期间基金净值增长率` desc limit 5	ccks_fund
select `单位净值(元)`, `单位累计净值(元)` from `公募基金净值` where `基金简称` = '国泰融信';	ccks_fund
select `基金经理姓名`,`总管理规模(亿元)` from `基金经理规模统计(新)` order by `总管理规模(亿元)` desc limit 1;	ccks_fund
select b.`证券简称`,b.`基金经理` from `公募基金债券组合明细` as a join `公募基金概况` as b on a.`基金内部编码`=b.`基金内部编码` order by a.`市值(元)` desc limit 1;	ccks_fund
select `中文名称缩写` from `A股增发` group by `中文名称缩写` having count(*) > 1;	ccks_stock
select `今年以来回报率(%)` from `公募基金净值最新区间表现` ;	ccks_fund
select `送股比例(10送X)` from `公司分红` where `所属基金/股票代码` ='000021';	ccks_stock
select `截止日期` ,`进口商品总额(百万美元)` , `进口同比增减` from `海关进出口`  where strftime('%Y', `截止日期`) < strftime('%Y', DATE('now', '-10 year'));	ccks_macro
select `基金简称`,`基金成立以来基准增长率(%)` from `公募基金最新基准收益率` order by `基金成立以来基准增长率(%)` limit 20;	ccks_fund
select `股东名称` from `企业之间参股情况`  where `所属基金/股票代码` ='300184' and strftime('%Y', `截止日期`) = strftime('%Y', DATE('now', '-1 year')) and round(strftime('%m',`截止日期`)/3.0 + 0.495) = 4 ;	ccks_stock
select `领导姓名`, `期末持股数(股)` from `公司报告期管理层持股` where `职位描述` like '%副总裁%'	ccks_stock
select `送股比例(10送X)`, `分红股本基数(股)` from `公司分红`  where `中文名称缩写` ='西藏发展' and strftime('%Y', `分红实施公告日`) = strftime('%Y', DATE('now', '-1 year')) ;	ccks_stock
select `国内信贷` from `中国货币与银行概览` order by `截止日期` desc limit 1;	ccks_macro
select `一个月回报率(%)` from  `公募基金净值最新区间表现` ;	ccks_fund
select  `所属基金/股票代码`, `中文名称缩写` from `公司分红`  where `实派(税后/人民币元)` > 10 and strftime('%Y', `分红实施公告日`) = strftime('%Y', DATE('now', '-2 year'));	ccks_stock
select `设立以来回报率(%)`, `设立以来年化回报率(%)` from `公募基金净值最新区间表现` ;	ccks_fund
select `领导姓名` from `公司报告期管理层持股` where `中文名称缩写` = '石化油服' order by `期末持股数(股)` desc limit 1	ccks_stock
select `股权被冻结质押股东名称`, `累计冻结质押股数(股)` from `股东股权冻结和质押统计` where `所属基金/股票代码` like '300%'	ccks_stock
select `基金简称` from `公募基金主要财务指标(季报)`  where strftime('%Y', `截止日期`)='2020' group by  `基金简称` order by sum(`基金本期利润`) desc limit 1	ccks_fund
select `一年回报率(%)`, `二年回报率(%)`, `三年回报率(%)` from `公募基金净值最新区间表现` where `基金简称` = '易方达中小企业A';	ccks_fund
select `设立以来年化回报率(%)` from `公募基金净值最新区间表现` ;	ccks_fund
select `基金类别描述`, count(*) from `公募基金最新收益率排名` where `指标周期` = '一年' and `基金收益率(%)` < 0 group by `基金类别描述`	ccks_fund
select `三年回报率(%)`, `五年回报率(%)`, `十年回报率(%)`, `设立以来回报率(%)` from `公募基金净值最新区间表现` ;	ccks_fund
select `中文名称缩写`, `总股本(股)` from `公司股本结构变动` where `中文名称缩写` = '东北证券' or `中文名称缩写` = '国元证券'	ccks_stock
select `证券简称` from `公募基金概况` order by `最低认购金额下限(元)` asc limit 1	ccks_fund
select a.`中文名称缩写`, b.`总经理`, b.`法人代表` from `公司分红` as a join `公司概况` as b on a.`公司代码` = b.`公司代码`  where strftime('%Y', a.`分红实施公告日`)='2021';	ccks_stock
select `个体单位` from `社会消费品零售总额` ;	ccks_macro
select `五年年化回报率(%)` from `公募基金净值最新区间表现` ;	ccks_fund
select `组织形式`, count(*) from `公募基金管理人概况` group by `组织形式` order by count(*) desc;	ccks_fund
select `(一)境内贷款` , `(二)境外贷款` , `农业存款` from `中国金融机构人民币信贷收支表`  where strftime('%Y', `截止日期`)<='2000' and `各项贷款` >1000000;	ccks_macro
select  `收益分配原则` from `公募基金概况` where `证券简称` = '招商成长'	ccks_fund
select count(*), `所属基金/股票代码` from `概念所属公司表`  group by `所属基金/股票代码` ;	ccks_stock
select `三年年化回报率(%)` , `五年年化回报率(%)` , `十年年化回报率(%)` from `公募基金净值最新区间表现` ;	ccks_fund
select b.`证券简称`,b.`基金投资范围` from `公募基金最新基准收益率` as a join `公募基金概况` as b on a.`基金内部编码`=b.`基金内部编码`  where a.`本月以来基金基准增长率(%)`<0;	ccks_fund
select `主要产品与业务名称` from `公司经营范围与行业变更` lb where `中文名称缩写` ='富临精工'	ccks_stock
select `证券简称` from `公募基金概况` order by `设立日期` desc	ccks_fund
select  `股权被冻结质押股东名称` from `股东股权冻结和质押`  where `占冻结质押方持股数比例` > 0.3 and strftime('%Y', `冻结质押期限截止日`) > strftime('%Y', DATE('now', '-2 year'));	ccks_stock
select `基金代码` , `单位基金净值周增长率` from  `公募基金净值` ;	ccks_fund
select `户均持股比例季度增长率(%)` from `股东户数`  where strftime('%Y', `截止日期`)='2020' and round(strftime('%m',`截止日期`)/3.0 + 0.495)=2 and `中文名称缩写`='京基智农';	ccks_stock
select `评估机构`,`签字评估师` from `A股发行申报企业信息` where `所属基金/股票代码`='300278';	ccks_stock
select `社会消费品零售总额(百万元)` from `社会消费品零售总额` where `省市` ='江苏';	ccks_macro
select `单位存款/企业存款` , `财政性存款` from `中国金融机构人民币信贷收支表`  where strftime('%Y', `截止日期`)='2004';	ccks_macro
select `截止日期` from `财政收支` where `省市` ='江苏' and `地方财政收入(百万元)` > 100 and `地方财政支出(百万元)` < 100;	ccks_macro
select `行业名称` from `公司经营范围与行业变更` where `中文名称缩写` ='深科技'	ccks_stock
select `主营业务收入(元)` from `公司主营业务构成`  where `中文名称缩写` ='中国石化' and strftime('%Y', `截止日期`) = strftime('%Y', DATE('now', '-1 year')) and round(strftime('%m',`截止日期`)/3.0 + 0.495) = 1;	ccks_stock
select `基金简称`, `指标周期`, `基金收益率(%)` from `公募基金最新收益率排名` where `基金简称` = '华夏创蓝筹ETF' or `基金简称` = '建信深证60ETF'	ccks_fund
select `总管理规模(亿元)` from `基金经理规模统计(新)` where `基金经理姓名`='张坤';	ccks_fund
select b.`基金经理姓名`, b.`总管理规模(亿元)`, b.`QDII管理规模(亿元)` from `公募基金经理基本资料` as a join `基金经理规模统计(新)` as b on a.`所属人员编码` = b.`基金经理代码` where a.`国籍` = '美国';	ccks_fund
select `实际控制人` from `公司实际控制人` group by `实际控制人` order by count(*) desc limit 1;	ccks_stock
select `证券代码` from `公募基金概况` where `证券简称` = '广发小盘A'	ccks_fund
select b.`中文名称缩写`, a.`董事会秘书` from `公司概况` as a join `自由流通股本` as b on a.`公司代码` = b.`公司代码` where b.`自由流通股本(归档后)(股)` > 10000000 and a.`所属城市` = '深圳市'	ccks_stock
select `对特定存款机构债权(百万元)` , `对其他金融机构债权/对非货币金融机构债权(百万元)` from `货币当局资产负债表` ;	ccks_macro
select `基金简称` from `公募基金重仓股票组合` group by `基金简称` order by sum(`市值(元)`) desc limit 1	ccks_fund
select count(*) from `A股发行申报企业信息` where `所属行业/领域`='银行业';	ccks_stock
select `基金经理姓名` from `公募基金经理基本资料` order by `出生日期` asc limit 1	ccks_fund
select a.`中文名称缩写` from `公司研发投入与产出` as a join  `公司概况` as b on a.`公司代码`=b.`公司代码`  where strftime('%Y', a.`截止日期`)=strftime('%Y', DATE('now', '-1 year')) and b.`省份`='浙江省' and `研发投入合计(元)`>100000000;	ccks_stock
select `中文名称缩写` from `股份回购`  where strftime('%Y', `预案公布日`) = strftime('%Y', DATE('now', '-1 year')) and (round(strftime('%m',`预案公布日`)/3.0 + 0.495) = 3 or round(strftime('%m',`预案公布日`)/3.0 + 0.495) = 4);	ccks_stock
select b.`中文名称缩写`, b.`实际控制人` from `公司概况` as a join `公司实际控制人` as b on a.`公司代码` = b.`公司代码` where a.`省份` = '浙江省';	ccks_stock
select `证券简称`,`基金经理` from `公募基金概况` where `基金管理人`='国泰基金管理有限公司' and `基金运作方式`='ETF';	ccks_fund
select count(*) from `公募基金最新基准收益率` as a join `公募基金概况` as b on a.`基金内部编码`=b.`基金内部编码` where a.`一个月基金基准增长率(%)`>0 and b.`基金经理`='朱少醒';	ccks_fund
select `指数` from `工业品出厂价格指数` where `数据统计期间` ='上年同期' and `指数类别` ='工业结构分类指数' and `指数名称` ='生活资料-食品';	ccks_macro
select `主营业务收入(元)` , `主营业务成本(元)`, `主营业务利润(元)` from `公司主营业务构成`  where strftime('%Y', `截止日期`) = strftime('%Y', DATE('now', '-1 year')) and `所属基金/股票代码` ='000822';	ccks_stock
select `收盘价(元)` from `日行情表`  where strftime('%Y', `交易日`)='2021' and round(strftime('%m',`交易日`)/3.0 + 0.495) = 1 and `所属基金/股票代码` = '300278';	ccks_stock
select `中文名称缩写` from `股东股权变动` order by `涉及股数(股)` desc limit 10	ccks_stock
select a.`一级行业名称` from `公司行业划分表` as a join `公司股本结构变动` as b on a.`公司代码` = b.`公司代码` where b.`未流通A股(股)` > 200000000 group by a.`一级行业名称` having count(*) > 50	ccks_stock
select  `基金公司名称` from  `公募基金获奖情况`  where strftime('%Y', `获奖年度`) >=2010 and `奖项名称` ='三年期股票型金基金奖' and `获奖对象` ='投资基金';	ccks_fund
select `姓名` from `公募基金经理(新)` where `证券代码` like '15%' and `任职期间基金净值增长率` > 0.7	ccks_fund
select `截止日期`, `总资产`, `总负债`, `国外净资产`, `国外负债` from `其他存款性公司资产负债表` where `总资产` > 50000000 order by `截止日期` desc limit 1;	ccks_macro
select `户均持股数季度增长率(%)` from `股东户数` where `中文名称缩写`='古井贡酒';	ccks_stock
select `收盘价(元)` from `日行情表`  where strftime('%Y', `交易日`)='2021' and strftime('%m', `交易日`)='4' and `中文名称缩写` = '华昌达';	ccks_stock
select `基金名称`, `评奖单位` from `公募基金获奖情况`;	ccks_fund
select `最低比率(%)` from `税率表` where `税率类别` ='农村信用社' and `税率项目` ='超额存款准备金率';	ccks_macro
select b.`中文名称缩写`, b.`二级行业名称` from `公司概况` as a join `公司行业划分表` as b on a.`公司代码` = b.`公司代码` where a.`省份` = '浙江省' and b.`一级行业名称` = '制造业';	ccks_stock
select `中文名称缩写` from `公司报告期管理层持股` where `领导姓名` = '刘明强'	ccks_stock
select b.`证券简称`,b.`基金投资目标` from `公募基金最新基准收益率` as a join `公募基金概况` as b on a.`基金内部编码`=b.`基金内部编码`  order by a.`一个月基金基准增长率(%)` desc limit 10;	ccks_fund
select `领导姓名`, `中文名称缩写` from `公司报告期管理层持股` where `职位描述` like '%董事长%' and `职位描述` like '%总裁%'	ccks_stock
select `董事会秘书`,`董秘电话` from `公司概况` where `A股证券代码`='600234';	ccks_stock
select `集体单位` from `社会消费品零售总额` ;	ccks_macro
select b.`基金经理` from `公募基金最新基准收益率` as a join `公募基金概况` as b on a.`基金内部编码`=b.`基金内部编码` where a.`本日基金基准增长率(%)`>0;	ccks_fund
select a.`省份` , count(*)  from `公司概况` as a join `概念所属公司表` as b on a.`公司代码` = b.`公司代码` where b.`概念名称` ='石墨烯' group by a.`省份` having count(*)>1;	ccks_stock
select a.`一级行业名称`, count(*) from `公司行业划分表` as a join `自由流通股本` as b on a.`公司代码` = b.`公司代码` where b.`自由流通比例(归档后)(%)` = 100 group by a.`一级行业名称`	ccks_stock
select a.`中文名称缩写`, a.`股权被冻结质押股东名称`, a.`累计冻结质押股数(股)` from `股东股权冻结和质押统计` as a join `公司概况` as b on a.`公司代码` = b.`公司代码` where b.`省份` = '河北省'	ccks_stock
select `进口商品总额(百万美元)`, `进口同比增减` from `海关进出口` where `出口同比增减` > 0 and `出口商品总额(百万美元)` > 20 and strftime('%Y', `截止日期`)<'2000';	ccks_macro
select `单位净值(元)` from `公募基金净值` where `基金简称` = '华安180ETF' and `截止日期` >= '2021-4-1';	ccks_fund
select `最高学历`, `证券从业经历(年)` from `公募基金经理基本资料` where `基金经理姓名` = '刘伟琳';	ccks_fund
select `基金经理姓名` from `公募基金经理基本资料` where `证券从业经历(年)` > 20 and `性别` = '女';	ccks_fund
select b.`中文名称缩写` from `公司行业划分表` as a join `公司股本结构变动` as b on a.`公司代码` = b.`公司代码` where a.`一级行业名称` = '建筑业' and b.`总股本(股)` > 10000000000	ccks_stock
select `基金经理姓名` from `基金经理规模统计(新)` order by `总管理规模(亿元)` desc limit 1;	ccks_fund
select `中文名称缩写` from `发行与上市中介机构` where `承销金额(元)`<100000000;	ccks_stock
select `社会消费品零售总额(百万元)` from `社会消费品零售总额` where `省市` ='天津' and `数据统计期间` ='年度';	ccks_macro
select `指数` from `工业品出厂价格指数`  where `指数名称` ='饮料制造业' and `数据统计期间` ='上年同期' and strftime('%Y', `截止日期`) = strftime('%Y', DATE('now', '-1 year')) ;	ccks_macro
select `基金经理姓名`,`混合型基金数量(只)` from `基金经理规模统计(新)` where `基金经理姓名`='刘格菘' or `基金经理姓名`='朱少醒';	ccks_fund
select `截止日期`, `对非金融机构债权`, `对非金融机构及住户负债` from `其他存款性公司资产负债表`  where strftime('%Y', `截止日期`) = strftime('%Y', date());	ccks_macro
select `二级行业名称` from `公司行业划分表` where `一级行业名称` = '制造业' group by `二级行业名称` order by count(*) desc limit 1	ccks_stock
select count(*) from `法人配售与战略投资者` ;	ccks_stock
select count(*) from `公募基金净值最新区间表现` where `设立以来回报率(%)` > 1000;	ccks_fund
select `指数类别` from `工业品出厂价格指数` ;	ccks_macro
select `基金简称` from `公募基金净值最新区间表现` where `基金简称` like '%稳健%' order by `日回报率(%)` desc limit 1;	ccks_fund
select b.`二级行业名称`, count(*) from `限售股票解禁时间表` as a join `公司行业划分表` as b on a.`公司代码` = b.`公司代码` where a.`已流通A股(万股)` > 5000 group by b.`二级行业名称`	ccks_stock
select `收盘价(元)` from `日行情表`  where strftime('%Y', `交易日`)='2021' and strftime('%m', `交易日`)='4' and `所属基金/股票代码` = '300278';	ccks_stock
select `股东名称`, `股东持股数量` from `企业之间参股情况` where `中文名称缩写` = '农发种业' and strftime('%Y', `截止日期`)<'2019';	ccks_stock
select `配股年度`, `募集资金总额(元)` from `A股配股` where `所属基金/股票代码` = '600859';	ccks_stock
select `股东名称` from `配股大股东认配状况` where `中文名称缩写`='博瑞传播' order by `实配股数(股)` desc limit 3;	ccks_stock
select `基金简称`,`本周以来基金基准增长率(%)` from `公募基金最新基准收益率` where `本周以来基金基准增长率(%)`<0 order by `本周以来基金基准增长率(%)` asc;	ccks_fund
select `主要业务` from `公司经营范围与行业变更` where `中文名称缩写` ='精研科技'	ccks_stock
select `中文名称缩写` from `股东户数` where `户均持股比例季度增长率(%)`>10;	ccks_stock
select `公司中文名称` from `股东户数`  where strftime('%Y', `截止日期`)='2019' order by  `股东总户数(户)` desc limit 5;	ccks_stock
select `中文名称缩写` from `股东户数` where `户均持股数半年增长率(%)`>20;	ccks_stock
select `对政府债权(净)` from `中国货币与银行概览` ;	ccks_macro
select `股权被冻结质押股东名称` from `股东股权冻结和质押` where `中文名称缩写` = '瑞茂通' and `占总股本比例` > 0.05 ;	ccks_stock
select `储蓄存款`, `农业存款` from `中国金融机构人民币信贷收支表`;	ccks_macro
select `进口商品总额(百万美元)`, `出口商品总额(百万美元)` from `海关进出口` ;	ccks_macro
select `基金经理姓名` from `公募基金经理基本资料` where `最高学历` = '博士'  order by `证券从业经历(年)` desc limit 1	ccks_fund
select `股权出让方名称`, `股权受让方名称` from `股东股权变动`  where `中文名称缩写` = '宝钢股份' and strftime('%Y', `股权正式变动日期/过户日期`)='2018'	ccks_stock
select `实收资本`, `国外净资产`, `国内信贷` from `中国货币与银行概览`  where strftime('%Y', `截止日期`) > strftime('%Y', DATE('now', '-2 year')) ;	ccks_macro
select `基金管理人简称`, `注册地址`, `注册资本(元)` from `公募基金管理人概况` where `注册资本(元)` > 10000000000;	ccks_fund
select `股权出让方名称`, `出让后持股数量(股)(份)`, `出让后持股比例` from `股东股权变动`  where `中文名称缩写` = '盛天网络' and strftime('%Y', `股权正式变动日期/过户日期`)='2018'	ccks_stock
select `机构全称` from `发行与上市中介机构`;	ccks_stock
select `毛利率` from `公司主营业务构成` where `中文名称缩写` ='西藏发展';	ccks_stock
select `进口商品总额(百万美元)`, `进口同比增减` from `海关进出口`  where strftime('%Y', `截止日期`) = strftime('%Y', DATE('now', '-2 year')) ;	ccks_macro
select `基金经理姓名` from `公募基金经理基本资料` where `国籍` != '中国';	ccks_fund
select `对其他金融机构债权` from `其他存款性公司资产负债表` ;	ccks_macro
select `收盘价(元)` from `日行情表`  where strftime('%Y', `交易日`)='2021' and strftime('%m', `交易日`)='1' and strftime('%d', `交易日`)='14' and `中文名称缩写` = '石基信息';	ccks_stock
select `增发目的` from `A股增发` where `所属基金/股票代码` = '300022';	ccks_stock
select a.`中文名称缩写`, a.`股权被冻结质押股东名称`, a.`累计冻结质押股数(股)` from `股东股权冻结和质押统计` as a join `公司概况` as b on a.`公司代码` = b.`公司代码` where b.`省份` = '浙江省'	ccks_stock
select `基金经理姓名` from `基金经理规模统计(新)` where `旗下基金总数(只)`>15;	ccks_fund
select `混合型基金数量(只)`, `混合型管理规模(亿元)` from `基金经理规模统计(新)` where `基金经理姓名` = '郑希';	ccks_fund
select `本日基金基准增长率(%)` from `公募基金最新基准收益率` where `基金简称`='富国天丰';	ccks_fund
select `所属地区`, count(*) from `公募基金管理人概况` where strftime('%Y', `成立日期`)>'2015' group by `所属地区`;	ccks_fund
