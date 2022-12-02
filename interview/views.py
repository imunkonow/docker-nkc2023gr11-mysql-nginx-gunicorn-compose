# from types import NoneType  # ryosuke error
import glob
import pandas as pd
import csv
import shutil
import os
from django.core.files.storage import FileSystemStorage
import codecs
from io import StringIO
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.pdfinterp import PDFResourceManager
import japanize_matplotlib
from django.conf import settings
from django_pandas.io import read_frame
import base64
import matplotlib.pyplot as plt
from django.shortcuts import render

try:
    from .import secret
except:
    pass

try:
    import seaborn as sns
except:
    pass
    
# Create your views here.

from django.http import HttpResponse
from .models import DB
from .models import Account

try:
    from . import azurespeech
    import azure.cognitiveservices.speech as speechsdk
except:
    pass

# 9/14

from django.shortcuts import render
from django.views.generic import TemplateView  # テンプレートタグ
from .forms import AccountForm, AddAccountForm  # ユーザーアカウントフォーム
from django.contrib.auth import authenticate
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
# ログイン・ログアウト処理に利用
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required

# 10/5
import json

########################
# 11/1
from django.shortcuts import render
import io
import matplotlib
matplotlib.use('Agg')

try:
    import seaborn as sns
except:
    pass


#######
# 11/2
# 必要なPdfminer.sixモジュールのクラスをインポート

# -*- coding: utf-8 -*-

######

# 11/2

# 11/8
#リアルタイム音声

import time
import re
#リアルタイム音声

# from scipy.io.wavfile import read, write


class utils():
    def __init__(self):
        plt.ion()
        fig = plt.figure(linewidth=1)
        self.fig = fig
        # self.fig.suptitle('subplot(left & right): ax1, ax2')

    def create_graph(self, x_list=None, x_list_only=None, t_list=None, xlabel=None, title=None, allfontsize=12, twobar=None, twobarlabel='全体', bartype=None, legend=None, labelname=None):

        if bartype == '2':
            self.fig.suptitle(f'{title}と欠席リミット比率')
            ax1 = self.fig.add_subplot(1, 2, 1)
            ax2 = self.fig.add_subplot(1, 2, 2)
            self.ax1 = ax1
            self.ax2 = ax2
            # plt.plot(t_list, x_list, label=f'出席番号{labelname}')
            self.ax1.set_title('年間欠席数')
            self.ax1.set_xlabel("日付")
            self.ax1.set_ylabel("日数")
            titleslice = title.find('の')
            # print(twobar)
            if twobar:
                self.ax1.plot(t_list, twobar, label=f'{twobarlabel}')
            ax1.plot(t_list, x_list, label=f'{title[:titleslice]}')
            print('plot')
            self.ax1.legend()
        # elif (bartype == 'pie'):
            # plt.pie(x_list, labels=t_list, counterclock=False)
            ax2.set_title('欠席の内訳')
            # ax2.set_xlabel("x")
            # ax2.set_ylabel("y1")

            # 残り日数
            x_list_only.append(33.4 - float(x_list[-1]))
            # print(x_list_only[-1])

            t_list.append(f'残り日数:\n{round(x_list_only[-1], 2)}日')

            # 円グラフか
            explode = []
            for i in x_list_only:
                explode.append(0)
            explode.pop()
            explode.append(0.1)
            print(explode)
            ax2.pie(x_list_only, labels=t_list, counterclock=False,
                    startangle=90, autopct="%.1f%%",
                    pctdistance=0.7, explode=explode)
            ax2.legend(bbox_to_anchor=(0.8, 1.45), loc='upper left',
                       borderaxespad=0, fontsize=8)
            # , wedgeprops={'linewidth': 3, 'edgecolor': "white"}  # 白い線でわける
        else:
            plt.cla()
            if twobar:
                plt.bar(t_list, twobar, align='edge', width=0.4, label='全体')
                plt.bar(t_list, x_list, align='center',
                        width=0.4, label='あなた')
                plt.legend()
            # plt.rcParams["font.size"] = allfontsize
            else:
                plt.xticks(fontsize=allfontsize)
                plt.title(title, fontsize=18)  #
                plt.xlabel(xlabel)  #
                plt.ylabel('数')  #
                plt.bar(t_list, x_list, align='center', width=0.4, label='全体')
                plt.legend()
                print('twobarelse')
    
    def get_image(self):
        buffer = io.BytesIO()
        if self.fig:
            self.fig.subplots_adjust(wspace=0.1, hspace=0.6)
            self.fig.savefig(buffer, format='png',
                             bbox_inches='tight', pad_inches=0)
            self.fig.savefig(str(settings.MEDIA_ROOT) + "/graph/graph.png", format='png',
                    bbox_inches='tight', pad_inches=0)
        else:
            self.plt.savefig(buffer, format='png')
        image_png = buffer.getvalue()
        graph = base64.b64encode(image_png)
        graph = graph.decode('utf-8')
        buffer.close()
        return graph
                
    def graph(request):
        accounts = Account.objects.all()
        dbs = DB.objects.all()

        users = accounts.all().count()
        contributors = dbs.exclude(Contributor=None).count()
        answers = dbs.exclude(Answer=None).count()
        feedbackers = dbs.exclude(FB=None).count()

        # print("users", users)
        # print("contributors", contributors)
        # print("answers", answers)
        # print("feedbacks", feedbacks)

        x_list = [users, contributors, answers, feedbackers]
        # 総ユーザー数, 総投稿者数, 総回答者数, 総フィードバック者数

        # x_list = [3, 6, 12, 24, 48, 96, 192, 384, 768, 1536, 3072]
        # FBReq = DB.objects.filter(FBReq=request.user)
        # AnswerReq = DB.objects.filter(AnswerReq=request.user)
        # Contributor = DB.objects.filter(Contributor=request.user)
        # WhoAnswers = DB.objects.filter(WhoAnswers=request.user)
        # FBer = DB.objects.filter(FBer=request.user)

        # 質問の数, 総回答数, フィードバック数, 回答リクエスト数, フィードバックリクエスト数

        t_list = ['ユーザー', '投稿', '回答', 'フィードバック']
        title = 'サイト統計'
        utils_graph = utils()
        utils_graph.create_graph(x_list=x_list, t_list=t_list,
                                 xlabel=None, title=title)
        graph = utils_graph.get_image()
        params = {
            "UserID": request.user,
            'graph': graph
        }
        return render(request, 'interview/graph.html', params)
                
