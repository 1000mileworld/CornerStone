%Backtest Cornerstone strategy
%purchase stock at end of year price
clear
warning('OFF', 'MATLAB:table:ModifiedAndSavedVarnames')

acct.funds = 10000; %starting capital
numStocks = 25; %for each growth and val
year_range = [2015,2020];
split = [0.5,0.5]; %[%growth, %value] - percent of capital for each strategy
%tax = 0.15; %account for long term capital gains tax
headers = ["Ticker","Quantity","CurrentPrice","TotalValue"];

xData = linspace(year_range(1),year_range(2),year_range(2)-year_range(1)+1);

disp('-----Simulating growth stocks-----')
[balance1] = runSim(split(1)*acct.funds,numStocks,year_range,headers,"growth");

disp('-----Simulating value stocks-----')
[balance2] = runSim(split(2)*acct.funds,numStocks,year_range,headers,"val");

totalBalance = balance1+balance2;

plot(xData,balance1,'b-*')
hold on
plot(xData,balance2,'r-*')
plot(xData,totalBalance,'k-s')

xlabel("Year","FontSize",16)
ylabel("Portolio ($)","FontSize",16)
legend("Growth","Value","Total","Location","best")

R_avg = (totalBalance(end)/totalBalance(1))^(1/(year_range(2)-year_range(1)))-1;
fprintf("Strategy returned an average of %.2f%% during the period %d-%d.\n",R_avg*100,year_range(1),year_range(2));

function [balance] = runSim(capital,numStocks,year_range,headers,type)
    acct.balance = 0; %value of purchased stocks
    acct.funds = capital;
    
    balance = zeros(1,year_range(2)-year_range(1)+1);

    for analysisYear=year_range(1):year_range(2)
        fprintf("Running year %d...\n",analysisYear);

        if type=="growth"
            [stockSelection, ~] = cornerstone(analysisYear); %growth
        else
            [~,stockSelection] = cornerstone(analysisYear); %value
        end
        %candidates = unique([growthStocks(1:numStocks);valStocks(1:numStocks)],'stable');

        stockList = stockSelection(1:numStocks);   
        dir_price = "../Data/Prices/"+num2str(analysisYear)+"/";
        %Symbols_price = getPriceSym(dir_price);
        if acct.balance==0
            [portfolio,acct.funds] = runStrat(headers,stockList,acct.funds,dir_price);
            acct.balance = sum(cell2mat(portfolio(:,find(headers=="TotalValue")))); %#ok<*FNDSB>
        else
            %update current price and sell if not on this year's list
            for ticker_row=1:numStocks
                portfolio{ticker_row,find(headers=="CurrentPrice")} = ...
                    getPrice(dir_price,portfolio{ticker_row,find(headers=="Ticker")});
                portfolio{ticker_row,find(headers=="TotalValue")} = ...
                    portfolio{ticker_row,find(headers=="Quantity")}*portfolio{ticker_row,find(headers=="CurrentPrice")};
            end
            acct.balance = sum(cell2mat(portfolio(:,find(headers=="TotalValue"))));
            [portfolio,acct.funds] = runStrat(headers,stockList,acct.balance+acct.funds,dir_price);
    %         for ticker_row=1:numStocks
    %             if ~ismember(p_growth{ticker_row,find(headers=="Ticker")},stockList)
    %                 acct.funds = acct.funds+p_growth{ticker_row,find(headers=="TotalValue")};
    %                 p_growth{ticker_row,find(headers=="Quantity")} = 0;
    %                 p_growth{ticker_row,find(headers=="TotalValue")} = 0;
    %             end
    %         end
        end
        balance(analysisYear-year_range(1)+1) = acct.funds+acct.balance;
    end

end

function [portfolio,funds] = runStrat(headers,stockList,capital,dir_price)
    funds = capital;
    numStocks = length(stockList);
    portfolio(:,find(headers=="Ticker")) = stockList;
    portfolio(:,find(headers=="Quantity")) = num2cell(zeros(numStocks,1));
    counter = 1;
    while funds~=0
        stock = stockList{counter};
        purchase_price = getPrice(dir_price,stock);
        if purchase_price>funds
           break 
        end
        ticker_row = find(portfolio(1:numStocks,find(headers=="Ticker"))==convertCharsToStrings(stock));
        portfolio{ticker_row,find(headers=="Quantity")} = ...
            portfolio{ticker_row,find(headers=="Quantity")}+1;
        portfolio{ticker_row,find(headers=="CurrentPrice")} = purchase_price;
        portfolio{ticker_row,find(headers=="TotalValue")} = ...
            portfolio{ticker_row,find(headers=="Quantity")}*portfolio{ticker_row,find(headers=="CurrentPrice")};
        funds = funds-purchase_price;

        if counter==numStocks
           counter = 1; 
        else
           counter = counter+1;
        end
    end
end

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
    try
        T_price = readtable(file);
        price = T_price.AdjClose(end);
    catch
        warning("No price data found for %s, setting price to 0.",stock)
        price = 0;
    end
end
