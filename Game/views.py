from django.shortcuts import redirect,render
from django.views.generic import TemplateView,View
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
import random
from Game.forms import AttackF

from User.models import Armor, Enemy, Newuser, Weapon

class Location1(LoginRequiredMixin,TemplateView):
    template_name='BK/home.html'

class Location2(LoginRequiredMixin,TemplateView):
    template_name='BK/loc_2.html'

class SleepRoom(LoginRequiredMixin,TemplateView):
    template_name='BK/sleep.html'

class Sleepes(LoginRequiredMixin,TemplateView):
    template_name="BK/sleep_mes.html"

def Sleeping(request,pk):
    user = Newuser.objects.get(pk=pk)
    if request.user.pk == user.pk:
        if user.health == 100:
            return redirect('sleep')
        else:
            if user.balance < 30:
                return redirect('sleep')
            else:
                user.balance -= 30
                user.health = 100
                user.save()
        return redirect('sleeped')
    else:
        return redirect('sleep')
    
class Location3(LoginRequiredMixin, TemplateView):
    template_name="BK/loc_3.html"

class Shop(LoginRequiredMixin, TemplateView):
    template_name="BK/shop.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["weapons"] = Weapon.objects.all()
        context['armors'] = Armor.objects.all()
        return context

def buyweapon(request,weapon):
    weapon = Weapon.objects.get(pk=weapon)
    user = request.user
    if user.balance>=weapon.balance:
        if user.weapon==weapon:
            return render(request,'BK/shop_err.html')
        else:
            user.balance -= weapon.balance
            user.weapon = weapon
            user.save()
    else:
        return render(request,'BK/shop_err.html')
    return redirect('success_b')

def buyarmor(request,armor):
    armor = Armor.objects.get(pk=armor)
    user = request.user
    if user.balance>=armor.balance:
        if user.armor==armor:
            return render(request,'BK/shop_err.html')
        else:
            user.balance -= armor.balance
            user.armor = armor
            user.save()
    else:
        return render(request,'BK/shop_err.html')
    return redirect('success_b')

class SuccesBuy(LoginRequiredMixin,TemplateView):
    template_name='BK/success_buy.html'

class Location4(LoginRequiredMixin,TemplateView):
    template_name='BK/loc_4.html'

class Dungeon(LoginRequiredMixin,View):
    def get(self,request,*args, **kwargs):
        if request.user.dungeon_loc == 3:
            request.user.health = 0
            request.user.dungeon_loc = 0
            request.user.is_fight = 0
            request.user.save()
            if request.user.enemy is not None:    
                enemy = Enemy.objects.get(slug=request.user.username)
                enemy.delete()
            return render(request,'BK/dungeon.html')
        else:
            return render(request,'BK/dungeon.html')

class DungeonGo(LoginRequiredMixin,View):

    def get(self,request,*args, **kwargs):
        if request.user.dungeon_loc == 3:
            request.user.health = 0
            request.user.dungeon_loc = 0
            request.user.is_fight = False
            request.user.save()
            if request.user.enemy is not None:    
                enemy = Enemy.objects.get(slug=request.user.username)
                enemy.delete()
        if request.user.health<10:
            return redirect('dungeon')
        select = random.randint(1,100)
        if select<=40:
            request.user.dungeon_loc = 1
            request.user.save()
            return redirect('dun_loc1')
        elif select>40 and select<=70:
            request.user.dungeon_loc = 2
            request.user.save()
            return redirect('dun_loc2')
        else:
            request.user.dungeon_loc = 3
            request.user.save()
            return redirect('dun_loc3')

class Dungeon_Loc1(LoginRequiredMixin,View):

    def get(self,request,*args, **kwargs):
        if request.user.dungeon_loc == 3:
            request.user.health = 0
            request.user.dungeon_loc = 0
            request.user.is_fight = False
            request.user.save()
            if request.user.enemy is not None:    
                enemy = Enemy.objects.get(slug=request.user.username)
                enemy.delete()    
        if self.request.user.dungeon_loc == 1:
            return render(request,'BK/dun1.html')
        else:
            self.request.user.dungeon_loc = 0
            self.request.user.save()
            return redirect('dungeon')


class Dungeon_Loc2(LoginRequiredMixin,View):
    
    def get(self,request,*args, **kwargs):   
        if request.user.dungeon_loc == 3:
            request.user.health = 0
            request.user.dungeon_loc = 0
            request.user.is_fight = False
            request.user.save() 
            if request.user.enemy is not None:    
                enemy = Enemy.objects.get(slug=request.user.username)
                enemy.delete()
        if self.request.user.dungeon_loc == 2:
            return render(request,'BK/dun2.html')
        else:
            self.request.user.dungeon_loc = 0
            self.request.user.save()
            return redirect('dungeon')


class Dungeon_Loc3(LoginRequiredMixin,View):
    def get(self,request,*args, **kwargs):    
        if self.request.user.dungeon_loc == 3:
            return render(request,'BK/dun3.html')
        else:
            self.request.user.dungeon_loc = 0
            self.request.user.save()
            return redirect('dungeon')

