class colors:
    PASS = '\033[32m'
    FAIL = '\033[31m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def Login(username,password):
    check=False
    file1=open("users.txt","r")
    for data in file1:
        list=data
        list=list.split(",")
        if list[2]==username and list[3]==password:
            check=True
            break
    if check==True:
        return True
    else:
        return False

def Check_repeated_name(username):
    check=False
    file1=open("users.txt","r")
    for data in file1:
        list=data
        list=list.split(",")
        if list[2]==username:
            check=True
            break
    if check==True:
        return True
    else:
        return False

def Authentication():
    global username
    global password
    choice=input(colors.BOLD+"Have you already created an account? (Y/N): "+colors.ENDC)
    if choice == "Y":
        username=str(input("Username: "))
        password=str(input("Password: "))
        if Login(username,password)==True:
            print(colors.PASS+"Login Successfully!\n"+colors.ENDC)
            #return(username)#### Detect is normal user or admin
        else:
            print(colors.FAIL+"Login failed, please try again."+colors.ENDC)
            Authentication()
    elif choice=="N" :
        username = input("Please enter an unique username: ")
        while Check_repeated_name(username)==True:
            username = input("Username existed, please enter another username: ")
        password = input("Please set the account password: ")
        firstname = input("Please enter your first name: ")
        lastname = input("Please enter your last name: ")
        file1 = open("users.txt", "a")
        file1.writelines(firstname +','+ lastname +','+ username +','+ password +','+ '' +','+'\n')
        file1.close()
        print(colors.PASS+"You have successfully created an account!"+colors.ENDC)
        #return(username)#### Detect is normal user or admin
    else:
        print(colors.BOLD+"Please enter 'Y' or 'N'."+colors.ENDC)
        Authentication()

def isAnchor(directsource):
    file1 = open("posts.txt", "r")
    for data in file1:
        list=data
        list=list.split(",")
        if list[0]==directsource and list[4]=='':
            return True
        else:
            return False

def IsFriend(x,y):
    file1 = open("users.txt", "r")
    global relationships
    relationships=''
    for data in file1:
        list=data
        list=list.split(",")
        if list[2] == x:            #Find the first user
            relationships=list[4]   #Check out all the friends of that user
            break
    relationships= relationships.split(' & ')
    if y in relationships:      #See another user is in the list ot not
        return True
    else:
        return False

def IsDirectSource(x,y):
    file1 = open("posts.txt", "r")
    global relationships
    relationships=''
    for data in file1:
        list=data
        list=list.split(",")
        if list[0] == y:            #Find the y article
            relationships=list[4]   #Find the directsource of y
            break

    if x in relationships:      #Macth the x article which might be a source
        return True
    else:
        return False

def IsSource(x,y):
    global source
    directsource=y      # Article y is the main character
    while directsource != "" and isAnchor(directsource) == False:
        file1 = open("posts.txt", "r")
        for data in file1:
            list = data
            list = list.split(",")
            if (list[0]) == str(directsource):
                source = list[4]    #Find the directsource record
                if source==x:      #Once record equal to x, return true
                    return True
        directsource = source
        file1.close()
    return False    #If not match x at all, return false

def Anchor(x):
    global source
    directsource=x      # Article x is the main character
    while directsource != "" and isAnchor(directsource) == False:
        file1 = open("posts.txt", "r")
        for data in file1:
            list = data
            list = list.split(",")
            if (list[0]) == str(directsource):
                source = list[4]    #Find the directsource record
                if isAnchor(source)==True:      #Call isAnchor function, if true then return
                    return source
        directsource = source
        file1.close()
    return False    #If not satify the while conditional at first, it means x dones own any source.

def DirectReport(x):
    global source
    directsource=x      # Article x is the main character
    result=[]
    file1 = open("posts.txt", "r")
    for data in file1:
        list = data
        list = list.split(",")
        if list[4]==directsource:    #Find the directsource record
            result.append(list[0])     #If quote section equal to x, add into result list

    file1.close()
    if len(result)>0:   #Check whether x has any source, count > 0
        return result
    else:               #If none of articles quote x, return false
        return False

def Report(x):
    global source
    result=[]
    file1 = open("posts.txt", "r")

    for i in range(1,len(open("posts.txt").readlines())+1): #loop through every posts
        if IsSource(x, i)==True:     #Check if i is a source of x
            result.append(i)        #If yes, add into the result list

    file1.close()
    if len(result)>0:   #Check whether x has any source, count > 0
        return result
    else:               #If none of articles quote x, return false
        return False