class utils2():
    def __init__(self):
        plt.ion()
        fig = plt.figure(linewidth=1)
        self.fig = fig
        # self.fig.suptitle('subplot(left & right): ax1, ax2')

    def create_graph(self, x_list2=None, x_list_only2=None, t_list2=None, xlabel2=None, title2=None, allfontsize2=12, twobar2=None, twobarlabel2='全体', bartype2=None, legend2=None, labelname2=None):


        self.fig.suptitle('CT4の年間累計欠席統計')
        self.fig.tight_layout()
        ax1 = self.fig.add_subplot(2, 2, 1)
        ax2 = self.fig.add_subplot(2, 2, 2)
        ax3 = self.fig.add_subplot(2, 2, 3)
        ax4 = self.fig.add_subplot(2, 2, 4)
        
        self.ax1 = ax1
        self.ax2 = ax2
        self.ax3 = ax3
        self.ax4 = ax4
        # plt.plot(t_list, x_list, label=f'出席番号{labelname}')
        # self.ax1.set_title('年間欠席数')
        # self.ax1.set_xlabel("日付")
        # self.ax1.set_ylabel("日数")
        titleslice = title2.find('の')
        # print(twobar)

        # self.ax1.plot(t_list, twobar)
        # print(t_list2, x_list2)
        
        
        # sns.lineplot(x="出席番号", y="10月年間累計欠席換算", data=x_list2, ax=ax1)
        ax1.scatter(t_list2, x_list2)
        ax1.set_title('散布図')
        ax1.set_xlabel('出席番号')
        ax1.set_ylabel('人数')
        
        # sns.histplot(x_list2, ax=ax2)
        ax2.hist(x_list2)
        self.ax2.set_xlabel("")
        ax2.set_title('ヒストグラム')
        self.ax2.set_xlabel("欠席日数")
        ax2.tick_params(labelbottom=True,
               labelleft=False,
               labelright=False,
               labeltop=False)
        
        # sns.boxplot(x_list2, ax=ax3)
        ax3.boxplot(x_list2)
        ax3.set_title('箱ひげ図')
        ax3.set_ylabel('欠席日数')
        ax3.set_xlabel('欠席日数情報')
        self.ax3.set_xticklabels(['CT4'])
        self.ax3.set_xticks([1])
        
        
        # sns.barplot(x=t_list2, y="10月年間累計欠席換算", data=x_list2, ax=ax4)

        ax4.violinplot(x_list2)
        ax4.set_title('バイオリンプロット')
        ax4.set_xlabel('欠席日数ボリュームゾーン')
        self.ax4.set_xticklabels(['CT4'])
        self.ax4.set_xticks([1])
        ax4.tick_params(labelbottom=True,
               labelleft=False,
               labelright=False,
               labeltop=False)
        
        # # メモリ線
        # ax.tick_params(bottom=False,
        #        left=False,
        #        right=False,
        #        top=False)
        
        
        # ax2.pie(x_list_only2, labels=t_list2, counterclock=False,
        #         startangle=90, autopct="%.1f%%",
        #         pctdistance=0.7, explode=[0, 0, 0, 0, 0, 0.1])
        # ax2.legend(bbox_to_anchor=(0.8, 1.45), loc='upper left',
        #             borderaxespad=0, fontsize=8)
            # , wedgeprops={'linewidth': 3, 'edgecolor': "white"}  # 白い線でわける

        
        # self.ax1.cla()
        # plt.rcParams["font.size"] = allfontsize
        # self.ax1.xticks(fontsize=allfontsize)
        # self.ax1.title(title, fontsize=18)  #

            # ax1.xlabel(xlabel)  #
            # ax1.ylabel('数')  #
            # ax1.legend()

    def get_image(self):
        buffer = io.BytesIO()
        if self.fig:
            self.fig.subplots_adjust(wspace=0.1, hspace=0.5)
            self.fig.savefig(buffer, format='png', pad_inches=0)
        else:
            self.plt.savefig(buffer, format='png')
        image_png = buffer.getvalue()
        graph = base64.b64encode(image_png)
        graph = graph.decode('utf-8')
        buffer.close()
        return graph
############################


#########################
# 11/1
class dfutil():
    def getcsv():
        qs = DB.objects.all()
        # dbを全取得

        # dbをdf(表)化
        # df = read_frame(qs)
        df = read_frame(qs, fieldnames=['Question', 'Answer', 'Memo', 'FB',
                        'Contributor', 'WhoAnswers', 'FBer', 'Genre', 'AnswerReq', 'FBReq'])

        # 元フォルダの削除と新規作成
        csvpwd = str(settings.MEDIA_ROOT) + "/csv"
        try:
            shutil.rmtree(csvpwd)
            print(f'{csvpwd}削除しました')
        except:
            print(f'{csvpwd}削除不可。')
        os.makedirs(csvpwd, exist_ok=True)

        # pathとファイル名の指定
        exp_path = str(settings.MEDIA_ROOT) + "/csv/mensetu.csv"

        # 保存場所とエンコーディング、インデックスの有無の指定
        df.to_csv(exp_path, encoding='cp932', index=None)  # , index=False
        return df


