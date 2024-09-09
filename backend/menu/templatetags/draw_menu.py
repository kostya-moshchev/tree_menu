from django import template
from menu.models import MenuItem
from django.urls import resolve

register = template.Library()

def build_menu_tree(menu_items, active_item, open_items):
    """Рекурсивно строит дерево меню с учетом активного элемента"""
    menu_tree = []
    for item in menu_items:
        is_open = item in open_items or item == active_item
        menu_tree.append({
            'item': item,
            'child_items': build_menu_tree(item.children.all(), active_item, open_items) if is_open else [],
            'is_active': item == active_item,
            'is_open': is_open
        })
    return menu_tree

def get_active_and_open_items(menu_items, current_url):
    """Находит активный элемент и его родителей для раскрытия"""
    active_item = None
    open_items = set()

    for item in menu_items:
        print(item.get_url())
        if '/' + str(item.get_url()) + '/' == current_url:
            active_item = item
            break

    if active_item:
        parent = active_item.parent
        while parent:
            open_items.add(parent)
            parent = parent.parent

    return active_item, open_items

@register.inclusion_tag('menu/draw_menu.html', takes_context=True)
def draw_menu(context, menu_name):
    """Создает меню с заданным именем из шаблона"""
    current_url = context['request'].path
    print(current_url)
    menu_items = MenuItem.objects.filter(menu_name=menu_name).prefetch_related('children')
    active_item, open_items = get_active_and_open_items(menu_items, current_url)
    menu_tree = build_menu_tree(menu_items.filter(parent__isnull=True), active_item, open_items)
    return {'items': menu_tree}
