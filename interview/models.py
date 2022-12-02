from django.db import models

# ユーザー認証
from django.contrib.auth.models import User

# Create your models here.
class DB(models.Model):
    id = models.AutoField(primary_key=True)
    Question = models.CharField(null=False, max_length=100)
    Answer = models.CharField(blank=True, null=True, max_length=500)
    Memo = models.CharField(blank=True, null=True, max_length=100)
    FB = models.CharField(blank=True, null=True, max_length=100)
    Contributor = models.CharField(blank=True, null=True, max_length=100)
    WhoAnswers = models.CharField(blank=True, null=True, max_length=100)
    FBer = models.CharField(blank=True, null=True, max_length=100)
    Genre = models.CharField(blank=True, null=True, max_length=100)
    AnswerReq = models.CharField(blank=True, null=True, max_length=100)
    FBReq = models.CharField(blank=True, null=True, max_length=100)
     
# ユーザーアカウントのモデルクラス
class Account(models.Model):

    # ユーザー認証のインスタンス(1vs1関係)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # 追加フィールド
    last_name = models.CharField(blank=True, null=True, max_length=100)
    first_name = models.CharField(max_length=100)
    account_image = models.ImageField(upload_to="account_image",blank=True)

    def __str__(self):
        return self.user.username