def csvDLUP(request):
    pandas = dfutil
    params = {
        "UserID": request.user,
        "accounts": Account.objects.all()
    }

    if request.method == 'POST':
        print("print", request.FILES)
        myfile = request.FILES['testfile']

        # もともとあったファイルを削除
        try:
            os.remove(str(settings.MEDIA_ROOT) + f"/csv/{myfile}")
            print("csv元ファイル削除")
        except:
            print('csvmyfile', (str(settings.MEDIA_ROOT) + f"/csv/{myfile}"))
            print('csv削除不可')

        print('myfile', myfile)
        fs = FileSystemStorage()
        filename = fs.save(str(settings.MEDIA_ROOT) + f"/csv/{myfile}", myfile)
        # uploaded_file_url = fs.url(filename)
        # params['uploaded_file_url'] = uploaded_file_url
        # pdftext = pdf_read_class
        # text = pdftext.pdf_to_text(myfile)
        with open(str(settings.MEDIA_ROOT) + f"/csv/{myfile}", encoding='cp932', newline='') as f:
            csvreader = csv.reader(f)
            i = 0
            for row in csvreader:
                postDB = DB
                if i > 0:
                    try:
                        for rowNum, Nonerow in enumerate(row):
                            if Nonerow == "":
                                row[rowNum] = None
                        postDB = postDB(Question=row[0], Answer=row[1], Memo=row[2], FB=row[3], Contributor=row[4],
                                        WhoAnswers=row[5], FBer=row[6], Genre=row[7], AnswerReq=row[8], FBReq=row[9])
                        postDB.save()
                    except:
                        print('csvのDB保存失敗')
                # print(row)
                i += 1

    df = pandas.getcsv()
    params["df"] = df.to_html()
    return render(request, "interview/csvDLUP.html", params)
#########################

#################
# 11/2


class pdf_read_class():
    def pdf_to_text(myfile):
        # PDFファイルを読込んで、Pythonのコンソールに出力する
        # 標準組込み関数open()でモード指定をbinaryでFileオブジェクトを取得
        # myfile = 'sample.pdf' # myfile[0:-3]
        fp = open(str(settings.MEDIA_ROOT) + f"/pdf/{myfile}", 'rb')

        # 出力先をPythonコンソールするためにIOストリームを取得
        outfp = StringIO()

        # 各種テキスト抽出に必要なPdfminer.sixのオブジェクトを取得する処理

        rmgr = PDFResourceManager()  # PDFResourceManagerオブジェクトの取得
        lprms = LAParams()          # LAParamsオブジェクトの取得
        # TextConverterオブジェクトの取得
        device = TextConverter(rmgr, outfp, laparams=lprms)
        iprtr = PDFPageInterpreter(rmgr, device)  # PDFPageInterpreterオブジェクトの取得

        # PDFファイルから1ページずつ解析(テキスト抽出)処理する
        for page in PDFPage.get_pages(fp):
            iprtr.process_page(page)

        text = outfp.getvalue()  # Pythonコンソールへの出力内容を取得

        outfp.close()  # I/Oストリームを閉じる
        device.close()  # TextConverterオブジェクトの解放
        fp.close()  # Fileストリームを閉じる

        return text

    def pdf_read(request):
        params = {
            "UserID": request.user
        }
        filename = ""
        params["textpath"] = ""

        # 元フォルダの削除と新規作成
        pdfpwd = str(settings.MEDIA_ROOT) + "/pdf"
        try:
            shutil.rmtree(pdfpwd)
            print(f'{pdfpwd}削除しました。')
        except:
            print(f'{pdfpwd}削除不可')
        os.makedirs(pdfpwd, exist_ok=True)

        if request.method == 'POST':
            print("print", request.FILES)
            myfile = request.FILES['testfile']

            # もともとあったファイルを削除
            try:
                os.remove(str(settings.MEDIA_ROOT) + f"/pdf/{myfile}")
                print("元ファイル削除")
            except:
                print('削除不可')

            print('myfile', myfile)
            fs = FileSystemStorage()
            filename = fs.save(str(settings.MEDIA_ROOT) +
                               f"/pdf/{myfile}", myfile)
            uploaded_file_url = fs.url(filename)
            params['uploaded_file_url'] = uploaded_file_url
            pdftext = pdf_read_class
            text = pdftext.pdf_to_text(myfile)

            # ファイル書き込み
            originalfilename = str(myfile)
            myfile = str(myfile)[0:-4]
            with codecs.open(str(settings.MEDIA_ROOT) + f"/text/{myfile}" + ".text", 'w', 'utf-8') as f:
                f.write(text)
                print('myfile', myfile)

            params["textpath"] = f"text/{myfile}.text"
            params["pdfpath"] = f"pdf/{myfile}.pdf"
            params["texthtml"] = text
            params["upload"] = originalfilename
            params["totext"] = originalfilename[0:-3] + 'text'

        print(params["textpath"])
        return render(request, "interview/pdf_read.html", params)

###################
# 11/4


