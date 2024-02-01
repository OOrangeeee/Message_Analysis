# 微信聊天记录分析

>写在前面：本程序是本人（在读大二学生）利用课余时间三天内写完的送给我女朋友的小惊喜，碍于课业压力，时间不足和能力有限本程序还有很多漏洞和缺点，任何问题都可以联系我（联系方式写在代码头了），有时间我会更新的，还希望大佬勿喷。

## 软件概述

>本软件专注于对已获取的微信聊天数据进行深入分析。
为了使用本软件的数据分析功能，您首先需要通过专业人士开发的“留痕”软件来爬取微信聊天记录并导出为csv格式。最后的板块内我分享了留痕的一个版本供大家使用并且分享了其仓库链接，请大家多多支持大佬的工作。一旦完成了微信数据的爬取和解密，便可将这些数据导入到我们的软件中，进行全面而详细的分析。
我的软件设计用以洞察和解读微信聊天记录，为用户提供深入的数据洞见。（特别适合情侣之间分析聊天记录

***注：如果想直接使用程序，请直接跳到最后，查看“运行程序”板块。爬取方式也在那里。生成的图片直接查看或许会失真（尤其是总体的热力图，plt的锅），请在文件夹中查看，是完全正常的。(图片的保存路径是./用户数据/data/src，用户数据文件夹就在exe的同级目录里)***

本软件致力于保障用户隐私，所有源代码均可供查阅，确保用户信息及聊天记录的安全性和保密性。我们以“晋**（化名：橙子）”和“宁*（化名：柠檬）”的聊天数据为例，展现了本软件的数据分析能力。若需更改分析对象，用户可在源代码中搜索并替换相应的名字。本软件提供的数据分析功能包括：

1. **聊天记录词频分析**：
   1. 对两人聊天记录中的高频词进行统计，生成三张精美的词云图（橙子一张，柠檬一张，以及二人共同的一张）。
2. **Emoji使用分析**：
   1. 统计两人最常用的emoji，并通过柱状图进行比较展示。
3. **表情包使用分析**：
   1. 分类统计两人使用的表情包种类，并以柱状图形式展示每人的种类数。
   2. 比较两人使用表情包的数量，并通过柱状图进行展示。
   3. 分析并对比两人使用不同表情包的频率，以柱状图形式展示。
4. **聊天热度分析**：
   1. 生成每月的日历形式热力图，分别针对橙子和柠檬，以及他们共同的记录。
   2. 统计并展示同一时期内的聊天热度变化，以折线图形式展示。
5. **聊天时间分析**：
   1. 分析一天24小时内两人的聊天活跃度，并生成相应的热力图（橙子一张，柠檬一张，以及共同的一张）。
6. **聊天情感分析（可选）**：
   1. 利用百度智能云的语句情感分析API，对聊天记录进行情感分析，并生成三张饼图（橙子一张，柠檬一张，以及共同的一张）。

所有分析结果和数据均可在根目录下的**用户数据**文件夹中查阅。这些功能旨在为用户提供深入、全面的聊天数据分析，帮助用户更好地理解和存储宝贵的交流信息。

**在2.0版本的重大更新后，程序现已实现全面优化，完美适配各类聊天记录。用户能够灵活地输入自己的姓名，并分析任意时间段的聊天内容，不再受限于之前的四个月时间限制。此外，程序还提供了便捷的情感分析功能选择，用户可根据需要轻松输入API相关信息进行分析。总的来说，经过全面升级的2.0版本，终于成为了一个真正优秀的产品。这一过程告诫我们，优化代码的重要性不容忽视，希望大家能从中汲取教训，千万不要把代码写死。**

## 环境配置

关于软件环境的配置，我有几点建议想与你分享。首先，我不建议你完全依赖导出的环境配置来搭建自己的系统。在实际操作中，**根据自己的需求逐步补充所缺少的组件往往是一个更为高效和灵活的方法**。原因很简单：每个人的需求和环境都是独一无二的，盲目跟随他人的配置可能并不适合你。

