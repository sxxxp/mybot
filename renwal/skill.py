# -*- coding: utf-8 -*-
import pymysql
import os
con=pymysql.connect(user=os.environ['user'],password=os.environ['password'],host=os.environ["host"],charset="utf8",database=os.environ["database"])
class Skill():
  def __init__(self,id):
    self.id=id
  def fight(self,effect,value):
    effect_list=["blood","stun","None","fire","ice"]
    name_list=["🩸","💫","","🔥","❄"]
    return name_list[effect_list.index(effect)],f"x{value}"
  def fighteffect(self,effect,myhp,mydamage,enemyhp,enemydamage):
    cur=con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS effect(skill_name TEXT PRIMARY KEY, skill_effect TEXT, skill_value INTEGER)")
    #cur.execute("INSERT INTO effect VALUES(%s,%s,%s)",("blood","damage","5"))
    con.commit()
    cur.execute("SELECT * FROM effect WHERE skill_name = %s",(effect))
    info=cur.fetchone()
    if info[1]=="damage":
      enemyhp-=info[2]
    elif info[1]=="stun":
      myhp+=enemydamage
    return myhp,info[2],enemyhp,enemydamage,info[1]
  def display(self,index):
    cur=con.cursor()
    cur.execute(f"SELECT * FROM `{self.id}_skill` LIMIT {index},1")
    return cur.fetchone()
  def select(self):
    cur=con.cursor()
    cur.execute(f"SELECT skill_name,skill_level,skill_maxlevel,skill_requirelevel FROM `{self.id}_skill`")
    return cur.fetchall()
  def require(self,index):
    cur=con.cursor()
    cur.execute("SELECT skill_point FROM user_stat WHERE id = %s",(self.id))
    point=cur.fetchone()[0]
    cur.execute(f"SELECT skill_point,skill_level,skill_maxlevel FROM `{self.id}_skill` LIMIT {index},1")
    skill=cur.fetchone()
    if point<skill[0]:
      return True
    elif skill[1]==skill[2]:
      return True
    else:
      return False
  def isSkill(self):
    cur=con.cursor()
    cur.execute("SELECT class FROM user_data WHERE id = %s",(self.id))
    clas=cur.fetchone()[0]
    cur.execute("SELECT * FROM skill WHERE skill_class = %s AND skill_level = 0",(clas))
    skill=cur.fetchall()
    skill=list(skill)
    cur.execute(f"SELECT skill_id FROM `{self.id}_skill`")
    primarykey=cur.fetchall()
    if primarykey:
      for i in range(len(primarykey)):
        j=0
        if primarykey[i][0] in skill[j]:
          del skill[j]
        else:
          j+=1    
    skill=tuple(skill)
    cur.executemany(f"INSERT INTO `{self.id}_skill` VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(skill))
    con.commit()
  def canskill(self):
    cur=con.cursor()
    cur.execute(f"SELECT skill_name,skill_mana,skill_hp FROM `{self.id}_skill` WHERE skill_level != 0 ")
    getSkill=cur.fetchall()
    if not len(getSkill):
      return True
    else:
      return False
class skillModify():
  def __init__(self,id):
    self.id=id
  def effect(self,value):
    effect=['blood','stun','None',]
    name=['출혈','기절','없음']   
    if effect.index(value)>-1:
      return name[effect.index(value)]
    else:
      return value
  def upgrade(self,id,level,point):
    print(point)
    cur=con.cursor()
    cur.execute(f"UPDATE user_stat SET skill_point=skill_point-{point} WHERE id = %s ",(self.id))
    con.commit()
    cur.execute(f"SELECT skill_point FROM user_stat WHERE id = %s",self.id)
    p=cur.fetchone()[0]
    print(p)
    cur.execute(f"SELECT * FROM skill WHERE skill_id = %s AND skill_level = %s ",(id,level+1))
    info=list(cur.fetchone())
    cur.execute(f"DELETE FROM `{self.id}_skill` WHERE skill_id = %s",(id))
    cur.execute(f"INSERT INTO `{self.id}_skill` VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(info))
    con.commit()
    return p