def attend(request):
    pandas = dfutil
    params = {
        "UserID": request.user,
        "accounts": Account.objects.all()
    }

    if request.method == 'POST':
        attendNum = int(request.POST.get("attendNum", ""))
    else:
        attendNum = 21

    df = pd.read_csv(
        f'{str(settings.MEDIA_ROOT)}/.secretcsv/.all.csv', encoding='cp932', index_col='出席番号')
    dfstd = pd.read_csv(
        f'{str(settings.MEDIA_ROOT)}/.secretcsv/.all.csv', encoding='cp932')
    df = df.drop('氏名', axis=1)
    # params["allcsv"] = df.to_html(na_rep='')

    # attendNum = 29
    df11 = df.loc[attendNum]
    # print(df11)
    
    # !変更箇所
    df11 = df11.loc[['4月年間累計欠席換算', '5月年間累計欠席換算', '6月年間累計欠席換算',
                     '7月年間累計欠席換算', '9月年間累計欠席換算', '10月年間累計欠席換算', '11月年間累計欠席換算']]
    # print(df11)

    # print('4月', df11.iloc[0]['10月年間累計欠席換算'])

    # !変更箇所
    x_list = [df11['4月年間累計欠席換算'], df11['5月年間累計欠席換算'], df11['6月年間累計欠席換算'],
              df11['7月年間累計欠席換算'], df11['9月年間累計欠席換算'],
              df11['10月年間累計欠席換算'], df11['11月年間累計欠席換算']]

    # !変更箇所
    x_list_only = [x_list[0], x_list[1] - x_list[0], x_list[2] - x_list[1],
                   x_list[3] - x_list[2], x_list[4] - x_list[3],
                   x_list[5] - x_list[4], x_list[6] - x_list[5]]
    
    # !変更箇所
    # 統計 偏差値
    dfonly = dfstd.loc[:,['出席番号', '11月年間累計欠席換算']]
    dfonlynum = dfonly.loc[:, dfonly.columns[0]]
    dfonly10 = dfonly.loc[:, [dfonly.columns[0], dfonly.columns[-1]]]
    dfonly10 = dfonly10.set_index('出席番号')
    attendValue = float(dfonly10.loc[attendNum].values)
    hensachi = (attendValue - dfonly10.mean(numeric_only=True))/dfonly10.std(numeric_only=True)*10+50

    # !変更箇所
    print('偏差値', hensachi.loc['11月年間累計欠席換算'])
    params['偏差値'] = round(hensachi.loc['11月年間累計欠席換算'], 2)

    # champion
    dfchamp = df.copy()
    dfchamp = dfchamp.sort_values([df.columns[-1]], ascending=[False])
    totalColumns = len(df)
    dfchamponly = dfchamp.iloc[:, 6:totalColumns-1:7]
    params["allcsv"] = dfchamponly.to_html(na_rep='')

    # !変更箇所
    dfchamponlyGraph = dfchamponly.copy()
    dfchamponlyGraph = dfchamponlyGraph[:1]
    twobar = [dfchamponlyGraph['4月年間累計欠席換算'], dfchamponlyGraph['5月年間累計欠席換算'], dfchamponlyGraph['6月年間累計欠席換算'],
              dfchamponlyGraph['7月年間累計欠席換算'], dfchamponlyGraph['9月年間累計欠席換算'],
              dfchamponlyGraph['10月年間累計欠席換算'], dfchamponlyGraph['11月年間累計欠席換算']]
    # print(dfchamp)

    # !変更箇所
    t_list = ['4月', '5月', '6月',
              '7月', '9月', '10月', '11月']
    
    twobarlabel = f'{t_list[-1]}のチャンピオン'

    title = f'出席番号{attendNum}の年間累計欠席日数'

    # 線グラフ
    utils1 = utils()
    utils1.create_graph(x_list=x_list, x_list_only=x_list_only, t_list=t_list, xlabel=None,
                        title=title, allfontsize=8, bartype='2', labelname=attendNum, twobar=twobar, twobarlabel=twobarlabel)
    # graph = utils.get_image()

    # params["graph"] = graph

    # # # 円グラフ
    # utils1.create_graph(x_list, t_list, xlabel=None,
    #                     title=title, allfontsize=8, bartype='pie', labelname=attendNum)
    # piegraph = utils.get_image()

    # params["piegraph"] = piegraph

    graph = utils1.get_image()

    params["graph"] = graph

    params['attendNums'] = list(range(1, 60))
    params['出席番号'] = attendNum
    
    # !変更箇所
    dfonly = dfstd.loc[:,['出席番号', '11月年間累計欠席換算']]
    
    x_list2 = dfonly.loc[:, [dfonly.columns[0], dfonly.columns[-1]]]
    x_list2 = dfonly.set_index('出席番号')
    
    params['describe'] = x_list2.describe().to_html
    
    t_list2 = dfonly.loc[:, dfonly.columns[0]]
    
    utilstoukei = utils2()
    utilstoukei.create_graph(x_list2=x_list2, x_list_only2=x_list_only, t_list2=t_list2, xlabel2=None,
                    title2=title, allfontsize2=8, bartype2='2', labelname2=attendNum, twobar2=twobar, twobarlabel2=twobarlabel)
    graph2 = utilstoukei.get_image()
    params["graph2"] = graph2
    return render(request, "interview/attend.html", context=params)


def allinput(request):
    postDB = DB
    params = {
        "UserID": request.user
    }
    if request.method == 'POST':
        Question = request.POST.get("Question", "")
        Answer = request.POST.get("Answer", "")
        Memo = request.POST.get("Memo", "")
        FB = request.POST.get("FB", "")
        Contributor = request.POST.get("Contributor", "")
        WhoAnswers = request.POST.get("WhoAnswers", "")
        FBer = request.POST.get("FBer", "")
        Genre = request.POST.get("contact", "")
        AnswerReq = request.POST.get("AnswerReq", "")
        FBReq = request.POST.get("FBReq", "")
        postDB = postDB(Question=Question, Answer=Answer, Memo=Memo, FB=FB, Contributor=Contributor,
                        WhoAnswers=WhoAnswers, FBer=FBer, Genre=Genre, AnswerReq=AnswerReq, FBReq=FBReq)
        postDB.save()

    return render(request, "interview/allinput.html", context=params)


def answer_let(request, question_id="1"):
    postDB = DB
    account = Account.objects.all()
    ctx = {}
    ctx["accounts"] = account
    ctx["UserID"] = request.user
    if request.method == 'POST':
        if request.POST.get("ans", ""):
            question = request.POST.get("question", "")
            ans = request.POST.get("ans", "")
            if request.POST.get("fbreq", ""):
                fbreq = request.POST.get("fbreq", "")
            else:
                fbreq = None
            if request.POST.get("memo", ""):
                memo = request.POST.get("memo", "")
            else:
                memo = None

            postDB = postDB(Question=question, Answer=ans, Memo=memo, WhoAnswers=request.user,
                            FBReq=fbreq)
            postDB.save()

        qs = DB.objects.all()
        # try:
        #     t = DB.objects.get(id=question_id)
        #     t.delete()
        # except:
        #     print("削除に失敗")

        ctx["object_list"] = qs

        ctx["index"] = question_id
        ctx["question_id"] = question_id

        # try:
        #     azurespeech.main(qs[0].Question)
        # except:
        #     print('音声出力のエラー')

        ctx["key"] = secret.subscription
        return render(request, "interview/answer_let.html", ctx)

    else:
        qs = DB.objects.all()
        ctx["object_list"] = qs
        ctx["question_id"] = question_id
    return render(request, "interview/answer_let.html", ctx)


