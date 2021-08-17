%Generate database of stock parameters and save as csv

analysis_year = 2020;

%% Getting tickers
disp("Getting company tickers from available price data...")

dir_price = "../Data/Prices/";
myFiles = dir(fullfile(dir_price+num2str(analysis_year),'*.csv'));

n = length(myFiles);
Symbols = strings(length(myFiles),1);
f = waitbar(0, 'Starting...');
for i=1:length(myFiles)
    name_cell = strsplit(myFiles(i).name,'.');
    Symbols(i) = convertCharsToStrings(name_cell{1});
    waitbar(i/n, f, sprintf('Progress: %d %%', floor(i/n*100)));
end
close(f)

%% Process nasdaq screener file
disp("Getting company tickers from available price data...")