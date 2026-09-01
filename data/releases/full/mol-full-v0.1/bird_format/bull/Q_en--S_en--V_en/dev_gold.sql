select FundTypeName, count(*) from mf_fundreturnrank where IndexCycle = '1 month' and FundReturn > 0 group by FundTypeName	ccks_fund
select b.SecuAbbr,b.InvestOrientation from mf_benchmarkgrowthrate as a join mf_fundarchives as b on a.InnerCode=b.InnerCode   where a.BenchGRForThisWeek>0;	ccks_fund
select SHName from lc_largeshsubscription  where strftime('%Y', InitialInfoPublDate)='2017' group by  SHName order by max(ActualShares) desc limit 1;	ccks_stock
select SHName from lc_largeshsubscription where ActualShares>500000 and OughtShares>500000;	ccks_stock
select a.ChiNameAbbr, a.LeaderName, a.PositionDescription from lc_executivesholdings as a join lc_sharetransfer as b on a.CompanyCode = b.CompanyCode order by b.PCTBeforeTran desc limit 5	ccks_stock
select ProportionGRHalfAYear from lc_shnumber where ChiNameAbbr='兴业证券';	ccks_stock
select GrossProfit from lc_mainoperincome where ChiNameAbbr ='西藏发展';	ccks_stock
select a.ChiNameAbbr, a.FPSHName, a.AccuPCTOfPled from lc_sharefpsta as a join lc_exgindustry as b on a.CompanyCode = b.CompanyCode where b.FirstIndustryName = 'Real Estate'	ccks_stock
select a.SecuAbbr from mf_fundmanagernew as a join mf_personalinfo as b on a.PersonalCode = b.PersonalCode where b.Education = 'Bachelor''s degree'	ccks_fund
select b.ChineseName,b.Education from mf_fmscaleanalysisn as a join mf_personalinfo as b on a.PersonalCode=b.PersonalCode where a.QDIINV>200;	ccks_fund
select ChiNameAbbr from lc_stockarchives where GeneralManager='孙健';	ccks_stock
select FundManager , Fund from mf_awards where AppraisalOrg = 'Securities Times';	ccks_fund
select b.SecuAbbr,b.Manager from mf_bondportifoliodetail as a join mf_fundarchives as b on a.InnerCode=b.InnerCode where a.BondAbbr='兴业转债';	ccks_fund
select ChiNameAbbr, ControllerName from lc_actualcontroller where SecuCode like '00%';	ccks_stock
select b.ChineseName, a.MaxRet from mf_fmperfanalysis as a join mf_personalinfo as b on a.PersonalCode = b.PersonalCode where b.Education = 'Doctoral degree' and a.IndexCycle = '1 year';	ccks_fund
select b.SecuAbbr,b.Manager from mf_bondportifoliodetail as a join mf_fundarchives as b on a.InnerCode=b.InnerCode group by b.SecuAbbr order by count(*) desc limit 10;	ccks_fund
select b.ChiNameAbbr,a.TotalRDInput from lc_intassetsdetail as a join lc_stockarchives as b on a.CompanyCode=b.CompanyCode   where b.State='浙江省' and strftime('%Y', a.EndDate)='2018';	ccks_stock
select b.Type, count(*) from mf_fundreturnrank as a join mf_fundarchives as b on a.InnerCode = b.InnerCode where a.IndexCycle = 'since inception' and a.FundReturnMean > 0 group by b.Type	ccks_fund
select a.FullName,b.SHName from lc_issueandlistagent as a join lc_largeshsubscription as b on a.CompanyCode=b.CompanyCode where a.ChiNameAbbr='天健集团';	ccks_stock
select count(*) from lc_mainoperincome where MainOperCost < 100000000;	ccks_stock
select a.SecuCode , b.SecretaryBD , b.SecretaryBDTel from lc_coconcept as a join lc_stockarchives as b on a.CompanyCode = b.CompanyCode where a.ConceptName ='East Data, West Computing' ;	ccks_stock
select InvestmentType, avg(FoundedSize) from mf_fundarchives group by InvestmentType;	ccks_fund
select ChiNameAbbr from lc_actualcontroller where ControllerName = '赵马克';	ccks_stock
select TurnoverDeals from qt_dailyquote where SecuCode = '601908';	ccks_stock
select a.SecuAbbr , b.SecretaryBD , b.SecretaryBDTel from lc_coconcept as a join lc_stockarchives as b on a.CompanyCode = b.CompanyCode where a.ConceptName ='3D Glass' ;	ccks_stock
select AccumulatedUnitNV , NVDailyGrowthRate from  mf_netvalue ;	ccks_fund
select distinct a.ChiNameAbbr from lc_dividend as a join lc_stockarchives as b on a.CompanyCode = b.CompanyCode where strftime('%Y', b.EstablishmentDate)>'2010' ;	ccks_stock
select count(*) from mf_fundreturnrank where FundReturn < 0 and FundAnnReturn < 0	ccks_fund
select a.Name from mf_fundmanagernew as a join mf_fundrisklevel as b on a.InnerCode = b.InnerCode where b.RiskLevel = 'Medium-Low' group by a.Name having count(a.SecuAbbr) > 5	ccks_fund
select SecuAbbr from mf_benchmarkgrowthrate where BenchGRFor3Year>0;	ccks_fund
select ChiNameAbbr, EndDate from qt_monthdata where PB < 5 and PETTM > 200;	ccks_stock
select count(*) from mf_fmretscaleanalysis as a join mf_personalinfo as b on a.PersonalCode = b.PersonalCode where a.TotalAUM > 100 and b.Education = 'Bachelor''s degree'	ccks_fund
select count(*) from lc_mainoperincome  where strftime('%Y', EndDate)='2020' and GrossProfit > 1	ccks_stock
select InvestAdvisorAbbrName from mf_investadvisoroutline where strftime('%Y', EstablishmentDate)>'2010';	ccks_fund
select a.SecuAbbr , b.SecretaryBD from lc_coconcept as a join lc_stockarchives as b on a.CompanyCode = b.CompanyCode where a.ConceptName ='Large Aircraft' ;	ccks_stock
select b.Education from mf_fmperfanalysis as a join mf_personalinfo as b on a.PersonalCode = b.PersonalCode where a.AnnAlphaCoef > 0.2 group by b.Education having count(*) > 5	ccks_fund
select InvestAdvisorAbbrName from mf_investadvisoroutline where LegalRepr like '周%';	ccks_fund
select a.SecuAbbr from mf_fundrisklevel as a join mf_fundarchives as b on a.InnerCode = b.InnerCode where a.RiskLevel = 'Medium-Low' and b.Type = '开放式'	ccks_fund
select b.ChineseName,b.Background from mf_fmscaleanalysisn as a join mf_personalinfo as b on a.PersonalCode=b.PersonalCode where a.EquityFundN>5;	ccks_fund
select MainOperIncome , MainIncomeGrowRateYOY from lc_mainoperincome where MainIncomeGrowRateYOY > 0 and ChiNameAbbr ='古井贡酒';	ccks_stock
select a.ChineseName, b.Education from mf_fmretscaleanalysis as a join mf_personalinfo as b on a.PersonalCode = b.PersonalCode where a.TimeInterval = 'Year to Date' order by a.AvgAUM desc limit 3	ccks_fund
select ChiName from lc_mainoperincome  where strftime('%Y', EndDate)='2020' and GrossProfit > 1	ccks_stock
select ChiNameAbbr, BonusShareRatio from lc_dividend where ChiNameAbbr = '京基智农' or ChiNameAbbr = '天健集团';	ccks_stock
select SHName from lc_largeshsubscription where OughtShares>2000000;	ccks_stock
select SHName,ActualShares from lc_largeshsubscription where ChiNameAbbr='同济科技';	ccks_stock
select OrganizationForm, count(*) from mf_investadvisoroutline group by OrganizationForm order by count(*) asc;	ccks_fund
select ActualShares from lc_largeshsubscription where SHName='杉杉集团';	ccks_stock
select InvestAdvisorAbbrName from mf_investadvisoroutline order by RegCapital desc limit 1;	ccks_fund
select a.SecuAbbr from mf_fundrisklevel as a join mf_fundarchives as b on a.InnerCode = b.InnerCode where a.RiskLevel = 'Medium-Low' and b.InvestmentType= 'Growth—Stable Growth'	ccks_fund
select ChiName, SHInvestSum from lc_relatedsh  where ChiNameAbbr = '航天发展' and strftime('%Y', EndDate)='2019' and strftime('%m', EndDate )='5'	ccks_stock
select a.FullName,a.LegalPersonRepr,b.SHName,b.ActualShares from lc_issueandlistagent as a join lc_largeshsubscription as b on a.CompanyCode=b.CompanyCode where a.ChiNameAbbr='东阿阿胶';	ccks_stock
select AvgHoldSumGRHalfAYear from lc_shnumber where ChiNameAbbr='工商银行';	ccks_stock
select count(*) from mf_fundrisklevel as a join mf_fundarchives as b on a.InnerCode = b.InnerCode where a.RiskLevel = 'Medium' and b.InvestmentType= 'Comprehensive'	ccks_fund
select b.SecuAbbr,b.Manager from mf_bondportifoliodetail as a join mf_fundarchives as b on a.InnerCode=b.InnerCode where a.BondAbbr='21国债01' order by a.HoldVolume desc limit 1;	ccks_fund
select State,City,AStockCode from lc_stockarchives where ChiNameAbbr='天娱数科';	ccks_stock
select b.SecuAbbr,b.Manager,b.RiskReturncharacter from mf_benchmarkgrowthrate as a join mf_fundarchives as b on a.InnerCode=b.InnerCode order by a.BenchGRForThisWeek desc limit 10;	ccks_fund
select SecuAbbr from mf_benchmarkgrowthrate where BenchGRFor2Year<0;	ccks_fund
select MainOperProfit, MainOperCost from lc_mainoperincome  where strftime('%Y', EndDate) = strftime('%Y', DATE('now', '-1 year')) and SecuCode ='000822';	ccks_stock
select InvestAdvisorName from mf_fundarchives where TrusteeName='中信银行股份有限公司' group by InvestAdvisorName order by count(*) desc limit 1;	ccks_fund
select MainIncomeGrowRateYOY from lc_mainoperincome where MainIncomeGrowRateYOY < 0 and SecuCode ='000822' and strftime('%Y', EndDate)>'2020'	ccks_stock
select b.ChiNameAbbr, a.GeneralManager from lc_stockarchives as a join lc_freefloat as b on a.CompanyCode = b.CompanyCode where b.TotalAShare > 10000000000	ccks_stock
select UnitNV , NVWeeklyGrowthRate from  mf_netvalue ;	ccks_fund
select b.RiskLevel, count(a.SecuAbbr) from mf_fundmanagernew as a join mf_fundrisklevel as b on a.InnerCode = b.InnerCode where a.Performance > 0 group by b.RiskLevel	ccks_fund
select BondFundN,BondFundNV from mf_fmscaleanalysisn where ChineseName='陈龙';	ccks_fund
select SecuAbbr from mf_benchmarkgrowthrate where BenchGRForThisWeek>5;	ccks_fund
select ProportionGRQuarter from lc_shnumber  where strftime('%Y', EndDate)='2020' and ChiNameAbbr='金禾实业';	ccks_stock
select a.SecuAbbr, a.RiskReturncharacter from mf_fundarchives as a join mf_fundrisklevel as b on a.InnerCode = b.InnerCode where b.RiskLevel = 'Medium'	ccks_fund
select  SecuCode  from lc_mainoperincome  where strftime('%Y', EndDate) > strftime('%Y', DATE('now', '-3 year')) and GrossProfit >1;	ccks_stock
select SecuAbbr from mf_benchmarkgrowthrate where BenchGRFor10Year>200;	ccks_fund
select InvestAdvisorName,count(*) from mf_fundarchives where FundType='Hybrid Fund' group by InvestAdvisorName order by count(*) desc limit 1;	ccks_fund
select InvestAdvisorAbbrName from mf_investadvisoroutline where RegCapital > 200000000 and strftime('%Y', EstablishmentDate)>'2015';	ccks_fund
select count(*) from lc_sharefp where ReceiverName ='中国进出口银行';	ccks_stock
select LegalRepr from mf_investadvisoroutline where InvestAdvisorAbbrName = '中银基金';	ccks_fund
select MainBusiness from lc_business where ChiNameAbbr ='深科技'	ccks_stock
select a.SecuCode, b.LegalRepr , b.OfficeAddr from lc_coconcept as a join lc_stockarchives as b on a.CompanyCode = b.CompanyCode where a.ConceptName ='Edge Computing' ;	ccks_stock
select ChiNameAbbr,AStockCode from lc_stockarchives where State='新疆维吾尔自治区';	ccks_stock
select a.FullName,b.AShareAbbr from lc_issueandlistagent as a join lc_stockarchives as b on a.CompanyCode=b.CompanyCode  where b.ChiNameAbbr='武汉控股';	ccks_stock
select b.Type, count(*) from mf_fundreturnrank as a join mf_fundarchives as b on a.InnerCode = b.InnerCode where a.IndexCycle = '6 months' and a.FundReturnMean < 0 group by b.Type	ccks_fund
select a.SecuAbbr from mf_fundrisklevel as a join mf_fundarchives as b on a.InnerCode = b.InnerCode where a.RiskLevel = 'Medium-High' and b.Type = '开放式'	ccks_fund
select IssueVolFloor, IssueVolCeiling from lc_ashareseasonednewissue where SecuCode = '002305';	ccks_stock
select SecuAbbr from mf_fundreturnrank where IndexCycle = '6 months' order by FundReturn desc limit 1	ccks_fund
select NetInterestExpense from lc_financialexpense where strftime('%Y', EndDate)<'2017' and ChiNameAbbr = '八方股份';	ccks_stock
select ChiNameAbbr, BonusShareRatio from lc_dividend order by BonusShareRatio desc limit 1;	ccks_stock
select ChiNameAbbr from lc_dividend order by BonusShareRatio desc limit 1;	ccks_stock
select SHName from lc_largeshsubscription where ChiNameAbbr='广州浪奇';	ccks_stock
select a.Name, a.Performance from mf_fundmanagernew as a join mf_fundarchives as b on a.InnerCode = b.InnerCode where b.SecuMarket = '上海期货交易所'	ccks_fund
select ChiNameAbbr, ControllerName from lc_actualcontroller where SecuCode like '6%';	ccks_stock
select SHName, HoldingSum from lc_relatedsh where ChiNameAbbr ='农发种业' and strftime('%Y', EndDate)<'2019';	ccks_stock
select count(*)  from lc_mainoperincome  where strftime('%Y', EndDate) > strftime('%Y', DATE('now', '-3 year')) and GrossProfit >1;	ccks_stock
select b.Background from mf_fundmanagernew as a join mf_personalinfo as b on a.PersonalCode = b.PersonalCode where Performance < 0 and ManagementTime > 200	ccks_fund
select a.ChineseName, b.Education, b.ExperienceTime from mf_fmretscaleanalysis as a join mf_personalinfo as b on a.PersonalCode = b.PersonalCode where a.WeightedAvgMonReturn > 0	ccks_fund
select RiskLevel from mf_fundrisklevel where SecuAbbr = '国金50'	ccks_fund
select InvestAdvisorAbbrName, EstablishmentDate from mf_investadvisoroutline where InvestAdvisorAbbrName = '大成基金' or InvestAdvisorAbbrName = '兴银基金';	ccks_fund
select State,City,EstablishmentDate from lc_stockarchives where ChiNameAbbr='同仁堂';	ccks_stock
select b.Manager,a.MarketValue from mf_bondportifoliodetail as a join mf_fundarchives as b on a.InnerCode=b.InnerCode where a.BondAbbr='博世转债';	ccks_fund
select ProportionGRQuarter from lc_shnumber  where strftime('%Y', EndDate)='2020' and round(strftime('%m',EndDate)/3.0 + 0.495)=2 and ChiNameAbbr='京基智农';	ccks_stock
select ChiNameAbbr from qt_monthdata  where PB < 1 and strftime('%Y', EndDate) = strftime('%Y', date()) and strftime('%m', EndDate)='1';	ccks_stock
select BenchGRFor6Month from mf_benchmarkgrowthrate where SecuAbbr='易方达中盘ETF';	ccks_fund
select b.ChineseName,b.BirthDate from mf_fmscaleanalysisn as a join mf_personalinfo as b on a.PersonalCode=b.PersonalCode order by a.BondFundNV desc limit 10;	ccks_fund
select a.ChiNameAbbr from lc_intassetsdetail as a join  lc_stockarchives as b on a.CompanyCode=b.CompanyCode  where strftime('%Y', a.EndDate)=strftime('%Y', DATE('now', '-1 year')) and b.State='浙江省' and TotalRDInput>100000000;	ccks_stock
select InvestAdvisorName from mf_fundarchives where TrusteeName='北京银行股份有限公司';	ccks_fund
select SecuAbbr,Manager from mf_fundarchives where InvestAdvisorName='合煦智远基金管理有限公司' and FundType='Bond Fund';	ccks_fund
select b.SecuAbbr,b.Manager from mf_benchmarkgrowthrate as a join mf_fundarchives as b on a.InnerCode=b.InnerCode order by a.BenchGRFor1Year desc limit 10	ccks_fund
select ChiName,AStockCode from lc_stockarchives where ChiNameAbbr='德美化工';	ccks_stock
select a.SecuAbbr,b.InvestField from mf_benchmarkgrowthrate as a join mf_fundarchives as b on a.InnerCode=b.InnerCode   where a.DailyBenchGR>0;	ccks_fund
select count(*) from lc_sharesfloatingschedule where Proportion1 < 20	ccks_stock
select SecuAbbr from mf_benchmarkgrowthrate order by BenchGRFor3Month desc limit 10;	ccks_fund
select a.ChineseName, b.Education from mf_fmretscaleanalysis as a join mf_personalinfo as b on a.PersonalCode = b.PersonalCode where a.AvgAUM < 20 and a.FundTypeName = 'Equity Fund'	ccks_fund
select ProportionGRQuarter from lc_shnumber  where strftime('%Y', EndDate)='2020' and round(strftime('%m',EndDate)/3.0 + 0.495)=4 and ChiNameAbbr='京基智农';	ccks_stock
select Education, Gender, count(*) from mf_personalinfo group by Education, Gender;	ccks_fund
select InvestAdvisorName,count(*) from mf_fundarchives where InvestStyle='Sector Equity – Financials & Real Estate' group by InvestAdvisorName;	ccks_fund
select SHName, SecuCode from lc_relatedsh  where SHInvestSum > 10000000 and strftime('%Y', EndDate) > strftime('%Y', DATE('now', '-2 year')) ;	ccks_stock
select a.SecuAbbr,a.DailyBenchGR from mf_benchmarkgrowthrate as a join mf_fundarchives as b on a.InnerCode=b.InnerCode  where b.Type='LOF';	ccks_fund
select ChiName from lc_relatedsh  where strftime('%Y', EndDate)='2010' and strftime('%m', EndDate )='5' and SHInvestSum > 100000000	ccks_stock
select SHName from lc_largeshsubscription where SecuCode='000686';	ccks_stock
select b.SecuAbbr,b.Manager from mf_bondportifoliodetail as a join mf_fundarchives as b on a.InnerCode=b.InnerCode where a.BondAbbr='百润转债' order by a.MarketValue desc limit 1;	ccks_fund
select b.Education from mf_fmperfanalysis as a join mf_personalinfo as b on a.PersonalCode = b.PersonalCode where a.AnnSortinoR > 2 group by b.Education having count(*) > 10	ccks_fund
select a.TotalAUMTypeAvg from mf_fmretandscalerank as a join mf_personalinfo as b on a.PersonalCode = b.PersonalCode where b.Education = 'Bachelor''s degree'	ccks_fund
select ChiNameAbbr from lc_shnumber where AvgHoldSumGRQuarter>5;	ccks_stock
select MainBusiness , IndustryName from lc_business where ChiNameAbbr ='浙大网新'	ccks_stock
select SHName from lc_largeshsubscription where SecuCode='600165';	ccks_stock
select a.Name, a.Performance from mf_fundmanagernew as a join mf_fundrisklevel as b on a.InnerCode = b.InnerCode where b.RiskLevel = 'Medium-High'	ccks_fund
select BonusShareRatio, CashDiviRMB from lc_dividend where SecuCode ='000552';	ccks_stock
select b.Type, count(*) from mf_netvalueperformancehis as a join mf_fundarchives as b on a.InnerCode = b.InnerCode where a.RRInSingleYear > 20 group by b.Type;	ccks_fund
select a.FullName,b.SHName from lc_issueandlistagent as a join lc_largeshsubscription as b on a.CompanyCode=b.CompanyCode where a.ChiNameAbbr='天健集团';	ccks_stock
select SecuAbbr from mf_benchmarkgrowthrate where BenchGRFor7Year>200;	ccks_fund
select b.SecuAbbr,b.Manager,a.BenchGRFor6Month from mf_benchmarkgrowthrate as a join mf_fundarchives as b on a.InnerCode=b.InnerCode where a.BenchGRFor6Month>0;	ccks_fund
select count(*) from lc_mainoperincome where ChiNameAbbr='中国石化' and MainOperIncome > 200000000000 ;	ccks_stock
select count(*) from lc_relatedsh  where strftime('%Y', EndDate)='2020' and strftime('%m', EndDate )='3' and SHInvestSum > 100000000	ccks_stock
select count(*) from mf_fundarchives  where strftime('%Y', StartDate)='2021' and strftime('%m', StartDate)='5' and FundType='Infrastructure Securities Investment Fund';	ccks_fund
select b.Manager,b.InvestAdvisorName,a.EquityFundNV from mf_fmscaleanalysisn as a join mf_fundarchives as b on a.ChineseName=b.Manager where a.EquityFundNV>50;	ccks_fund
select b.SecuAbbr,b.Manager,b.ProfitDistributionRule from mf_benchmarkgrowthrate as a join mf_fundarchives as b on a.InnerCode=b.InnerCode order by a.WeeklyBenchGR desc limit 10;	ccks_fund
select InvestAdvisorName,count(*) from mf_fundarchives where FundNature='QDII Fund' and InvestmentType='Optimized Index-Based' group by InvestAdvisorName order by count(*) desc limit 1;	ccks_fund
select b.SecuAbbr,b.InvestTarget from mf_benchmarkgrowthrate as a join mf_fundarchives as b on a.InnerCode=b.InnerCode   order by a.BenchGRForThisWeek desc limit 10;	ccks_fund
select a.ChiNameAbbr from lc_mainoperincome as a join lc_stockarchives as b on a.CompanyCode = b.CompanyCode  where b.State ='浙江省' and strftime('%Y', EndDate)='2020' order by  a.MainOperCost limit 1;	ccks_stock
select SecuAbbr from mf_benchmarkgrowthrate order by BenchGRForThisQuarter desc limit 10;	ccks_fund
select b.ChineseName,b.Gender,b.Education from mf_fmscaleanalysisn as a join mf_personalinfo as b on a.PersonalCode=b.PersonalCode where a.EquityFundNV>100;	ccks_fund
select ChiNameAbbr, MainBusiness from lc_business where ChiNameAbbr ='南华生物' or ChiNameAbbr ='浙大网新'	ccks_stock
select RRInSelectedMonth, RRInSingleMonth from mf_netvalueperformancehis where SecuAbbr = '天弘恒享';	ccks_fund
select LegalRepr,GeneralManager from lc_stockarchives where AStockCode='600135';	ccks_stock
select a.ChiNameAbbr, a.City, a.GeneralManager from lc_stockarchives as a join lc_exgindustry as b on a.CompanyCode = b.CompanyCode where b.FirstIndustryName = 'Manufacturing'	ccks_stock
select ChiName, ChiNameAbbr from lc_buyback  where strftime('%Y', AdvanceDate) > strftime('%Y', DATE('now', '-2 year'));	ccks_stock
select b.Manager,b.InvestAdvisorName from mf_bondportifoliodetail as a join mf_fundarchives as b on a.InnerCode=b.InnerCode where a.BondAbbr='20国开08' order by a.MarketValue desc limit 1;	ccks_fund
select ChiNameAbbr from lc_stockarchives where GeneralManager like '刘%';	ccks_stock
select MainOperIncome, MainOperProfit from lc_mainoperincome  where strftime('%Y', EndDate) = strftime('%Y', DATE('now', '-1 year')) and SecuCode ='000752';	ccks_stock
select a.SecuAbbr,b.Manager from mf_benchmarkgrowthrate as a  join mf_fundarchives as b on a.InnerCode=b.InnerCode  where a.DailyBenchGR<0;	ccks_fund
select LegalRepr,GeneralManager from lc_stockarchives where ChiNameAbbr='维宏股份';	ccks_stock
select SecuAbbr,BenchGRFor1Year from mf_benchmarkgrowthrate;	ccks_fund
select SecuAbbr,SecuCode,InvestAdvisorName from mf_fundarchives where Manager='张坤';	ccks_fund
select ChiNameAbbr, ControllerName from lc_actualcontroller where SecuCode like '300%' order by SecuCode;	ccks_stock
select a.Education, count(*) from mf_personalinfo as a join mf_fmscaleanalysisn as b on a.PersonalCode = b.PersonalCode where b.TotalFundNV > 100 group by a.Education;	ccks_fund
select SHName, SecuCode, SHInvestSum from lc_relatedsh  where SHInvestSum > 10000000 and strftime('%Y', EndDate) = strftime('%Y', DATE('now', '-2 year')) ;	ccks_stock
select ChiNameAbbr from lc_shnumber where HoldProportionPAccount<10;	ccks_stock
select b.SecuAbbr,b.Type from mf_benchmarkgrowthrate as a join mf_fundarchives as b on a.InnerCode=b.InnerCode  where a.MonthlyBenchGR<0;	ccks_fund
select b.Education, count(*) from mf_fmperfanalysis as a join mf_personalinfo as b on a.PersonalCode = b.PersonalCode where a.AnnAlphaCoef > 0.5 group by b.Education	ccks_fund
select b.SecuAbbr,b.InvestAdvisorName from mf_benchmarkgrowthrate as a join mf_fundarchives as b on a.InnerCode=b.InnerCode  where a.MonthlyBenchGR>8;	ccks_fund
select ServiceLine from mf_investadvisoroutline where InvestAdvisorAbbrName = '方正富邦基金';	ccks_fund
select b.Manager,b.InvestAdvisorName from mf_fmscaleanalysisn as a join mf_fundarchives as b on a.ChineseName=b.Manager order by a.NumberOfFunds desc limit 1;	ccks_fund
select SHName, HoldingSum from lc_relatedsh  where SecuCode ='000948' and strftime('%Y', EndDate) > strftime('%Y', DATE('now', '-3 year'));	ccks_stock
select a.SecuCode , b.LegalRepr , b.SecretaryBD from lc_coconcept as a join lc_stockarchives as b on a.CompanyCode = b.CompanyCode where a.ConceptName ='Industrial Internet' ;	ccks_stock
select ChineseName from mf_personalinfo  where Nationality = '缅甸' and strftime('%Y', PracticeDate)='2015';	ccks_fund
select ChiNameAbbr from lc_mainoperincome  where strftime('%Y', EndDate) = strftime('%Y', DATE('now', '-1 year')) order by  MainOperIncome desc limit 1;	ccks_stock
select b.ChineseName, b.TotalFundNV, b.EquityFundNV, b.HybridFundNV from mf_personalinfo as a join mf_fmscaleanalysisn as b on a.PersonalCode = b.PersonalCode where a.Nationality != '关岛';	ccks_fund
select SHName,OughtShares,ActualShares from lc_largeshsubscription where ChiNameAbbr='双节电气';	ccks_stock
select b.SecuAbbr,b.InvestTarget from mf_benchmarkgrowthrate as a join mf_fundarchives as b on a.InnerCode=b.InnerCode  order by a.MonthlyBenchGR desc limit 10;	ccks_fund
select SecuAbbr from mf_fundarchives where FundType='Other Type' and InvestStyle='配置型';	ccks_fund
select InvestAdvisorAbbrName from mf_investadvisoroutline where RegCapital < 1000000000;	ccks_fund
select SecuCode, ControllerName from lc_actualcontroller where SecuCode = '600881' or SecuCode = '601158';	ccks_stock
select SecuAbbr,DailyBenchGR from mf_benchmarkgrowthrate where DailyBenchGR>0 order by DailyBenchGR desc;	ccks_fund
select b.ChiNameAbbr, b.ControllerName from lc_stockarchives as a join lc_actualcontroller as b on a.CompanyCode = b.CompanyCode where a.City = '杭州市';	ccks_stock
select count(*) from mf_fundarchives  where SecuMarket='上海黄金交易所' and Type='开放式' and strftime('%Y', ListedDate)='2021';	ccks_fund
select b.Manager,a.BondAbbr from mf_bondportifoliodetail as a join mf_fundarchives as b on a.InnerCode=b.InnerCode where a.SecuAbbr='富国天丰';	ccks_fund
select BusinessMinor from lc_business lb where ChiNameAbbr ='深科技'	ccks_stock
select SecuCode from mf_fundarchives where SecuAbbr='易方达人工智能ETF';	ccks_fund
select b.Type, count(*) from mf_fundreturnrank as a join mf_fundarchives as b on a.InnerCode = b.InnerCode where a.IndexCycle = '1 year' and a.FundReturn < 0 group by b.Type	ccks_fund
select FPSHName, AccuFPShares from lc_sharefpsta where ChiNameAbbr = '新天然气' and AccuPCTOfPled > 0.8	ccks_stock
select count(*) from lc_stockarchives as a join lc_freefloat as b on a.CompanyCode = b.CompanyCode where a.State = '江苏省' and b.AdjFreeFloatRatio = 100	ccks_stock
select SHName, HoldingPCT from lc_relatedsh where ChiNameAbbr = '诺德股份';	ccks_stock
select ChiNameAbbr from lc_financialexpense order by NetInterestExpense asc	ccks_stock
select SHName,OughtShares from lc_largeshsubscription where ChiNameAbbr='天山股份';	ccks_stock
select SHName from lc_largeshsubscription where SecuCode='600797';	ccks_stock
select MainOperIncome , MainOperCost, MainOperProfit from lc_mainoperincome  where strftime('%Y', EndDate) = strftime('%Y', DATE('now', '-1 year')) and SecuCode ='000822';	ccks_stock
select AShareAbbr,AStockCode from lc_stockarchives where AStockCode='600190';	ccks_stock
select MainBusiness, IndustryName from lc_business where ChiNameAbbr = '精研科技'	ccks_stock
select b.ChiNameAbbr from lc_intassetsdetail as a join lc_stockarchives as b on a.CompanyCode=b.CompanyCode  where b.State='广东省' order by a.RDStaffNum desc limit 50;	ccks_stock
select SecuAbbr,BenchGRForThisWeek from mf_benchmarkgrowthrate where BenchGRForThisWeek<0 order by BenchGRForThisWeek;	ccks_fund
select a.SecuAbbr from mf_fundreturnrank as a join mf_fundarchives as b on a.InnerCode = b.InnerCode where b.FundType = 'Bond Fund' and a.FundReturnMean > 0	ccks_fund
select b.SecuAbbr,b.Manager from mf_bondportifoliodetail as a join mf_fundarchives as b on a.InnerCode=b.InnerCode group by b.SecuAbbr order by count(*) desc limit 1;	ccks_fund
select b.Manager,a.BondAbbr,a.MarketValue from mf_bondportifoliodetail as a join mf_fundarchives as b on a.InnerCode=b.InnerCode where a.SecuAbbr='富国天丰';	ccks_fund
select b.SecuAbbr,b.Manager from mf_bondportifoliodetail as a join mf_fundarchives as b on a.InnerCode=b.InnerCode where a.BondAbbr='南银转债';	ccks_fund
select UnderwritingVol from lc_issueandlistagent where ChiNameAbbr='天健集团';	ccks_stock
select ChiNameAbbr from lc_shnumber where AvgHoldSumGRQuarter<5;	ccks_stock
select b.SecuAbbr,b.Manager from mf_bondportifoliodetail as a join mf_fundarchives as b on a.InnerCode=b.InnerCode where a.BondAbbr='杭银转债';	ccks_fund
select a.SecuAbbr from mf_fundrisklevel as a join mf_fundarchives as b on a.InnerCode = b.InnerCode where a.RiskLevel = 'Medium' and b.FundType= 'Bond Fund'	ccks_fund
select ChiNameAbbr,RegArea from lc_stockarchives where City='长春市';	ccks_stock
select a.Name, b.Education from mf_fundmanagernew as a join mf_personalinfo as b on a.PersonalCode = b.PersonalCode order by a.ManagementTime desc limit 1	ccks_fund
select a.ChiNameAbbr, a.GeneralManager, a.LegalRepr from lc_stockarchives as a join lc_actualcontroller as b on a.CompanyCode = b.CompanyCode where b.NationalityDesc = 'United States';	ccks_stock
select SHName,ActualShares from lc_largeshsubscription where SecuCode='600110';	ccks_stock
select OrganizationForm, count(*) from mf_investadvisoroutline group by OrganizationForm;	ccks_fund
select a.FullName,a.UnderwritingSum,b.SHName,b.ActualShares from lc_issueandlistagent as a join lc_largeshsubscription as b on a.CompanyCode=b.CompanyCode where a.ChiNameAbbr='天健集团';	ccks_stock
select SHName from lc_relatedsh  where HoldingSum > 10000000 and strftime('%Y', EndDate)='2020' ;	ccks_stock
select SecuAbbr from mf_fundreturnrank where IndexCycle = 'year to date' and FundReturn < 0	ccks_fund
select DepositsWithCentralBank  from ed_otherdepositorycorpbs ;	ccks_macro
select FPSHName from lc_sharefpsta where ChiNameAbbr = '哈尔斯' or ChiNameAbbr = '京运通'	ccks_stock
select EndDate, ClaimsOnGovernment , ClaimsOnCentralBank from ed_otherdepositorycorpbs  where strftime('%Y', EndDate) = strftime('%Y', DATE('now', '-1 year')) and round(strftime('%m',EndDate)/3.0 + 0.495) = 4;	ccks_macro
select count(*) from mf_fundreturnrank where SecuCode like '16%' and FundReturn > 0	ccks_fund
select ChineseName from mf_fmscaleanalysisn where EquityFundNV > 200;	ccks_fund
select InvestAdvisorName from mf_fundarchives where InvestmentType='Index-Based' group by InvestAdvisorName order by count(*) desc limit 1;	ccks_fund
select TurnoverVolume, TurnoverValue from qt_dailyquote where ChiNameAbbr = '科思股份';	ccks_stock
select ChineseName from mf_personalinfo where ChineseName like '王%' and ExperienceTime > 10;	ccks_fund
select SecuCode, ChiNameAbbr from lc_dividend where BonusShareRatio is not null;	ccks_stock
select PlaYear, PlaPrice, PlaProceeds from lc_ashareplacement where ChiNameAbbr = '四川美丰';	ccks_stock
select Fund from mf_awards where FundCompany ='鹏华基金管理有限公司';	ccks_fund
select count(*) from mf_chargeratenew where ClientType ='Pension Fund Client';	ccks_fund
select b.Type from mf_netvalueperformancehis as a join mf_fundarchives as b on a.InnerCode = b.InnerCode group by b.Type order by avg(a.NVDailyGrowthRate) desc limit 1;	ccks_fund
select AccumulatedUnitNV from mf_netvalue  where SecuAbbr = '国投瑞盈' and strftime('%Y', EndDate) = strftime('%Y', date());	ccks_fund
select SponsorName from lc_ipodeclaration where ChiNameAbbr='红塔证券';	ccks_stock
select CSRCIndustryName from lc_ipodeclaration where strftime('%Y', EndDate)>'2017' group by CSRCIndustryName order by count(*) desc limit 1;	ccks_stock
select IndexValue from ed_producerpiformp  where IndexName ='Metal Products' and ReportPeriod ='Same period last year' and strftime('%Y', EndDate) = strftime('%Y', DATE('now', '-1 year')) ;	ccks_macro
select RRInFiveYear from mf_netvalueperformancehis ;	ccks_fund
select RatioCeiling from ed_taxrate where TypeName ='Rural Credit Cooperatives' and ItemName ='Excess Reserve Requirement Ratio';	ccks_macro
select b.ChiNameAbbr, a.FirstIndustryName from lc_exgindustry as a join lc_sharestru as b on a.CompanyCode = b.CompanyCode where b.TotalShares > 10000000000	ccks_stock
select GDP, PrimaryIndustryGDP, SecondIndustryGDP, ThirdIndustryGDP from ed_grossdomesticproduct ;	ccks_macro
select PracticeDate from mf_personalinfo where ChineseName = '柳军';	ccks_fund
select b.LeaderName, b.ChiNameAbbr from lc_stockarchives as a join lc_executivesholdings as b on a.CompanyCode = b.CompanyCode where a.State = '浙江省' and b.PositionDescription like '%Deputy General Manager%'	ccks_stock
select ConceptName from lc_coconcept where SecuCode ='002354';	ccks_stock
select a.ChiNameAbbr , b.State, b.City from lc_business as a join lc_stockarchives as b on a.CompanyCode = b.CompanyCode where a.IndustryName ='Capital Market Services';	ccks_stock
select NationalityDesc, count(ChiNameAbbr) from lc_actualcontroller group by NationalityDesc;	ccks_stock
select SecuAbbr,SecuCode from mf_bondportifoliodetail where BondCode='128125'	ccks_fund
select ChiNameAbbr from lc_stockholdingst  where strftime('%Y', EndDate)='2021' order by  TrustCompaniesHoldPropA desc limit 10;	ccks_stock
select Bonds, CentralBankBonds from ed_chinamoneyandbanking  where strftime('%Y', EndDate) = strftime('%Y', DATE('now', '-1 year')) ;	ccks_macro
select a.ChiNameAbbr from lc_stockarchives as a join lc_exgindustry as b on a.CompanyCode = b.CompanyCode where a.State = '广东省' and b.FirstIndustryName = 'Real Estate'	ccks_stock
select b.ChiNameAbbr,a.SHName from lc_largeshsubscription as a join lc_stockarchives as b on a.CompanyCode=b.CompanyCode  where b.City='广州市';	ccks_stock
select LeaderName, ChiNameAbbr from lc_executivesholdings where PositionDescription like '%Chairman of the Board%' or PositionDescription like '%Vice Chairman of the Board%'	ccks_stock
select b.ChiNameAbbr, b.Ashares from lc_exgindustry as a join lc_sharestru as b on a.CompanyCode = b.CompanyCode where a.FirstIndustryName = 'Manufacturing' order by b.Ashares desc	ccks_stock
select Maturity, RatioFloor, RatioCeiling from ed_taxrate where TypeName ='Outright Repurchase of Government Bonds' and ItemName ='Handling Fee';	ccks_macro
select LocalGovRevenue, LocalGovExpenditure from ed_financialbalance  where strftime('%Y', EndDate)='2010' ;	ccks_macro
select count(*) from mf_awards where AwardName = '三年持续回报明星基金公司奖';	ccks_fund
select EndDate, TotalAssets, TotalLiabilities from ed_otherdepositorycorpbs where TotalLiabilities < 5000000 and TotalAssets > 50000000;	ccks_macro
select a.ChineseName, b.Education from mf_fmretandscalerank as a join mf_personalinfo as b on a.PersonalCode = b.PersonalCode where a.TimeInterval = 'Past 1 Year' order by a.ReturnTypeAvg desc limit 5	ccks_fund
select b.ChiNameAbbr from lc_stockarchives as a join lc_freefloat as b on a.CompanyCode = b.CompanyCode where a.State = '广东省' and b.TotalAShare > 100000000	ccks_stock
select FundCompany from mf_awards where AppraisalOrgCode ='14561';	ccks_fund
select GDP, GDPPerCapita from ed_grossdomesticproduct where Province ='浙江';	ccks_macro
select  SecuCode, SecuAbbr from mf_netvalueperformancehis where AnnualizedRRSinceStart > 30;	ccks_fund
select SecuAbbr from mf_benchmarkgrowthrate where DailyBenchGR>0 order by DailyBenchGR desc	ccks_fund
select StateOwnedUnits, CollectiveUnits, JointVentures from ed_retailvalueofscgoods ;	ccks_macro
select SecuCode , MainOperProfit from lc_mainoperincome where MainOperProfit > 100000000;	ccks_stock
select FullName from lc_issueandlistagent where ChiNameAbbr='天健集团';	ccks_stock
select EndDate, Province, PrimaryIndustryGDP, SecondIndustryGDP, ThirdIndustryGDP from ed_grossdomesticproduct  where strftime('%Y', EndDate) > strftime('%Y', DATE('now', '-5 year') ) ;	ccks_macro
select a.State, count(*) from lc_stockarchives as a join lc_business as b on a.CompanyCode = b.CompanyCode where b.IndustryName ='Pharmaceutical Manufacturing' group by a.State ;	ccks_stock
select FullName,UnderwritingSum from lc_issueandlistagent where SecuCode='000401';	ccks_stock
select ChiNameAbbr, SecuCode from lc_legaldistribution  where strftime('%Y', InfoPublDate) = strftime('%Y', DATE('now', '-1 year'));	ccks_stock
select ImValueOfGoods , ExValueOfGoods from ed_exportimport  where GYoYOfExValueGoods > 0 and GYoYOfImValueGoods < 0 and strftime('%Y', EndDate)='2000';	ccks_macro
select CashDiviRMB from lc_dividend where SecuCode ='000021';	ccks_stock
select RRInTwoYear from mf_netvalueperformancehis ;	ccks_fund
select count(*) from lc_ashareseasonednewissue  where strftime('%Y', AdvanceDate)='2020';	ccks_stock
select SHName,ActualShares from lc_largeshsubscription where SecuCode='600110';	ccks_stock
select SecuAbbr from mf_fundarchives order by EstablishmentDate asc limit 1	ccks_fund
select SecuAbbr,MarketValue from mf_bondportifoliodetail where BondCode='128125'	ccks_fund
select b.ChineseName from mf_managerexperience a join mf_personalinfo b on a.PersonalCode = b.PersonalCode order by a.EmploymentCompany desc limit 1	ccks_fund
select AnnualizedRRInTenYear from mf_netvalueperformancehis ;	ccks_fund
select ChiName from mf_fundarchives where SecuCode='160215';	ccks_fund
select a.City , count(*)  from lc_stockarchives as a join lc_coconcept as b on a.CompanyCode = b.CompanyCode where b.ConceptName ='Domestic Software' group by a.City;	ccks_stock
select b.Type, count(*) from mf_netvalueperformancehis as a join mf_fundarchives as b on a.InnerCode = b.InnerCode where a.RRInSingleYear > 20 group by b.Type;	ccks_fund
select CashDiviRMB from lc_dividend where SecuCode ='000040';	ccks_stock
select DivIntervalDes, ChargeRateDes from mf_chargeratenew where SecuAbbr ='富国创新药ETF';	ccks_fund
select count(*) from lc_ashareplacement where PlaProceeds > 10000000000;	ccks_stock
select OtherForeignAssets, AbroadLiability from ed_moneyauthoritybs ;	ccks_macro
select LeaderName, ChiNameAbbr from lc_executivesholdings where PositionDescription like '%Chairman of the Board%' and PositionDescription like '%General Manager%'	ccks_stock
select IndustryName from lc_business where ChiNameAbbr ='精研科技'	ccks_stock
select RRInThreeYear from mf_netvalueperformancehis ;	ccks_fund
select AccountingFirm,SignatureAccountant from lc_ipodeclaration where ChiNameAbbr='大业股份';	ccks_stock
select ActualShares from lc_largeshsubscription where ChiNameAbbr='深科技';	ccks_stock
select ChiNameAbbr from lc_exgindustry where SecondIndustryName = 'Capital Market Services'	ccks_stock
select b.TotalRDInput from lc_ipodeclaration as a join lc_intassetsdetail as b on a.CompanyCode=b.CompanyCode  where strftime('%Y', a.EndDate)>'2018' and a.SponsorName='广发证券';	ccks_stock
select ThirdIndustryGDP from ed_grossdomesticproduct ;	ccks_macro
select State,LegalRepr from lc_stockarchives where ChiNameAbbr='五粮液';	ccks_stock
select OtherInstiHoldPropA from lc_stockholdingst  where strftime('%Y', EndDate)='2020' and round(strftime('%m',EndDate)/3.0 + 0.495)=1 and ChiNameAbbr='步步高';	ccks_stock
select TotalAssets from ed_moneyauthoritybs ;	ccks_macro
select Authorizer from lc_sharetrustee  where strftime('%Y', InfoPublDate)='2018' and ChiNameAbbr='新日恒力' order by  PCTOfAuthorizer desc limit 1;	ccks_stock
select ExImValueOfGoods, ImValueOfGoods, ExValueOfGoods from ed_exportimport ;	ccks_macro
select a.Education, max(b.TotalFundNV) from mf_personalinfo as a join mf_fmscaleanalysisn as b on a.PersonalCode = b.PersonalCode group by a.Education;	ccks_fund
select SecuCode from lc_mainoperincome where MainIncomeGrowRateYOY < 0 and strftime('%Y', EndDate)<'2019';	ccks_stock
select LeaderName, PositionDescription, ChiNameAbbr from lc_executivesholdings  where strftime('%Y', EndDate)='2020' order by  ShareAmount desc limit 5	ccks_stock
select avg(RatioInNV)  from mf_keystockportfolio where SecuAbbr = '富国天惠A'	ccks_fund
select EndDate,  SubjectSum from ed_newincreasingloan where ReportPeriod ='End-of-period cumulative' ;	ccks_macro
select b.Manager,a.BondAbbr from mf_bondportifoliodetail as a join mf_fundarchives as b on a.InnerCode=b.InnerCode where a.SecuCode='160615';	ccks_fund
select FullName,Address from lc_issueandlistagent where ChiNameAbbr='湖北宜化';	ccks_stock
select TotalSavings , TotalLoans from ed_chinafibalancesheetrmb;	ccks_macro
select ChiNameAbbr,QFIIHoldPropA from lc_stockholdingst  where strftime('%Y', EndDate)='2020';	ccks_stock
select b.ChineseName from mf_managerexperience a join mf_personalinfo b on a.PersonalCode = b.PersonalCode order by a.EmploymentCompany asc  limit 1	ccks_fund
select TotalShare, FloatShare from qt_monthdata where ChiNameAbbr = '东方电子';	ccks_stock
select RetailValueOfSCGoods from ed_retailvalueofscgoods where Province ='北京' and ReportPeriod ='End-of-period cumulative' and strftime('%Y', EndDate)>='2000';	ccks_macro
select ClosePrice, FloatShare from qt_monthdata where SecuCode = '000822';	ccks_stock
select ChineseName from mf_fmscaleanalysisn order by NumberOfFunds desc limit 1;	ccks_fund
select b.SecuAbbr from mf_netvalueperformancehis as a join mf_fundarchives as b on a.InnerCode = b.InnerCode where b.FundType = 'Equity Fund' and a.RRInSingleWeek > 5;	ccks_fund
select SecuAbbr from mf_fundarchives  where strftime('%Y', EstablishmentDate)=strftime('%Y', DATE('now', '-1 year')) and round(strftime('%m',EstablishmentDate)/3.0 + 0.495)=1	ccks_fund
select City from lc_stockarchives where State='广东省' group by City order by count(*) desc limit 1;	ccks_stock
select ChiNameAbbr from lc_actualcontroller where NationalityDesc = 'United States';	ccks_stock
select SHName, SecuCode, HoldingSum from lc_relatedsh  where HoldingSum > 10000000  and strftime('%Y', EndDate) >= strftime('%Y', DATE('now', '-2 year'));	ccks_stock
select  Fund from  mf_awards  where strftime('%Y', Year) >=2010 and AppraisalOrg ='China Securities Journal' ;	ccks_fund
select MainOperIncome, MainOperCost, MainOperProfit from lc_mainoperincome  where strftime('%Y', EndDate) = strftime('%Y', DATE('now', '-1 year')) and ChiNameAbbr ='古井贡酒';	ccks_stock
select SHName, HoldingPCT from lc_relatedsh where ChiNameAbbr = '诺德股份';	ccks_stock
select a.ChiNameAbbr, b.FirstIndustryName from lc_sharetransfer as a join lc_exgindustry as b on a.CompanyCode = b.CompanyCode where a.PCTAfterTran > 0.5	ccks_stock
select a.SecuAbbr from mf_netvalueperformancehis as a join mf_fundarchives as b on a.InnerCode = b.InnerCode and b.FundType ='Equity Fund' where a.AnnualizedRRSinceStart > 50;	ccks_fund
select b.SecuAbbr from mf_benchmarkgrowthrate as a join mf_fundarchives as b on a.InnerCode=b.InnerCode where a.BenchGRFor6Month>5 and b.InvestmentType='Index-Based';	ccks_fund
select  SecuCode, SecuAbbr  from mf_netvalueperformancehis where RRSinceStart < -30;	ccks_fund
select a.SecuAbbr, b.FoundedSize, b.FundType from mf_netvalueperformancehis as a join mf_fundarchives as b on a.InnerCode = b.InnerCode order by a.NVDailyGrowthRate desc limit 3;	ccks_fund
select MainBusiness from lc_business where ChiNameAbbr ='深科技'	ccks_stock
select EndDate, StateOwnedControlledComAP, CollectiveComAP from ed_industryproduction where Province ='上海' and StatStandard ='All Industrial Enterprises' and ReportPeriod ='End-of-period cumulative' ;	ccks_macro
select SecuCode , UnitNV from  mf_netvalue ;	ccks_fund
select InvolvedTrustSum from lc_sharetrustee  where strftime('%Y', InfoPublDate)='2016' and ChiNameAbbr='澳柯玛';	ccks_stock
select a.SecuAbbr, a.SecuCode from mf_netvalueperformancehis as a join mf_fundarchives as b on a.InnerCode = b.InnerCode and b.FundType ='Hybrid Fund' where a.AnnualizedRRSinceStart > 30;	ccks_fund
select DiviBase, BonusShareRatio, TranAddShareRaio from lc_dividend  where SecuCode ='000728' and strftime('%Y', DividendImplementDate) > strftime('%Y', DATE('now', '-2 year'));	ccks_stock
select SecuAbbr, NVDailyGrowthRate, RRInSingleWeek from mf_netvalueperformancehis where RRInSingleMonth > 5;	ccks_fund
select b.SecuAbbr, b.RiskLevel from mf_fundmanagernew as a join mf_fundrisklevel as b on a.InnerCode = b.InnerCode where strftime('%Y', a.AccessionDate)>'2021'	ccks_fund
select MainBusiness from lc_business where ChiNameAbbr ='浙大网新'	ccks_stock
select MonthlyBenchGR from mf_benchmarkgrowthrate where SecuAbbr='华夏行业';	ccks_fund
select count(*) from lc_stockarchives where City='厦门市';	ccks_stock
select b.SecuAbbr,b.Manager,b.InvestTarget from mf_benchmarkgrowthrate as a join mf_fundarchives as b on a.InnerCode=b.InnerCode where a.BenchGRFor5Year>20;	ccks_fund
select b.SecuAbbr,b.Manager from mf_bondportifoliodetail as a join mf_fundarchives as b on a.InnerCode=b.InnerCode where a.BondAbbr='海亮转债';	ccks_fund
select AvgAUMTypeAvg from mf_fmretandscalerank where ChineseName = '贾成东';	ccks_fund
select a.City , count(*)  from lc_stockarchives as a join lc_coconcept as b on a.CompanyCode = b.CompanyCode where b.ConceptName ='Cloud Computing'group by a.City order by count(*) desc limit 1 ;	ccks_stock
select StateOwnedUnits from ed_retailvalueofscgoods ;	ccks_macro
select BuybackSum, BuybackMoney from lc_buyback where SecuCode = '300011';	ccks_stock
select RRSinceStart from mf_netvalueperformancehis ;	ccks_fund
select RRInThreeMonth, RRInSixMonth, RRInSingleYear from mf_netvalueperformancehis where SecuAbbr = '博时策略';	ccks_fund
select FPSHName, sum(AccuFPShares) from lc_sharefpsta where ChiNameAbbr = '完美世界' group by FPSHName	ccks_stock
select BuybackSum, Percentage from lc_buyback where ChiNameAbbr = '南都电源' order by AdvanceDate desc limit 1	ccks_stock
select count(*) from lc_mainoperincome  where strftime('%Y', EndDate) = strftime('%Y', DATE('now', '-1 year')) and MainOperIncome > 100000000;	ccks_stock
select b.SHName,a.FullName from lc_issueandlistagent as a join lc_largeshsubscription as b on a.CompanyCode=b.CompanyCode where a.ChiNameAbbr='东旭蓝天';	ccks_stock
select OtherAssets, OtherLiabilities from ed_otherdepositorycorpbs ;	ccks_macro
select ChineseName from mf_fmscaleanalysisn order by EquityFundN desc limit 1;	ccks_fund
select b.FirstIndustryName, count(*) from lc_sharesfloatingschedule as a join lc_exgindustry as b on a.CompanyCode = b.CompanyCode where a.NewMarketableAShares > 100 group by b.FirstIndustryName	ccks_stock
select a.ConceptName, count(*) from lc_coconcept as a join lc_stockarchives as b on a.CompanyCode = b.CompanyCode where b.State ='海南省' group by a.ConceptName ;	ccks_stock
select BondAbbr from mf_bondportifoliodetail where SecuAbbr='鹏华价值' order by MarketValue desc limit 1;	ccks_fund
select City,RegArea from lc_stockarchives where AStockCode='600165';	ccks_stock
select SecuAbbr from mf_fundarchives where Manager = '王帅'	ccks_fund
select ClosePrice, FloatShare, TotalShare from qt_monthdata  where SecuCode = '600649' and strftime('%Y', EndDate)='2021' and round(strftime('%m',EndDate)/3.0 + 0.495) = 3;	ccks_stock
select BuybackSum, Percentage from lc_buyback  where ChiNameAbbr = '江苏租赁' and strftime('%Y', AdvanceDate)='2019' ;	ccks_stock
select TradingDay, OpenPrice, ClosePrice from qt_dailyquote where ChiNameAbbr = '山煤国际' and strftime('%Y', TradingDay)>='2018';	ccks_stock
select LeaderName from lc_executivesholdings where SecuCode = '000430'	ccks_stock
select ChiName from lc_stockarchives where strftime('%Y', EstablishmentDate)>'2001';	ccks_stock
select SumBeforeTran, PCTBeforeTran from lc_sharetransfer where SecuCode = '300707'	ccks_stock
select BonusShareRatio, CashDiviRMB from lc_dividend where ChiNameAbbr ='东北证券';	ccks_stock
select AnnualizedRRInThreeYear from mf_netvalueperformancehis ;	ccks_fund
select b.Type, avg(a.RRInSingleYear) from mf_netvalueperformancehis as a join mf_fundarchives as b on a.InnerCode = b.InnerCode group by b.Type;	ccks_fund
select IssuePurpose from lc_ashareseasonednewissue where SecuCode = '300391';	ccks_stock
select EndDate,  SubjectSum from ed_newincreasingloan  where ReportPeriod ='Month' and strftime('%Y', EndDate) = strftime('%Y', DATE('now', '-2 year'));	ccks_macro
select count(*) from lc_stockarchives where State='北京市';	ccks_stock
select MainOperIncome, MainOperProfit from lc_mainoperincome  where strftime('%Y', EndDate) = strftime('%Y', DATE('now', '-1 year')) and SecuCode ='000752';	ccks_stock
select ProportionGRHalfAYear from lc_shnumber  where strftime('%Y', EndDate)='2020' and ChiNameAbbr='京基智农';	ccks_stock
select SecuAbbr from mf_bondportifoliodetail where BondCode='128125' order by HoldVolume desc limit 1;	ccks_fund
select AccumulatedUnitNV , NVDailyGrowthRate,NVWeeklyGrowthRate from  mf_netvalue where SecuAbbr = '华安180ETF';	ccks_fund
select count(*)  from lc_coconcept as a join lc_stockarchives as b on a.CompanyCode = b.CompanyCode where a.ConceptName ='Internet Finance' and b.City ='杭州市';	ccks_stock
select WebSite from mf_investadvisoroutline where InvestAdvisorAbbrName = '浦银安盛基金';	ccks_fund
select Fund from  mf_awards  where strftime('%Y', Year) = strftime('%Y', DATE('now', '-2 year'));	ccks_fund
select BonusShareRatio, CashDiviRMB from lc_dividend where ChiNameAbbr ='古井贡酒';	ccks_stock
select ChiNameAbbr from lc_issueandlistagent where UnderwritingVol>50000000;	ccks_stock
select ChiNameAbbr from lc_stockarchives where AStockCode like '600%';	ccks_stock
select AnnualizedRRInTwoYear from mf_netvalueperformancehis ;	ccks_fund
select NetAbroadAssets, DomesticLoans from ed_chinamoneyandbanking where strftime('%Y', EndDate)<'2000';	ccks_macro
select DivIntervalDes, ChargeRateDes from mf_chargeratenew where SecuCode ='159748';	ccks_fund
select SHName from lc_largeshsubscription where ChiNameAbbr='恒生电子' order by ActualShares desc limit 1;	ccks_stock
select RRInTenYear , AnnualizedRRInTenYear from mf_netvalueperformancehis ;	ccks_fund
select IndexName, IndexValue from ed_producerpiformp where IndexType ='Industrial Structure Classification Index' and ReportPeriod ='Same month last year' and strftime('%Y', EndDate)>='2010';	ccks_macro
select SHName, SecuCode, SHInvestSum from lc_relatedsh  where SHInvestSum > 10000000 and strftime('%Y', EndDate) = strftime('%Y', DATE('now', '-2 year')) ;	ccks_stock
select FundTypeName, count(*) from mf_fundreturnrank where IndexCycle = 'since inception' and FundReturnMean > 0 group by FundTypeName	ccks_fund
select SponsorName from lc_ipodeclaration where AccountingFirm='立信会计事务所' order by EndDate desc limit 1;	ccks_stock
select IndexValue from ed_producerpiformp where ReportPeriod ='Same period last year' and IndexType ='Industrial Structure Classification Index' and IndexName ='Production Materials – Processing';	ccks_macro
select IssueVolFloor, IssueVolCeiling from lc_ashareseasonednewissue where ChiNameAbbr = '吉峰科技';	ccks_stock
select AquiredSum, AquirerAmount from lc_legaldistribution  where AquirerName ='邱丕云' and strftime('%Y', InfoPublDate) > strftime('%Y', DATE('now', '-3 year')) order by  AquirerAmount desc ;	ccks_stock
select DistributionSum, AquirerName, AquiredSum from lc_legaldistribution where SecuCode ='600517' ;	ccks_stock
select SecuAbbr from mf_netvalueperformancehis order by RRSinceStart desc limit 1;	ccks_fund
select InvestAdvisorAbbrName from mf_investadvisoroutline order by EstablishmentDate desc limit 1;	ccks_fund
select IndexValue from ed_producerpiformp  where IndexName ='Pharmaceutical Manufacturing' and ReportPeriod ='Same month last year' and strftime('%Y', EndDate) = strftime('%Y', DATE('now', '-1 year')) and round(strftime('%m',EndDate)/3.0 + 0.495) = 1 ;	ccks_macro
select SHName,ActualShares,OughtShares from lc_largeshsubscription where SecuCode='000423';	ccks_stock
select SHName from lc_largeshsubscription where OughtShares>2000000;	ccks_stock
select max(PETTM) from qt_monthdata  where SecuCode  = '600352' and strftime('%Y', EndDate)='2022';	ccks_stock
select TotalLiabilities from ed_otherdepositorycorpbs ;	ccks_macro
select a.ChineseName, b.Background from mf_fmperfanalysis as a join mf_personalinfo as b on a.PersonalCode = b.PersonalCode where a.MaxRet > 2	ccks_fund
select DivStand1 , StDivStand1, EnDivStand1 from mf_chargeratenew where SecuCode ='501065';	ccks_fund
select SecuCode, BuybackMoney from lc_buyback where strftime('%Y', AdvanceDate) >= '2019' ;	ccks_stock
select ClaimsOnOtherDepositCorp, ClaimsOnOtherResidentSec from ed_otherdepositorycorpbs where TotalAssets > 50000000;	ccks_macro
select b.ChineseName from mf_managerexperience a join mf_personalinfo b on a.PersonalCode = b.PersonalCode group by b.ChineseName order by count(*) desc limit 1	ccks_fund
select SecuAbbr,Manager from mf_fundarchives where InvestStyle='Large-Cap Value Equity';	ccks_fund
select a.SecuAbbr, a.RiskReturncharacter from mf_fundarchives as a join mf_fundrisklevel as b on a.InnerCode = b.InnerCode where b.RiskLevel = 'Medium'	ccks_fund
select OrganizationForm, count(*) from mf_investadvisoroutline group by OrganizationForm;	ccks_fund
select b.LeaderName, b.PositionDescription from lc_stockarchives as a join lc_executivesholdings as b on a.CompanyCode = b.CompanyCode where a.State = '浙江省' and b.SecuCode like '300%'	ccks_stock
select LocalGovRevenue, LocalGovExpenditure from ed_financialbalance where Province ='上海';	ccks_macro
select SecuAbbr from mf_mainfinancialindexq  where strftime('%Y', EndDate)='2020' and round(strftime('%m',EndDate)/3.0 + 0.495) = 4 and NetAssetsValue > 10000000000	ccks_fund
select count(*) from lc_stockarchives where State='山西省';	ccks_stock
select ChiNameAbbr from lc_ashareseasonednewissue  where strftime('%Y', AdvanceDate)='2022';	ccks_stock
select ChiNameAbbr from lc_exgindustry where FirstIndustryName = 'Construction'	ccks_stock
select SecuAbbr from mf_fundrisklevel where RiskLevel = 'Medium-High'	ccks_fund
select TotalProfit from mf_mainfinancialindexq  where SecuAbbr = '华夏50ETF' and strftime('%Y', EndDate)='2021' and round(strftime('%m',EndDate)/3.0 + 0.495) = 1	ccks_fund
select BusinessMajor from lc_business lb where ChiNameAbbr ='南华生物'	ccks_stock
select RRInTenYear from mf_netvalueperformancehis ;	ccks_fund
select SHName from lc_largeshsubscription where ChiNameAbbr='亚泰集团' order by ActualShares desc limit 1;	ccks_stock
select State, City from lc_stockarchives where State='湖南省' and City='长沙市';	ccks_stock
select ChiNameAbbr,avg(ActualShares) from lc_largeshsubscription group by ChiNameAbbr;	ccks_stock
select ChineseName from mf_fmscaleanalysisn where TotalFundNV < 1;	ccks_fund
select ChiNameAbbr from lc_sharesfloatingschedule where SecuCode like '6%' order by TotalAShares desc limit 1	ccks_stock
select MainOperIncome from lc_mainoperincome  where ChiNameAbbr ='冰山冷热' and strftime('%Y', EndDate)='2020'	ccks_stock
select InvestAdvisorName from mf_fundarchives group by InvestAdvisorName order by count(*) desc limit 1;	ccks_fund
select SHName,OughtShares from lc_largeshsubscription where ChiNameAbbr='天山股份';	ccks_stock
select b.Manager from mf_benchmarkgrowthrate as a join mf_fundarchives as b on a.InnerCode=b.InnerCode order by a.BenchGRFor3Month desc limit 10;	ccks_fund
select SHName, HoldingSum from lc_relatedsh where ChiNameAbbr ='力源信息' ;	ccks_stock
select count(*) from lc_stockarchives where City='武汉市';	ccks_stock
select CollectiveUnits, SelfEmployed from ed_retailvalueofscgoods  where ReportArea ='Provincial and Municipal' and ReportPeriod ='End-of-period cumulative' and strftime('%Y', EndDate) = strftime('%Y', DATE('now', '-1 year')) ;	ccks_macro
select BondAbbr from mf_bondportifoliodetail where SecuAbbr='鹏华价值' and HoldVolume>50000;	ccks_fund
select RetailValueOfSCGoods from ed_retailvalueofscgoods where Province ='北京';	ccks_macro
select RetailValueOfSCGoods from ed_retailvalueofscgoods where Province ='北京' and ReportPeriod ='End-of-period cumulative';	ccks_macro
select InterestExpense, ExchangeProLoss from lc_financialexpense  where ChiNameAbbr = '万达信息' and strftime('%Y', EndDate)>'2016'	ccks_stock
select EndDate,  SubjectSum from ed_newincreasingloan where ReportPeriod ='Month' and SubjectSum > 150000;	ccks_macro
select ChiName, SHInvestSum from lc_relatedsh  where ChiNameAbbr = '常山北明' and strftime('%Y', EndDate)='2020' and strftime('%m', EndDate )='3'	ccks_stock
select AgriculturalDeposits, SavingsDeposits from ed_chinafibalancesheetrmb;	ccks_macro
select a.ChiNameAbbr, a.FPSHName from lc_sharefpsta as a join lc_exgindustry as b on a.CompanyCode = b.CompanyCode where b.FirstIndustryName = 'Construction' order by a.AccuProportion desc	ccks_stock
select SecuAbbr,BenchGRForThisMonth from mf_benchmarkgrowthrate where BenchGRForThisMonth>5;	ccks_fund
select count(*) from lc_mainoperincome  where strftime('%Y', EndDate)='2020' and GrossProfit > 1	ccks_stock
select RRInSelectedMonth from  mf_netvalueperformancehis ;	ccks_fund
select SecuAbbr from mf_bondportifoliodetail where BondAbbr='华海转债' and HoldVolume>1000000;	ccks_fund
select a.ChiNameAbbr from lc_mainoperincome as a join lc_stockarchives as b on a.CompanyCode = b.CompanyCode   where strftime('%Y', a.EndDate)='2020' and b.State = '浙江省' order by  a.MainOperIncome desc limit 1;	ccks_stock
select count(distinct ChiNameAbbr) from qt_monthdata where strftime('%Y', EndDate)='2022' and round(strftime('%m',EndDate)/3.0 + 0.495)=1 and ClosePrice<2;	ccks_stock
select ChiName, count(*) from lc_sharefp  where strftime('%Y', EndDate)='2020' and strftime('%m', EndDate)='3' group by  ChiName	ccks_stock
select UnderwritingSum from lc_issueandlistagent where ChiNameAbbr='常山北明';	ccks_stock
select OfficeAddr from mf_investadvisoroutline where InvestAdvisorAbbrName = '建信基金';	ccks_fund
select max(RetailValueOfSCGoods) from ed_retailvalueofscgoods where Province='上海' and ReportPeriod ='End-of-period cumulative' ;	ccks_macro
select SecuAbbr from mf_netvalueperformancehis where RRInSingleMonth > 5 and RRInSingleWeek > 3;	ccks_fund
select TotalAUMRank from mf_fcretscalerank where AbbrChiName='中信证券';	ccks_fund
select Authorizer,AuthorizedReceiver from lc_sharetrustee  where strftime('%Y', InfoPublDate)='2019' and ChiNameAbbr='诺德股份';	ccks_stock
select ReserveAssets  from ed_otherdepositorycorpbs ;	ccks_macro
select NetAssetsValue from mf_mainfinancialindexq where SecuAbbr = '南方积配' order by EndDate desc limit 1	ccks_fund
select ChineseName from mf_personalinfo where Education = 'Doctoral degree'  and Gender = '男' and ChineseName like '李%'	ccks_fund
select BondFundN,BondFundNV from mf_fmscaleanalysisn where ChineseName='陈龙';	ccks_fund
select PrimaryIndustryGDP, SecondIndustryGDP, ThirdIndustryGDP from ed_grossdomesticproduct ;	ccks_macro
select AbbrChiName,AvgAUMTypeAvg from mf_fcretscalerank order by AvgAUMRank limit 1;	ccks_fund
select max(ClosePrice) from qt_monthdata where ChiNameAbbr = '东方电子'	ccks_stock
select ExpenditureCityMC from ed_financialbalance  where Province ='北京' and strftime('%Y', EndDate) = strftime('%Y', DATE('now', '-2 year')) ;	ccks_macro
select FundsHoldPropA from lc_stockholdingst  where strftime('%Y', EndDate)='2020' and strftime('%m', EndDate)='6' and ChiNameAbbr='中航重机';	ccks_stock
select AStockCode from lc_stockarchives where ChiNameAbbr='康盛股份';	ccks_stock
select SecuAbbr from mf_benchmarkgrowthrate where BenchGRFor10Year>200;	ccks_fund
select AquiredSum , AquirerAmount from lc_legaldistribution where AquirerName ='林泗华' ;	ccks_stock
select HoldProportionPAccount from lc_shnumber  where strftime('%Y', EndDate)='2019' and round(strftime('%m',EndDate)/3.0 + 0.495)=1 and ChiNameAbbr='东旭蓝天';	ccks_stock
select avg(a.AnnualizedRRSinceStart) from mf_netvalueperformancehis as a join mf_fundarchives as b on a.InnerCode = b.InnerCode and b.FundType ='Equity Fund' ;	ccks_fund
select LinkMan from mf_investadvisoroutline where InvestAdvisorAbbrName = '南方基金';	ccks_fund
select BusinessMinor from lc_business lb where ChiNameAbbr ='深科技'	ccks_stock
select a.Name from mf_fundmanagernew as a join mf_personalinfo as b on a.PersonalCode = b.PersonalCode where a.Performance > 0 and b.ExperienceTime < 2	ccks_fund
select BasisCode , RatioFloor, RatioCeiling from ed_taxrate where TypeName ='Pledged Repurchase of Corporate Bonds' and ItemName = 'Handling Fee' ;	ccks_macro
select a.State , count(*) from lc_stockarchives as a join lc_business as b on a.CompanyCode = b.CompanyCode where b.IndustryName ='Professional and Technical Services' group by a.State order by count(*) desc limit 1 ;	ccks_stock
select SocialSecuFundHoldPropA from lc_stockholdingst  where strftime('%Y', EndDate)='2020' and strftime('%m', EndDate)='5' and ChiNameAbbr='奥普光电';	ccks_stock
select SponsorName,LawFirm,AccountingFirm from lc_ipodeclaration where SecuCode='300278';	ccks_stock
select LeaderName from lc_executivesholdings where ChiNameAbbr = '越剑智能' and ShareAmountBeginning > 10000000	ccks_stock
select EvalAgent from lc_ipodeclaration where ChiNameAbbr='福斯特';	ccks_stock
select count(*) from mf_fundmanagernew where Performance < 0	ccks_fund
select a.ChiNameAbbr, b.LegalRepr from lc_sharesfloatingschedule as a join lc_stockarchives as b on a.CompanyCode = b.CompanyCode where a.Proportion2 > 20	ccks_stock
select ChineseName, QDIIN, QDIINV from mf_fmscaleanalysisn where ChineseName = '徐猛' or ChineseName = '范冰';	ccks_fund
select max(IndexValue) from ed_producerpiformp  where IndexName ='Textile' and ReportPeriod ='Same period last year' and strftime('%Y', EndDate) = strftime('%Y', DATE('now', '-1 year'));	ccks_macro
select ActualShares from lc_largeshsubscription where SHName='杉杉集团';	ccks_stock
select FullName,LegalPersonRepr from lc_issueandlistagent where ChiNameAbbr='东阿阿胶';	ccks_stock
select b.SecuAbbr, a.RRInSingleYear, a.RRInTwoYear from mf_netvalueperformancehis as a join mf_fundarchives as b on a.InnerCode = b.InnerCode where b.FundType = 'Bond Fund';	ccks_fund
select FinanceDeposits from ed_chinafibalancesheetrmb;	ccks_macro
select SecuAbbr from mf_fundreturnrank where IndexCycle = '6 months' order by FundReturn desc limit 1	ccks_fund
select a.FundAnnReturnMean from mf_fundreturnrank as a join mf_fundarchives as b on a.InnerCode = b.InnerCode where b.Type = 'LOF'	ccks_fund
select a.ChiNameAbbr from lc_sharestru as a join lc_exgindustry as b on a.CompanyCode = b.CompanyCode where b.FirstIndustryName = 'Manufacturing' order by a.AFloats desc limit 20	ccks_stock
select BondAbbr from mf_bondportifoliodetail where SecuCode='166001';	ccks_fund
select count(*) from lc_buyback  where strftime('%Y', AdvanceDate)='2021' ;	ccks_stock
select InvestAdvisorAbbrName from mf_investadvisoroutline where LegalRepr like '周%';	ccks_fund
select Education, Gender, count(*) from mf_personalinfo group by Education, Gender;	ccks_fund
select SHName, max(ActualShares) from lc_largeshsubscription where strftime('%Y', InitialInfoPublDate)>'2018' group by SHName;	ccks_stock
select FCDeposits , NetAbroadAssets from ed_chinamoneyandbanking  where strftime('%Y', EndDate) = strftime('%Y', DATE('now', '-2 year')) ;	ccks_macro
select AnnualizedRRInTwoYear , AnnualizedRRInTenYear from mf_netvalueperformancehis ;	ccks_fund
select Authorizer from lc_sharetrustee  where strftime('%Y', InfoPublDate)='2014' order by  InvolvedTrustSum desc limit 1;	ccks_stock
select ChargeRateTyDes , ChargeRateDes from mf_chargeratenew where SecuCode ='501065';	ccks_fund
select max(TotalAssets), min(TotalAssets) , max(TotalLiabilities), min(TotalLiabilities)  from ed_otherdepositorycorpbs;	ccks_macro
select b.FirstIndustryName, count(*) from lc_sharesfloatingschedule as a join lc_exgindustry as b on a.CompanyCode = b.CompanyCode where a.Proportion2 > 60 group by b.FirstIndustryName	ccks_stock
select  AquirerName from lc_legaldistribution  where AquiredSum > 10000 and strftime('%Y', InfoPublDate) = strftime('%Y', DATE('now', '-1 year'));	ccks_stock
select  Maturity,  RatioFloor, RatioCeiling from ed_taxrate where TypeName ='Outright Repurchase of Government Bonds' and ItemName ='Handling Fee' ;	ccks_macro
select EndDate, HIValueAP from ed_industryproduction where ReportArea ='National' and StatStandard ='State-Owned and Above-Designated-Size Industrial Enterprises' and ReportPeriod ='月度';	ccks_macro
select InsuranceCorpsHoldPropA from lc_stockholdingst where ChiNameAbbr='恒生电子';	ccks_stock
select TurnoverDeals from qt_dailyquote where SecuCode = '601908';	ccks_stock
select a.Name from mf_fundmanagernew as a join mf_fundarchives as b on a.InnerCode = b.InnerCode where b.FundType = 'Equity Fund'	ccks_fund
select RRSinceThisYear from mf_netvalueperformancehis ;	ccks_fund
select count(*) from lc_legaldistribution  where AquiredSum > 10000 and strftime('%Y', InfoPublDate) = strftime('%Y', DATE('now', '-1 year'));	ccks_stock
select b.City, count(*) from lc_coconcept as a join lc_stockarchives as b on a.CompanyCode = b.CompanyCode where a.ConceptName ='OLED' group by b.City ;	ccks_stock
select SecuCode, ChiNameAbbr from lc_buyback  where BuybackSum > 100000 and strftime('%Y', AdvanceDate) > strftime('%Y', DATE('now', '-2 year'));	ccks_stock
select NVDailyGrowthRate, RRInSelectedWeek, RRInSingleWeek from mf_netvalueperformancehis where SecuAbbr = '华宝宝盛';	ccks_fund
select EndDate, RetailValueOfSCGoods from ed_retailvalueofscgoods where Province ='上海' and ReportPeriod ='Year' and strftime('%Y', EndDate)<'2010';	ccks_macro
select b.SecuAbbr,b.FundType from mf_bondportifoliodetail as a join mf_fundarchives as b on a.InnerCode=b.InnerCode where a.BondAbbr='海亮转债';	ccks_fund
select EndDate, IndustrialValueAdded from ed_industryproduction where ReportArea ='National' and StatStandard ='State-Owned and Above-Designated-Size Industrial Enterprises' and ReportPeriod ='End-of-period cumulative';	ccks_macro
select count(*) from lc_ashareseasonednewissue  where strftime('%Y', AdvanceDate) > strftime('%Y', DATE('now', '-5 year'));	ccks_stock
select ChiName from mf_fundarchives where SecuAbbr='博时主题';	ccks_fund
select WholesaleRetailTrade , FoodBeverage from ed_retailvalueofscgoods ;	ccks_macro
select MoneyReserves , SelfOwnedMoney from ed_moneyauthoritybs  where strftime('%Y', EndDate) = strftime('%Y', DATE('now', '-2 year')) ;	ccks_macro
select ChiName, HoldingSum from lc_relatedsh  where ChiNameAbbr = '航天发展' and strftime('%Y', EndDate)='2020' and strftime('%m', EndDate )='3'	ccks_stock
select Authorizer from lc_sharetrustee  where strftime('%Y', InfoPublDate)='2018' and ChiNameAbbr='新北洋';	ccks_stock
select a.State, count(*) from lc_stockarchives as a join lc_sharestru as b on a.CompanyCode = b.CompanyCode where b.NonListedShares > 200000000 group by a.State	ccks_stock
select a.IndustryName , count(*) from lc_business as a join lc_stockarchives as b on a.CompanyCode = b.CompanyCode  where strftime('%Y', b.EstablishmentDate)='2010' group by  a.IndustryName having count(*)>10;	ccks_stock
select avg(b.TotalFundNV) from mf_personalinfo as a join mf_fmscaleanalysisn as b on a.PersonalCode = b.PersonalCode where a.ExperienceTime < 5;	ccks_fund
select FloChargeRate , DivIntervalDes  from mf_chargeratenew where SecuAbbr ='富国创新药ETF';	ccks_fund
select RatioCeiling from ed_taxrate where TypeName ='A Share' and ItemName = 'Securities Transaction Stamp Tax' and SecuMarket ='Shenzhen Stock Exchange' ;	ccks_macro
select Nationality, count(*) from mf_personalinfo group by Nationality	ccks_fund
select count(*) from lc_legaldistribution  where strftime('%Y', InfoPublDate)='2021';	ccks_stock
select b.Nationality from mf_fmperfanalysis as a join mf_personalinfo as b on a.PersonalCode = b.PersonalCode where a.AnnSharpeR > 2 group by b.Nationality having count(*) > 20	ccks_fund
select count(*) from lc_freefloat  where TotalAShare > 10000000000 and strftime('%Y', ChangeDate)='2021'	ccks_stock
select FundManager , Fund from mf_awards where AppraisalOrgCode = '40981';	ccks_fund
select  SecuCode from lc_relatedsh  where SHName ='顾瑜' and SHInvestSum > 1000000 and strftime('%Y', EndDate) = strftime('%Y', DATE('now', '-1 year'));	ccks_stock
select a.State , count(*) from lc_stockarchives as a join lc_business as b on a.CompanyCode = b.CompanyCode where b.IndustryName ='Agriculture' group by a.State ;	ccks_stock
select count(*) from mf_bondportifoliodetail where SecuAbbr='博时主题';	ccks_fund
select a.SecuCode, a.ChiNameAbbr from lc_coconcept as a join lc_stockarchives as b on a.CompanyCode = b.CompanyCode where a.ConceptName ='Integrated Circuit' and b.City ='西安市';	ccks_stock
select SocialSecuFundHoldPropA from lc_stockholdingst  where strftime('%Y', EndDate)='2019' and strftime('%m', EndDate)='2' and ChiNameAbbr='中航重机';	ccks_stock
select ChineseName from mf_personalinfo where strftime('%Y', BirthDate)>'1990';	ccks_fund
select NumberOfFunds from mf_fmretscaleanalysis where ChineseName = '付浩';	ccks_fund
select max(IndexValue), min(IndexValue) from ed_producerpiformp  where IndexName ='Food Manufacturing' and ReportPeriod ='Same period last year' and strftime('%Y', EndDate)='2008' ;	ccks_macro
select BuybackSum, Percentage, BuybackMoney from lc_buyback where ChiNameAbbr = '浙江龙盛' ;	ccks_stock
select RRInFiveYear from mf_netvalueperformancehis ;	ccks_fund
select ClaimsToGov, ClaimsToNonfinancialInst, ClaimsToSpecificSavingOrg from ed_chinamoneyandbanking ;	ccks_macro
select IndexName, IndexValue from ed_producerpiformp where ReportPeriod ='Same month last year' and IndexType ='Industrial Structure Classification Index';	ccks_macro
select FirstIndustryName from lc_exgindustry where ChiNameAbbr = '普路通'	ccks_stock
select SecuAbbr from mf_bondportifoliodetail where BondCode='200203';	ccks_fund
select Province, PrimaryIndustryGDP, SecondIndustryGDP, ThirdIndustryGDP from ed_grossdomesticproduct  where strftime('%Y', EndDate) = strftime('%Y', DATE('now', '-2 year') ) ;	ccks_macro
select NVDailyGrowthRate from mf_netvalue where SecuAbbr = '华安石油A';	ccks_fund
select  SecuCode from lc_sharefp  where strftime('%Y', EndDate) > strftime('%Y', DATE('now', '-2 year'));	ccks_stock
select EndDate, ClaimsOnGovernment, ClaimsOnCentralBank from ed_otherdepositorycorpbs where TotalAssets > 30000000;	ccks_macro
select BondAbbr,MarketValue,RatioInNV from mf_bondportifoliodetail where SecuCode='161010';	ccks_fund
select AquirerName from lc_legaldistribution where SecuCode = '002981';	ccks_stock
select ChineseName from mf_fmscaleanalysisn where BondFundN>3;	ccks_fund
select  ChiNameAbbr from lc_legaldistribution  where strftime('%Y', InfoPublDate) = strftime('%Y', DATE('now', '-1 year')) ;	ccks_stock
select SecondIndustryName from lc_exgindustry where FirstIndustryName = 'Information Transmission, Software, and Information Technology Services' group by SecondIndustryName order by count(*) desc limit 2	ccks_stock
select State, City from lc_stockarchives where ChiNameAbbr='华昌达';	ccks_stock
select  AquirerName from lc_legaldistribution  where strftime('%Y', InfoPublDate)='2020'	ccks_stock
select EndDate, NVWeeklyGrowthRate from  mf_netvalue  where strftime('%Y', EndDate) > strftime('%Y', DATE('now', '-2 year')) and SecuCode ='160416' ;	ccks_fund
select b.FundType from mf_netvalueperformancehis as a join mf_fundarchives as b on a.InnerCode = b.InnerCode group by b.FundType order by avg(a.RRInSingleMonth) desc limit 1;	ccks_fund
select AnnualizedRRInTwoYear from mf_netvalueperformancehis ;	ccks_fund
select a.BondAbbr,a.MarketValue, b.Manager from mf_bondportifoliodetail as a join mf_fundarchives as b on a.InnerCode=b.InnerCode where a.SecuCode='510130';	ccks_fund
select AbbrChiName from mf_fcretscalerank where FundTypeName='Bond Fund' order by TotalAUMTypeAvg desc limit 10;	ccks_fund
select a.SecuAbbr, a.BriefIntro from mf_fundarchives as a join mf_fundrisklevel as b on a.InnerCode = b.InnerCode where b.RiskLevel = 'Medium-High'	ccks_fund
select b.SecuAbbr,b.Manager,a.BenchGRFor6Month from mf_benchmarkgrowthrate as a join mf_fundarchives as b on a.InnerCode=b.InnerCode where a.BenchGRFor6Month>0;	ccks_fund
select b.State from lc_mainoperincome as a join lc_stockarchives as b on a.CompanyCode = b.CompanyCode where a.MainOperIncome > 100000000000;	ccks_stock
select CSRCIndustryName,count(*) from lc_ipodeclaration  where strftime('%Y', EndDate)='2012' group by  CSRCIndustryName;	ccks_stock
select a.Name, b.Education from mf_fundmanagernew as a join mf_personalinfo as b on a.PersonalCode = b.PersonalCode where a.Performance < 0.1	ccks_fund
select EndDate, Province, IndustrialValueAdded from ed_industryproduction where ReportArea = 'Provincial and Municipal' and StatStandard ='State-Owned and Above-Designated-Size Industrial Enterprises' and ReportPeriod ='Year' ;	ccks_macro
select SponsorName, LawFirm from lc_ipodeclaration where ChiNameAbbr='红塔证券' order by EndDate desc limit 1;	ccks_stock
select FPSHName from lc_sharefp where ChiNameAbbr = '瑞茂通' and InvolvedSum > 1000000 ;	ccks_stock
select StockAbbr from mf_keystockportfolio where StockAbbr is not null group by  StockAbbr order by count(*) desc limit 1	ccks_fund
select RRSinceStart from mf_netvalueperformancehis ;	ccks_fund
select SecuAbbr,RiskReturncharacter from mf_fundarchives where InvestStyle='Sector Equity – Pharmaceuticals';	ccks_fund
select EnterpriseIncome, EnterpriseIncomeTax from ed_financialbalance  where GEnterpriseIncome > 5 and Province ='北京' and strftime('%Y', EndDate) > strftime('%Y', DATE('now', '-5 year')) ;	ccks_macro
select AnnualizedRRInTenYear , AnnualizedRRSinceStart  from mf_netvalueperformancehis ;	ccks_fund
select a.Education, avg(b.TotalFundNV) from mf_personalinfo as a join mf_fmscaleanalysisn as b on a.PersonalCode = b.PersonalCode group by a.Education;	ccks_fund
select b.Education, count(*) from mf_fmperfanalysis as a join mf_personalinfo as b on a.PersonalCode = b.PersonalCode where a.AnnAlphaCoef > 0.5 group by b.Education	ccks_fund
select Province from ed_grossdomesticproduct  where strftime('%Y', EndDate) = strftime('%Y', DATE('now', '-1 year')) and GDPGrowthYOY > 0.5;	ccks_macro
select MainOperIncome from lc_mainoperincome  where ChiNameAbbr='中国石化' and strftime('%Y', EndDate) = strftime('%Y', DATE('now', '-1 year')) and round(strftime('%m',EndDate)/3.0 + 0.495) = 1 ;	ccks_stock
select EndDate, LIValueAP from ed_industryproduction where ReportArea ='National' and StatStandard ='All Industrial Enterprises' and ReportPeriod ='End-of-period cumulative';	ccks_macro
select UnitNV , NVWeeklyGrowthRate from  mf_netvalue ;	ccks_fund
select ChineseName from mf_fmscaleanalysisn order by QDIINV desc limit 1;	ccks_fund
select count(*) from lc_buyback  where strftime('%Y', AdvanceDate)='2021' ;	ccks_stock
select ChiNameAbbr from qt_monthdata  where strftime('%Y', EndDate)='2020' group by  ChiNameAbbr order by max(TotalShare) desc limit 10;	ccks_stock
select ChineseName, EquityFundN, EquityFundNV from mf_fmscaleanalysisn where EquityFundN > 5;	ccks_fund
select NVDailyGrowthRate from  mf_netvalueperformancehis ;	ccks_fund
select ChiNameAbbr from lc_actualcontroller where NationalityDesc != 'China';	ccks_stock
select ProportionGRHalfAYear from lc_shnumber where ChiNameAbbr='兴业证券';	ccks_stock
select MainOperCost, MainOperProfit from lc_mainoperincome  where ChiNameAbbr ='古井贡酒' and strftime('%Y', EndDate)='2018';	ccks_stock
select count(TradingDay) from qt_dailyquote where ChiNameAbbr = '科思股份' and TurnoverValue > 100000000;	ccks_stock
select a.SecuAbbr, a.RRSinceStart from mf_netvalueperformancehis as a join mf_fundarchives as b on a.InnerCode = b.InnerCode and b.FundType ='Bond Fund' ;	ccks_fund
select DiviBase, CashDiviRMB from lc_dividend  where ChiNameAbbr ='深科技' and strftime('%Y', DividendImplementDate) > strftime('%Y', DATE('now', '-3 year'));	ccks_stock
select SecuAbbr from mf_keystockportfolio where StockAbbr = '海康威视'	ccks_fund
select EndDate,  SubjectSum from ed_newincreasingloan  where ReportPeriod ='End-of-period cumulative' and SubjectSum > 150000 and strftime('%Y', EndDate)>='2000';	ccks_macro
select  SecuCode from lc_dividend  where BonusShareRatio > 0.5 and strftime('%Y', DividendImplementDate) = strftime('%Y', DATE('now', '-1 year'));	ccks_stock
select ChiNameAbbr from lc_financialexpense order by Commission desc limit 1	ccks_stock
select EndDate, TotalAssets  from ed_otherdepositorycorpbs order by TotalAssets desc limit 1;	ccks_macro
select b.SecuAbbr,a.BenchGRForThisWeek from mf_benchmarkgrowthrate as a join mf_fundarchives as b on a.InnerCode=b.InnerCode   where b.Type='LOF';	ccks_fund
select  RatioCeiling from ed_taxrate where TypeName ='Chinese Large-Sized Banks' and ItemName = 'Excess Reserve Requirement Ratio'  ;	ccks_macro
select CorporateSavings from ed_chinafibalancesheetrmb;	ccks_macro
select b.SecuAbbr from mf_benchmarkgrowthrate as a join mf_fundarchives as b on a.InnerCode=b.InnerCode  where b.Type='LOF' and a.BenchGRForThisMonth>0;	ccks_fund
select ImValueOfGoods , ExValueOfGoods from ed_exportimport  where ImValueOfGoods < 20 and ExValueOfGoods > 40 and strftime('%Y', EndDate) > strftime('%Y', DATE('now', '-3 year'));	ccks_macro
select b.ChiNameAbbr from lc_largeshsubscription as a join lc_stockarchives as b on a.CompanyCode=b.CompanyCode  where b.State='福建省' and a.OughtShares>1000000;	ccks_stock
select DomesticLoans, FCDeposits from ed_chinamoneyandbanking where strftime('%Y', EndDate)>='2005';	ccks_macro
select SHName from lc_largeshsubscription where ChiNameAbbr='浙大网新' order by ActualShares desc limit 1;	ccks_stock
select a.AvgAUMTypeRank from mf_fmretandscalerank as a join mf_personalinfo as b on a.PersonalCode = b.PersonalCode where b.Education = 'Bachelor''s degree'	ccks_fund
select ChargeRateTyDes, ChargeRateDes from mf_chargeratenew where SecuAbbr ='南方天元' ;	ccks_fund
select RightRegDate , CashDiviRMB from lc_dividend where CashDiviRMB > 5 and ChiNameAbbr = '古井贡酒';	ccks_stock
select a.Name from mf_fundmanagernew as a join mf_personalinfo as b on a.PersonalCode = b.PersonalCode where a.ManagementTime > 200 and b.Education = 'Doctoral degree'	ccks_fund
select a.ChiNameAbbr, b.LeaderName, b.PositionDescription from lc_sharetransfer as a join lc_executivesholdings as b on a.CompanyCode = b.CompanyCode order by a.PCTBeforeTran desc limit 5	ccks_stock
select a.ChineseName, b.PracticeDate from mf_fmperfanalysis as a join mf_personalinfo as b on a.PersonalCode = b.PersonalCode where a.IndexCycle = '3 years' order by a.CalmarR desc limit 10	ccks_fund
select FirstIndustryName, SecondIndustryName from lc_exgindustry where ChiNameAbbr = '西藏发展'	ccks_stock
select b.Type, count(*) from mf_fundreturnrank as a join mf_fundarchives as b on a.InnerCode = b.InnerCode where a.IndexCycle = '6 months' and a.FundReturnMean < 0 group by b.Type	ccks_fund
select ChiNameAbbr, avg(TurnoverValue) from qt_dailyquote  where strftime('%Y', TradingDay)='2021' and round(strftime('%m',TradingDay)/3.0 + 0.495) = 4 group by  ChiNameAbbr;	ccks_stock
select BenchGRForThisMonth from mf_benchmarkgrowthrate where SecuAbbr='交银治理ETF';	ccks_fund
select UnitNV, AccumulatedUnitNV, DiscountRatio from mf_netvalue where SecuAbbr = '华安180ETF' ;	ccks_fund
select moneyAndQuasimoney, money1, Quasimoney from ed_chinamoneyandbanking  where strftime('%Y', EndDate) > strftime('%Y', DATE('now', '-2 year')) ;	ccks_macro
select b.ChineseName,b.BirthDate from mf_fmscaleanalysisn as a join mf_personalinfo as b on a.PersonalCode=b.PersonalCode order by a.BondFundNV desc limit 10;	ccks_fund
select SecuAbbr from mf_mainfinancialindexq  where strftime('%Y', EndDate)='2021' and round(strftime('%m',EndDate)/3.0 + 0.495) = 1 and NetAssetsValue > 10000000000	ccks_fund
select a.SecondIndustryName, count(*) from lc_exgindustry as a join lc_freefloat as b on a.CompanyCode = b.CompanyCode  where b.AFloats > 10000000000 and strftime('%Y', ChangeDate)='2019' group by  a.SecondIndustryName	ccks_stock
select b.Nationality, count(*) from mf_fmretscaleanalysis as a join mf_personalinfo as b on a.PersonalCode = b.PersonalCode where a.AvgAUM > 500 group by b.Nationality	ccks_fund
select moneyAndQuasimoney, money1, Quasimoney from ed_chinamoneyandbanking  where strftime('%Y', EndDate)<'1995';	ccks_macro
select ChiNameAbbr, TradingDay from qt_dailyquote where TurnoverValue > 1000000000;	ccks_stock
select ChiNameAbbr from lc_stockarchives where LegalRepr='张利忠';	ccks_stock
select OtherForeignAssets, OtherLiability from ed_moneyauthoritybs ;	ccks_macro
select UnitNV, NVDailyGrowthRate from  mf_netvalue  where round(strftime('%m',EndDate)/3.0 + 0.495) = round(strftime('%m',date()) / 3.0 + 0.495) and SecuAbbr ='华安石油A' ;	ccks_fund
select City,count(*) from lc_stockarchives where State='陕西省' group by City order by count(*) desc limit 1;	ccks_stock
select SecuAbbr,HoldVolume from mf_bondportifoliodetail where BondAbbr='温氏转债';	ccks_fund
select LeaderName, PositionDescription from lc_executivesholdings where ChiNameAbbr = '依米康'	ccks_stock
select ChiName from lc_relatedsh  where ChiNameAbbr = '航天发展' and strftime('%Y', EndDate)='2020' and strftime('%m', EndDate )='8'	ccks_stock
select PRconfirmationdate from mf_fundarchives where SecuAbbr = '招商成长'	ccks_fund
select a.ReturnTypeRank from mf_fmretandscalerank as a join mf_personalinfo as b on a.PersonalCode = b.PersonalCode where b.ExperienceTime > 10	ccks_fund
select EndDate, NetAbroadAssets from ed_chinamoneyandbanking where NetAbroadAssets > 1000000;	ccks_macro
select ChineseName,TotalFundNVRank from mf_fmscaleanalysisn;	ccks_fund
select SponsorName from lc_ipodeclaration where AccountingFirm='立信会计事务所';	ccks_stock
select avg(RRInSingleYear) from mf_netvalueperformancehis;	ccks_fund
select Forex, MoneyAndGold, OtherForeignAssets from ed_moneyauthoritybs where TotalAssets > 10;	ccks_macro
select LeaderName, PositionDescription from lc_executivesholdings where ChiNameAbbr = '福星股份' and LeaderName like '%谭%'	ccks_stock
select LoanToGov, FinanceDeposits from ed_chinafibalancesheetrmb  where strftime('%Y', EndDate) > strftime('%Y', DATE('now', '-2 year')) ;	ccks_macro
select b.SecuAbbr, b.RiskLevel from mf_fundmanagernew as a join mf_fundrisklevel as b on a.InnerCode = b.InnerCode where strftime('%Y', a.DimissionDate)<'2020'	ccks_fund
select a.SecuCode, b.State, b.City from lc_business as a join lc_stockarchives as b on a.CompanyCode = b.CompanyCode where a.IndustryName ='Professional and Technical Services';	ccks_stock
select SHNum,AverageHoldSum from lc_shnumber  where ChiNameAbbr='新天然气' and strftime('%Y', EndDate)='2016';	ccks_stock
select EndDate,  SubjectSum, YOY from ed_newincreasingloan  where ReportPeriod ='Month' and SubjectSum > 100000 and strftime('%Y', EndDate) = strftime('%Y', DATE('now', '-2 year'));	ccks_macro
select b.ChiNameAbbr from lc_stockarchives as a join lc_sharestru as b on a.CompanyCode = b.CompanyCode where a.State = '上海市' and b.AFloats > 10000000	ccks_stock
select ChiNameAbbr, AquirerAmount from lc_legaldistribution  where AquirerName ='广发估值优势混合型证券投资基金' and strftime('%Y', InfoPublDate) = strftime('%Y', DATE('now', '-1 year')) ;	ccks_stock
select NationalityDesc from lc_actualcontroller group by NationalityDesc order by count(*) desc limit 3;	ccks_stock
select AbbrChiName from mf_fcretscalerank where FundTypeName='Bond Fund' order by TotalAUMRank limit 10;	ccks_fund
select a.ChineseName, b.PracticeDate from mf_fmretandscalerank as a join mf_personalinfo as b on a.PersonalCode = b.PersonalCode where a.TimeInterval = 'Past 1 Day' order by a.AvgAUMTypeAvg desc limit 1	ccks_fund
select ChineseName, BondFundN, BondFundNV from mf_fmscaleanalysisn order by BondFundNV desc limit 1;	ccks_fund
select NVWeeklyGrowthRate from  mf_netvalue where SecuCode = '510220';	ccks_fund
select EndDate, UnitNV from mf_netvalue where SecuAbbr = '泰达效率';	ccks_fund
select b.FundType, count(*) from mf_netvalueperformancehis as a join mf_fundarchives as b on a.InnerCode = b.InnerCode where a.AnnualizedRRSinceStart > 10 group by b.FundType;	ccks_fund
select LeaderName, ChiNameAbbr from lc_executivesholdings where PositionDescription like '%Chairman of the Board%' and PositionDescription like '%President%'	ccks_stock
select ChiNameAbbr, SecuCode from lc_legaldistribution  where strftime('%Y', InfoPublDate) = strftime('%Y', DATE('now', '-1 year')) ;	ccks_stock
select ChiNameAbbr from lc_sharesfloatingschedule where NewMarketableAShares <= 1000	ccks_stock
select count(distinct FundCompanyCode) from mf_awards ;	ccks_fund
select EndDate, IndustrialValueAdded from ed_industryproduction where ReportArea ='National' and StatStandard ='All Industrial Enterprises' and ReportPeriod ='月度';	ccks_macro
select EndDate, IndustrialOutputValueAP from ed_industryproduction where ReportArea ='National' and StatStandard ='All Industrial Enterprises' and ReportPeriod ='月度';	ccks_macro
select count(*) from lc_business as a join lc_stockarchives as b on a.CompanyCode = b.CompanyCode where b.State = '江苏省' and a.IndustryName ='Agricultural and By-Product Processing';	ccks_stock
select EndDate, Forex, MoneyAndGold, OtherForeignAssets from ed_moneyauthoritybs where TotalAssets < 10;	ccks_macro
select WholesaleRetailTrade, FoodBeverage from ed_retailvalueofscgoods  where Province='上海' and ReportPeriod ='Year' and strftime('%Y', EndDate)='2004';	ccks_macro
select a.FirstIndustryName, count(*) from lc_exgindustry as a join lc_sharestru as b on a.CompanyCode = b.CompanyCode where b.NonRestrictedShares  > 10000000000 group by a.FirstIndustryName	ccks_stock
select a.City , count(*)  from lc_stockarchives as a join lc_coconcept as b on a.CompanyCode = b.CompanyCode where b.ConceptName ='Big Data' group by a.City ;	ccks_stock
select State from lc_stockarchives  where strftime('%Y', EstablishmentDate)='2000' group by  State order by count(*) desc limit 1;	ccks_stock
select a.IndustryName, count(*) from lc_business as a join lc_stockarchives as b on a.CompanyCode = b.CompanyCode where b.State = '江苏省' group by a.IndustryName ;	ccks_stock
select SecuAbbr from mf_bondportifoliodetail where BondCode='200203' order by HoldVolume limit 1;	ccks_fund
select ChiNameAbbr from lc_stockarchives where State='山东省';	ccks_stock
select ChiName from lc_shnumber  where strftime('%Y', EndDate)='2016' order by  SHNum desc limit 1;	ccks_stock
select RRInSelectedMonth, RRInSingleMonth from mf_netvalueperformancehis where SecuAbbr = '天弘恒享';	ccks_fund
select ReportPeriod,  IndexValue from ed_producerpiformp where  IndexType ='National Economic Industry Index' and IndexName ='Metal Products';	ccks_macro
select IndustrialValueAdded from ed_industryproduction  where Province ='上海' and StatStandard ='All Industrial Enterprises' and ReportPeriod ='Year' and strftime('%Y', EndDate)='2000';	ccks_macro
select count(*) from lc_buyback  where BuybackMoney >= 100000000 and strftime('%Y', AdvanceDate) = strftime('%Y', DATE('now', '-1 year'));	ccks_stock
select count(*) from lc_sharetransfer where PCTBeforeTran > 0.2	ccks_stock
select b.ChiNameAbbr, b.ControllerName from lc_stockarchives as a join lc_actualcontroller as b on a.CompanyCode = b.CompanyCode where a.City = '杭州市';	ccks_stock
select RRInSixMonth from  mf_netvalueperformancehis ;	ccks_fund
select PaidinCapital from ed_otherdepositorycorpbs ;	ccks_macro
select ChiNameAbbr from lc_sharesfloatingschedule where Proportion2 > 50	ccks_stock
select BondAbbr from mf_bondportifoliodetail where SecuAbbr='中银中国A';	ccks_fund
select a.ChiNameAbbr from lc_sharesfloatingschedule as a join lc_exgindustry as b on a.CompanyCode = b.CompanyCode where b.FirstIndustryName = 'Manufacturing' order by a.Proportion1 desc limit 1	ccks_stock
select count(*) from mf_awards ;	ccks_fund
select ChiNameAbbr, IssuePurpose from lc_ashareseasonednewissue  where strftime('%Y', AdvanceDate)='2021';	ccks_stock
select GDP from ed_grossdomesticproduct ;	ccks_macro
select count(*) from mf_fmscaleanalysisn where TotalFundNV > 500;	ccks_fund
select count(*) from lc_legaldistribution  where strftime('%Y', InfoPublDate) = strftime('%Y', DATE('now', '-1 year'));	ccks_stock
select Fund from mf_awards where AwardName = 'China Equity Hedge Fund Award Nomination' and AppraisalOrg ='Morningstar Information';	ccks_fund
select CSRCIndustryName from lc_ipodeclaration where ChiNameAbbr='红塔证券';	ccks_stock
select b.Type, count(*) from mf_fundreturnrank as a join mf_fundarchives as b on a.InnerCode = b.InnerCode where a.IndexCycle = '1 year' and a.FundReturn < 0 group by b.Type	ccks_fund
select EndDate, RetailValueOfSCGoods from ed_retailvalueofscgoods  where ReportArea ='National' and ReportPeriod ='Year' and strftime('%Y', EndDate) > strftime('%Y', DATE('now', '-3 year')) ;	ccks_macro
select a.ConceptName, count(*) from lc_coconcept as a join lc_stockarchives as b on a.CompanyCode = b.CompanyCode where b.State ='广东省' group by a.ConceptName having count(*)>4  ;	ccks_stock
select BondAbbr from mf_bondportifoliodetail where SecuCode='160611';	ccks_fund
select InvestStyle,count(*) from mf_fundarchives group by InvestStyle;	ccks_fund
select SHName, HoldingPCT from lc_relatedsh  where ChiNameAbbr = '农发种业' and strftime('%Y', EndDate)='2019' ;	ccks_stock
select  SecuCode from lc_relatedsh  where SHName ='万安集团有限公司' and strftime('%Y', EndDate) = strftime('%Y', DATE('now', '-1 year'));	ccks_stock
select b.SecuAbbr,b.InvestAdvisorName from mf_bondportifoliodetail as a join mf_fundarchives as b on a.InnerCode=b.InnerCode where a.BondAbbr='21国债06' order by a.RatioInNV desc limit 1;	ccks_fund
select InvestAdvisorAbbrName from mf_investadvisoroutline order by RegCapital desc limit 3;	ccks_fund
select a.State , count(*)  from lc_stockarchives as a join lc_coconcept as b on a.CompanyCode = b.CompanyCode where b.ConceptName ='Chip Concept' group by a.State having count(*)>5;	ccks_stock
select count(*) from lc_business where IndustryName like '%Computer%' or IndustryName like '%Communication%'	ccks_stock
select b.InvestmentType,count(*) from mf_benchmarkgrowthrate as a join mf_fundarchives as b on a.InnerCode=b.InnerCode where a.BenchGRForThisYear<0 group by b.InvestmentType;	ccks_fund
select count(*) from mf_fmretscaleanalysis as a join mf_personalinfo as b on a.PersonalCode = b.PersonalCode where a.TotalAUM > 100 and b.Education = 'Bachelor''s degree'	ccks_fund
select avg(b.TotalFundNV) from mf_personalinfo as a join mf_fmscaleanalysisn as b on a.PersonalCode = b.PersonalCode where a.ExperienceTime > 15;	ccks_fund
select EndDate, Province, IndustrialOutputValueAP from ed_industryproduction where ReportArea ='Provincial and Municipal' and StatStandard ='All Industrial Enterprises' and ReportPeriod ='End-of-period cumulative'  ;	ccks_macro
select MaxChargeRate, MinChargeRate from mf_chargeratenew where SecuAbbr ='南方天元';	ccks_fund
select b.Type, count(*) from mf_fundreturnrank as a join mf_fundarchives as b on a.InnerCode = b.InnerCode where a.IndexCycle = '1 month' and a.FundReturn > 0 group by b.Type	ccks_fund
select a.DistributionSum from lc_legaldistribution as a  where strftime('%Y', a.InfoPublDate)='2020' and strftime('%m', a.InfoPublDate)='3' and a.ChiNameAbbr ='国网英大'	ccks_stock
select ThirdIndustryGDP from ed_grossdomesticproduct ;	ccks_macro
select ExpensedRDInput,CapitalizedRDInput from lc_intassetsdetail  where strftime('%Y', EndDate)=strftime('%Y', DATE('now', '-1 year')) and ChiNameAbbr='深科技';	ccks_stock
select count(*) from lc_executivesholdings where  ChiNameAbbr = '拓维信息' and (PositionDescription like '%Director%' or PositionDescription like '%Chairman%') and PositionDescription not like '%Supervisory%'	ccks_stock
select a.Name, a.SecuAbbr from mf_fundmanagernew as a join mf_personalinfo as b on a.PersonalCode = b.PersonalCode where b.Education = 'Bachelor''s degree'	ccks_fund
select count(*) from lc_sharesfloatingschedule where AccuMarketableAShares > 1000	ccks_stock
select a.IssueObject, b.GeneralManager, b.LegalRepr from lc_ashareseasonednewissue as a join lc_stockarchives as b on a.CompanyCode = b.CompanyCode where a.ChiNameAbbr = '晶盛机电';	ccks_stock
select b.ChineseName,b.BirthDate from mf_fmscaleanalysisn as a join mf_personalinfo as b on a.PersonalCode=b.PersonalCode where a.BondFundN>3;	ccks_fund
select count(*) from lc_mainoperincome  where MainOperIncome > 100000000 and strftime('%Y', EndDate)>='2019';	ccks_stock
select RiskLevel from mf_fundrisklevel where SecuAbbr = '国金50'	ccks_fund
select ChiNameAbbr from lc_actualcontroller where ControllerName = '中国烟草总公司';	ccks_stock
select LeaderName from lc_executivesholdings where ChiNameAbbr = '恒宝股份' and PositionDescription like '%Vice President%'	ccks_stock
select a.IndustryName , count(*) from lc_business as a join lc_stockarchives as b on a.CompanyCode = b.CompanyCode  where strftime('%Y', b.EstablishmentDate)='2020' group by  a.IndustryName ;	ccks_stock
select ChiNameAbbr from lc_freefloat order by AFloats desc limit 5	ccks_stock
select SecuAbbr, SecuCode  from mf_mainfinancialindexq  where strftime('%Y', EndDate)='2021' group by  SecuAbbr order by sum(TotalProfit) desc limit 10	ccks_fund
select CSRCIndustryName from lc_ipodeclaration group by CSRCIndustryName order by count(*) asc, min(id) asc limit 10;	ccks_stock
select a.State from lc_stockarchives as a join lc_sharestru as b on a.CompanyCode = b.CompanyCode where b.NonListedShares > 200000000 group by a.State having count(*) > 10	ccks_stock
select b.City, count(*) from lc_sharesfloatingschedule as a join lc_stockarchives as b on a.CompanyCode = b.CompanyCode where a.NewMarketableAShares > 100 group by b.City	ccks_stock
select SecuAbbr from mf_benchmarkgrowthrate where BenchGRForThisWeek<0 order by BenchGRForThisWeek limit 10;	ccks_fund
select a.Name from mf_fundmanagernew as a join mf_fundrisklevel as b on a.InnerCode = b.InnerCode where b.RiskLevel = 'Medium-Low' group by a.Name having count(a.SecuAbbr) > 5	ccks_fund
select RRInSingleWeek from  mf_netvalueperformancehis ;	ccks_fund
select GYoYOfImValueGoods, GYoYOfExValueGoods from ed_exportimport ;	ccks_macro
select SecuritiesCorpsHoldPropA from lc_stockholdingst  where strftime('%Y', EndDate)='2020' and strftime('%m', EndDate)='2' and ChiNameAbbr='重庆建工';	ccks_stock
select EndDate, UnitNV from  mf_netvalue  where strftime('%Y', EndDate) > strftime('%Y', DATE('now', '-2 year')) and SecuAbbr ='华安石油A' ;	ccks_fund
select ChiNameAbbr from lc_freefloat where TotalAShare > 1000000000 order by AdjFreeFloatRatio desc	ccks_stock
select avg(NumberOfFunds) from mf_fmscaleanalysisn;	ccks_fund
select a.State from lc_stockarchives as a join lc_exgindustry as b on a.CompanyCode = b.CompanyCode where b.FirstIndustryName = 'Wholesale and Retail Trade' group by a.State having count(*) > 3	ccks_stock
select ChiNameAbbr from lc_stockarchives where SecretaryBD='冯莉';	ccks_stock
select AccuMarketableAShares, NonMarketableAShares from lc_sharesfloatingschedule where ChiNameAbbr = '通富微电' or ChiNameAbbr = '海亮股份'	ccks_stock
select IssuePurpose from lc_ashareseasonednewissue where ChiNameAbbr = '京能置业';	ccks_stock
select a.SecuAbbr,a.DailyBenchGR from mf_benchmarkgrowthrate as a join mf_fundarchives as b on a.InnerCode=b.InnerCode   where b.FundType='Equity Fund';	ccks_fund
select ExperienceTime from mf_personalinfo where ChineseName = '蒋一茜';	ccks_fund
select GDP, GDPPerCapita from ed_grossdomesticproduct ;	ccks_macro
select BondAbbr,MarketValue,RatioInNV from mf_bondportifoliodetail where SecuCode='159901';	ccks_fund
select GrossProfit from lc_mainoperincome  where strftime('%Y', EndDate) = strftime('%Y', DATE('now', '-1 year')) and ChiNameAbbr ='冰山冷热';	ccks_stock
select b.Education, count(*) from mf_managerexperience a join mf_personalinfo b on a.PersonalCode = b.PersonalCode where a.InvestAdvisorName like '富国基金%' and a.Incumbent = 'Yes'  group by b.Education	ccks_fund
select RRInSingleYear from mf_netvalueperformancehis ;	ccks_fund
select RRInSelectedWeek, RRInSingleWeek from mf_netvalueperformancehis where SecuAbbr = '银华纯债';	ccks_fund
select count(*) from mf_benchmarkgrowthrate as a join mf_fundarchives as b on a.InnerCode=b.InnerCode where a.BenchGRForThisMonth>3 and b.Type='ETF';	ccks_fund
select FullName,UnderwritingSum from lc_issueandlistagent where ChiNameAbbr='南华生物';	ccks_stock
select EndDate, SubjectSum from ed_newincreasingloan;	ccks_macro
select BonusShareRatio, CashDiviRMB from lc_dividend  where SecuCode ='000752' and strftime('%Y', DividendImplementDate) = strftime('%Y', DATE('now', '-1 year')) ;	ccks_stock
select FPSHName, PCTOfPledger from lc_sharefp  where strftime('%Y', EndDate) = strftime('%Y', DATE('now', '-1 year'));	ccks_stock
select DailyBenchGR from mf_benchmarkgrowthrate where SecuCode='512500';	ccks_fund
select RRSinceStart, AnnualizedRRSinceStart from mf_netvalueperformancehis ;	ccks_fund
select RRSinceThisYear from mf_netvalueperformancehis ;	ccks_fund
select ChiNameAbbr from lc_ashareseasonednewissue order by PlannedProceeds desc limit 1;	ccks_stock
select b.ChiNameAbbr from lc_issueandlistagent as a join lc_stockarchives as b on a.CompanyCode=b.CompanyCode  where b.State='辽宁省' and a.UnderwritingVol>1000000 and a.UnderwritingSum>10000000;	ccks_stock
select LeaderName from lc_executivesholdings  where ChiNameAbbr = '科拓生物' and strftime('%Y', EndDate)='2020'	ccks_stock
select AquirerName from lc_legaldistribution  where SecuCode = '603059' and strftime('%Y', InfoPublDate) = strftime('%Y', DATE('now', '-1 year')) and strftime('%m', InfoPublDate)='4' order by  AquirerAmount desc limit 10 ;	ccks_stock
select a.ConceptName, count(*) from lc_coconcept as a join lc_stockarchives as b on a.CompanyCode = b.CompanyCode where b.City ='南京市' group by a.ConceptName ;	ccks_stock
select ExpenditureCityMC, OperatingExpensesCESH from ed_financialbalance where Province ='四川';	ccks_macro
select EndDate, ImValueOfGoods , ExValueOfGoods from ed_exportimport  where GYoYOfExValueGoods > 0 and ExValueOfGoods > 40 and strftime('%Y', EndDate) > strftime('%Y', DATE('now', '-10 year'));	ccks_macro
select Province from ed_grossdomesticproduct  where strftime('%Y', EndDate) = strftime('%Y', DATE('now', '-1 year')) order by  PrimaryIndustryGDP desc limit 10;	ccks_macro
select SHName from lc_relatedsh  where HoldingSum > 10000000 and SecuCode ='600110' and strftime('%Y', EndDate) = strftime('%Y', DATE('now', '-1 year'));	ccks_stock
select SecuCode, HoldingSum, SHInvestSum from lc_relatedsh where SHName ='顾瑜';	ccks_stock
select AnnualizedRRInThreeYear from mf_netvalueperformancehis ;	ccks_fund
select SecuAbbr from mf_bondportifoliodetail where BondAbbr='20国债10';	ccks_fund
select SecuAbbr from mf_fundarchives  where InvestAdvisorName='易方达基金管理有限公司' and FundType='Equity Fund' and strftime('%Y', EstablishmentDate)='2021';	ccks_fund
select EndDate, TotalLiability from ed_moneyauthoritybs  order by TotalLiability  desc ;	ccks_macro
select SecuAbbr, InvestAdvisorName from mf_fundarchives order by EstablishmentDate asc limit 1	ccks_fund
select CashDiviRMB, ActualCashDiviRMB from lc_dividend  where ChiNameAbbr ='古井贡酒' and strftime('%Y', DividendImplementDate) = strftime('%Y', DATE('now', '-1 year')) ;	ccks_stock
select a.City, count(*) from lc_stockarchives as a join lc_sharestru as b on a.CompanyCode = b.CompanyCode where b.NonRestrictedShares > 10000000000 group by a.City	ccks_stock
select AnnualizedRRInThreeYear from mf_netvalueperformancehis ;	ccks_fund
select a.ActualShares,a.OughtShares from lc_largeshsubscription as a join lc_stockarchives as b on a.CompanyCode=b.CompanyCode  where b.State='广西省';	ccks_stock
select FinancialBonds, SharesAndOtherInvestments from ed_chinafibalancesheetrmb;	ccks_macro
select GDP, GDPPerCapita from ed_grossdomesticproduct where Province ='山东' ;	ccks_macro
select b.ChiNameAbbr from lc_intassetsdetail as a join lc_stockarchives as b on a.CompanyCode=b.CompanyCode  where b.State='广东省' order by a.RDStaffNumRatio desc, a.RDInputRatio desc limit 10;	ccks_stock
select InterestExpense from lc_financialexpense  where ChiNameAbbr = '再升科技' or ChiNameAbbr = '蓝思科技' and strftime('%Y', EndDate)='2017'	ccks_stock
select BondAbbr from mf_bondportifoliodetail where SecuAbbr='易方达中盘ETF' order by RatioInNV desc limit 1;	ccks_fund
select a.State , count(*)  from lc_stockarchives as a join lc_coconcept as b on a.CompanyCode = b.CompanyCode where b.ConceptName ='Large Aircraft' group by a.State ;	ccks_stock
select RRInThreeMonth from mf_netvalueperformancehis where SecuAbbr = '诺德债券';	ccks_fund
select EstablishmentDate from lc_stockarchives where ChiNameAbbr='华昌达';	ccks_stock
select SecuCode , SHInvestSum from lc_relatedsh  where SHName ='万安集团有限公司' and strftime('%Y', EndDate) = strftime('%Y', DATE('now', '-2 year'));	ccks_stock
select ChiNameAbbr from lc_ashareseasonednewissue  where strftime('%Y', AdvanceDate)='2022';	ccks_stock
select TotalShares, Ashares from lc_sharestru where SecuCode = '600371'	ccks_stock
select EndDate, LIValueAP from ed_industryproduction where ReportArea ='National' and StatStandard ='State-Owned and Above-Designated-Size Industrial Enterprises' and ReportPeriod ='End-of-period cumulative';	ccks_macro
select count(a.Name) from mf_fundmanagernew as a join mf_personalinfo as b on a.PersonalCode = b.PersonalCode where b.Education = 'Doctoral degree' and b.Gender = '男'	ccks_fund
select AdvanceDate, IssuePurpose, IssueObject from lc_ashareseasonednewissue where ChiNameAbbr = '大业股份';	ccks_stock
select SecuAbbr from mf_fundreturnrank where FundTypeName = 'Equity Fund' and FundAnnReturn > 0	ccks_fund
select SignatureAccountant,SignatureLaw from lc_ipodeclaration where ChiNameAbbr='华纳百录';	ccks_stock
select ChiNameAbbr , BuybackMoney from lc_buyback  where (ChiNameAbbr = '会稽山' or ChiNameAbbr = '宝钢股份') and strftime('%Y', AdvanceDate)='2020' ;	ccks_stock
select ChiNameAbbr from lc_financialexpense order by ExchangeProLoss desc limit 20	ccks_stock
select FundTypeName from mf_fcretscalerank where AbbrChiName='中信证券' order by TotalAUMRank desc limit 1;	ccks_fund
select b.SecuAbbr,b.Manager from mf_bondportifoliodetail as a join mf_fundarchives as b on a.InnerCode=b.InnerCode where a.BondAbbr='百润转债' order by a.MarketValue desc limit 1;	ccks_fund
select count(*) from lc_legaldistribution  where AquiredSum < 10000 and strftime('%Y', InfoPublDate) = strftime('%Y', DATE('now', '-1 year'));	ccks_stock
select SecuAbbr from mf_benchmarkgrowthrate where BenchGRFor7Year>200;	ccks_fund
select StDivStand1, EnDivStand1 from mf_chargeratenew where ChargeRateTyDes ='Index Licensing Fee';	ccks_fund
select StockAbbr, count(*) from mf_keystockportfolio where StockAbbr = '宁德时代' or StockAbbr = '贵州茅台' group by StockAbbr	ccks_fund
select b.SecuAbbr, b.RiskLevel from mf_fundmanagernew as a join mf_fundrisklevel as b on a.InnerCode = b.InnerCode where a.ManagementTime > 1000	ccks_fund
select JointVentures, SelfEmployed from ed_retailvalueofscgoods where Province ='浙江' and ReportPeriod ='Year';	ccks_macro
select b.SecuAbbr,b.FundType,b.Manager from mf_benchmarkgrowthrate as a join mf_fundarchives as b on a.InnerCode=b.InnerCode where a.BenchGRFor10Year>50;	ccks_fund
select ChiName from lc_sharefp  where strftime('%Y', EndDate)='2018' and strftime('%m', EndDate)='5' order by  InvolvedSum desc limit 10	ccks_stock
select count(*) from mf_bondportifoliodetail where SecuAbbr='华夏50ETF';	ccks_fund
select  FPSHName from lc_sharefp  where strftime('%Y', EndDate) > strftime('%Y', DATE('now', '-3 year'));	ccks_stock
select count(*) from mf_fundmanagernew where Incumbent = 'Incumbent' and PostName = 'Fund Manager Assistant'	ccks_fund
select b.ChineseName, b.TotalFundNV, b.EquityFundNV, b.HybridFundNV from mf_personalinfo as a join mf_fmscaleanalysisn as b on a.PersonalCode = b.PersonalCode where a.Nationality != 'China';	ccks_fund
select IssuePurpose from lc_ashareseasonednewissue where ChiNameAbbr = '京能置业';	ccks_stock
select b.FundType from mf_netvalueperformancehis as a join mf_fundarchives as b on a.InnerCode = b.InnerCode group by b.FundType having avg(a.RRInSingleYear) > 1;	ccks_fund
select SecuCode, FloatShare from qt_monthdata where SecuCode = '600168' or SecuCode = '000422';	ccks_stock
select Website from lc_stockarchives where ChiNameAbbr='万科';	ccks_stock
select FundManager , AwardName from mf_awards where AppraisalOrg = 'Securities Times';	ccks_fund
select b.Manager,b.InvestAdvisorName from mf_fmscaleanalysisn as a join mf_fundarchives as b on a.ChineseName=b.Manager order by a.NumberOfFunds desc limit 1;	ccks_fund
select BuybackPrice, BuybackSum from lc_buyback  where ChiNameAbbr = '南都电源' and strftime('%Y', AdvanceDate)='2021'	ccks_stock
select TotalShare, PB, PETTM from qt_monthdata where SecuCode = '000935';	ccks_stock
select a.ChineseName, b.Background from mf_fmretscaleanalysis as a join mf_personalinfo as b on a.PersonalCode = b.PersonalCode where a.WeightedAvgReturn > 0 and a.TimeInterval = 'Past 10 Years'	ccks_fund
select Fund from mf_awards where strftime('%Y', Year) >=2015 and AwardName ='投资基金';	ccks_fund
select  ClientType from mf_chargeratenew where SecuCode ='160133';	ccks_fund
select ExValueOfGoods, GYoYOfExValueGoods from ed_exportimport  where strftime('%Y', EndDate) = strftime('%Y', DATE('now', '-1 year')) ;	ccks_macro
select ChiNameAbbr from lc_sharestru where RestrictAShareP > 100000000	ccks_stock
select SecuCode from mf_benchmarkgrowthrate where BenchGRFor5Year>50;	ccks_fund
select GDPPerCapita from ed_grossdomesticproduct ;	ccks_macro
select FPSHName, InvolvedSum from lc_sharefp where ChiNameAbbr = '瑞茂通';	ccks_stock
select ChineseName,HybridFundNV from mf_fmscaleanalysisn order by HybridFundNV desc limit 10;	ccks_fund
select EndDate,  DepositsWithCentralBank , CashInVault from ed_otherdepositorycorpbs  where strftime('%Y', EndDate)>='2008';	ccks_macro
select ChiNameAbbr from lc_stockarchives where State='湖北省' and City='武汉市';	ccks_stock
select a.ChiNameAbbr from lc_stockarchives as a join lc_exgindustry as b on a.CompanyCode = b.CompanyCode where a.State = '浙江省' and b.FirstIndustryName = 'Scientific Research and Technology Services'	ccks_stock
select AvgHoldSumGRHalfAYear from lc_shnumber  where strftime('%Y', EndDate)='2020' and ChiNameAbbr='京基智农';	ccks_stock
select WholesaleRetailTrade from ed_retailvalueofscgoods ;	ccks_macro
select BusinessMajor from lc_business lb where ChiNameAbbr ='天齐锂业'	ccks_stock
select LegalRepr from lc_stockarchives where ChiNameAbbr='药明康德';	ccks_stock
select ChargeRateTyDes , DivStand1  from mf_chargeratenew where SecuAbbr ='汇添富经典';	ccks_fund
select ChiNameAbbr, ControllerName from lc_actualcontroller where SecuCode like '00%';	ccks_stock
select count(*) from lc_sharefp where InvolvedSum > 10000000;	ccks_stock
select SecuAbbr from mf_benchmarkgrowthrate order by BenchGRFor3Year desc limit 1;	ccks_fund
select SecuAbbr from mf_benchmarkgrowthrate where BenchGRFor3Year>0;	ccks_fund
select SecuAbbr,AnnualizedBRForSince from mf_benchmarkgrowthrate order by AnnualizedBRForSince desc limit 10;	ccks_fund
select RRInFiveYear from mf_netvalueperformancehis ;	ccks_fund
select SecuCode, ChiNameAbbr from lc_coconcept where ConceptName like '%New Energy%';	ccks_stock
select ChiNameAbbr from lc_financialexpense order by Commission desc limit 5	ccks_stock
select ChiNameAbbr,AStockCode from lc_stockarchives where State='新疆维吾尔自治区';	ccks_stock
select RRInSingleYear , RRInThreeYear, RRInFiveYear from mf_netvalueperformancehis ;	ccks_fund
select count(*) from mf_fundarchives  where SecuMarket='Shanghai Stock Exchange' and Type='LOF' and strftime('%Y', ListedDate)='2021';	ccks_fund
select ChineseName from mf_personalinfo  where strftime('%Y', PracticeDate) = strftime('%Y', date())	ccks_fund
select a.State from lc_stockarchives as a join lc_sharestru as b on a.CompanyCode = b.CompanyCode where b.NonRestrictedShares > 10000000000 group by a.State having count(*) > 10	ccks_stock
select TotalProfitPerShare from mf_mainfinancialindexq  where SecuAbbr = '招商成长' and strftime('%Y', EndDate)='2021' and round(strftime('%m',EndDate)/3.0 + 0.495) = 3	ccks_fund
select * from mf_netvalueperformancehis where RRInSingleYear > 50 and RRInTwoYear > 50;	ccks_fund
select count(*)  from lc_coconcept as a join lc_stockarchives as b on a.CompanyCode = b.CompanyCode where a.ConceptName ='E-Commerce Concept' and b.City ='杭州市';	ccks_stock
select a.SecuCode , b.OfficeAddr from lc_business as a join lc_stockarchives as b on a.CompanyCode = b.CompanyCode where a.IndustryName ='Retail Trade';	ccks_stock
select SecuCode from lc_coconcept where ConceptName like '%百度概念%' and ConceptName like '%阿里概念%';	ccks_stock
select GDP, GDPPerCapita from ed_grossdomesticproduct  where Province ='山东' and  strftime('%Y', EndDate) > strftime('%Y', DATE('now', '-5 year') ) ;	ccks_macro
select Education from mf_personalinfo group by Education having avg(ExperienceTime) > 10;	ccks_fund
select DepositsIncludedInM2 from ed_otherdepositorycorpbs ;	ccks_macro
select count(*) from mf_fmscaleanalysisn where QDIINV > 200;	ccks_fund
select count(*) from lc_business as a join lc_business as b on  a.IndustryName = b.IndustryName where b.ChiNameAbbr = '深科技'	ccks_stock
select count(*) from lc_ashareseasonednewissue  where strftime('%Y', AdvanceDate)='2022';	ccks_stock
select ShareAmountBeginning, ShareAmount from lc_executivesholdings where ChiNameAbbr = '顺网科技' and PositionDescription like '%Chairman of the Board%'	ccks_stock
select EndDate, LIValueAP from ed_industryproduction where ReportArea ='National' and StatStandard ='State-Owned and Above-Designated-Size Industrial Enterprises' and ReportPeriod ='Year';	ccks_macro
select b.SecuAbbr,b.Manager from mf_bondportifoliodetail as a join mf_fundarchives as b on a.InnerCode=b.InnerCode order by a.HoldVolume desc limit 10;	ccks_fund
select a.SecuAbbr from mf_fundreturnrank as a join mf_fundarchives as b on a.InnerCode = b.InnerCode where b.FundType = 'Equity Fund' order by FundAnnReturn desc limit 10	ccks_fund
select IndexValue from ed_producerpiformp where ReportPeriod ='Same period last year' and IndexType ='Industrial Structure Classification Index' and IndexName ='Consumer Goods – Durable Consumer Goods';	ccks_macro
select a.AnnReturnSD, a.AnnDSRisk from mf_fmperfanalysis as a join mf_personalinfo as b on a.PersonalCode = b.PersonalCode where b.ExperienceTime < 5	ccks_fund
select count(*) from mf_netvalueperformancehis where RRInSingleYear > 30 and RRInTwoYear > 30 and RRInThreeYear > 30;	ccks_fund
select count(*) from lc_executivesholdings where  SecuCode = '002104' and  PositionDescription like '%Vice President%'	ccks_stock
select b.SecuAbbr ,b.Manager from mf_benchmarkgrowthrate as a join mf_fundarchives as b on a.InnerCode=b.InnerCode  where a.BenchGRForThisMonth>5;	ccks_fund
select EndDate, RetailValueOfSCGoods from ed_retailvalueofscgoods  where ReportArea ='Provincial and Municipal' and ReportPeriod ='End-of-period cumulative' and strftime('%Y', EndDate) > strftime('%Y', DATE('now', '-3 year')) ;	ccks_macro
select Gender, count(*) from mf_personalinfo group by Gender;	ccks_fund
select FundManager from mf_awards where AppraisalOrg = 'China Fund News';	ccks_fund
select ClosePrice from qt_dailyquote  where strftime('%Y', TradingDay)='2021' and strftime('%m', TradingDay)='1' and strftime('%d', TradingDay)='21' and SecuCode = '002153';	ccks_stock
select AquirerName, AquirerAmount from lc_legaldistribution  where SecuCode = '603059' and strftime('%Y', InfoPublDate)='2020' order by  AquirerAmount desc ;	ccks_stock
select ChiNameAbbr from lc_dividend  where strftime('%Y', DividendImplementDate) > strftime('%Y', DATE('now', '-10 year')) group by  ChiNameAbbr order by count(*) desc limit 1;	ccks_stock
select PCTBeforeTran, PCTAfterTran from lc_sharetransfer  where ChiNameAbbr = '朗新科技' and strftime('%Y', TranDate)='2019'	ccks_stock
select b.ChiNameAbbr, a.FirstIndustryName from lc_exgindustry as a join lc_sharestru as b on a.CompanyCode = b.CompanyCode order by NonListedShares desc limit 5	ccks_stock
select count(distinct AwardName) from mf_awards ;	ccks_fund
select SecretaryBDTel from lc_stockarchives where ChiNameAbbr='万科';	ccks_stock
select ChiNameAbbr from lc_sharesfloatingschedule order by TotalAShares desc limit 10	ccks_stock
select a.SecuCode, a.ChiNameAbbr from lc_coconcept as a join lc_stockarchives as b on a.CompanyCode = b.CompanyCode where b.State ='安徽省' and a.ConceptName ='Autonomous Driving';	ccks_stock
select count(*) from lc_mainoperincome where ChiNameAbbr='中国石化' and MainOperIncome > 200000000000 ;	ccks_stock
select ChiName, HoldingPCT from lc_relatedsh  where ChiNameAbbr = '航天发展' and strftime('%Y', EndDate)='2020' and strftime('%m', EndDate )='3'	ccks_stock
select SecuAbbr from mf_mainfinancialindexq  where strftime('%Y', EndDate)='2020' group by  SecuAbbr having sum(TotalProfit) > 1000000000	ccks_fund
select  RatioCeiling from ed_taxrate where TypeName ='Chinese Large-Sized Banks' and ItemName = 'Excess Reserve Requirement Ratio'  ;	ccks_macro
select AStockCode,AShareAbbr from lc_stockarchives where ChiNameAbbr='科大讯飞';	ccks_stock
select a.SecuCode , b.SecretaryBD , b.OfficeAddr from lc_coconcept as a join lc_stockarchives as b on a.CompanyCode = b.CompanyCode where a.ConceptName ='Sharing Economy' ;	ccks_stock
select ChiNameAbbr, PlaYear, PlaProceeds from lc_ashareplacement where PlaProceeds < 100000000;	ccks_stock
select ChiNameAbbr,RegAddr from lc_stockarchives where City='银川市';	ccks_stock
select ChiNameAbbr from lc_actualcontroller where ControllerName = '福建省财政厅';	ccks_stock
select NVDailyGrowthRate from  mf_netvalueperformancehis ;	ccks_fund
select a.SecuCode , b.State  from lc_coconcept as a join lc_stockarchives as b on a.CompanyCode = b.CompanyCode where a.ConceptName ='Metaverse' ;	ccks_stock
select ChineseName from mf_fmscaleanalysisn where EquityFundNV > 100 and HybridFundNV > 50;	ccks_fund
select ChiNameAbbr from lc_financialexpense order by InterestExpense desc limit 10	ccks_stock
select ReportPeriod, IndexType, IndexValue from ed_producerpiformp where  IndexName ='Metallurgical';	ccks_macro
select SecuAbbr from mf_fundreturnrank where FundReturn > 0 and FundAnnReturn > 0	ccks_fund
select RRInTwoYear from mf_netvalueperformancehis ;	ccks_fund
select b.ChiNameAbbr from lc_issueandlistagent as a join lc_stockarchives as b on a.CompanyCode=b.CompanyCode  where b.State='上海市' and a.UnderwritingVol>1000000;	ccks_stock
select ChiNameAbbr from lc_financialexpense order by Commission desc	ccks_stock
select ChargeRateDes from  mf_chargeratenew where SecuAbbr ='富国300ESGETF';	ccks_fund
select FPSHName, InvolvedSum from lc_sharefp where SecuCode = '600180' and PCTOfTotalShares >=0.05 ;	ccks_stock
select FullName from lc_issueandlistagent order by UnderwritingVol desc limit 100;	ccks_stock
select ChiNameAbbr from lc_freefloat where AdjFreeFloatRatio = 100	ccks_stock
select ChiNameAbbr from lc_ashareplacement  where strftime('%Y', PlaYear) = strftime('%Y', DATE('now', '-2 year'));	ccks_stock
select a.TransfererName, a.SumBeforeTran, a.PCTBeforeTran from lc_sharetransfer as a join lc_stockarchives as b on a.CompanyCode = b.CompanyCode where b.State = '江苏省'	ccks_stock
select count(*) from lc_business where IndustryName like '%Computer%'	ccks_stock
select EndDate, IndustrialOutputValueAP from ed_industryproduction where ReportArea ='National' and StatStandard ='All Industrial Enterprises' and ReportPeriod ='End-of-period cumulative';	ccks_macro
select ChiNameAbbr from lc_mainoperincome  where strftime('%Y', EndDate)='2021' order by  MainOperIncome desc limit 5;	ccks_stock
select SecuAbbr, Name from mf_fundmanagernew order by Performance desc limit 5	ccks_fund
select UnitNV, AccumulatedUnitNV from mf_netvalue where SecuAbbr = '国泰融信';	ccks_fund
select ChineseName,TotalFundNV from mf_fmscaleanalysisn order by TotalFundNV desc limit 1;	ccks_fund
select b.SecuAbbr,b.Manager from mf_bondportifoliodetail as a join mf_fundarchives as b on a.InnerCode=b.InnerCode order by a.MarketValue desc limit 1;	ccks_fund
select ChiNameAbbr from lc_ashareseasonednewissue group by ChiNameAbbr having count(*) > 1;	ccks_stock
select RRSinceThisYear from mf_netvalueperformancehis ;	ccks_fund
select BonusShareRatio from lc_dividend where SecuCode ='000021';	ccks_stock
select EndDate ,ImValueOfGoods , GYoYOfImValueGoods from ed_exportimport  where strftime('%Y', EndDate) < strftime('%Y', DATE('now', '-10 year'));	ccks_macro
select SecuAbbr,BenchGRForSince from mf_benchmarkgrowthrate order by BenchGRForSince limit 20;	ccks_fund
select SHName from lc_relatedsh  where SecuCode ='300184' and strftime('%Y', EndDate) = strftime('%Y', DATE('now', '-1 year')) and round(strftime('%m',EndDate)/3.0 + 0.495) = 4 ;	ccks_stock
select LeaderName, ShareAmount from lc_executivesholdings where PositionDescription like '%Vice President%'	ccks_stock
select BonusShareRatio, DiviBase from lc_dividend  where ChiNameAbbr ='西藏发展' and strftime('%Y', DividendImplementDate) = strftime('%Y', DATE('now', '-1 year')) ;	ccks_stock
select DomesticLoans from ed_chinamoneyandbanking order by EndDate desc limit 1;	ccks_macro
select RRInSingleMonth from  mf_netvalueperformancehis ;	ccks_fund
select  SecuCode, ChiNameAbbr from lc_dividend  where ActualCashDiviRMB > 10 and strftime('%Y', DividendImplementDate) = strftime('%Y', DATE('now', '-2 year'));	ccks_stock
select RRSinceStart, AnnualizedRRSinceStart from mf_netvalueperformancehis ;	ccks_fund
select LeaderName from lc_executivesholdings where ChiNameAbbr = '石化油服' order by ShareAmount desc limit 1	ccks_stock
select FPSHName, AccuFPShares from lc_sharefpsta where SecuCode like '300%'	ccks_stock
select SecuAbbr from mf_mainfinancialindexq  where strftime('%Y', EndDate)='2020' group by  SecuAbbr order by sum(TotalProfit) desc limit 1	ccks_fund
select RRInSingleYear, RRInTwoYear, RRInThreeYear from mf_netvalueperformancehis where SecuAbbr = '易方达中小企业A';	ccks_fund
select AnnualizedRRSinceStart from mf_netvalueperformancehis ;	ccks_fund
select FundTypeName, count(*) from mf_fundreturnrank where IndexCycle = '1 year' and FundReturn < 0 group by FundTypeName	ccks_fund
select RRInThreeYear, RRInFiveYear, RRInTenYear, RRSinceStart from mf_netvalueperformancehis ;	ccks_fund
select ChiNameAbbr, TotalShares from lc_sharestru where ChiNameAbbr = '东北证券' or ChiNameAbbr = '国元证券'	ccks_stock
select SecuAbbr from mf_fundarchives order by LowestSumSubLL asc limit 1	ccks_fund
select a.ChiNameAbbr, b.GeneralManager, b.LegalRepr from lc_dividend as a join lc_stockarchives as b on a.CompanyCode = b.CompanyCode  where strftime('%Y', a.DividendImplementDate)='2021';	ccks_stock
select SelfEmployed from ed_retailvalueofscgoods ;	ccks_macro
select AnnualizedRRInFiveYear from mf_netvalueperformancehis ;	ccks_fund
select OrganizationForm, count(*) from mf_investadvisoroutline group by OrganizationForm order by count(*) desc;	ccks_fund
select DomesticLoans , OverseasLoans , AgriculturalDeposits from ed_chinafibalancesheetrmb  where strftime('%Y', EndDate)<='2000' and TotalLoans >1000000;	ccks_macro
select  ProfitDistributionRule from mf_fundarchives where SecuAbbr = '招商成长'	ccks_fund
select count(*), SecuCode from lc_coconcept  group by SecuCode ;	ccks_stock
select AnnualizedRRInThreeYear , AnnualizedRRInFiveYear , AnnualizedRRInTenYear from mf_netvalueperformancehis ;	ccks_fund
select b.SecuAbbr,b.InvestField from mf_benchmarkgrowthrate as a join mf_fundarchives as b on a.InnerCode=b.InnerCode  where a.BenchGRForThisMonth<0;	ccks_fund
select MainName from lc_business lb where ChiNameAbbr ='富临精工'	ccks_stock
select SecuAbbr from mf_fundarchives order by EstablishmentDate desc	ccks_fund
select  FPSHName from lc_sharefp  where PCTOfPledger > 0.3 and strftime('%Y', EndDate) > strftime('%Y', DATE('now', '-2 year'));	ccks_stock
select SecuCode , NVWeeklyGrowthRate from  mf_netvalue ;	ccks_fund
select ProportionGRQuarter from lc_shnumber  where strftime('%Y', EndDate)='2020' and round(strftime('%m',EndDate)/3.0 + 0.495)=2 and ChiNameAbbr='京基智农';	ccks_stock
select EvalAgent,SignatureEvaluator from lc_ipodeclaration where SecuCode='300278';	ccks_stock
select RetailValueOfSCGoods from ed_retailvalueofscgoods where Province ='江苏';	ccks_macro
select CorporateSavings , FinanceDeposits from ed_chinafibalancesheetrmb  where strftime('%Y', EndDate)='2004';	ccks_macro
select EndDate from ed_financialbalance where Province ='江苏' and LocalGovRevenue > 100 and LocalGovExpenditure < 100;	ccks_macro
select IndustryName from lc_business where ChiNameAbbr ='深科技'	ccks_stock
select MainOperIncome from lc_mainoperincome  where ChiNameAbbr ='中国石化' and strftime('%Y', EndDate) = strftime('%Y', DATE('now', '-1 year')) and round(strftime('%m',EndDate)/3.0 + 0.495) = 1;	ccks_stock
select SecuAbbr, IndexCycle, FundReturn from mf_fundreturnrank where SecuAbbr = '华夏创蓝筹ETF' or SecuAbbr = '建信深证60ETF'	ccks_fund
select TotalFundNV from mf_fmscaleanalysisn where ChineseName='张坤';	ccks_fund
select b.ChineseName, b.TotalFundNV, b.QDIINV from mf_personalinfo as a join mf_fmscaleanalysisn as b on a.PersonalCode = b.PersonalCode where a.Nationality = 'United States';	ccks_fund
select ControllerName from lc_actualcontroller group by ControllerName order by count(*) desc limit 1;	ccks_stock
select SecuCode from mf_fundarchives where SecuAbbr = '广发小盘A'	ccks_fund
select b.ChiNameAbbr, a.SecretaryBD from lc_stockarchives as a join lc_freefloat as b on a.CompanyCode = b.CompanyCode where b.AdjFreeFloats > 10000000 and a.City = '深圳市'	ccks_stock
select ClaimToSavingsInst , ClaimtoOtherFinNonFinInst from ed_moneyauthoritybs ;	ccks_macro
select SecuAbbr from mf_keystockportfolio group by SecuAbbr order by sum(MarketValue) desc limit 1	ccks_fund
select count(*) from lc_ipodeclaration where CSRCIndustryName='Banking';	ccks_stock
select ChineseName from mf_personalinfo order by BirthDate asc limit 1	ccks_fund
select a.ChiNameAbbr from lc_intassetsdetail as a join  lc_stockarchives as b on a.CompanyCode=b.CompanyCode  where strftime('%Y', a.EndDate)=strftime('%Y', DATE('now', '-1 year')) and b.State='浙江省' and TotalRDInput>100000000;	ccks_stock
select ChiNameAbbr from lc_buyback  where strftime('%Y', AdvanceDate) = strftime('%Y', DATE('now', '-1 year')) and (round(strftime('%m',AdvanceDate)/3.0 + 0.495) = 3 or round(strftime('%m',AdvanceDate)/3.0 + 0.495) = 4);	ccks_stock
select b.ChiNameAbbr, b.ControllerName from lc_stockarchives as a join lc_actualcontroller as b on a.CompanyCode = b.CompanyCode where a.State = '浙江省';	ccks_stock
select SecuAbbr,Manager from mf_fundarchives where InvestAdvisorName='国泰基金管理有限公司' and Type='ETF';	ccks_fund
select count(*) from mf_benchmarkgrowthrate as a join mf_fundarchives as b on a.InnerCode=b.InnerCode where a.MonthlyBenchGR>0 and b.Manager='朱少醒';	ccks_fund
select IndexValue from ed_producerpiformp where ReportPeriod ='Same period last year' and IndexType ='Industrial Structure Classification Index' and IndexName ='Consumer Goods – Food';	ccks_macro
select MainOperIncome , MainOperCost, MainOperProfit from lc_mainoperincome  where strftime('%Y', EndDate) = strftime('%Y', DATE('now', '-1 year')) and SecuCode ='000822';	ccks_stock
select ClosePrice from qt_dailyquote  where strftime('%Y', TradingDay)='2021' and round(strftime('%m',TradingDay)/3.0 + 0.495) = 1 and SecuCode = '300278';	ccks_stock
select ChiNameAbbr from lc_sharetransfer order by InvolvedSum desc limit 10	ccks_stock
select a.FirstIndustryName from lc_exgindustry as a join lc_sharestru as b on a.CompanyCode = b.CompanyCode where b.NonListedShares > 200000000 group by a.FirstIndustryName having count(*) > 50	ccks_stock
select  FundCompany from  mf_awards  where strftime('%Y', Year) >=2010 and AwardName ='Three-Year Equity Jinfund Award' and WinnerType ='Investment Fund';	ccks_fund
select Name from mf_fundmanagernew where SecuCode like '15%' and Performance > 0.7	ccks_fund
select EndDate, TotalAssets, TotalLiabilities, ForeignAssets, ForeignLiabilities from ed_otherdepositorycorpbs where TotalAssets > 50000000 order by EndDate desc limit 1;	ccks_macro
select AvgHoldSumGRQuarter from lc_shnumber where ChiNameAbbr='古井贡酒';	ccks_stock
select ClosePrice from qt_dailyquote  where strftime('%Y', TradingDay)='2021' and strftime('%m', TradingDay)='4' and ChiNameAbbr = '华昌达';	ccks_stock
select Fund, AppraisalOrg from mf_awards;	ccks_fund
select RatioFloor from ed_taxrate where TypeName ='Rural Credit Cooperatives' and ItemName ='Excess Reserve Requirement Ratio';	ccks_macro
select b.ChiNameAbbr, b.SecondIndustryName from lc_stockarchives as a join lc_exgindustry as b on a.CompanyCode = b.CompanyCode where a.State = '浙江省' and b.FirstIndustryName = 'Manufacturing';	ccks_stock
select ChiNameAbbr from lc_executivesholdings where LeaderName = '刘明强'	ccks_stock
select b.SecuAbbr,b.InvestTarget from mf_benchmarkgrowthrate as a join mf_fundarchives as b on a.InnerCode=b.InnerCode  order by a.MonthlyBenchGR desc limit 10;	ccks_fund
select LeaderName, ChiNameAbbr from lc_executivesholdings where PositionDescription like '%Chairman of the Board%' and PositionDescription like '%President%'	ccks_stock
select SecretaryBD,SecretaryBDTel from lc_stockarchives where AStockCode='600234';	ccks_stock
select CollectiveUnits from ed_retailvalueofscgoods ;	ccks_macro
select b.Manager from mf_benchmarkgrowthrate as a join mf_fundarchives as b on a.InnerCode=b.InnerCode where a.DailyBenchGR>0;	ccks_fund
select a.State , count(*)  from lc_stockarchives as a join lc_coconcept as b on a.CompanyCode = b.CompanyCode where b.ConceptName ='Graphene' group by a.State having count(*)>1;	ccks_stock
select a.FirstIndustryName, count(*) from lc_exgindustry as a join lc_freefloat as b on a.CompanyCode = b.CompanyCode where b.AdjFreeFloatRatio = 100 group by a.FirstIndustryName	ccks_stock
select a.ChiNameAbbr, a.FPSHName, a.AccuFPShares from lc_sharefpsta as a join lc_stockarchives as b on a.CompanyCode = b.CompanyCode where b.State = '河北省'	ccks_stock
select ImValueOfGoods, GYoYOfImValueGoods from ed_exportimport where GYoYOfExValueGoods > 0 and ExValueOfGoods > 20 and strftime('%Y', EndDate)<'2000';	ccks_macro
select UnitNV from mf_netvalue where SecuAbbr = '华安180ETF' and EndDate >= '2021-4-1';	ccks_fund
select Education, ExperienceTime from mf_personalinfo where ChineseName = '刘伟琳';	ccks_fund
select ChineseName from mf_personalinfo where ExperienceTime > 20 and Gender = '女';	ccks_fund
select b.ChiNameAbbr from lc_exgindustry as a join lc_sharestru as b on a.CompanyCode = b.CompanyCode where a.FirstIndustryName = 'Construction' and b.TotalShares > 10000000000	ccks_stock
select ChineseName from mf_fmscaleanalysisn order by TotalFundNV desc limit 1;	ccks_fund
select ChiNameAbbr from lc_issueandlistagent where UnderwritingSum<100000000;	ccks_stock
select RetailValueOfSCGoods from ed_retailvalueofscgoods where Province ='天津' and ReportPeriod ='Year';	ccks_macro
select IndexValue from ed_producerpiformp  where IndexName ='Beverage Manufacturing' and ReportPeriod ='Same period last year' and strftime('%Y', EndDate) = strftime('%Y', DATE('now', '-1 year')) ;	ccks_macro
select ChineseName,HybridFundN from mf_fmscaleanalysisn where ChineseName='刘格菘' or ChineseName='朱少醒';	ccks_fund
select EndDate, ClaimsOnOtherNFInstitute, LiabilitiesToNFInst from ed_otherdepositorycorpbs  where strftime('%Y', EndDate) = strftime('%Y', date());	ccks_macro
select SecondIndustryName from lc_exgindustry where FirstIndustryName = 'Manufacturing' group by SecondIndustryName order by count(*) desc limit 1	ccks_stock
select count(*) from lc_legaldistribution ;	ccks_stock
select count(*) from mf_netvalueperformancehis where RRSinceStart > 1000;	ccks_fund
select IndexType from ed_producerpiformp ;	ccks_macro
select SecuAbbr from mf_netvalueperformancehis where SecuAbbr like '%稳健%' order by NVDailyGrowthRate desc limit 1;	ccks_fund
select b.SecondIndustryName, count(*) from lc_sharesfloatingschedule as a join lc_exgindustry as b on a.CompanyCode = b.CompanyCode where a.AccuMarketableAShares > 5000 group by b.SecondIndustryName	ccks_stock
select ClosePrice from qt_dailyquote  where strftime('%Y', TradingDay)='2021' and strftime('%m', TradingDay)='4' and SecuCode = '300278';	ccks_stock
select SHName, HoldingSum from lc_relatedsh where ChiNameAbbr = '农发种业' and strftime('%Y', EndDate)<'2019';	ccks_stock
select PlaYear, PlaProceeds from lc_ashareplacement where SecuCode = '600859';	ccks_stock
select SHName from lc_largeshsubscription where ChiNameAbbr='博瑞传播' order by ActualShares desc limit 3;	ccks_stock
select SecuAbbr,BenchGRForThisWeek from mf_benchmarkgrowthrate where BenchGRForThisWeek<0 order by BenchGRForThisWeek asc;	ccks_fund
select MainBusiness from lc_business where ChiNameAbbr ='精研科技'	ccks_stock
select ChiNameAbbr from lc_shnumber where ProportionGRQuarter>10;	ccks_stock
select ChiName from lc_shnumber  where strftime('%Y', EndDate)='2019' order by  SHNum desc limit 5;	ccks_stock
select ChiNameAbbr from lc_shnumber where AvgHoldSumGRHalfAYear>20;	ccks_stock
select ClaimsToGov from ed_chinamoneyandbanking ;	ccks_macro
select FPSHName from lc_sharefp where ChiNameAbbr = '瑞茂通' and PCTOfTotalShares > 0.05 ;	ccks_stock
select SavingsDeposits, AgriculturalDeposits from ed_chinafibalancesheetrmb;	ccks_macro
select ImValueOfGoods, ExValueOfGoods from ed_exportimport ;	ccks_macro
select ChineseName from mf_personalinfo where Education = 'Doctoral degree'  order by ExperienceTime desc limit 1	ccks_fund
select TransfererName, ReceiverName from lc_sharetransfer  where ChiNameAbbr = '宝钢股份' and strftime('%Y', TranDate)='2018'	ccks_stock
select CapitalReceived, NetAbroadAssets, DomesticLoans from ed_chinamoneyandbanking  where strftime('%Y', EndDate) > strftime('%Y', DATE('now', '-2 year')) ;	ccks_macro
select InvestAdvisorAbbrName, RegAddr, RegCapital from mf_investadvisoroutline where RegCapital > 10000000000;	ccks_fund
select TransfererName, SumAfterTran, PCTAfterTran from lc_sharetransfer  where ChiNameAbbr = '盛天网络' and strftime('%Y', TranDate)='2018'	ccks_stock
select FullName from lc_issueandlistagent;	ccks_stock
select GrossProfit from lc_mainoperincome where ChiNameAbbr ='西藏发展';	ccks_stock
select ImValueOfGoods, GYoYOfImValueGoods from ed_exportimport  where strftime('%Y', EndDate) = strftime('%Y', DATE('now', '-2 year')) ;	ccks_macro
select ChineseName from mf_personalinfo where Nationality != 'China';	ccks_fund
select ClaimsOnOtherFInstitute from ed_otherdepositorycorpbs ;	ccks_macro
select ClosePrice from qt_dailyquote  where strftime('%Y', TradingDay)='2021' and strftime('%m', TradingDay)='1' and strftime('%d', TradingDay)='14' and ChiNameAbbr = '石基信息';	ccks_stock
select IssuePurpose from lc_ashareseasonednewissue where SecuCode = '300022';	ccks_stock
select a.ChiNameAbbr, a.FPSHName, a.AccuFPShares from lc_sharefpsta as a join lc_stockarchives as b on a.CompanyCode = b.CompanyCode where b.State = '浙江省'	ccks_stock
select ChineseName from mf_fmscaleanalysisn where NumberOfFunds>15;	ccks_fund
select HybridFundN, HybridFundNV from mf_fmscaleanalysisn where ChineseName = '郑希';	ccks_fund
select DailyBenchGR from mf_benchmarkgrowthrate where SecuAbbr='富国天丰';	ccks_fund
select Region, count(*) from mf_investadvisoroutline where strftime('%Y', EstablishmentDate)>'2015' group by Region;	ccks_fund
