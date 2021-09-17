from django.http import response
import pandas as pd
import joblib
import json
from django.contrib.auth import authenticate,login,logout
from .models import FileUser, FileUser2
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import association_rules
from django.contrib import messages
from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from .forms import CreateUserForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required


def register(request):
	if request.user.is_authenticated:
		return redirect('home')
	else:
		form = CreateUserForm()
		if request.method == 'POST':
			form = CreateUserForm(request.POST)
			if form.is_valid():
				form.save()
				user = form.cleaned_data.get('username')
				messages.success(request, 'Account was created for ' + user)

				return redirect('login')
			

		context = {'form':form}
		return render(request, 'authenticate/register.html', context)

def loginPage(request):
	if request.user.is_authenticated:
		return redirect('home')
	else:
		if request.method == 'POST':
			username = request.POST.get('username')
			password =request.POST.get('password')

			user = authenticate(request, username=username, password=password)

			if user is not None:
				login(request, user)
				return redirect('home')
			else:
				messages.info(request, 'Username OR password is incorrect')

		context = {}
		return render(request, 'authenticate/login.html', context)


def logoutUser(request):
	logout(request)
	return redirect('login')

@login_required(login_url='login')
def home(request):
    return render(request, 'authenticate/home.html', {})


@login_required(login_url='login')
def upload(request):
    name = {}
    if request.method == 'POST':
        uploaded_file = request.FILES['document']
        fs = FileSystemStorage()
        ne = fs.save(uploaded_file.name, uploaded_file)
       
        name['fname'] = uploaded_file.name
    
    return render(request, 'authenticate/upload.html', name)

@login_required(login_url='login')
def associateCourse(request):
    rules = joblib.load('model.sav')
    temp = {}
    fileModel = 0
    if request.method == 'POST':
        uploaded_file = request.FILES['document']
        if uploaded_file.name.endswith('.csv'):
            temp['support'] = request.POST.get('support')
            temp['confidence'] = request.POST.get('confidence')  
                
            df = pd.read_csv(uploaded_file)
            df = df.astype(str)

            lists = df.values.tolist()

            te = TransactionEncoder()
            te_ary = te.fit(lists).transform(lists)

            dfs = pd.DataFrame(te_ary, columns=te.columns_)
            dfs.drop('nan', axis=1, inplace=True)

            support = float(temp['support'])
            confidence = float(temp['confidence'])

            itemsets = apriori(dfs, min_support=support, use_colnames=True, max_len = 2 )
            
            rules = association_rules(itemsets, metric='confidence', min_threshold=confidence)

            rules["antecedents"] = rules["antecedents"].apply(lambda x: list(x)[0]).astype("unicode")
            rules["consequents"] = rules["consequents"].apply(lambda x: list(x)[0]).astype("unicode")    

            rules = rules[['antecedents','consequents','support','confidence','lift'] ]
            dFile = []
            rules = rules.sort_values(['confidence'], ascending =[False])
            for i in range(0,len(rules)):
                dictFile = {'antecedents':rules.iloc[i]['antecedents'],'consequents':rules.iloc[i]['consequents'],'support':rules.iloc[i]['support'],'confidence':rules.iloc[i]['confidence'],'lift':rules.iloc[i]['lift']}
                dFile.append(dictFile)

            fileModel = 0
            if FileUser.objects.all():
                fileModel = FileUser.objects.last()
                fileModel = fileModel.id
            json_data = dFile
            json_format = json.dumps(json_data)
            json_df = pd.read_json(json_format)
            json_df.to_csv('media/results'+str(fileModel+1)+'.csv')
            fileModel = FileUser.objects.create(userupload='results'+str(fileModel+1)+'.csv',title='title'+str(fileModel+1))
            return render(request, 'authenticate/upload.html', {'rule':rules,'file' : fileModel})

        else:
            messages.warning(request, 'File was not uploaded. Please use csv file extension!')

    return render(request, 'authenticate/upload.html', {'rule':rules,})

@login_required(login_url='login')
def check(request):
    return render(request, 'authenticate/check.html', {})

