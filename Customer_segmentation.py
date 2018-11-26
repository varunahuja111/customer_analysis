
import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt

df = pd.read_excel('Customer_data.xlsx')
df.head()
df = df[df.Country == "United Kingdom" ]
df = df[pd.notnull(df['CustomerID'])]
df= df[(df['Quantity']>0)]
#df.shape
#df.info()
df['TotalPrice'] = df['Quantity'] * df['UnitPrice']
m1= df['InvoiceDate'].min()
m2= df['InvoiceDate'].max()
NOW = pd.to_datetime(m2)
df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
NOW += dt.timedelta(days=1)
rfmTable = df.groupby('CustomerID').agg({'InvoiceDate': lambda x: (NOW - x.max()).days, 'InvoiceNo': lambda x: len(x), 'TotalPrice': lambda x: x.sum()})
rfmTable['InvoiceDate'] = rfmTable['InvoiceDate'].astype(int)
rfmTable.rename(columns={'InvoiceDate': 'recency', 
                         'InvoiceNo': 'frequency', 
                         'TotalPrice': 'monetary_value'}, inplace=True )
rfmTable.head()
quartiles=rfmTable.quantile(q=[0.25,0.5,0.75])
quartiles=quartiles.to_dict()
segmented_rfm = rfmTable
def RScore(x,p,d):
    if x <= d[p][0.25]:
        return 1
    elif x <= d[p][0.50]:
        return 2
    elif x <= d[p][0.75]: 
        return 3
    else:
        return 4
    
def FMScore(x,p,d):
    if x <= d[p][0.25]:
        return 4
    elif x <= d[p][0.50]:
        return 3
    elif x <= d[p][0.75]: 
        return 2
    else:
        return 1
segmented_rfm['r_quartile'] = segmented_rfm['recency'].apply(RScore, args=('recency',quartiles,))
segmented_rfm['f_quartile'] = segmented_rfm['frequency'].apply(FMScore, args=('frequency',quartiles,))
segmented_rfm['m_quartile'] = segmented_rfm['monetary_value'].apply(FMScore, args=('monetary_value',quartiles,))
segmented_rfm.head()
segmented_rfm['RFMScore'] = segmented_rfm.r_quartile.map(str)+ segmented_rfm.f_quartile.map(str)+ segmented_rfm.m_quartile.map(str)
#print(segmented_rfm[segmented_rfm['RFMScore']=='111'].sort_values('monetary_value', ascending=False).head(10))
#best=filter(lambda x:x['RFMScore']=='111',segmented_rfm)
#print(best)
bt=len(segmented_rfm[segmented_rfm['RFMScore']=='111'])
ly=len(segmented_rfm[(segmented_rfm['f_quartile']==1) & (segmented_rfm['m_quartile']>1) & (segmented_rfm['r_quartile']>1) ])
bs=len(segmented_rfm[(segmented_rfm['m_quartile']==1) & (segmented_rfm['f_quartile']>1) & (segmented_rfm['r_quartile']>1) ])
al=len(segmented_rfm[segmented_rfm['RFMScore']=='311'])
lc=len(segmented_rfm[segmented_rfm['RFMScore']=='411'])
lcc=len(segmented_rfm[segmented_rfm['RFMScore']=='444'])
print("Best Customers: ",bt)
print('Loyal Customers: ',ly)
print("Big Spenders: ",bs)
print('Almost Lost: ',al)
print('Lost Customers: ',lc)
print('Lost Cheap Customers: ',lcc)

def Find_segment(r,d):
    if r== '111':
        return 'Best Customers' 
    elif r=='311':
        return 'Almost Lost' 
    elif r=='411':
        return 'Lost Customers' 
    elif r=='444':
        return 'Lost Cheap Customers'
    elif (r=='414')| (r=='413')| (r=='412')| (r=='312')| (r=='313')| (r=='314')| (r=='211')| (r=='212')| (r=='213')| (r=='214')| (r=='112')| (r=='113')| (r=='114'):
    #elif [(segmented_rfm['f_quartile']==1) & (segmented_rfm['m_quartile']>1) & (segmented_rfm['r_quartile']>1)] :
        return 'Loyal Customers' 
    else:
        return 'Big Spenders'
#segmented_rfm=segmented_rfm.assign(Segment = Find_segment(segmented_rfm['RFMScore']))
#segmented_rfm['Segments'] = segmented_rfm.apply(lambda row : Find_segment(row),axis=1)    
segmented_rfm['Segments'] = segmented_rfm['RFMScore'].apply(Find_segment,args=('RFMScore',))
#segmented_rfm['Segments'] = segmented_rfm['f_quartile'].apply(Find_segment_usingf_Quartile,args=('f_quartile'))
#segmented_rfm['Segments'] = segmented_rfm['m_quartile'].apply(Find_segment_usingm_Quartile,args=('m_quartile'))
#plot = segmented_rfm.plot.pie(y='Segments', figsize=(5, 5))
colors = ["#E13F29", "#D69A80", "#D63B59", "#AE5552", "#CB5C3B", "#EB8076", "#96624E"]
labels='Best Customers','Loyal Customers','Big Spenders','Almost Lost','Lost Customers','Lost Cheap Customers',
sizes=[bt,ly,bs,al,lc,lcc] 
print(labels)
print(sizes)
plt.pie(sizes,labels=labels,colors=colors,startangle=90)
plt.show()