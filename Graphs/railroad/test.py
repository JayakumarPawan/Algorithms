import matplotlib.pyplot as plt
import pandas as pd
x = [100,200,300,400,500,600,700,800,900,1000]

y_1 = [0.003,.005,.006,.007,.007,.008,.007,.012,.015,.017]
y_2 = [.001,.003,.002,.006,.008,.009,.011,.011,.014,.018]
y_3 = [.001,.001,.003,.006,.007,.008,.007,.013,.014,.016]

y1 = [.001,.011,.026,.045,.072,.102,.139,.162,.204,.215]
y2 = [0.005, .023, .048,.091,.1,.103,.142,.177,.231,.288]
y3 = [.002,.011,.025,.046,.072,.095,.108,.184,.235,.27]

y_ = zip(y_1,y_2,y_3)

y = zip(y1,y2,y3)

yf = [(a+b+c)/3 for a,b,c in y_]
yf2 = [(a+b+c)/3 for a,b,c in y]
df = pd.DataFrame({'Num Points':x,"Time in seconds for recursive":yf,"Time in seconds for brute force":yf2})
plt.plot('Num Points',"Time in seconds for recursive", data =df, marker = 'o',color = 'pink')
plt.plot('Num Points',"Time in seconds for brute force", data =df, marker = 'o',color = 'black')
plt.legend()
plt.xlabel('Number of Points')
plt.show()