def GetU(x):
    file1 = open("users.txt", "r")
    for data in file1:
        list = data
        list = list.split(",")
        if list[2]==x:  #Return whole set of information if x==username
            return(list)
    return False    #Return false if cannot find

def GetA(x):
    file1 = open("posts.txt", "r")
    for data in file1:
        list = data
        list = list.split(",")
        if list[0]==x:  #Return whole set of information if x==username
            return(list)
    return False    #Return false if cannot find

def NicePrintU(x):
    result = GetU(x)
    if result != False:
        firstname = result[0]
        lastname = result[1]
        username = result[2]
        password = result[3]
        friends = result[4]
        import hashlib  # pip install hashlib !!!
        password=str(password).encode('utf-8')  #Encrypt the password (sensitive information)
        sha256 = hashlib.sha256()
        sha256.update(password)
        password = sha256.hexdigest()
        print(colors.PASS + 'Firstname: {}\nLastname: {}\nUsername: {}\nEncrypted Password: {}\nFriends: {}\n'.format(str(firstname),str(lastname),str(username),str(password),str(friends))+colors.ENDC)
    else:
        print(colors.FAIL + 'Sorry, cannot find the right user.\n' + colors.ENDC)

def NicePrintA(x):
    result = GetA(x)
    if result != False:
        index=result[0]
        title=result[1]
        content=result[2]
        date=result[3]
        directsource=result[4]
        user=result[5]
        print(colors.PASS + 'Index: {}\nTitle: {}\nContent: {}\nDate: {}\nDirect Source: {}\nWriter: {}\n'.format(
            str(index), str(title), str(content), str(date), str(directsource),str(user)) + colors.ENDC)
    else:
        print(colors.FAIL + 'Sorry, cannot find the right article.\n' + colors.ENDC)

def Influence_post():            #Find influence score of each article

    dict_post={}
    count = len(open("posts.txt").readlines())
    for i in range(1,count+1):      # Add all keys to dictionary (Posts)
        dict_post[i]=0
    #print(dict_post)

    global source
    for i in range(1,count+1):

        directsource=i
        while directsource != "" and isAnchor(directsource)==False:
            file1 = open("posts.txt", "r")
            for data in file1:
                list = data
                list = list.split(",")
                if (list[0]) == str(directsource):
                    source=list[4]
            if source !='':
                dict_post[int(source)] = int(dict_post[int(source)])+1
            directsource = source
            file1.close()

    return dict_post

def Influence_user():
    dict_user={}
    file1 = open("users.txt", "r")
    for data in file1:
        list = data
        list = list.split(",")
        dict_user[list[2]]=0
    #print(dict_user)       # Check every keys (username) are included in dictionary
    file1.close()

    dict_post = Influence_post()  # Call the function to get the influence score per article
    for key in dict_user.keys():
        file1 = open("posts.txt", "r")
        for data in file1:
            list = data
            list = list.split(",")
            if list[5] == key:      # list[5] is author, Clarify articles belonged to which user accordingly
                index=list[0]
                dict_user[key]=int(dict_user[key])+int(dict_post[int(index)])

    return(dict_user)


def KOL(t,p):
    import math
    global dict_user
    dict_user = Influence_user()
    maximum_kol=math.floor(len(dict_user)*p*0.01)  #The maximum number of KOL can be generated
    minimum_influence=t

    list_influence=[]       #Store all the individual influence point into a list, then sort
    for influence in dict_user.values():
        if influence >= t:
            list_influence.append(influence)
    list_influence.sort(reverse=True)   #From large to small
    list_influence=list_influence[0:maximum_kol]   #Take the top scores only, follow maximum_kol

    final_kol=[]                   #Find the appropriate KOLs by matching the top score list
    for key in dict_user.keys():
        if dict_user[key] in list_influence:
            final_kol.append(key)

    return final_kol

def Action():
    choice=eval(input("1. Add Friend\n2. Add Post\n3. Log out\n"+colors.BOLD+"Please select your following action by entering a number 1 / 2 / 3: "+colors.ENDC))
    return choice

