# -*- coding: utf-8 -*-
import math
import random
import pymysql
import discord
import os
con=pymysql.connect(user=os.environ['user'],password=os.environ['password'],host=os.environ["host"],charset="utf8",database=os.environ["database"])
#경험치바
class Exp():
  def __init__(self,now,max):
    self.now = now
    self.max = max
  def string(self):
    return f"{self.now}/{self.max}"
  def percent(self):
    return (self.now/self.max)*100
  def block(self,list:list):
    string=""
    cnt=1
    for _ in range(int(self.percent()/10)):
      cnt+=1
      string+=str(list[10])
    if float(self.percent())%10 >=9.5:
      string+=str(list[11])
    else:
      string+=str(list[int(self.percent())%10])
    while cnt<10:
      cnt+=1
      string+=str(list[0])
    return string

#클래스명
class Class():
  def __init__(self,number):
    self.number=number
  def display(self):
    class_name=['초보자','전사','궁수','마법사','도적']
    return class_name[self.number]
    
class Reinforce():
  def __init__(self,gold,item,number,rank):
    self.gold=int(gold)
    self.item=item
    self.number=number
    self.rank=rank
  def require(self):
    cur=con.cursor()
    cur.execute(f"SELECT * FROM rein_money WHERE `rank` = %s",(self.rank))
    money=cur.fetchone()[self.number+1]
    money=int(money)
    if self.gold < money or self.item < money/50:
      return True
    else:
      return False
  def rein(self):
    cur=con.cursor()
    cur.execute(f"SELECT * FROM rein_percent WHERE `rank` = %s",(self.rank))
    percent=cur.fetchone()[self.number+1]
    percent=int(percent)
    r = random.randint(1,100)
    if percent-r>=0:
      return True
    else:
      return False
  def display(self):
    cur=con.cursor()
    cur.execute(f"SELECT * FROM rein_money WHERE `rank` = %s",(self.rank))
    money=cur.fetchone()[self.number+1]
    money=int(money)
    cur.execute(f"SELECT * FROM rein_percent WHERE `rank` = %s",(self.rank))
    percent=cur.fetchone()[self.number+1]
    percent = int(percent)
    return money,percent

#스테이터스 이름
class Modify():
  def __init__(self,*args):
    self.arg=args[0]
  def statModify(self):
    stat=["힘","민첩","지능","행운","체력","마나"]
    stat_colum=['str','dex','int','luck','hp','mp']
    return stat[stat_colum.index(self.arg)]