def feedback_only(request, question_id="1"):
    postDB = DB
    account = Account.objects.all()
    ctx = {}
    ctx["accounts"] = account
    ctx["UserID"] = request.user
    if request.method == 'POST':
        question = request.POST.get("question", "")
        ans = request.POST.get("ans", "")
        fbreq = request.POST.get("fbreq", "")

        if fbreq:
            postDB = postDB(Question=question, Answer=ans,
                            FBer=request.user)
            postDB.save()

        qs = DB.objects.all()
        # try:
        #     t = DB.objects.get(id=question_id)
        #     t.delete()
        # except:
        #     print("削除に失敗")

        ctx["object_list"] = qs

        ctx["index"] = question_id
        ctx["question_id"] = question_id

        question = request.GET.get("question", "")

        # try:
        #     azurespeech.main(qs[0].Question)
        # except:
        #     print('音声出力のエラー')

        ctx["key"] = secret.subscription
        return render(request, "interview/feedback_only.html", ctx)

    else:
        qs = DB.objects.all()
        ctx["object_list"] = qs
        ctx["question_id"] = question_id
    return render(request, "interview/feedback_only.html", ctx)
######

# index


def index(request):
    return HttpResponseRedirect(reverse('question_Main'))

# ホーム


def question_Main(request):
    qs = DB.objects.filter(Answer=None).order_by("?").first()
    params = {"UserID": request.user, "object_list": qs}
    accounts = Account.objects.all()
    dbs = DB.objects.all()

    users = accounts.all().count()
    contributors = dbs.exclude(Contributor=None).count()
    answers = dbs.exclude(Answer=None).count()
    feedbackers = dbs.exclude(FB=None).count()

    # print("users", users)
    # print("contributors", contributors)
    # print("answers", answers)
    # print("feedbacks", feedbacks)

    x_list = [users, contributors, answers, feedbackers]
    # 総ユーザー数, 総投稿者数, 総回答者数, 総フィードバック者数

    # x_list = [3, 6, 12, 24, 48, 96, 192, 384, 768, 1536, 3072]
    # FBReq = DB.objects.filter(FBReq=request.user)
    # AnswerReq = DB.objects.filter(AnswerReq=request.user)
    # Contributor = DB.objects.filter(Contributor=request.user)
    # WhoAnswers = DB.objects.filter(WhoAnswers=request.user)
    # FBer = DB.objects.filter(FBer=request.user)

    # 質問の数, 総回答数, フィードバック数, 回答リクエスト数, フィードバックリクエスト数

    t_list = ['ユーザー', '投稿', '回答', 'フィードバック']
    # xlabel = '総ユーザー数, 総投稿者数, 総回答者数, 総フィードバック者数'
    title = 'サイト統計'

    utils_questionMain = utils()
    utils_questionMain.create_graph(
        x_list=x_list, t_list=t_list, xlabel=None, title=title)
    graph = utils_questionMain.get_image()
    params["graph"] = graph

    return render(request, "interview/question_Main.html", context=params)
    # else:
    #     ctx = {}
    #     params = {"UserID":request.user,}
    #     ctx["UserID"] = params
    #     qs = DB.objects.all()
    #     ctx["object_list"] = qs
    #     ctx["key"] = secret.subscription
    #     text = request.POST.get("text", "")

    #     return render(request, "interview/question_Main.html", ctx)


def mensetu_Main(request):
    template_name = "interview/mensetu_Main.html"
    return render(request, "interview/mensetu_Main.html")


def answer_List(request):
    template_name = "interview/answer_List.html"

    ctx = {
        "UserID": request.user
    }
    qs = DB.objects.all()
    ctx["object_list"] = qs
    return render(request, "interview/answer_List.html", ctx)


def question(request):
    template_name = "interview/question.html"
    postDB = DB
    accountDB = Account
    params = {
        "UserID": request.user
    }
    params["accounts"] = accountDB.objects.all()

    if request.method == 'POST':
        question = request.POST.get("q", "")
        if request.POST.get("AR", ""):
            AR = request.POST.get("AR", "")
        else:
            AR = None

        if request.POST.get("contact", ""):
            genre = request.POST.get("contact", "")
        else:
            genre = None

        if question:
            postDB = postDB(Question=question, AnswerReq=AR,
                            Contributor=request.user, Genre=genre)
            postDB.save()
        return render(request, "interview/question.html", params)

    else:
        return render(request, "interview/question.html", params)
    # return render(request, "interview/question.html", dic)


def question_List(request):
    ctx = {
        "UserID": request.user
    }
    if request.method == 'POST':
        if request.POST.get("Genre", "") == "all":
            qs = DB.objects.filter(Answer=None)
        else:
            Genre = request.POST.get("Genre", "")
            qs = DB.objects.filter(Answer=None, Genre=Genre)

        ctx["object_list"] = qs
        return render(request, "interview/question_List.html", ctx)
    else:
        qs = DB.objects.filter(Answer=None)

        ctx["object_list"] = qs
        return render(request, "interview/question_List.html", ctx)


def feedback_List(request):
    ctx = {
        "UserID": request.user
    }
    qs = DB.objects.all()
    ctx["object_list"] = qs
    return render(request, "interview/feedback_List.html", ctx)


def feedback_yet(request):
    ctx = {
        "UserID": request.user
    }
    qs = DB.objects.filter(FB=None,)
    ctx["object_list"] = qs
    return render(request, "interview/feedback_yet.html", ctx)


def feedback(request):
    ctx = {
        "UserID": request.user
    }
    qs = DB.objects.filter(FB=None, Contributor=None)
    ctx["object_list"] = qs
    return render(request, "interview/feedback.html", ctx)


