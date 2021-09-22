%filter stocks by parameter

yr = 2017;
headers = ["Ticker","LastSale","MarketCap","Sector","ReportDate",...
    "Revenue","NetIncome","NetIncomePrev"...
    "SharesOutstanding","CashFlow","ShareholderYield",...
    "ThreeMonthPriceAppreciation","SixMonthPriceAppreciation","TwelveMonthPriceAppreciation"];
loadFile = "fundamentals_"+num2str(yr)+".csv";

T = readtable(loadFile);
T = filterT(T);

%ind = find(strcmpi(T.Properties.VariableNames,'TwelveMonthPriceAppreciation'));
%T = sortrows(T,ind,'descend');

function T = filterT(T)
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
end