class MakeItem():
  def __init__(self,id):
    checking=Default(id)
    checking.isInventory()
    checking.isItem()
  def make(self,name,id,data,am):
    cur=con.cursor()
    ne,nea,ea,nu,nua,ua=self.callamount(name,id,data)
    for i in range(len(ne)):
      cur.execute(f"UPDATE `{id}_etc` SET item_amount=item_amount-{int(nea[i])*am} WHERE item_code={ne[i]}")
    for i in range(len(nu)):
      cur.execute(f"UPDATE `{id}_use` SET item_amount=item_amount-{int(nua[i])*am} WHERE item_code={nu[i]}")
    con.commit()    
    if name=="무기":
      category="_weapon"
    elif name=="방어구":
      category="_wear"
    elif name=="소비":
      category="_use"
    else:
      category="_etc"
    if name=="소비" or name=="기타": 
      cur.execute(f"UPDATE `{id}{category}` SET item_amount=item_amount+{am} WHERE item_name=%s",data)
      con.commit()
  def callamount(self,name,id,data):
    if name=="무기":
      return self.weapon(id,data)
    if name=="방어구":
      return self.wear(id,data)
    if name=="소비":
      return self.use(id,data)
    if name=="기타":
      return self.etc(id,data)
  def itemlist(self,name):
    cur=con.cursor()
    if name=="무기":
      cur.execute("SELECT * FROM make_weapon")
    if name=="방어구":
      cur.execute("SELECT * FROM make_wear")
    if name=="소비":
      cur.execute("SELECT * FROM make_use")
    if name=="기타":
      cur.execute("SELECT * FROM make_etc")
    return cur.fetchall() 
  def weapon(self,id,name):
    cur=con.cursor()
    cur.execute(f"SELECT * FROM make_weapon WHERE item_name = %s",name)
    make_item=cur.fetchone()
    if make_item[1]:
      need_etc=make_item[1].split(" ")
      need_etc_amount=make_item[2].split(" ")
      etc_amount=[]
      for i in need_etc:
        cur.execute(f"SELECT item_amount FROM `{id}_etc` WHERE item_code={i}")
        etc_amount.append(cur.fetchone()[0])
    if make_item[3]:
      need_use=make_item[3].split(" ")
      need_use_amount=make_item[4].split(" ")
      use_amount=[]
      for i in need_use:
        cur.execute(f"SELECT item_amount FROM `{id}_use` WHERE item_code={i}")
        use_amount.append(cur.fetchone()[0])
    try:
      need_use
    except UnboundLocalError:
      need_use=""
      need_use_amount=""
      use_amount=""
    try:
      need_etc
    except UnboundLocalError:
      need_etc=""
      need_etc_amount=""
      etc_amount=""    
    return need_etc,need_etc_amount,etc_amount,need_use,need_use_amount,use_amount

  def wear(self,id,name):
    cur=con.cursor()
    cur.execute(f"SELECT * FROM make_wear WHERE item_name = %s ",name)
    make_item=cur.fetchone()
    if make_item[1]:
      need_etc=make_item[1].split(" ")
      need_etc_amount=make_item[2].split(" ")
      etc_amount=[]
      for i in need_etc:
        cur.execute(f"SELECT item_amount FROM `{id}_etc` WHERE item_code={i}")
        etc_amount.append(cur.fetchone()[0])
    if make_item[3]:
      need_use=make_item[3].split(" ")
      need_use_amount=make_item[4].split(" ")
      use_amount=[]
      for i in need_use:
        cur.execute(f"SELECT item_amount FROM `{id}_use` WHERE item_code={i}")
        use_amount.append(cur.fetchone()[0])
    try:
      need_use
    except UnboundLocalError:
      need_use=""
      need_use_amount=""
      use_amount=""
    try:
      need_etc
    except UnboundLocalError:
      need_etc=""
      need_etc_amount=""
      etc_amount=""
    return need_etc,need_etc_amount,etc_amount,need_use,need_use_amount,use_amount

  def use(self,id,name):
    cur=con.cursor()
    cur.execute(f"SELECT * FROM make_use WHERE item_name = %s ",name)
    make_item=cur.fetchone()
    if make_item[4]:
      need_etc=make_item[4].split(" ")
      need_etc_amount=make_item[5].split(" ")
      etc_amount=[]
      for i in need_etc:
        cur.execute(f"SELECT item_amount FROM `{id}_etc` WHERE item_code={i}")
        etc_amount.append(cur.fetchone()[0])
    if make_item[6]:
      need_use=make_item[6].split(" ")
      need_use_amount=make_item[7].split(" ")
      use_amount=[]
      for i in need_use:
        cur.execute(f"SELECT item_amount FROM `{id}_use` WHERE item_code={i}")
        use_amount.append(cur.fetchone()[0])
    try:
      need_use
    except UnboundLocalError:
      need_use=""
      need_use_amount=""
      use_amount=""
    try:
      need_etc
    except UnboundLocalError:
      need_etc=""
      need_etc_amount=""
      etc_amount=""
    return need_etc,need_etc_amount,etc_amount,need_use,need_use_amount,use_amount
  def disable(self,name,id,data,am):
    ne,nea,ea,nu,nua,ua=self.callamount(name,id,data)
    if ne:
      for i in range(len(nea)):
        if int(nea[i])*am>int(ea[i]):
          return True
    if nu:
      for i in range(len(nua)):
        if int(nua[i])*am>int(ua[i]):
          return True
    return False
  def etc(self,id,name):
    cur=con.cursor()
    cur.execute("SELECT * FROM make_etc WHERE item_name = %s",(name))
    make_item=cur.fetchone()
    if make_item[4]:
      need_etc=make_item[4].split(" ")
      need_etc_amount=make_item[5].split(" ")
      etc_amount=[]
      for i in need_etc:
        cur.execute(f"SELECT item_amount FROM `{id}_etc` WHERE item_code={i}")
        etc_amount.append(cur.fetchone()[0])
    if make_item[6]:
      need_use=make_item[6].split(" ")
      need_use_amount=make_item[7].split(" ")
      use_amount=[]
      for i in need_use:
        cur.execute(f"SELECT item_amount FROM `{id}_use` WHERE item_code={i}")
        use_amount.append(cur.fetchone()[0])
    try:
      need_use
    except UnboundLocalError:
      need_use=""
      need_use_amount=""
      use_amount=""
    try:
      need_etc
    except UnboundLocalError:
      need_etc=""
      need_etc_amount=""
      etc_amount=""
    return need_etc,need_etc_amount,etc_amount,need_use,need_use_amount,use_amount
    
