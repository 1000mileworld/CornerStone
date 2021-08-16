%calculate average values for data
%clear

%market capitalization, shares outstanding, cashflow, sales
warning('OFF', 'MATLAB:table:ModifiedAndSavedVarnames')

analysis_year = 2020;

file1 = "nasdaq_screener.csv";
T_nasdaq = readtable(file1);

marketCap_total = T_nasdaq.MarketCap(~isnan(T_nasdaq.MarketCap));
marketCap_avg = sum(marketCap_total)/length(marketCap_total);

disp("Determining values from income statement...")
dir_income = "Finpie method/Data/Income/";
myFiles = dir(fullfile(dir_income,'*.csv'));
revenue_total = 0; %in millions
shares_outstanding_total = 0;
sum_income = 0;

for i=1:length(myFiles)
    
    file = convertCharsToStrings(myFiles(i).folder)+"\"+convertCharsToStrings(myFiles(i).name);

    T_income = readtable(file);
    idx = find(year(T_income.date)==analysis_year);
    if ~isempty(idx)
        revenue_total = revenue_total+max(T_income.revenue(idx)); %may be multiple values for same year
        shares_outstanding_total = shares_outstanding_total+max(T_income.shares_outstanding(idx));
        sum_income = sum_income+1;
    else
        disp("Check file for missing income params: "+myFiles(i).name)
    end
end

revenue_avg = revenue_total/sum_income;
shares_outstanding_avg = shares_outstanding_total/sum_income;
