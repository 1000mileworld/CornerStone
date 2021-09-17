%Backtest Cornerstone strategy
%v2: add portfolio values throughout the year
clear
warning('OFF', 'MATLAB:table:ModifiedAndSavedVarnames')

acct.funds = 10000; %starting capital
numStocks = 25; %for each growth and val
year_range = [2015,2020]; %years used for backtest (starting with last day of that year)
split = [0.5,0.5]; %[%growth, %value] - percent of capital for each strategy
headers = ["Ticker","Quantity","CurrentPrice","TotalValue"];
file_bench = "VOO.csv"; %file to use for benchmark when comparing strategy

%xData = linspace(year_range(1)+1,year_range(2)+1,year_range(2)-year_range(1)+1);
[x_bench,y_bench] = getBench(year_range,file_bench,acct.funds);

disp('-----Simulating growth stocks-----')
[t1,b1] = runSim(split(1)*acct.funds,numStocks,year_range,headers,"growth");

disp('-----Simulating value stocks-----')
[t2,b2] = runSim(split(2)*acct.funds,numStocks,year_range,headers,"val");

totalBalance = b1+b2;

plot(x_bench,y_bench,'g')
hold on
plot(t1,b1,'b')
plot(t2,b2,'r')
plot(t1,totalBalance,'k')

xlabel("Year","FontSize",16)
ylabel("Portolio ($)","FontSize",16)
legend("Benchmark","Growth","Value","Total","Location","best")

R_avg = (totalBalance(end)/totalBalance(1))^(1/(year_range(2)-year_range(1)))-1;
fprintf("Strategy returned an average of %.2f%% per year during the period %d-%d.\n",...
    R_avg*100,year_range(1),year_range(2));

R_bench = (y_bench(end)/y_bench(1))^(1/(year_range(2)-year_range(1)))-1;
fprintf("Benchmark returned an average of %.2f%% during the same period.\n",R_bench*100);

function [time,balance] = runSim(capital,numStocks,year_range,headers,type)
    acct.balance = 0; %value of purchased stocks
    acct.funds = capital;
    time = [];
    balance = [];
    
    %balance = zeros(1,year_range(2)-year_range(1)+1);

    for analysisYear=year_range(1):year_range(2)
        fprintf("Running year %d...\n",analysisYear);

        if type=="growth"
            [stockSelection, ~] = cornerstone(analysisYear); %growth
        else
            [~,stockSelection] = cornerstone(analysisYear); %value
        end
        
        stockList = stockSelection(1:numStocks);   
        dir_price = "../Data/Prices/"+num2str(analysisYear)+"/";       

        ref_price = "AAPL.csv";
        T_ref = readtable(dir_price+ref_price);
        numDays = height(T_ref); %total number of trading days expected
            
        if acct.balance==0
            [portfolio,acct.funds] = runStrat(headers,stockList,acct.funds,dir_price);
            acct.balance = sum(cell2mat(portfolio(:,find(headers=="TotalValue")))); %#ok<*FNDSB>
            time = [time T_ref.Date(end)];
        else
            time = [time; T_ref.Date];
            %update stock portfolio for the current analysis year
            p_balance = zeros(numDays,numStocks);
            for stock_idx=1:numStocks
                quantity = portfolio{stock_idx,find(headers=="Quantity")};
                [~,T_price] = getPrice(dir_price,portfolio{stock_idx,find(headers=="Ticker")});
                if height(T_price)==numDays %data for all trading days of the year is available
                    p_balance(:,stock_idx) = T_price.AdjClose.*quantity;
                else %data for some trading days are missing
                    for day=1:numDays
                        if ismember(T_ref.Date(day),T_price.Date)
                            row = find(T_price.Date==T_ref.Date(day));
                        else
                            [~,row] = min(abs(T_price.Date-T_ref.Date(day)));
                        end
                        p_balance(day,stock_idx) = T_price.AdjClose(row)*quantity;
                    end
                end
            end
            
            acct.balance = sum(p_balance,2);
            [portfolio,acct.funds] = runStrat(headers,stockList,sum(p_balance(end,:))+acct.funds,dir_price);
        end
        balance = [balance; acct.funds+acct.balance];

    end

end

function [portfolio,funds] = runStrat(headers,stockList,capital,dir_price)
    %returns a portfolio with ticker, quantity, current price, and total
    %value
    
    funds = capital;
    numStocks = length(stockList);
    portfolio(:,find(headers=="Ticker")) = stockList;
    portfolio(:,find(headers=="Quantity")) = num2cell(zeros(numStocks,1));
    counter = 1;
    while funds~=0
        stock = stockList{counter};
        [purchase_price,~] = getPrice(dir_price,stock);
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

function [price,T_price] = getPrice(dir_price,stock)
    file = dir_price+stock+".csv";
    try
        T_price = readtable(file);
        price = T_price.AdjClose(end);
    catch
        warning("No price data found for %s, setting price to 0.",stock)
        price = 0;
    end
end

function [xData,yData] = getBench(year_range,file_bench,capital)
    T_bench = readtable(file_bench);

    selection1 = find(year(T_bench.Date)==year_range(1));
    selection2 = find(year(T_bench.Date)==year_range(2));

    if isempty(selection1) || isempty(selection2)
        disp('Selected dates outside of range in benchmark file.')
    else
        startRow = selection1(end);
        endRow = selection2(end);
        shares = floor(capital/T_bench.AdjClose(startRow));
        leftover = capital-T_bench.AdjClose(startRow)*shares;
        yData = T_bench.AdjClose(startRow:endRow).*shares+leftover;
        xData = T_bench.Date(startRow:endRow);
    end
end