def feedback_let(request, question_id="1"):
    template_name = "interview/feedback_let.html"
    postDB = DB
    ctx = {
        "UserID": request.user
    }
    if request.method == 'POST':
        question = request.POST.get("question", "")
        ans = request.POST.get("ans", "")
        feedback = request.POST.get("feedback", "")
        if request.POST.get("memo", ""):
            memo = request.POST.get("memo", "")
        else:
            memo = None

        if feedback:
            postDB = postDB(Question=question, Answer=ans, Memo=memo,
                            FB=feedback, FBer=request.user)
            postDB.save()

        qs = DB.objects.all()
        # try:
        #     t = DB.objects.get(id=question_id)
        #     t.delete()
        # except:
        #     print("削除に失敗")

        ctx["object_list"] = qs

        ctx["index"] = question_id
        ctx["question_id"] = question_id

        question = request.GET.get("question", "")

        # try:
        #     azurespeech.main(qs[0].Question)
        # except:
        #     print('音声出力のエラー')

        ctx["key"] = secret.subscription
        return render(request, "interview/feedback_let.html", ctx)

    else:
        question = request.GET.get("question", "")
        ans = request.GET.get("ans", "")
        memo = request.GET.get("memo", "")
        feedback = request.POST.get("feedback", "")

        qs = DB.objects.all()
        ctx["object_list"] = qs
        ctx["question_id"] = question_id
        ctx["key"] = secret.subscription
        return render(request, "interview/feedback_let.html", ctx)


def question_yet(request):
    ctx = {
        "UserID": request.user
    }
    qs = DB.objects.all()
    ctx["object_list"] = qs
    return render(request, "interview/question_yet.html", ctx)


def mensetu(request, question_id="1"):
    template_name = "interview/mensetu.html"
    postDB = DB
    accountDB = Account
    ctx = {
        "UserID": request.user
    }
    ctx["accounts"] = accountDB.objects.all()

    if request.method == 'POST':
        myfile = None
        try:
            myfile = request.FILES['testfile']
        except:
            None
            
        if myfile:
            print("print", request.FILES)
            myfile = request.FILES['testfile']

            # もともとあったファイルを削除
            try:
                os.remove(str(settings.MEDIA_ROOT) + f"/sound/{myfile}")
                print("音声元ファイル削除")
            except:
                print('音声myfile', (str(settings.MEDIA_ROOT) + f"/sound/{myfile}"))
                print('音声削除不可')

            print('myfile', myfile)
            fs = FileSystemStorage()
            filenamesave = fs.save(str(settings.MEDIA_ROOT) + f"/sound/{myfile}", myfile)
            
                    # This example requires environment variables named "SPEECH_KEY" and "SPEECH_REGION"
            speech_config = speechsdk.SpeechConfig(secret.subscription, 'japanwest')
            speech_config.speech_recognition_language="ja-JP"

            audio_config = speechsdk.audio.AudioConfig(filename=f'{str(settings.MEDIA_ROOT)}/sound/{myfile}')
            speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

            print("Speak into your microphone.")
            speech_recognition_result = speech_recognizer.recognize_once_async().get()

            if speech_recognition_result.reason == speechsdk.ResultReason.RecognizedSpeech:
                print("Recognized: {}".format(speech_recognition_result.text))
            elif speech_recognition_result.reason == speechsdk.ResultReason.NoMatch:
                print("No speech could be recognized: {}".format(speech_recognition_result.no_match_details))
            elif speech_recognition_result.reason == speechsdk.ResultReason.Canceled:
                cancellation_details = speech_recognition_result.cancellation_details
                print("Speech Recognition canceled: {}".format(cancellation_details.reason))
                if cancellation_details.reason == speechsdk.CancellationReason.Error:
                    print("Error details: {}".format(cancellation_details.error_details))
                    print("Did you set the speech resource key and region values?")
            id = request.POST.get("qestionid", "")
            qs = DB.objects.filter(id=id).first()  
            print('myfile')
            print(secret.subscription)
            ctx['myfile'] = str(myfile)
        else:
            genre = request.POST.get("contact", "")
            print(genre)
            if genre != 'random':
                qs = DB.objects.filter(
                    Answer=None, Genre=f'{genre}').order_by("?").first()
            elif genre == 'random':
                qs = DB.objects.filter(
                    Answer=None).order_by("?").first()
            else:
                qs = DB.objects.filter(
                    Answer=None).order_by("?").first()  
            print('else')
            
        genre = request.POST.get("contact", "")
        question = request.POST.get("question", "")
        ans = request.POST.get("ans", "")
        if request.POST.get("memo", ""):
            memo = request.POST.get("memo", "")
        else:
            memo = None
        if request.POST.get("fbreq", ""):
            fbreq = request.POST.get("fbreq", "")
        else:
            fbreq = None

        print(memo, fbreq)
        if ans:
            postDB = postDB(Question=question, Answer=ans,
                            Memo=memo, FBReq=fbreq, WhoAnswers=request.user)
            print(postDB.id)
            postDB.save()



        ctx["object_list"] = qs

        ctx["index"] = question_id
        ctx["question_id"] = question_id

        question = request.GET.get("question", "")

        # try:
        #     azurespeech.main(qs[0].Question)
        # except:
        #     print('音声出力のエラー')

        ctx["key"] = secret.subscription
        ctx['nextgenre'] = genre
        print(genre)
        
                #リアルタイム音声
        # while(1):
        #     azurespeech.sub()
        
        if myfile:
            ctx['soundtext'] = speech_recognition_result.text
        
        ctx['qs'] = qs
        print(qs.id)
        return render(request, "interview/mensetu.html", ctx)

    else:
        qs = DB.objects.filter(id=question_id).first()
        # qs = DB.objects.filter(Answer="", Memo="").order_by("?")
        # qs = DB.objects.filter(Answer="", Memo="").order_by("?").first()
        # qs = DB.objects.all()
        print(qs)

        ctx["object_list"] = qs
        ctx["question_id"] = question_id
        ctx["key"] = secret.subscription
        
        return render(request, "interview/mensetu.html", ctx)


def hensyu(request):
    template_name = "interview/hensyu.html"
    ctx = {
        "UserID": request.user
    }
    qs = DB.objects.filter(Answer=None)
    ctx["object_list"] = qs
    return render(request, "interview/hensyu.html", ctx)