至于为什么不提供一个自动化的环境配置程序，诚实地说，这主要是因为我有些懒惰。编写这样的程序需要花费大量的时间和精力，而且往往难以满足所有人的需求。

如果你不想深入自定义名称、月份等参数（这需要修改代码，尽管只是几个参数，但前提是你需要有足够的专业知识来阅读和理解代码），你可以选择使用我预先打包好的程序。我已经尽可能地将其配置得简单易用，希望能够满足你的基本需求。

感谢你的理解和支持！希望我的建议对你有所帮助。

``` bash
# This file may be used to create an environment using:
# $ conda create --name <env> --file <this file>
# platform: win-64
altgraph=0.17.3=py39haa95532_0
blas=1.0=mkl
bottleneck=1.3.5=py39h080aedc_0
brotli=1.0.9=h2bbff1b_7
brotli-bin=1.0.9=h2bbff1b_7
ca-certificates=2023.12.12=haa95532_0
contourpy=1.2.0=py39h59b6b97_0
cycler=0.11.0=pyhd3eb1b0_0
et_xmlfile=1.1.0=py39haa95532_0
fonttools=4.25.0=pyhd3eb1b0_0
freetype=2.12.1=ha860e81_0
future=0.18.3=py39haa95532_0
giflib=5.2.1=h8cc25b3_3
icc_rt=2022.1.0=h6049295_2
icu=73.1=h6c2663c_0
importlib_resources=6.1.1=py39haa95532_1
intel-openmp=2023.1.0=h59b6b97_46320
joblib=1.2.0=py39haa95532_0
jpeg=9e=h2bbff1b_1
kiwisolver=1.4.4=py39hd77b12b_0
krb5=1.20.1=h5b6d351_0
lerc=3.0=hd77b12b_0
libbrotlicommon=1.0.9=h2bbff1b_7
libbrotlidec=1.0.9=h2bbff1b_7
libbrotlienc=1.0.9=h2bbff1b_7
libclang=14.0.6=default_hb5a9fac_1
libclang13=14.0.6=default_h8e68704_1
libdeflate=1.17=h2bbff1b_1
libpng=1.6.39=h8cc25b3_0
libpq=12.15=h906ac69_1
libtiff=4.5.1=hd77b12b_0
libwebp=1.3.2=hbc33d0d_0
libwebp-base=1.3.2=h2bbff1b_0
lz4-c=1.9.4=h2bbff1b_0
matplotlib=3.8.0=py39haa95532_0
matplotlib-base=3.8.0=py39h4ed8f06_0
mkl=2023.1.0=h6b88ed4_46358
mkl-service=2.4.0=py39h2bbff1b_1
mkl_fft=1.3.8=py39h2bbff1b_0
mkl_random=1.2.4=py39h59b6b97_0
munkres=1.1.4=py_0
numexpr=2.8.7=py39h2cd9be0_0
numpy=1.26.3=py39h055cbcc_0
numpy-base=1.26.3=py39h65a83cf_0
openjpeg=2.4.0=h4fc8c34_0
openpyxl=3.0.10=py39h2bbff1b_0
openssl=3.0.12=h2bbff1b_0
packaging=23.1=py39haa95532_0
pandas=1.2.4=pypi_0
pefile=2022.5.30=py39haa95532_0
pillow=10.0.1=py39h045eedc_0
pip=23.3.1=py39haa95532_0
ply=3.11=py39haa95532_0
pyinstaller=5.13.2=py39h2bbff1b_0
pyinstaller-hooks-contrib=2022.14=py39haa95532_0
pyparsing=3.0.9=py39haa95532_0
pyqt=5.15.10=py39hd77b12b_0
pyqt5-sip=12.13.0=py39h2bbff1b_0
python=3.9.18=h1aa4202_0
python-dateutil=2.8.2=pyhd3eb1b0_0
python-tzdata=2023.3=pyhd3eb1b0_0
pytz=2023.3.post1=py39haa95532_0
pywin32=305=py39h2bbff1b_0
pywin32-ctypes=0.2.0=py39haa95532_1000
qt-main=5.15.2=h19c9488_10
scikit-learn=1.3.0=py39h4ed8f06_0
scipy=1.11.4=py39h309d312_0
seaborn=0.12.2=py39haa95532_0
setuptools=68.2.2=py39haa95532_0
sip=6.7.12=py39hd77b12b_0
six=1.16.0=pyhd3eb1b0_1
sqlite=3.41.2=h2bbff1b_0
tbb=2021.8.0=h59b6b97_0
threadpoolctl=2.2.0=pyh0d69192_0
tk=8.6.12=h2bbff1b_0
tomli=2.0.1=py39haa95532_0
tornado=6.3.3=py39h2bbff1b_0
tzdata=2023d=h04d1e81_0
vc=14.2=h21ff451_1
vs2015_runtime=14.27.29016=h5e58377_2
wheel=0.41.2=py39haa95532_0
wordcloud=1.9.2=py39h2bbff1b_0
xz=5.4.5=h8cc25b3_0
zipp=3.17.0=py39haa95532_0
zlib=1.2.13=h8cc25b3_0
zstd=1.5.5=hd43e919_0
absl-py==0.15.0
altgraph @ file:///C:/b/abs_f2edualeyv/croot/altgraph_1670426107695/work
astunparse==1.6.3
baidu-aip==4.16.13
Bottleneck @ file:///C:/Windows/Temp/abs_3198ca53-903d-42fd-87b4-03e6d03a8381yfwsuve8/croots/recipe/bottleneck_1657175565403/work
cachetools==5.3.2
certifi==2023.11.17
chardet==3.0.4
charset-normalizer==3.3.2
clang==5.0
click==8.1.7
colorama==0.4.6
contourpy @ file:///C:/b/abs_853rfy8zse/croot/contourpy_1700583617587/work
cycler @ file:///tmp/build/80754af9/cycler_1637851556182/work
et-xmlfile==1.1.0
filelock==3.9.0
fire==0.5.0
flatbuffers==1.12
fonttools==4.25.0
fsspec==2023.4.0
future @ file:///C:/b/abs_3dcibf18zi/croot/future_1677599891380/work
gast==0.4.0
google-auth==2.25.2
google-auth-oauthlib==1.2.0
google-pasta==0.2.0
grpcio==1.60.0
h11==0.9.0
h2==3.2.0
h5py==3.1.0
hpack==3.0.0
hstspreload==2024.1.5
httpcore==0.9.1
httpx==0.13.3
hyperframe==5.2.0
icon-font-to-png==0.4.1
idna==2.10
importlib-metadata==7.0.0
importlib-resources @ file:///C:/b/abs_d0dmp77t95/croot/importlib_resources-suite_1704281892795/work
install==1.3.5
jieba==0.42.1
Jinja2==3.1.2
joblib==1.3.2
Keras-Preprocessing==1.1.2
kiwisolver @ file:///C:/b/abs_88mdhvtahm/croot/kiwisolver_1672387921783/work
libclang==16.0.6
libretranslatepy==2.1.1
lxml==5.1.0
Markdown==3.5.1
MarkupSafe==2.1.3
matplotlib @ file:///C:/b/abs_e26vnvd5s1/croot/matplotlib-suite_1698692153288/work
mkl-fft @ file:///C:/b/abs_19i1y8ykas/croot/mkl_fft_1695058226480/work
mkl-random @ file:///C:/b/abs_edwkj1_o69/croot/mkl_random_1695059866750/work
mkl-service==2.4.0
mpmath==1.3.0
munkres==1.1.4
networkx==3.0
numexpr @ file:///C:/b/abs_5fucrty5dc/croot/numexpr_1696515448831/work
numpy @ file:///C:/b/abs_16b2j7ad8n/croot/numpy_and_numpy_base_1704311752418/work/dist/numpy-1.26.3-cp39-cp39-win_amd64.whl#sha256=02e606e23ca31bb00a40d147fd1ce4dd7d241395346a4196592d5abe54a333bc
oauthlib==3.2.2
openpyxl==3.0.10
opt-einsum==3.3.0
packaging @ file:///C:/b/abs_28t5mcoltc/croot/packaging_1693575224052/work
palettable==3.3.3
pandas==1.2.4
pefile @ file:///C:/b/abs_feg_7trsni/croot/pefile_1670877329726/work
Pillow==9.3.0
ply==3.11
pyasn1==0.5.1
pyasn1-modules==0.3.0
pyinstaller @ file:///C:/b/abs_b94gi_3vjm/croot/pyinstaller_1703109616045/work
pyinstaller-hooks-contrib @ file:///C:/b/abs_c2hemrb3nh/croot/pyinstaller-hooks-contrib_1670877320457/work
pyparsing @ file:///C:/Users/BUILDE~1/AppData/Local/Temp/abs_7f_7lba6rl/croots/recipe/pyparsing_1661452540662/work
PyQt5==5.15.10
PyQt5-sip @ file:///C:/b/abs_c0pi2mimq3/croot/pyqt-split_1698769125270/work/pyqt_sip
python-dateutil==2.8.2
pytz==2023.3.post1
pywin32==305.1
pywin32-ctypes @ file:///C:/ci/pywin32-ctypes_1607553594546/work
requests==2.31.0
requests-oauthlib==1.3.1
rfc3986==1.5.0
rsa==4.9
scikit-learn==1.3.2
scipy==1.11.4
seaborn @ file:///C:/b/abs_68ltdkoyoo/croot/seaborn_1673479199997/work
sip @ file:///C:/b/abs_edevan3fce/croot/sip_1698675983372/work
six==1.15.0
sniffio==1.3.0
stylecloud==0.5.2
sympy==1.12
tensorboard==2.15.1
tensorboard-data-server==0.7.2
tensorflow-estimator==2.15.0
tensorflow-gpu==2.6.0
tensorflow-io-gcs-filesystem==0.31.0
termcolor==1.1.0
threadpoolctl==3.2.0
tinycss==0.4
tomli @ file:///C:/Windows/TEMP/abs_ac109f85-a7b3-4b4d-bcfd-52622eceddf0hy332ojo/croots/recipe/tomli_1657175513137/work
torch==2.1.2+cu118
torchaudio==2.1.2+cu118
torchvision==0.16.2+cu118
tornado @ file:///C:/b/abs_0cbrstidzg/croot/tornado_1696937003724/work
translate==3.6.1
typing-extensions==3.7.4.3
tzdata==2023.3
urllib3==2.1.0
Werkzeug==3.0.1
wordcloud @ file:///C:/b/abs_66ccn47hik/croot/wordcloud_1687301655958/work
wrapt==1.12.1
zipp==3.17.0
```

如需配置环境可参考上方文档。

## 运行代码

clone后在clone的文件夹下打开cmd，输入以下代码：

```bash
python
main.py
```

随后根据软件提示使用即可。

## 运行程序

如果有不懂代码的朋友想使用此软件，本软件也贴心的准备好了打包好的程序，只需要前往此链接，下载压缩包后解压根目录下的**橙子的聊天记录分析器**压缩包，进入**橙子的聊天记录分析器**文件夹中启动**橙子的聊天记录分析器.exe**即可。

为了帮助大家使用，其中还包含了大佬的爬取微信聊天记录的软件（留痕），请大家多多支持大佬的工作。

```bash
链接：https://pan.baidu.com/s/1zRRj7sT3snTyQsQFfwD_RA?pwd=0714 
提取码：0714 
--来自百度网盘超级会员V6的分享
```

欢迎大家使用此软件分析聊天记录。

另外为了方便大家爬取解密微信聊天记录在此附上大佬的git仓库，用于爬取数据：

```bash
https://github.com/LC044/WeChatMsg
```

2024.1.20 橙子

>2024.1.25更新
>2024.1.26更新
>2024.1.27更新
>2024.1.30更新