#데미지 계산
class Damage():
  def __init__(self,stat, item, times, crit):
    self.stat =stat
    self.item = item
    self.times = times
    self.crit = crit
  def display(self):
    return math.trunc((self.stat+self.item)*self.times)
  def critical(self):
    r = random.randint(1,100)
    if self.crit-r>=0:
      return self.display()*2,True
    else:
      return self.display(),False

#체력 계산
class Hp():
  def __init__(self,stat,item,collection):
    self.stat=stat
    self.item=item
    self.collection=collection
  def display(self):
    return self.stat+self.item+self.collection 

#아이템 컬렉션
class Collection():
  def __init__(self,value,amount):
    self.value=value
    self.amount=amount
  def display(self):
    if self.value==1:
      return "기초 방어구세트"
    elif self.value==0:
      return "기초 악세서리세트"
    else:
      return "없음"

#인벤토리생성,레벨업
class Default():
  def __init__(self,id):
    self.id=id
  def isItem(self):
    cur=con.cursor()
    li=['use','etc','cash']
    for i in li:
      cur.execute(f"CREATE TABLE IF NOT EXISTS `{i}`(item_code INTEGER PRIMARY KEY, item_name INTEGER, item_amount INTEGER, sold_gold INTEGER,trade INTEGER,url TEXT)")
    con.commit()

    def etc():

      cur.execute(f"SELECT * FROM `etc`")
      data=cur.fetchall()
      data=list(data)
      cur.execute(f"SELECT item_code FROM `{self.id}_etc`")
      primarykey=cur.fetchall()
      if primarykey:
        for i in range(len(primarykey)):
          j=0
          if primarykey[i][0] in data[j]:
            del data[j]
          else:
            j+=1
      cur.executemany(f"INSERT INTO `{self.id}_etc` VALUES(%s,%s,%s,%s,%s,%s)",data)
      con.commit()
    def use():
      cur.execute(f"SELECT * FROM `use`")
      data=cur.fetchall()
      data=list(data)
      cur.execute(f"SELECT item_code FROM `{self.id}_use`")
      primarykey=cur.fetchall()
      if primarykey:
        for i in range(len(primarykey)):
          j=0
          if primarykey[i][0] in data[j]:
            del data[j]
          else:
            j+=1
      cur.executemany(f"INSERT INTO `{self.id}_use` VALUES(%s,%s,%s,%s,%s,%s)",data)
      con.commit()
    use()
    etc()
    con.commit()
  def isInventory(self):
    cur=con.cursor()
  def first(self):
    cur=con.cursor()
    cur.execute(f"INSERT INTO `{self.id}_weapon` VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(None,"초보자의 검",0,"F",1,5,0,0,0,0,1,None,None,None,1,None))
    con.commit()

  def isLevel(self):
    cur=con.cursor()
    cur.execute("SELECT exp,level FROM user_data WHERE id = %s",(self.id))
    exp,level=cur.fetchone()
    exp=int(exp)
    level=int(level)
    gap=0
    while exp>=(level*30)*(int(level/15+1)):
      exp-=(level*30)*(int(level/15+1))
      gap+=1
      level+=1
    stat=gap*3
    cur.execute(f"UPDATE user_data SET exp={exp}, level={level} WHERE id =%s",(self.id))
    cur.execute(f"UPDATE user_stat SET stat_point=stat_point+{stat},skill_point=skill_point+{gap} WHERE id=%s",(self.id))
    con.commit()
    if gap>0:
      return level
    else:
      return None
#전투보상
class Reward():
  def __init__(self,floor,id,exp,money):
    self.floor=floor
    self.id =id
    self.exp=exp
    self.money=money
  def etc(self,enemy):
    code=enemy[7].split()
    percent=enemy[8].split()
    amount=enemy[9].split()
    rand=[]
    length=len(percent)
    for i in range(len(amount)):
      if i %2==0:
        rand.append(random.randint(int(amount[i]),int(amount[i+1])))
    j=0
    for i in range(length):
      if int(percent[i-j]) < random.randint(1,101): 
        del code[i-j]
        del rand[i-j]
        del percent[i-j]
        j+=1
    name=[]
    for i in range(len(rand)):
      cur=con.cursor()
      cur.execute(f"UPDATE `user_etc` SET item_amount=item_amount+{rand[i]} WHERE item_code=%s and id = %s",(code[i],self.id))
      cur.execute(f"SELECT item_name FROM `{self.id}_etc` WHERE item_code = %s",(code[i]))
      name.append(cur.fetchone()[0])
    con.commit()
    return name,rand
  def use(self,enemy):
    cur=con.cursor()
    code=enemy[10].split()
    percent=enemy[11].split()
    amount=enemy[12].split()
    rand=[]
    length=len(percent)
    for i in range(len(amount)):
      if i %2==0:
        rand.append(random.randint(int(amount[i]),int(amount[i+1])))
    j=0
    for i in range(length):
      if int(percent[i-j]) < random.randint(1,101): 
        del code[i-j]
        del rand[i-j]
        del percent[i-j]
        j+=1
    name=[]
    for i in range(len(rand)):
      cur.execute(f"UPDATE `user_use` SET item_amount=item_amount+{rand[i]} WHERE item_code=%s and id=%s",(code[i],self.id))
      cur.execute(f"SELECT item_name FROM `{self.id}_use` WHERE item_code = %s",(code[i]))
      name.append(cur.fetchone()[0])
    con.commit()
    return name,rand
  def defualt(self):
    cur=con.cursor()
    cur.execute(f"UPDATE user_data SET exp=exp+{self.exp}, money=money+{self.money} WHERE id = %s",(self.id))   
    con.commit() 
  def wear(self):
    if self.get():
      cur=con.cursor()
      cur.execute(f"SELECT COUNT(*) FROM loot_table_wear WHERE floor=%s",(self.floor))
      amount = cur.fetchone()
      amount=int(amount[0])
      if amount==0:
        return None      
      amount = random.randint(0,amount-1)
      cur.execute(f"SELECT * FROM loot_table_wear WHERE floor = %s LIMIT {amount}, 1",(self.floor))
      info = cur.fetchone()
      stat=[]
      for i in range(3):
        if i==1:
          stat.append(0)
        stat.append(info[i])
      for i in range(6):
        stat.append(random.randint(info[i*2+3],info[i*2+4]))
      stat.append(info[15])
      for i in range(3):
        stat.append(None)
      stat.append(0)
      stat.append(info[16])   
      stat.append(info[18])
      cur.execute(f"INSERT INTO `user_wear` WHERE id={self.id} VALUES(NULL,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(stat))  
      con.commit()
      return info[0]
    return None
  def weapon(self):
    if self.get():
      cur=con.cursor()
      cur.execute(f"SELECT COUNT(*) FROM loot_table_weapon WHERE floor=%s",(self.floor))
      amount = cur.fetchone()
      amount=int(amount[0])
      if amount==0:
        return None
      amount = random.randint(0,amount-1)
      cur.execute(f"SELECT * FROM loot_table_weapon WHERE floor = %s LIMIT {amount}, 1",(self.floor))
      info = cur.fetchone()
      stat=[]
      for i in range(3):
        if i==1:
          stat.append(0)
        stat.append(info[i])
      for i in range(6):
        if i==5:
          stat.append(random.randint(info[i*2+3],info[i*2+4])/100)
        else:
          stat.append(random.randint(info[i*2+3],info[i*2+4]))
      for i in range(3):
        stat.append(None)
      stat.append(0)
      stat.append(info[16])
      cur.execute(f"INSERT INTO `user_weapon` WHERE id={self.id} VALUES(NULL,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(stat))  
      con.commit()
      return info[0]
    return None
  def get(self):
    if 10-random.randint(1,100)>=0:
      return True
    else: 
      return False

class Dungeon():
  def __init__(self,id,dic,floor):
    self.id=id
    self.dic=dic
    self.floor=floor
  def go(self):
    if self.id in self.dic and self.dic[self.id]:
      return self.dic,"이미 던전에 있어요!"
    self.dic[self.id]=True
    cur=con.cursor()
    cur.execute(f"SELECT COUNT(*) FROM enemy WHERE floor = {self.floor}")
    check = cur.fetchone()
    if int(check[0]) == 0:
      self.dic[self.id] = False # enter = True
      return self.dic,"몬스터를 만나지 못했어요!"
    return self.dic,None
  def stat(self):
    cur=con.cursor()
    cur.execute(f"SELECT COUNT(*) FROM enemy WHERE floor = {self.floor}")
    check=cur.fetchone()
    r=random.randint(0,int(check[0])-1)
    cur.execute(f"SELECT * FROM enemy WHERE floor = {self.floor} LIMIT {r}, 1")  
    enemy=cur.fetchone()
    cur.execute(f"SELECT str,hp,name,mp FROM user_stat WHERE id = %s",(self.id))
    stat=cur.fetchone()
    cur.execute(f"SELECT SUM(str),SUM(hp),SUM(mp) FROM `{self.id}_wear` WHERE wear=1 ")
    item=cur.fetchone()
    if not item[0] and not item[1] and not item[1]:
      item = (0,0,0)
    cur.execute(f"SELECT str,damage,mp FROM `{self.id}_weapon` WHERE wear = 1")
    weapon=cur.fetchone()
    if not weapon:
      weapon = (0,1,0)
    #if weapon[2] == None:
      #weapon=(0,1,1)
    #if item[2]==None:
      #item=(0,0,0)
    mp=item[2]+weapon[2]+stat[3]
    hp=Hp(int(stat[1])*5+50,item[1],0)
    damage=Damage(stat[0],item[0]+weapon[0],weapon[1],30)
    return self.dic,int(hp.display()),int(mp),damage,enemy
#인벤토리
class ItemInventory():
  def __init__(self,id,value):
    self.id = id
    self.value = value
  def item(self):
    cur=con.cursor()
    cur.execute(f"SELECT * FROM `user{self.value}` WHERE id={self.id}")
    items=cur.fetchall()
    return items
  def display(self,item):
    cur=con.cursor()
    item=list(item)
    if self.value=="_weapon":
      item.pop(0)
      cur.execute(f"SELECT * FROM `user{self.value}` WHERE wear = 1 AND id={self.id}")
      wearing = cur.fetchone()
      gap=["" for _ in range(13)]
      if wearing:
        wearing = list(wearing)
        wearing.pop(0)
        for i in range(4,13):
          if wearing[i] == None or item[i] == None:
            input=0
          elif i==9:
            input=round(item[i]-wearing[i],2)
          else:
            input=int(item[i])-int(wearing[i])
          if input>0:
            input=f"(+{input})"
          elif input==0:
            input=""
          else:
            input=f"({input})"
          gap[i]=input
      gap.insert(6,"")
      info=['이름','강화수치','등급','레벨제한','힘','민첩','\u200b','지능','행운','마나','데미지 배수','추가옵션','추가옵션','추가옵션']
      true=[True,True,True,False,True,True,True,True,True,True,False,True,True,True]
      url=item.pop()
      item.pop()
      item.insert(6,"\u200b")
    elif self.value=="_wear": 
      item.pop(0)
      cur.execute(f"SELECT * FROM `{self.id}{self.value}` WHERE wear = 1 AND part = {item[15]}")
      wearing = cur.fetchone()
      gap=["" for _ in range(15)]
      if wearing:
        wearing = list(wearing)
        for i in range(4,13):
          if i==9:
            input=0
          if wearing[i]==None or item[i]==None:
            input=0
          else:
            input=int(item[i])-int(wearing[i])
          if input>0:
            input=f"(+{input})"
          elif input==0:
            input=""
          else:
            input=f"({input})"
          gap[i]=input
      info =['이름','강화수치','등급','레벨제한','힘','민첩','지능','행운','체력',"마나",'컬렉션','추가옵션','추가옵션','추가옵션','착용부위']
      true =[True,True,True,False,True,True,True,True,True,True,False,True,True,True,False]
      url=item.pop()
      item.pop(-2)
      collection=Collection(item.pop(10),0)
      item.insert(10,collection.display())
      name=["","투구","티셔츠","벨트","장갑","보조무기","갑옷","하의","신발","반지1","반지2","목걸이","팔찌"]
      item.append(name[item.pop()])
    else:
      info =['아이템 코드','이름','갯수','판매가격','거래여부']
      true=[True,True,True,True,False]
      item[4]="거래가능" if item[4]==1 else "거래불가"
      url=item.pop()
      gap=None
    return info,true,url,item,gap