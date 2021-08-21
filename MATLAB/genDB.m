%Generate database of stock parameters and save as csv
fclose('all');
warning('OFF', 'MATLAB:table:ModifiedAndSavedVarnames')

analysisYear = 2020;
headers = ["Ticker","LastSale","MarketCap","Sector","Revenue","NetIncome","NetIncomePrev"...
    "SharesOutstanding","CashFlow","ShareholderYield"];
saveFile = "fundamentals_"+num2str(analysisYear)+".csv";

file_nasdaq = "../nasdaq_screener.csv";
dir_price = "../Data/Prices/"+num2str(analysisYear)+"/";
dir_cashflow = "../Finpie method/Data/Cashflow/";
dir_income = "../Finpie method/Data/Income/";
%% Getting tickers
% disp("Getting company tickers from available price and fundamental data...")
% 
% dirData = "../Finpie method/Data/Income/";
% myFiles = dir(fullfile(dirData,'*.csv'));
% 
% n = length(myFiles);
% Symbols = strings(length(myFiles),1);
% f = waitbar(0, 'Starting...');
% for i=1:n
%     nameCell = strsplit(myFiles(i).name,'_');
%     Symbols(i) = convertCharsToStrings(nameCell{1});
%     waitbar(i/n, f, sprintf('Progress: %d %%', floor(i/n*100)));
% end
% close(f)

%% Get data for each ticker
headers_cell = cell(1,length(headers));
fid = fopen(saveFile,'w');
for i=1:length(headers)
   headers_cell{i} = char(headers(i));
end

db = cell(length(Symbols),length(headers));
T_nasdaq = readtable(file_nasdaq);

for i=1:5
    fprintf("Processing data for %d of %d Symbols (%s)\n",i,length(Symbols),Symbols(i));
    ticker = Symbols(i);
    
    %Ticker
    db{i,find(headers=="Ticker")} = ticker; %#ok<*FNDSB>
    
    %Process nasdaq screener file
    idx_nasdaq = find(T_nasdaq.Symbol==ticker);
    if ~isempty(idx_nasdaq)
        %Last Sale
        tempCell = strsplit(T_nasdaq.LastSale{idx_nasdaq},'$');
        db{i,find(headers=="LastSale")} = str2double(tempCell{end});
        
        %Market Cap
        db{i,find(headers=="MarketCap")} = T_nasdaq.MarketCap(idx_nasdaq);
        
        %Sector
        db{i,find(headers=="Sector")} = T_nasdaq.Sector{idx_nasdaq};
    end
    
    %Process income statement
    file_income = dir_income+ticker+"_income.csv";
    try
        T_income = readtable(file_income);
        idx_income = find(year(T_income.date)==analysisYear);
        if ~isempty(idx_income)
            
            %Revenue
            db{i,find(headers=="Revenue")} = max(T_income.revenue(idx_income)); %may be multiple values for same year
            
            %Net Income
            db{i,find(headers=="NetIncome")} = max(T_income.net_income(idx_income));
            
            %Net Income for Previous Year
            idx_income_prev = find(year(T_income.date)==analysisYear-1);
            if ~isempty(idx_income_prev)
                db{i,find(headers=="NetIncomePrev")} = max(T_income.net_income(idx_income_prev));
            end
            
            %Shares Outstanding
            db{i,find(headers=="SharesOutstanding")} = max(T_income.shares_outstanding(idx_income));
        end
    catch
        warning('No income statement found, assigning NANs to parameters.');
        db{i,find(headers=="Revenue")} = nan;
        db{i,find(headers=="NetIncome")} = nan;
        db{i,find(headers=="NetIncomePrev")} = nan;
        db{i,find(headers=="SharesOutstanding")} = nan;
    end
    
    %Process cash flow statement
    file_cashflow = dir_cashflow+ticker+"_cashflow.csv";
    try
        T_cashflow = readtable(file_cashflow);
        idx_cashflow = find(year(T_cashflow.date)==analysisYear);
        if ~isempty(idx_cashflow)
           
            %Cash Flow
            operations = T_cashflow.cash_flow_from_operating_activities(idx_cashflow);
            investments = T_cashflow.cash_flow_from_investing_activities(idx_cashflow);
            financial = T_cashflow.cash_flow_from_financial_activities(idx_cashflow);
            db{i,find(headers=="CashFlow")} = operations(end)+investments(end)+financial(end);
            
            %Shareholder Yield
            if T_nasdaq.MarketCap(idx_nasdaq)~=0
                dividends = sum(T_cashflow.total_common_and_preferred_stock_dividends_paid(idx_cashflow));
                shareRepurchase = sum(T_cashflow.net_total_equity_issued_to_repurchased(idx_cashflow));
                debtRepay = sum(T_cashflow.debt_issuance_to_retirement_net___total(idx_cashflow));
                returnedCapital = -(dividends+shareRepurchase+debtRepay);
                db{i,find(headers=="ShareholderYield")} = returnedCapital/T_nasdaq.MarketCap(idx_nasdaq);
            end
        end
    catch
        warning('No cash flow statement found, assigning NANs to parameters.');
        db{i,find(headers=="CashFlow")} = nan;
        db{i,find(headers=="ShareholderYield")} = nan;
    end
end

disp("Done!")

T = cell2table(db,'VariableNames',headers_cell);
writetable(T,saveFile)
fclose(fid);
