%Implement Cornerstone strategy
%clear

analysisYear = 2020;
loadFile = "fundamentals_"+num2str(analysisYear)+".csv";
numStocks = 50; %each for growth and value

%growth = [];
%value = [];

%% Filter data for invalid values
T = readtable(loadFile);
for i=2:length(T.Properties.VariableNames)
    header = T.Properties.VariableNames{i};
    colData = T.(header);
    if header=="Sector"
        select = cellfun(@(C) strcmp(C,''), colData);
    elseif header=="ReportDate"
        select = isnat(colData) | month(colData)<=3;
    else
        select = isnan(colData);
    end
    T(select,:) = [];
end

%% Compute averages
[totalStocks,~] = size(T);
avg_3M = sum(T.ThreeMonthPriceAppreciation)/totalStocks;
avg_6M = sum(T.SixMonthPriceAppreciation)/totalStocks;
avg_MCap = sum(T.MarketCap)/totalStocks;
avg_shares = sum(T.SharesOutstanding)/totalStocks;
avg_cash = sum(T.CashFlow)/totalStocks;
avg_sales = sum(T.Revenue)/totalStocks; %in millions

%% Find growth stock candidates
T_growth = T;

%Desired criteria
condition = T_growth.MarketCap>300e6; %small cap
T_growth(~condition,:) = [];

condition = T_growth.MarketCap./(T_growth.Revenue.*1e6)<1.5 & T_growth.Revenue>0; %P/S ratio
T_growth(~condition,:) = [];

condition = T_growth.NetIncome>T_growth.NetIncomePrev & T_growth.NetIncome>0 & T_growth.NetIncomePrev>0; %Earnings higher than previous year
T_growth(~condition,:) = [];

condition = T_growth.ThreeMonthPriceAppreciation>avg_3M; %3 month price appreciation greater than avg.
T_growth(~condition,:) = [];

condition = T_growth.SixMonthPriceAppreciation>avg_6M; %6 month price appreciation greater than avg.
T_growth(~condition,:) = [];

T_growth.ProfitMargin = T_growth.NetIncome./T_growth.Revenue;
ind = find(strcmpi(T_growth.Properties.VariableNames,'ProfitMargin')); %rank top 100 by profit margin
T_growth = sortrows(T_growth,ind,'descend');
if height(T_growth)>100
   T_growth(101:end,:) = []; 
end

ind = find(strcmpi(T_growth.Properties.VariableNames,'TwelveMonthPriceAppreciation'));
T_growth = sortrows(T_growth,ind,'descend');

if height(T_growth)<numStocks
    growthStocks = T_growth.Ticker;
else
    growthStocks = T_growth.Ticker(1:numStocks);
end

writeData(growthStocks,"growth.txt")

%% Functions
function [] = writeData(data,fileName)
    fid = fopen(fileName,'w');
    for i=1:length(data)
        fprintf(fid,'%s\n',data{i});
    end
    fclose(fid);
end
