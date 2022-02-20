from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from . import settings
from . import models
import datetime
import os, secrets, string, time
from datetime import datetime

'''
userProp={}

## Get IP address
def get_ip():
    res = ''.join(secrets.choice(string.ascii_uppercase + string.digits + string.ascii_lowercase) for i in range(20))
    return res
'''

curl = settings.CURRENT_URL
media_url = settings.MEDIA_URL
base_dir = settings.BASE_DIR


def home(request):
    if request.method == "GET":
        return render(request, "home.html", {'curl':curl, 'output': ''})
    else:
        pass


def register(request):
    if request.method == "GET":
        return render(request, "register.html", {'output': '', 'curl': curl})
    else:
        email = request.POST.get("email")

        query = "select email from registered where email = '" + str(email) + "';"
        models.cursor.execute(query)
        existingEmail = models.cursor.fetchall()


        try:
            existingEmail = existingEmail[0][0]
            return render(request, "register.html", {'curl': curl, 'output': '---------- Email Already Exists ----------', 'regError': 1})
        except:
            pass


        name = request.POST.get("name")

        password = request.POST.get("password")
        mobile = request.POST.get("mobile")
        dob = request.POST.get("dob")
        city = request.POST.get("city")
        address = request.POST.get("address")
        gender = request.POST.get("gender")
        now = datetime.now()
        dateofreg = now
        # print(now)

        query = "insert into registered values(NULL,'%s','%s', '%s', '%s','%s','%s','%s','%s','%s','User',1)" % (name,email,password,mobile,dob,city,address,gender,dateofreg)
        models.cursor.execute(query)
        models.db.commit()

        query = "select id from registered where email = '" + str(email) + "';"
        models.cursor.execute(query)
        id = models.cursor.fetchall()
        id = id[0][0]
        print(id)

        query = "insert into userqueries values('%s', NULL, NULL, '%s')" % (id, email)
        models.cursor.execute(query)
        models.db.commit()

        return render(request, "register.html", {'curl': curl, 'output': 'Registered Successfully...', 'regError': 0})


def login(request):
    if request.method == "GET":
        return render(request, "login.html", {'output':'', 'curl': curl, 'loginError': 0})
    else:
        email = request.POST.get("email")
        password = request.POST.get("password")

        query = "select * from registered where email = '" + str(email) + "' and password = '" + str(password) + "';"
        print(query)

        models.cursor.execute(query)
        userDetails = models.cursor.fetchall()
        # print(userDetails, email, password)

        if len(userDetails) > 0:
            userid = userDetails[0][0]
            print(userid)
            # return render(request, "login.html", {'curl': curl, 'output': '---------- Login Successful ----------'})
            if userDetails[0][10] == "User":
                return redirect(curl + "userhome/?userid=" + str(userid))
            else:
                return redirect(curl + "adminhome/?userid=" + str(userid))
        else:
            return render(request, "login.html", {'curl': curl, 'output': '---------- Incorrect Email or Password ----------', 'loginError': 1})

# ---------- Admin Views ----------
def adminhome(request):
    query = " select count(userquery) from userqueries where userquery is Not NULL;"
    models.cursor.execute(query)
    pendingRequests = models.cursor.fetchall()
    pendingRequests = pendingRequests[0][0]
    print(pendingRequests)
    return render(request, 'adminhome.html', {'curl': curl, 'pendingRequests': pendingRequests})


def viewuser(request):
    query1 = "select * from registered where type = 'User';"
    models.cursor.execute(query1)
    totalUsers = models.cursor.fetchall()
    totalNoUsers = len(totalUsers)
    # print(totalUsers)

    query2 = "select * from userqueries;"
    models.cursor.execute(query2)
    totalUserQueries = models.cursor.fetchall()
    # print(totalUserQueries)
    totalUserDetails = list(zip(totalUsers, totalUserQueries))

    return render(request, 'viewuser.html', {'curl': curl, 'totalNoUsers':totalNoUsers, 'totalUserDetails':totalUserDetails})


def manageuser(request):
    query = "select * from registered where type = 'User';"
    models.cursor.execute(query)
    totalUsers = models.cursor.fetchall()
    totalNoUsers = len(totalUsers)
    print(totalUsers)
    return render(request, 'manageuser.html', {'curl': curl,  'totalUsers':totalUsers, 'totalNoUsers':totalNoUsers})


def answerquery(request):
    if request.method == "GET":
        userid = request.GET.get("userid")

        query1 = "select * from registered where id = '%s';" % (userid)
        models.cursor.execute(query1)
        userDetail = models.cursor.fetchall()
        print(userDetail)

        query2 = "select userquery from userqueries where id = '%s';" % (userid)
        models.cursor.execute(query2)
        userQuerySolution = models.cursor.fetchall()
        print(userQuerySolution)

        return render(request, 'answerquery.html', {'curl': curl, "userid":userid, 'userDetail': userDetail, 'userQuerySolution': userQuerySolution})
    else:
        solution = request.POST.get("solution")
        email = request.POST.get("email")

        query = "update userqueries set solution = '%s' where email = '%s';" % (solution, email)
        print(query)
        models.cursor.execute(query)
        models.db.commit()

        return render(request, 'viewuser.html', {'curl': curl})


# ---------- User Views ----------


def userhome(request):
    userid = request.GET.get("userid")
    return render(request, 'userhome.html', {'curl': curl, 'userid': userid})


def checkresult(request):
    userid = request.GET.get("userid")

    query = "select userquery, solution from userqueries where id = '%s';" % (userid)
    models.cursor.execute(query)
    userQuerySolution = models.cursor.fetchall()
    print(userQuerySolution)

    return render(request, 'checkresult.html', {'curl': curl, 'userid': userid, 'userQuerySolution':userQuerySolution})


def askquery(request):
    if request.method == "GET":
        userid = request.GET.get("userid")
        return render(request, "askquery.html", {'curl': curl, 'userid': userid})
    else:
        userquery = request.POST.get("userquery")
        email = request.POST.get("email")

        # query = "insert into userqueries values('%s', '%s', NULL)" % (userid, userquery)
        query = "update userqueries set userquery = '%s' where email = '%s';" % (userquery, email)
        print(query)
        models.cursor.execute(query)
        models.db.commit()

        return render(request, "askquery.html", {'curl': curl, 'subError': 0, 'userid': 6})
