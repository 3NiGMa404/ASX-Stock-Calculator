import urllib.request
import re
import os
os.system('color b')
name=input('What is your name? ').lower().capitalize()
try:
    txt=open(name+'-ASX.txt','r').read()
except:
    if not input(name + ' not found, create new portfolio? ').lower().startswith('y'):
        exit()
    num=int(input('how many companies to you own shares in? '))
    wrt=open(name+'-ASX.txt','w+')
    wrt.close()
    for i in range(num):
        stock_name=input('Enter ASX stock code: ').upper()
        curr_value=input('How much did you buy these shares for (each)? ')
        amount=input('How many of these shares do you have? ')
        wrt=open(name+'-ASX.txt','a')
        wrt.write('\n'+stock_name+'/'+amount+'/'+curr_value)
    wrt.close()
    input('Thankyou! Your data has been saved!\nRestart the program to view your data!')
    exit()


stocks=txt.split('\n')
if '' in stocks:
    stocks.remove('')
values=[]
value_lst=[]
olds=[]
os.system('cls')
print('Hey, '+name.capitalize()+'!\nYou have shares in {} companies'.format(len(stocks)))
for stock in stocks:
    stock_name=stock.split('/')[0]
    fp = urllib.request.urlopen("https://finance.yahoo.com/quote/"+stock_name+".AX?p="+stock_name+".AX&.tsrc=fin-srch")
    mybytes = fp.read()
    mystr = mybytes.decode("utf8")
    myls=mystr.split('<span class="Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(ib)" data-reactid="32">')
    fp.close()
    mystr=myls[1]
    num_shares=int(stock.split('/')[1])
    mystr=mystr.split('<')[0]
    values.append(round(float(mystr),2))
    value_lst.append(round(float(mystr),2)*num_shares)
    old_value=round(float(stock.split('/')[2]),2)
    olds.append(old_value*num_shares)
    fp2 = urllib.request.urlopen("https://finance.yahoo.com/quote/"+stock_name+".AX/history?p="+stock_name+".AX")
    mystr2=fp2.read().decode('utf8')
    print('\nASX Code: {}\nBought Price: ${}\nValue Per Share: ${}\nProfit Margin: {}%\nNet Profit Per Share: ${}\nPosition Value: ${}'.format(stock_name,old_value,mystr,(round((100*float(mystr)/old_value)-100,3)),round(float(mystr)-old_value,2),round(float(mystr)*num_shares,2)))
    try:
        
        div=round(float(re.findall(r''+datetime.today().strftime('%B')[0:3]+' '+datetime.today().strftime('%d')+', '+datetime.today().strftime('%Y')+'</span></td><td class="Ta\(c\) Py\(10px\) Pstart\(10px\)" colspan="6" data-reactid="[\d]+"><strong data-reactid="[\d]+">(.*)</', mystr2)[0].split('</')[0]),2)
        print("Today's Dividend: ${}".format(div))
    except:
        print('No Dividends Today')
        


if sum(value_lst)/sum(olds)<1:
    os.system('color c')
else:
    os.system('color a')
print('\n')
print('Total Profit Margin: {}%'.format(round(100*sum(value_lst)/sum(olds)-100,2)))
print('Total Profit: ${}'.format(round(sum(value_lst)-sum(olds),2)))
print('Portfolio Value: ${}'.format(round(sum(value_lst),2)))
input()
