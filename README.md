# QUIZ APP

<img src='/erd.png'>

- users app
- quiz app

******** USERS APP *************

   - auth işlemleri için TokenAuthentication kullandık.

```html
pip install djangorestframework

INSTALLED_APPS = [
    ...
    'rest_framework.authtoken',
    'rest_framework',
]


REST_FRAMEWORK = { 'DEFAULT_AUTHENTICATION_CLASSES': [ 'rest_framework.authentication.TokenAuthentication' ] }


python manage.py migrate

```

- serializers.py User modelini import ettik, user modeli içinde gelen email field ni uniq ve zorunlu yapmak için tekrar tanımlıyoruz. 

- DRF UniqueValidator kullandık,

```
from rest_framework.validators import UniqueValidator

uniq olması gereken field içerine tanımladık,

validators=[UniqueValidator(queryset=User.objects.all())]

```

- password field validated işlemine tabi tutuyoruz, DRF passwor validate import ettik


```
from django.contrib.auth.password_validation import validate_password
 
ilgili field içinde tanımladık

validators=[validate_password],


password2 ile aynı olması için password2 tanımladık.
```



```
validate işlemine tabi tutulan fieldlerden sonra class Meta ile kayıt aşamasında kullanılacak fieldları aldık

    class Meta:
        model= User
        field = (
            'username',
            'email',
            'first_name',
            'last_name',
            'password',
            'password2'
        )

#aşağıda iki password ıyaslamasını yaptık

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {'password' : 'Password fields didnt match'}
            )     

        return attrs

# create işlemiş yapılma aşamasını dizayn ettik, user ile password aynı anda kayıt için göndermiyoruz. ilk önce pop ile password data dan ayırdık, password haricindeki user i tüm field ları ile çağırdık, ayırıp tanımladığımız password değişkenine atadığımız passwordu set işlemi ile user a eşitledik, 

    def create(self, validated_data) :
        validated_data.pop('password2')
        password = validated_data.pop('password')
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user 

```

* register işlemini views ve urls.py dosyalarına aktarıyoruz,


```
views.py

from django.shortcuts import render
from django.contrib.auth.models import User
from .serializers import RegisterSerializer
from rest_framework.generics import CreateAPIView

class RegisterView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

# buraya kadar olan kısım register işlemi için 



from django.urls import path
from .views import RegisterView


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),

]

bu asamada token kodu henüz oluşturmadık.


token oluşturmak için farklı bir kaç yöntem mevcut, signal, dj-rest-auht paketi gibi,
bu app de

obtain_auth_token views i var rest_framework un
db de userin tokeni varsa getiriyor, yoksa yeniden oluşturuyor

urls.py ekledik
from rest_framework.authtoken import views


path('login/', views.obtain_auth_token, name="login")

http://127.0.0.1:8000/user/login/ browserpi de gözükmez postmanda login olmamız gerekyor.

login olduktan sonra Token oluştu.
```

** user register olduğunda aynı anda login olması için views.py da 

   - CreateAPIView -> create in source kodundan create func override ediyoruz

```


  def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = Token.objects.create(user=user)
        data = serializer.data
        data['token'] = token.key
        headers = self.get_success_headers(serializer.data)
        return Response(data, status=status.HTTP_201_CREATED, headers=headers)

```




******** QUİZ APP *************

- ERD diyagramına göre models.py dosyamızı oluşturduk,

- Oluşturulan models.py dan serializers.py oluşturduk

- ModelSerializer ile devam ettik, 