@login_required(login_url='login')
def checkCourse(request):
    rules = joblib.load('model.sav')
    temp = {}
    predict = None
    answer=''
    if request.method == 'POST':
        uploaded_file = request.FILES['documents']
        if uploaded_file.name.endswith('.csv'):
            temp['course1'] = request.POST.get('course1')
            temp['course2'] = request.POST.get('course2') 
                
            df = pd.read_csv(uploaded_file)
            
            df = df.astype(str)

            lists = df.values.tolist()

            te = TransactionEncoder()
            te_ary = te.fit(lists).transform(lists)

            dfs = pd.DataFrame(te_ary, columns=te.columns_)
            dfs.drop('nan', axis=1, inplace=True)

            itemsets = apriori(dfs, min_support=0.05, use_colnames=True, max_len = 2 )
            
            rules = association_rules(itemsets, metric='confidence', min_threshold=0.1)
            rules["antecedents"] = rules["antecedents"].apply(lambda x: list(x)[0]).astype("unicode")
            rules["consequents"] = rules["consequents"].apply(lambda x: list(x)[0]).astype("unicode") 
            
            rules = rules[['antecedents','consequents','support','confidence','lift'] ]

            result = rules.loc[(rules['antecedents'] == temp[   'course1']) & (rules['consequents'] == temp['course2'])]
            result=result.values.tolist()
            
            def ans(res):
                answer=''
                if not res:
                    answer = 'No rules exist for this association!'
                else:
                    for row in res:
                        answer = ('{} and {} are likely to occur with a support of {}% and confideence of {}%'.format(row[0],row[1], (row[2]*100),(row[3]*100)))

                return answer
            answer = ans(result)
            # print(answer)
            predict = True
        else:
            messages.warning(request, 'File was not uploaded. Please use csv file extension!')

    return render(request, 'authenticate/check.html', {'results':answer,'predict':predict})


@login_required(login_url='login')
def chart(request):
    file = joblib.load('model.sav')
    Gender_GPA = {}
    Box_Gender = {}
    Class_Bar = {}
    CGPA_Change = {}
    if request.method == 'POST':
        uploaded_file = request.FILES['vizfile']
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv( uploaded_file)
        # df = pd.DataFrame(data=data, index=None)

            df['PRE_CGPA'] = df['PRE WTS'] / df['PRE UNIT']
            df['CGPA_CHANGE'] = (df['CGPA'] - df['PRE_CGPA']) * 100
            df['CHANGE'] = df['CGPA_CHANGE'].apply(lambda x: 'increase' if x > 0 else 'decrease')
            cols = df.iloc[:,6:18]
            print(len(df))
            # bar 1
            totalMale =0
            totalFemale = 0 
            male =0 
            female =0
            
            for i in range(0,len(df)) :
                
                if not str(df.iloc[i]['GPA']) == 'nan':
                    print(str(df.iloc[i]['GPA']))
                    if  df.iloc[i]['GENDER'] == 'M':
                        totalMale = float(df.iloc[i]['GPA']) + totalMale   
                        male = 1 + male
                    elif  df.iloc[i]['GENDER']=='F':
                        totalFemale = float(df.iloc[i]['GPA']) + totalFemale   
                        female =  1 + female
                        
            Gender_GPA = {'male':totalMale/male,'female':totalFemale/female}
           
           # boxplot1
            df = df.reset_index()
            rslt_df = df[df['GENDER'] == 'M']
            cgpa_male = rslt_df['GPA'].tolist()
            rslt_df2 = df[df['GENDER'] == 'F']
            cgpa_female = rslt_df2['GPA'].tolist()

            
            print(cgpa_male[1])
            Box_Gender = {'cgpa_male': cgpa_male, 'cgpa_female':cgpa_female}

            # doughnut chart 
            details = df.apply(lambda x : True
            if x['CLASS'] == "1st" else False, axis = 1)
            class1 = len(details[details == True].index)

            details = df.apply(lambda x : True
            if x['CLASS'] == "2|1" else False, axis = 1)
            class2 = len(details[details == True].index)

            details = df.apply(lambda x : True
            if x['CLASS'] == "2|2" else False, axis = 1)
            class3 = len(details[details == True].index)

            details = df.apply(lambda x : True
            if x['CLASS'] == "3rd" else False, axis = 1)
            class4 = len(details[details == True].index)

            Class_Bar = {'class1':class1,'class2':class2,'class3':class3,'class4':class4}

            # bar chart 2
            totalcl1 =0
            totalcl2 =0
            totalcl3 =0
            totalcl4 =0
            cl1 = 0
            cl2 = 0 
            cl3 = 0
            cl4 = 0
            
            for i in range(0,len(df)) :
                
                if not str(df.iloc[i]['CGPA_CHANGE']) == 'nan':
                    # print(str(df.iloc[i]['GPA']))
                    if  df.iloc[i]['CLASS'] == '1st':
                        totalcl1 = float(df.iloc[i]['CGPA_CHANGE']) + totalcl1   
                        cl1 = 1 + cl1
                    elif  df.iloc[i]['CLASS']=='2|1':
                        totalcl2 = float(df.iloc[i]['CGPA_CHANGE']) + totalcl2   
                        cl2 =  1 + cl2
                    elif  df.iloc[i]['CLASS']=='2|2':
                        totalcl3 = float(df.iloc[i]['CGPA_CHANGE']) + totalcl3   
                        cl3 =  1 + cl3
                    elif  df.iloc[i]['CLASS']=='3rd':
                        totalcl4 = float(df.iloc[i]['CGPA_CHANGE']) + totalcl4   
                        cl4 =  1 + cl4
                    print(cl1)    
            CGPA_Change = {'cl1':totalcl1/cl1,'cl2':totalcl2/cl2,'cl3':totalcl3/cl3,'cl4':totalcl4/cl4}
        else:
            messages.warning(request, 'File was not uploaded. Please use csv file extension!')
        
      
    return render(request, 'authenticate/chart.html', {'Gender_GPA':Gender_GPA,'Box_Gender':Box_Gender,'Class_Bar':Class_Bar,'CGPA_Change':CGPA_Change})


