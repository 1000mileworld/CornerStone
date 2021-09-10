%Backtest Cornerstone strategy
%purchase stock at end of year price
clear
warning('OFF', 'MATLAB:table:ModifiedAndSavedVarnames')

trade.funds = 5000; %starting capital
numStocks = 25; %for each growth and val
year_range = [2015,2020];
split = [0.5,0.5]; %[%growth, %value] - percent of capital for each strategy
%tax = 0.15; %account for long term capital gains tax

headers = ["Ticker","Quantity","CurrentPrice","TotalValue"];
%portfolio = cell(numStocks*2,length(headers));
trade.balance = 0; %value of purchased stocks
xData = linspace(year_range(1),year_range(2),year_range(2)-year_range(1)+1);
yData = zeros(1,year_range(2)-year_range(1)+1);

for analysisYear=year_range(1):year_range(2)

    [growthStocks, valStocks] = cornerstone(analysisYear);
    %candidates = unique([growthStocks(1:numStocks);valStocks(1:numStocks)],'stable');
    
    stockList = growthStocks(1:numStocks);   
    dir_price = "../Data/Prices/"+num2str(analysisYear)+"/";
    %Symbols_price = getPriceSym(dir_price);
    
    if trade.balance==0 %no purchased stocks
        p_growth(:,find(headers=="Ticker")) = stockList; %#ok<*FNDSB>
        p_growth(:,find(headers=="Quantity")) = num2cell(zeros(numStocks,1));
        counter = 1;
        while trade.funds~=0
            stock = stockList{counter};
            purchase_price = getPrice(dir_price,stock);
            if purchase_price>trade.funds
               break 
            end
            ticker_row = find(p_growth(1:numStocks,find(headers=="Ticker"))==convertCharsToStrings(stock));
            p_growth{ticker_row,find(headers=="Quantity")} = ...
                p_growth{ticker_row,find(headers=="Quantity")}+1;
            p_growth{ticker_row,find(headers=="CurrentPrice")} = purchase_price;
            p_growth{ticker_row,find(headers=="TotalValue")} = ...
                p_growth{ticker_row,find(headers=="Quantity")}*p_growth{ticker_row,find(headers=="CurrentPrice")};
            trade.funds = trade.funds-purchase_price;
            
            if counter==numStocks
               counter = 1; 
            else
               counter = counter+1;
            end
        end
    else
        %update current price and sell if not on this year's list   
        for ticker_row=1:numStocks
            p_growth{ticker_row,find(headers=="CurrentPrice")} = ...
                getPrice(dir_price,p_growth{ticker_row,find(headers=="Ticker")});
            p_growth{ticker_row,find(headers=="TotalValue")} = ...
                p_growth{ticker_row,find(headers=="Quantity")}*p_growth{ticker_row,find(headers=="CurrentPrice")};
            if ~ismember(p_growth{ticker_row,find(headers=="Ticker")},stockList)
                trade.funds = trade.funds+p_growth{ticker_row,find(headers=="TotalValue")};
                p_growth{ticker_row,find(headers=="Quantity")} = 0;
                p_growth{ticker_row,find(headers=="TotalValue")} = 0;
            end
        end
        %p_goal: ideal portfolio for this year
    end
    trade.balance = sum(cell2mat(p_growth(:,find(headers=="TotalValue"))));
    yData(analysisYear-year_range(1)+1) = trade.funds+trade.balance;
end

plot(xData,yData,'o')

function [Symbols] = getPriceSym(dir_price)
    priceFiles = dir(fullfile(dir_price,'*.csv'));
    Symbols = strings(length(priceFiles),1);
    for i=1:length(priceFiles)
        nameCell = strsplit(priceFiles(i).name,'.');
        Symbols(i) = convertCharsToStrings(nameCell{1});
    end
end

function [price] = getPrice(dir_price,stock)
    file = dir_price+stock+".csv";
    T_price = readtable(file);
    price = T_price.AdjClose(end);
end