class PayBadGuys(LoginRequiredMixin,View):
    def get(self,request,*args, **kwargs):
        pay = random.randint(0,100)
        if self.request.user.balance>pay:    
            self.request.user.balance -= pay
            self.request.user.dungeon_loc = 0
            self.request.user.save()
        else:
            return render(request,'BK/pay_err.html',context={'price':pay}) 
        return render(request,'BK/payed.html',context={'price':pay})    

class TakeTreasure(LoginRequiredMixin,View):
    def get(self,request,*args, **kwargs):
        if request.user.dungeon_loc == 2:
            pay = 0
            damage = random.randint(0,15)
            if request.user.dungeon_lvl <= 3:
                pay = random.randint(50,100)
            elif request.user.dungeon_lvl > 3 and request.user.dungeon_lvl <= 9:
                pay = random.randint(100,200)
            elif request.user.dungeon_lvl > 9:
                pay = random.randint(300,500)
            request.user.balance += pay
            request.user.dungeon_loc = 0
            request.user.health -= damage
            request.user.save()
            return render(request,'BK/success_take.html',context={'price':pay})
        else:
            return redirect('dungeon')

class Fight(LoginRequiredMixin,UserPassesTestMixin,View):

    def get(self,request,*args, **kwargs):
        form_class = AttackF()
        if request.user.is_fight==False:
            request.user.is_fight = True
            rnd = random.randint(1,3)
            if request.user.dungeon_lvl <= 3:
                enemy = Enemy.objects.create(name="Bad Guy",attack=5,defence=2,lvl=1,slug=request.user.username)
            elif request.user.dungeon_lvl > 3 and request.user.dungeon_lvl <= 9:
                enemy = Enemy.objects.create(name="Bad Guy_2",attack=10,defence=8,lvl=2,slug=request.user.username,weapon=Weapon.objects.get(pk=2),armor=Armor.objects.get(pk=2))
            elif request.user.dungeon_lvl > 9:
                enemy = Enemy.objects.create(name="Bad Guy_3",attack=30,defence=25,lvl=3,slug=request.user.username,weapon=Weapon.objects.get(pk=4),armor=Armor.objects.get(pk=4))
            request.user.enemy = enemy
            request.user.save()
            return render(request,'BK/fight.html',context={'enemy':enemy,'form':form_class})
        else:
            enemy = Enemy.objects.get(slug=request.user.username)
            if request.user.health <= 0:
                request.user.dungeon_loc = 0
                request.user.is_fight = False
                if enemy.health >= 100:
                    request.user.dungeon_lvl -= 1
                self.request.user.save()          
                enemy.delete()
                return redirect('loc1')
            elif enemy.health <= 0:
                request.user.is_fight = False
                request.user.dungeon_loc = 0
                request.user.exp += random.randint(15,30)
                request.user.balance += random.randint(20,50)
                if request.user.health >= 100:
                    request.user.dungeon_lvl += 1
                self.request.user.save()
                enemy.delete()
                return redirect('dungeon_go')
            return render(request,'BK/fight.html',context={'enemy':enemy,'form':form_class})
    
    def post(self,request,*args, **kwargs):
        enemy = Enemy.objects.get(slug=request.user.username)
        if request.user.health <= 0:
            request.user.health = 0
            request.user.dungeon_loc = 0
            request.user.is_fight = False
            if enemy.health >= 100:
                    request.user.dungeon_lvl -= 1
            self.request.user.save()
            enemy.delete()
            return redirect('loc1')
        elif enemy.health <= 0:
            request.user.is_fight = False
            request.user.dungeon_loc = 0
            request.user.exp += random.randint(15,30)
            request.user.balance += random.randint(20,50)
            if request.user.health >= 100:
                request.user.dungeon_lvl += 1
            self.request.user.save()
            enemy.delete()
            return redirect('dungeon_go')
        choic = {0:'head',1:'body',2:'lags'}
        selat = random.randint(0,2)
        seldef = random.randint(0,2)
        if request.POST['attack'] == choic[seldef]:
            pass
        else:
            if request.user.ReturnAllDamage() - (int(enemy.ReturnAllArmor()/2))>=0:    
                enemy.health -= request.user.ReturnAllDamage() - (int(enemy.ReturnAllArmor()/2))
                enemy.save()
            else:
                pass
        if request.POST['defence'] == choic[selat]:
            pass
        else:
            if enemy.ReturnAllDamage() - (int(request.user.ReturnAllArmor()/2))>=0:
                request.user.health -= enemy.ReturnAllDamage() - (int(request.user.ReturnAllArmor()/2))
                request.user.save()
            else:
                pass
        return redirect('fight',self.kwargs['pk'])


    
    def test_func(self):
        user = Newuser.objects.get(pk=self.kwargs['pk'])
        return self.request.user==user