@login_required(login_url='login')   
def cpredictCourse(request):
    name = {}
    print('hellp')
    if request.method == 'POST':
        uploaded_file = request.FILES['cpredictdocs']
        fs = FileSystemStorage()
        ne = fs.save(uploaded_file.name, uploaded_file)
        
        name['fname'] = uploaded_file.name

    return render(request, 'authenticate/cpredict.html', {})

@login_required(login_url='login')
def cpredict(request):
    
    print('hello')
    result_perf = joblib.load('./authenticate/model_alg/model3.sav')
    temp = {}
    fileModel2 = 0
    if request.method == 'POST':
        print('hello')
        uploaded_file = request.FILES['cpredictdocs']
        if uploaded_file.name.endswith('.csv'):
            temp['support'] = request.POST.get('supports')
            temp['confidence'] = request.POST.get('confidences')   
                
            df = pd.read_csv(uploaded_file)
            df.set_index('S/N', inplace=True)

            support = float(temp['support'])
            confidence = float(temp['confidence'])

            # create frequent itemsets
            itemsets = apriori(df, min_support=support, use_colnames=True)

            # convert into rules
            rules = association_rules(itemsets, metric='confidence', min_threshold=confidence)

            rules["antecedents"] = rules["antecedents"].apply(lambda x: list(x)[0]).astype("unicode")
            rules["consequents"] = rules["consequents"].apply(lambda x: list(x)[0]).astype("unicode")


            rules = rules[['antecedents','consequents','support','confidence','lift']]
            rules = rules.sort_values(['confidence'], ascending =[False])

            result_perf = rules.loc[(rules['consequents'] == 'CPerformance_Poor')| (rules['consequents'] == 'CPerformance_Fair') | (rules['consequents'] == 'CPerformance_Good')]
            result_perf = result_perf[['antecedents','consequents','support','confidence','lift'] ]
            result_perf.reset_index(drop=True,inplace=True)
            dFile = []
            
           
            for i in range(0,len(result_perf)):
                dictFile = {'antecedents':result_perf.iloc[i]['antecedents'],'consequents':result_perf.iloc[i]['consequents'],'support':result_perf.iloc[i]['support'],'confidence':result_perf.iloc[i]['confidence'],'lift':result_perf.iloc[i]['lift']}
                dFile.append(dictFile)
            fileModel2 = 0
            if FileUser2.objects.all():
                fileModel2 = FileUser2.objects.last()
                fileModel2 = fileModel2.id
            json_data = dFile
            json_format = json.dumps(json_data)
            json_df = pd.read_json(json_format)
            json_df.to_csv('media/download'+str(fileModel2+1)+'.csv')
            fileModel2 = FileUser2.objects.create(userupload='download'+str(fileModel2+1)+'.csv',titles='titles'+str(fileModel2+1))
            return render(request, 'authenticate/cpredict.html', {'her':result_perf,'file' : fileModel2})
          
        else:
            messages.warning(request, 'File was not uploaded. Please use csv file extension!')

    return render(request, 'authenticate/cpredict.html', {'her':result_perf,})