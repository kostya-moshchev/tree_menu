from django import template
from typing import List, Dict, Optional, Set, Tuple, Any

from menu.models import MenuItem


register = template.Library()


def build_menu_tree(menu_items: List[MenuItem],
                    active_item: Optional[MenuItem],
                    open_items: Set[MenuItem]) -> List[Dict[str, Any]]:
    """Рекурсивно строит дерево меню с учетом активного элемента"""
    menu_tree = []
    for item in menu_items:
        is_open = item in open_items or item == active_item
        menu_tree.append({
            'item': item,
            'child_items': build_menu_tree(
                item.children.all(), active_item, open_items
            ) if is_open else [],
            'is_active': item == active_item,
            'is_open': is_open
        })
    return menu_tree


def get_active_and_open_items(
        menu_items: List[MenuItem], current_url: str
) -> Tuple[Optional[MenuItem], Set[MenuItem]]:
    """Находит активный элемент и его родителей для раскрытия"""
    active_item = None
    open_items = set()

    for item in menu_items:
        if str(item.get_url()).strip('/') == current_url.strip('/'):
            active_item = item
            break

    if active_item:
        parent = active_item.parent
        while parent:
            open_items.add(parent)
            parent = parent.parent
    print(type(active_item))
    return active_item, open_items


@register.inclusion_tag('menu/draw_menu.html', takes_context=True)
def draw_menu(context: Dict[str, Any], menu_name: str) -> Dict[str, Any]:
    """Создает меню с заданным именем из шаблона"""
    current_url = context['request'].path
    menu_items = MenuItem.objects.filter(menu_name=menu_name
                                         ).prefetch_related('children')
    active_item, open_items = get_active_and_open_items(
        menu_items, current_url)
    menu_tree = build_menu_tree(menu_items.filter(parent__isnull=True),
                                active_item, open_items)
    return {'items': menu_tree}
