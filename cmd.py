import bpy
from bpy.types import (PropertyGroup , UIList , Operator)
import imp

from . import utils
imp.reload(utils)


#アイテム-------------------------------------------------------
#ItemPropertyはリストのに登録される一つのアイテムを表している

#リストからアイテムを取得
def get_item(self):
    return self["name"]

#リストに選択を登録する
def set_item(self, value):
    self["name"] = value

def showhide(self, value):
    ob = utils.getActiveObj()
    for mod in ob.modifiers :
            if mod.name == self["name"]:
                mod.show_viewport = self["bool_val"]


#---------------------------------------------------------------------------------------
def reload():
    ui_list = bpy.context.window_manager.kiamodifierlist_list
    itemlist = ui_list.itemlist

    clear()
    ob =utils.getActiveObj()

    for mod in ob.modifiers:
        item = itemlist.add()
        item.name = mod.name
        item.bool_val = mod.show_viewport
        ui_list.active_index = len(itemlist) - 1


def clear():
    ui_list = bpy.context.window_manager.kiamodifierlist_list
    itemlist = ui_list.itemlist    
    itemlist.clear()

#---------------------------------------------------------------------------------------
#リストのモディファイヤを探しだし、リストでの順位とモディファイヤの順位を比較する
#その差を出してmove_upで順番を変更する
#---------------------------------------------------------------------------------------
def move(type):
    ui_list = bpy.context.window_manager.kiamodifierlist_list
    itemlist = ui_list.itemlist
    index = ui_list.active_index

    if len(itemlist) < 2:
        return

    if type == 'UP':
        v = index -1
    elif type == 'DOWN':
        v = index + 1
    elif type == 'TOP':
        v = 0
    elif type == 'BOTTOM':
        v = len(itemlist) - 1


    itemlist.move(index, v)
    ui_list.active_index = v

    ob =utils.getActiveObj()

    for order_list,listitem in enumerate(itemlist):
        for order,mod in enumerate(ob.modifiers):
            
            if mod.name == listitem.name:
                if (order_list < order):
                    for i in range(order - order_list):
                        bpy.ops.object.modifier_move_up(modifier = mod.name )



#---------------------------------------------------------------------------------------
#選択されたモディファイヤをapply
#apply remove を1つの関数で扱うように変更
#---------------------------------------------------------------------------------------
def apply(mode):
    props = bpy.context.scene.kiamodifierlist_props
    props.handler_through = True

    ui_list = bpy.context.window_manager.kiamodifierlist_list
    itemlist = ui_list.itemlist
    active_index = ui_list.active_index

    if len(itemlist) == 0:
        return
    indexarray = []

    for index , mod in enumerate(itemlist):
        if mode == 0:# apply active index
            if active_index == index:
                bpy.ops.object.modifier_apply( modifier = mod.name )    

        elif mode == 1:# apply checked
            if mod.bool_val:
                bpy.ops.object.modifier_apply( modifier = mod.name )    
                indexarray.append(index)

        elif mode == 2:# remove active index
            if active_index == index:
                bpy.ops.object.modifier_remove( modifier = mod.name )

        elif mode == 3:#remove checked
            if mod.bool_val:
                bpy.ops.object.modifier_remove( modifier = mod.name )
                indexarray.append(index)

    reload()
    if len(itemlist)-1 < active_index:
        ui_list.active_index = len(itemlist)-1

    props.handler_through = False