def hensyu_tuika(request):
    template_name = "interview/hensyu_tuika.html"
    ctx = {
        "UserID": request.user
    }
    qs = DB.objects.all()
    ctx["object_list"] = qs
    return render(request, "interview/hensyu_tuika.html", ctx)

# 6/27

# def login(request):
#     template_name = "interview/login.html"
#     ctx = {}
#     qs = DB.objects.all()
#     ctx["object_list"] = qs
#     return render(request, "interview/login.html", ctx)

# def login_Main(request):
#     template_name = "interview/login_Main.html"
#     ctx = {}
#     qs = DB.objects.all()
#     ctx["object_list"] = qs
#     return render(request, "interview/login_Main.html", ctx)

# def account_create(request):
#     template_name = "interview/account_create.html"
#     ctx = {}
#     qs = DB.objects.all()
#     ctx["object_list"] = qs
#     return render(request, "interview/account_create.html", ctx)


def update(request, question_id="1"):
    postDB = DB
    accountDB = Account
    ctx = {
        "UserID": request.user
    }
    ctx["accounts"] = accountDB.objects.all()
    if request.method == 'POST':
        question = request.POST.get("question", "")

        postDB = DB.objects.get(id=question_id)

        postDB.Question = question
        if request.POST.get("AR", ""):
            postDB.AnswerReq = request.POST.get("AR", "")
        else:
            postDB.AnswerReq = None
        postDB.save()

        qs = DB.objects.all()
        ctx["object_list"] = qs

        ctx["index"] = question_id
        ctx["question_id"] = question_id
        return render(request, "interview/hensyu.html", ctx)

    else:

        question = request.GET.get("question", "")
        ans = request.GET.get("ans", "")
        memo = request.GET.get("memo", "")

        qs = DB.objects.all()
        ctx["object_list"] = qs
        ctx["index"] = question_id
        ctx["question_id"] = question_id
    return render(request, "interview/update.html", ctx)


def delete(request, question_id="1"):
    postDB = DB
    ctx = {
        "UserID": request.user
    }
    if request.method == 'POST':
        postDB = DB.objects.get(id=question_id)
        postDB.delete()

        qs = DB.objects.all()
        ctx["object_list"] = qs

        ctx["index"] = question_id
        ctx["question_id"] = question_id
        return render(request, "interview/hensyu.html", ctx)

    else:

        question = request.GET.get("question", "")
        ans = request.GET.get("ans", "")
        memo = request.GET.get("memo", "")

        qs = DB.objects.all()
        ctx["object_list"] = qs
        ctx["index"] = question_id
        ctx["question_id"] = question_id
    return render(request, "interview/delete.html", ctx)

# 9/14
# ログイン


def Login(request):
    # POST
    if request.method == 'POST':
        # フォーム入力のユーザーID・パスワード取得
        ID = request.POST.get('userid')
        Pass = request.POST.get('password')

        # Djangoの認証機能
        user = authenticate(username=ID, password=Pass)

        # ユーザー認証
        if user:
            # ユーザーアクティベート判定
            if user.is_active:
                # ログイン
                login(request, user)
                # ホームページ遷移
                return HttpResponseRedirect(reverse('question_Main'))
            else:
                # アカウント利用不可
                return HttpResponse("アカウントが有効ではありません")
        # ユーザー認証失敗
        else:
            return HttpResponse("ログインIDまたはパスワードが間違っています<br><a href='/'>戻る</a>")
    # GET
    else:
        return render(request, 'interview/login.html')


# ログアウト
@ login_required
def Logout(request):
    logout(request)
    # ログイン画面遷移
    return HttpResponseRedirect(reverse('Login'))

# 新規登録


class AccountRegistration(TemplateView):

    def __init__(self):
        self.params = {
            "AccountCreate": False,
            "account_form": AccountForm(),
            "add_account_form": AddAccountForm(),
        }

    # Get処理
    def get(self, request):
        self.params["account_form"] = AccountForm()
        self.params["add_account_form"] = AddAccountForm()
        self.params["AccountCreate"] = False
        return render(request, "interview/register.html", context=self.params)

    # Post処理
    def post(self, request):
        self.params["account_form"] = AccountForm(data=request.POST)
        self.params["add_account_form"] = AddAccountForm(data=request.POST)

        # フォーム入力の有効検証
        if self.params["account_form"].is_valid() and self.params["add_account_form"].is_valid():
            # アカウント情報をDB保存
            account = self.params["account_form"].save()
            # パスワードをハッシュ化
            account.set_password(account.password)
            # ハッシュ化パスワード更新
            account.save()

            # 下記追加情報
            # 下記操作のため、コミットなし
            add_account = self.params["add_account_form"].save(commit=False)
            # AccountForm & AddAccountForm 1vs1 紐付け
            add_account.user = account

            # 画像アップロード有無検証
            if 'account_image' in request.FILES:
                add_account.account_image = request.FILES['account_image']

            # モデル保存
            add_account.save()

            # アカウント作成情報更新
            self.params["AccountCreate"] = True

        else:
            # フォームが有効でない場合
            print(self.params["account_form"].errors)

        return render(request, "interview/register.html", context=self.params)


