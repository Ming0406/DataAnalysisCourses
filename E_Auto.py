import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px


month_sales = df1.groupby(['年份', '月份'])['销量'].sum().reset_index()
month_sales["日期"] = month_sales["年份"].astype(str) + "-" + month_sales["月份"].astype(str)
fig = px.bar(month_sales,  # 上面指定的数据
       title="中国电动汽车月销售量",
       template="plotly_white",  # 分别主题设置为：plotly、plotly_dark
       x="日期",  # 横坐标
       y="销量",  # 纵坐标
       color="销量")  # 颜色取值
fig.show()

yearly_sales = df1.groupby('年份')['销量'].sum().reset_index()
# 计算销量同比数据
yearly_sales['销量同比'] = round(yearly_sales['销量'].diff() / yearly_sales['销量'].shift(1)*100, 2)

fig1 = go.Figure(data=[go.Table(
    header=dict(values=list(yearly_sales.columns),
                fill_color='paleturquoise',
                align='left'),  # 指定标题

    cells=dict(values=[yearly_sales.年份, yearly_sales.销量, yearly_sales.销量同比],
               fill_color='lavender',  # 给出数据，颜色和对齐方式
               align='left'))
])

fig1.show()

from plotly.subplots import make_subplots

fig2 = make_subplots(specs=[[{"secondary_y":True}]])
fig2.add_trace(
    go.Scatter(x=yearly_sales["年份"], y=yearly_sales["销量"], name="销量"), secondary_y=True
)
fig2.add_trace(
    go.Bar(x=yearly_sales["年份"], y=yearly_sales["销量同比"], name="销量同比（%）" )
)
fig2.update_yaxes(go.layout.YAxis(tickformat="", showgrid=False), secondary_y=True)
fig2.update_layout(go.Layout(title=go.layout.Title(text="中国电动汽车年销售量")), template="plotly_white")
fig2.show()


cx_sales = df1.groupby(['年份',"车型"])['销量'].sum().reset_index()
cx_sales = cx_sales[cx_sales["销量"] > 45000]
fig3 = px.line(cx_sales, x="年份", y="销量", color="车型", title="电动汽车分型号销量(年销量大于4.5万)")
fig3.update_layout(height=600, template="plotly_white")
# 添加水平参考线
fig3.add_hline(y=45000, line_dash="dash", line_color="gray")
# 修改线条样式
fig3.update_traces(line=dict(width=3))  # 设置线宽为3
# 显示图表
fig3.show()

df_2023 = df1[df1["年份"] == 2023]
cx_2023 = df_2023.groupby(['厂商', '车型'])['销量'].sum().reset_index()
# 绘制旭日图
fig4 = px.sunburst(cx_2023, path=['厂商', '车型'],
                  values='销量',
                  color='车型',
                  color_discrete_sequence=px.colors.qualitative.Plotly,
                 )
# 设置图形布局
fig4.update_layout(
    title={
        'text': "2023年厂商汽车车型销量分布",
        'x': 0.2,   # 将标题移动到右上角居中位置
        'y': 0.95,
        'xanchor': 'center',
        'yanchor': 'top'
    },
    margin=dict(l=20, r=20, t=50, b=20),  # 设置边距
    sunburstcolorway=["#636EFA", "#EF553B", "#00CC96", "#AB63FA", "#FFA15A", "#19D3F3", "#FF6692", "#B6E880", "#FF97FF", "#FECB52"],
    uniformtext=dict(minsize=10, mode='hide')  # 将图中太小的占比统一改为"其他"
)
# 调整图形布局, 使其不会太紧凑
fig4.update_traces(textinfo='label+percent entry')
fig4.update_layout(margin=dict(t=0, l=0, r=0, b=0))
# 显示图例
fig4.update_layout(legend=dict(font=dict(size=20)))
# 显示图表
fig4.show()

cs_sales = df1.groupby(['年份',"厂商"])['销量'].sum().reset_index()
fig5 = px.bar(cs_sales,x="年份",y="销量",color="厂商",text_auto=",",title="中国各厂商电动汽车销量（年）")
fig5.update_layout(height=1200)
fig5.show()

df1["最低售价"] = df1["售价（万元）"].astype(str).str.split(r'[-~到至]').str[0].str.strip()
df1["最低售价"] = pd.to_numeric(df1["最低售价"], errors='coerce')
cs1 = df1[df1["最低售价"] >= 10]
cs1_sales = cs1.groupby(['年份',"厂商"])['销量'].sum().reset_index()
fig6 = px.bar(cs1_sales,x="年份",y="销量",color="厂商",text_auto=",",title="电车各品牌汽车销量(单价大于10万)")
fig6.update_layout(height=1200)
fig6.show()