def Admin():
    choice=eval(input("1. Add Friend\n2. Add Post\n3. Log out\n4. IsFriend\n5. isDirectSource\n6. isSource\n7. Anchor\n8. DirectReport\n9. Report\n10. NicePrintU\n11. NicePrintA\n12. GetU\n13. GetA\n14. KOL\n"+colors.BOLD+"Please select your following action by entering a number from 1 to 14: "+colors.ENDC))
    return choice

def main():

    Authentication()
    while True:
        if username == 'Admin':
            action=Admin()
        else:
            action=Action()
        if action==1:
            friend=input("Please input your friend's username: ")
            if Check_repeated_name(friend)==True:
                print(colors.PASS+"You have built a relationship with {}.\n"+colors.ENDC.format(friend))
                file1 = open("users.txt", "r")
                for data in file1:  # Add frd to User active side
                    list = data
                    list = list.split(",")
                    if list[2] == username:
                        target=data
                        a_file = open("users.txt", "r")
                        lines = a_file.readlines()
                        a_file.close()
                        new_file = open("users.txt", "w")
                        for line in lines:
                            if line != data:
                                new_file.write(line)
                        target=target.split(",")
                        if target[4]=="":
                            target[4]=friend
                        else:
                            target[4]=target[4]+' & '+friend
                        target[4] = str(target[4])

                        new_file.write(list[0]+','+list[1]+','+list[2]+','+list[3]+','+str(target[4])+',\n')
                        new_file.close()
                        break
                file1 = open("users.txt", "r")
                for data in file1:          # Add frd to User passive side
                    list = data
                    list = list.split(",")
                    if list[2] == friend:
                        target=data
                        a_file = open("users.txt", "r")
                        lines = a_file.readlines()
                        a_file.close()
                        new_file = open("users.txt", "w")
                        for line in lines:
                            if line != data:
                                new_file.write(line)
                        target=target.split(",")
                        if target[4]=="":
                            target[4]=username
                        else:
                            target[4]=target[4]+' & '+username
                        target[4] = str(target[4])

                        new_file.write(list[0]+','+list[1]+','+list[2]+','+list[3]+','+str(target[4])+',\n')
                        new_file.close()
                        break

            else:
                print(colors.FAIL+"The user is not found.\n"+colors.ENDC)

        elif action== 2:

            title = str(input("Please enter an title: "))
            content = str(input("Please enter the main content: "))
            author = username
            from datetime import date
            date = date.today()
            index = len(open("posts.txt").readlines())+1
            choice = str(input("Do you quote any source? (Y/N): "))
            if choice == "Y":
                quote = str(input("Please enter the index of the quoted post: "))
                while not int(quote) > 0 or not int(quote) < index:
                    quote = str(input("Please enter the CORRECT index of the quoted post: "))
            else:
                quote=""
            file1 = open("posts.txt", "a")
            file1.writelines(str(index)+','+title+','+content+','+str(date)+','+str(quote)+','+author+','+'\n')
            file1.close()
            print(colors.PASS+"You have successfully uploaded a post! \n"+colors.ENDC)

        elif action == 3:
            main()

        elif action == 4 and username=='Admin': #Check only Admin could choose items 4 to 14 !!!
            while True:
                try:
                    global x,y
                    xy = input('Please input two username separated by comma: ')
                    xy = xy.split(',')
                    x= xy[0]    #First user
                    y= xy[1]    #Second user
                    break
                except :
                    print(colors.FAIL + 'Wrong input!' + colors.ENDC)
            if IsFriend(x,y)==True:     #Call Function IsFriend()
                print(colors.PASS+'Yes, they are friend.\n'+colors.ENDC)
            else:
                print(colors.FAIL+'No, they are not friend.\n'+ colors.ENDC)

        elif action == 5 and username == 'Admin':
            while True:
                try:
                    xy = input('Please input two article indexes separated by comma: ')
                    xy = xy.split(',')
                    x= xy[0]    #First article
                    y= xy[1]    #Second article
                    break
                except :
                    print(colors.FAIL + 'Wrong input!' + colors.ENDC)
            if IsDirectSource(x,y)==True:     #Call Function IsDirectSource()
                print(colors.PASS+'Yes, '+ x +' is a direct source of '+ y +'\n'+colors.ENDC)
            else:
                print(colors.FAIL+'No, '+ x +' is not a direct source of '+ y +'\n'+colors.ENDC)

        elif action == 6 and username == 'Admin':
            global source
            while True:
                try:
                    xy = input('Please input two article indexes separated by comma: ')
                    xy = xy.split(',')
                    x= xy[0]    #First article
                    y= xy[1]    #Second article
                    break
                except :
                    print(colors.FAIL + 'Wrong input!' + colors.ENDC)

            if IsSource(x,y)==True:     #Call Function IsDirectSource()
                print(colors.PASS+'Yes, '+ x +' is a source of '+ y +'\n'+colors.ENDC)
            else:
                print(colors.FAIL+'No, '+ x +' is not a source of '+ y +'\n'+colors.ENDC)

        elif action == 7 and username == 'Admin':
            while True:
                try:
                    x = input('Please input an article index: ')
                    break
                except :
                    print(colors.FAIL + 'Wrong input!' + colors.ENDC)

            result = Anchor(x)
            if result != False:     #Call Function IsDirectSource()
                print(colors.PASS+ result +' is the anchor for '+ x +'\n'+colors.ENDC)
            else:
                print(colors.FAIL+'Sorry, article'+ x +' does not have any source.'+'\n'+colors.ENDC)

        elif action == 8 and username == 'Admin':
            while True:
                try:
                    x = input('Please input an article index: ')
                    break
                except :
                    print(colors.FAIL + 'Wrong input!' + colors.ENDC)

            result = DirectReport(x)
            if result != False:     #Call Function IsDirectSource()
                print(colors.PASS+ str(result) +' is the list of reports indexes directly quote article '+ x +'.\n'+colors.ENDC)
            else:
                print(colors.FAIL+'Sorry, article '+ x +' does not have any direct report.'+'\n'+colors.ENDC)

        elif action == 9 and username == 'Admin':
            while True:
                try:
                    x = input('Please input an article index: ')
                    break
                except:
                    print(colors.FAIL + 'Wrong input!' + colors.ENDC)

            result = Report(x)
            if result != False:  # Call Function IsDirectSource()
                print(colors.PASS + str(result) + ' is the list of reports indexes quote article ' + x + '.\n' + colors.ENDC)
            else:
                print(colors.FAIL + 'Sorry, article ' + x + ' does not have any report.' + '\n' + colors.ENDC)

        elif action == 10 and username == 'Admin':
            while True:
                try:
                    x = input('Please input a username: ')
                    break
                except:
                    print(colors.FAIL + 'Wrong input!' + colors.ENDC)

            NicePrintU(x)

        elif action == 11 and username == 'Admin':
            while True:
                try:
                    x = input('Please input an article index: ')
                    break
                except:
                    print(colors.FAIL + 'Wrong input!' + colors.ENDC)

            NicePrintA(x)

        elif action == 12 and username == 'Admin':
            while True:
                try:
                    x = input('Please input a username: ')
                    break
                except:
                    print(colors.FAIL + 'Wrong input!' + colors.ENDC)

            result=GetU(x)
            if result != False:
                print(colors.PASS+ str(result) +colors.ENDC)
            else:
                print(colors.FAIL+'Sorry, cannot find the right user.\n'+colors.ENDC)

        elif action == 13 and username == 'Admin':
            while True:
                try:
                    x = input('Please input an article index: ')
                    break
                except:
                    print(colors.FAIL + 'Wrong input!' + colors.ENDC)
            result=GetA(x)
            if result != False:
                print(colors.PASS+str(result)+colors.ENDC)
            else:
                print(colors.FAIL+'Sorry, cannot find the right article.\n'+colors.ENDC)

        elif action == 14 and username == 'Admin':
            while True:
                try:
                    t = eval(input('Please input the minimum influence score of a user: '))
                    break
                except:
                    print(colors.FAIL + 'Wrong input!' + colors.ENDC)
            while True:
                try:
                    p = eval(input('Please input the maximum percentage (0 to 100) of KOL among all users : '))
                    break
                except:
                    print(colors.FAIL + 'Wrong input!' + colors.ENDC)

            result = KOL(t,p)

            if result != []:
                print(colors.PASS + "The following list contains all the KOLs: " + str(result) + colors.ENDC)
                for i in result:
                    relationships = []  #Asuuming everyone has no relationships at first
                    for y in dict_user.keys():
                        if IsFriend(i,y) == True:   #Call Isfriend() function to check
                            relationships.append(y) #If true, add into relationships list
                    print(colors.PASS + i +' : '+str(relationships)+colors.ENDC)
                print("") #formatting
            else:
                print(colors.FAIL+'There is no KOL.\n'+colors.ENDC)


main()