class profile(TemplateView):
    def __init__(self):
        self.params = {
            "AccountCreate": False,
            "account_form": AccountForm(),
            "add_account_form": AddAccountForm(),
        }

    # Get処理
    def get(self, request):
        # self.params["account_form"] = AccountForm()
        # self.params["add_account_form"] = AddAccountForm()
        # self.params["AccountCreate"] = False

        account = Account.objects.filter(user=request.user).first()
        print(account)
        print(request.GET.get("changefirst", ""))

        # lastN = account.objects.all()
        imagepath = str(account.account_image)
        print(imagepath.find('account_image'))
        imagepath = imagepath[int(imagepath.find('account_image')):]
        print('imagepath', imagepath)
        params = {"UserID": request.user,
                  "last_name": account.last_name,
                  "first_name": account.first_name,
                  "account": account,
                  "email": account,
                  "filename": imagepath,
                  }
        return render(request, "interview/profile.html", params)

    # Post処理
    def post(self, request):
        account = Account.objects.filter(user=request.user).first()
        print(account)
        print(request.GET.get("changefirst", ""))

        # lastN = account.objects.all()

        params = {"UserID": request.user,
                  }
        imagepath = str(account.account_image)
        print(imagepath.find('account_image'))
        imagepath = imagepath[int(imagepath.find('account_image')):]
        # プロフィール変更
        print("print", request.FILES)
        myfile = "画像なし"
        params['filename'] = account.account_image
        filepath = imagepath
        filename = imagepath
        print('filename', filename)
        if request.FILES:
            myfile = request.FILES['testfile']

            # もともとあったファイルを削除
            try:
                os.remove(str(settings.MEDIA_ROOT) +
                          f"/account_image/{myfile}")
                print("元ファイル削除")
            except:
                print('削除不可')

            print('myfile', myfile)
            fs = FileSystemStorage()
            filepath = str(settings.MEDIA_ROOT) + f"/account_image/{myfile}"
            filename = fs.save(filepath, myfile)
        params['filename'] = str(filename)

        postDB = Account.objects.get(user=request.user)
        print('postDB', postDB)
        print('type', type(postDB))

        if request.POST.get("last_name", ""):
            postDB.last_name = request.POST.get("last_name", "")
        if request.POST.get("first_name", ""):
            postDB.first_name = request.POST.get("first_name", "")
        postDB.account_image = filepath
        postDB.save()

        params['last_name'] = postDB.last_name
        params['first_name'] = postDB.first_name
        return render(request, "interview/profile.html", params)


class mail(TemplateView):

    def __init__(self):
        self.params = {
            "AccountCreate": False,
            "account_form": AccountForm(),
            "add_account_form": AddAccountForm(),
        }

    # Get処理
    def get(self, request):
        # self.params["account_form"] = AccountForm()
        # self.params["add_account_form"] = AddAccountForm()
        # self.params["AccountCreate"] = False

        account = Account.objects.filter(user=request.user).first()
        print(account)
        # lastN = account.objects.all()
        FBReq = DB.objects.filter(FBReq=request.user)
        AnswerReq = DB.objects.filter(AnswerReq=request.user)
        Contributor = DB.objects.filter(Contributor=request.user)
        WhoAnswers = DB.objects.filter(WhoAnswers=request.user)
        FBer = DB.objects.filter(FBer=request.user)

        params = {"UserID": request.user,
                  "last_name": account,
                  "first_name": account,
                  "account": account,
                  "FBReq": FBReq,
                  "AnswerReq": AnswerReq,
                  "Contributor": Contributor,
                  "WhoAnswers": WhoAnswers,
                  "FBer": FBer,
                  }

        # 11/1
        accounts = Account.objects.all()
        dbs = DB.objects.all()

        ContributorCount = Contributor.count()
        WhoAnswersCount = WhoAnswers.count()
        FBerCount = FBer.count()
        AnswerReqCount = AnswerReq.count()
        FBReqCount = FBReq.count()

        # print("users", users)
        # print("contributors", contributors)
        # print("answers", answers)
        # print("feedbacks", feedbacks)

        x_list = [ContributorCount, WhoAnswersCount,
                  FBerCount, AnswerReqCount, FBReqCount]
        print('mailxlist', x_list)
        # 総ユーザー数, 総投稿者数, 総回答者数, 総フィードバック者数

        # x_list = [3, 6, 12, 24, 48, 96, 192, 384, 768, 1536, 3072]
        # FBReq = DB.objects.filter(FBReq=request.user)
        # AnswerReq = DB.objects.filter(AnswerReq=request.user)
        # Contributor = DB.objects.filter(Contributor=request.user)
        # WhoAnswers = DB.objects.filter(WhoAnswers=request.user)
        # FBer = DB.objects.filter(FBer=request.user)

        # 質問の数, 総回答数, フィードバック数, 回答リクエスト数, フィードバックリクエスト数

        t_list = ['質問', '回答', 'フィードバック', '回答リクエスト', 'FBリクエスト']
        title = 'あなたのステータス'

        # 全体DB
        AContributorCount = dbs.exclude(Contributor=None).count()
        AWhoAnswersCount = dbs.exclude(WhoAnswers=None).count()
        AFBerCount = dbs.exclude(FBer=None).count()
        AAnswerReqCount = dbs.exclude(AnswerReq=None).count()
        AFBReqCount = dbs.exclude(FBReq=None).count()

        twobar = [AContributorCount, AWhoAnswersCount,
                  AFBerCount, AAnswerReqCount, AFBReqCount]
        utils_mail = utils()
        utils_mail.create_graph(x_list=x_list, t_list=t_list, xlabel=None,
                                title=title, allfontsize=8, twobar=twobar,)
        graph = utils_mail.get_image()

        params["graph"] = graph
        return render(request, "interview/mail.html", params)

    # #Post処理
    # def post(self,request):
    #     self.params["account_form"] = AccountForm(data=request.POST)
    #     self.params["add_account_form"] = AddAccountForm(data=request.POST)

    #     #フォーム入力の有効検証
    #     if self.params["account_form"].is_valid() and self.params["add_account_form"].is_valid():
    #         # アカウント情報をDB保存
    #         account = self.params["account_form"].save()
    #         # パスワードをハッシュ化
    #         account.set_password(account.password)
    #         # ハッシュ化パスワード更新
    #         account.save()

    #         # 下記追加情報
    #         # 下記操作のため、コミットなし
    #         add_account = self.params["add_account_form"].save(commit=False)
    #         # AccountForm & AddAccountForm 1vs1 紐付け
    #         add_account.user = account

    #         # 画像アップロード有無検証
    #         if 'account_image' in request.FILES:
    #             add_account.account_image = request.FILES['account_image']

    #         # モデル保存
    #         add_account.save()

    #         # アカウント作成情報更新
    #         self.params["AccountCreate"] = True

    #     else:
    #         # フォームが有効でない場合
    #         print(self.params["account_form"].errors)

        # return render(request,"interview/profile.html",context=self.params)
