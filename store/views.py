from django.shortcuts import redirect, render, HttpResponse
from store.models import *
from cart.cart import Cart
import re
import json
from django.core.paginator import Paginator, EmptyPage
from django.http import JsonResponse
from django.template.loader import render_to_string




# Create your views here.

def index(request):
    cart = Cart(request)

    list_mi_products = []
    list_mi_note_products = []
    list_poco_products = []
    list_redmi_products = []
    list_redmi_note_products = []
    list_gaming_products = []
    list_all_products = []

    all_products = Product.objects.all().order_by('-price')
    
    # max_value = Product.objects.values_list('price').order_by('-price').last()    

    # Lọc
    categories = Category.objects.all()
    
    
    print(len(all_products))
    mi_products = Product.objects.filter(category_id = 1).order_by('-price')
    mi_note_products = Product.objects.filter(category_id = 2).order_by('-price')
    poco_products = Product.objects.filter(category_id = 3).order_by('-price')
    redmi_products = Product.objects.filter(category_id = 4).order_by('-price')
    redmi_note_products = Product.objects.filter(category_id = 5).order_by('-price')
    gaming_products = Product.objects.filter(category_id = 6).order_by('-price')
    # Lấy ra id của các categories
    list_id_categories  = []
    for name in categories.values_list():
        list_id_categories.append(name[0])
    
    list_id_categories = [0,] + list_id_categories

    # Bỏ các sản phẩm có giá là liên hệ
    for product in mi_products:
        if product.price != "Liênhệ":
            list_mi_products.append(product)

    for product in mi_note_products:
        if product.price != "Liênhệ":
            list_mi_note_products.append(product)

    for product in poco_products:
        if product.price != "Liênhệ":
            list_poco_products.append(product)

    for product in redmi_products:
        if product.price != "Liênhệ":
            list_redmi_products.append(product)
    
    for product in redmi_note_products:
        if product.price != "Liênhệ":
            list_redmi_note_products.append(product)
   
    for product in gaming_products:
        if product.price != "Liênhệ":
            list_gaming_products.append(product)
    
    for product in all_products:
        if product.price != "Liênhệ":
            list_all_products.append(product)

    # # Kiểm tra nếu là AJAX request
    # if request.is_ajax():
    #     products_name_data = [{'name': product.name, 'price': product.price} for product in all_products]
    #     return JsonResponse({
    #         'products': products_name_data,

    #     })
    
    
    return render(request, 'store/index.html', {
        'categories':categories,
        'products_all_10': list_all_products[:10],    
        'products_all_8': list_all_products[:8],
        'list_id_categories':list_id_categories,
        'mi_products':list_mi_products[:8],
        'mi_note_products':list_mi_note_products[:8],
        'poco_products':list_poco_products[:8],
        'redmi_products':list_redmi_products[:8],
        'redmi_note_products':list_redmi_note_products[:8],
        'gaming_products':list_gaming_products[:8],
        'cart':cart,

    })


def shop_grid(request, pk):
    cart = Cart(request)
    categories = Category.objects.all()
    all_products_no_contact = Product.objects.exclude(price__icontains='Liênhệ')
    min_value = Product.objects.exclude(price__icontains='Liênhệ').values_list('price').order_by('price')[0][0]
    max_value = Product.objects.exclude(price__icontains='Liênhệ').values_list('price').order_by('price')[len(all_products_no_contact) - 1][0]
    min_price = float(request.GET.get('min_price', min_value)) 
    max_price = float(request.GET.get('max_price', max_value))
    

    list_products = Product.objects.filter(price__range=(min_price, max_price)).order_by('price')
    products_count = list_products.count()
    if pk == 0: 
        products = Product.objects.all().order_by('name')
    else:
        products = Product.objects.filter(category_id = pk).order_by('name')
    
    # Các sản phẩm nổi bật
    list_feature_products = []
    feature_products = Product.objects.all().order_by('-price')
    for product in feature_products:
        if product.price != "Liênhệ":
            list_feature_products.append(product)


    print("Sản phẩm cuối cùng: %s"  %list_products.last())
    print("Min: %s" %min_price)
    print("Max: %s" %max_price)
    print("Số lượng sản phẩm: %s" %products_count)

    # Phân trang
    page = request.GET.get('page', 1)
    paginator = Paginator(list_products, 15)

    try:
        products_pager = paginator.page(page)
    except EmptyPage:
        products_pager = paginator.page(paginator.num_pages)
    
    return render(request, 'store/shop-grid.html',{
        'categories':categories,
        'products': products_pager,
        'total_products': products_count,
        'feature_products_1': list_feature_products[:3],
        'feature_products_2': list_feature_products[3:6],
        'list_products': list_products,
        'min_value':min_value,
        'max_value':max_value,
        'products_count': products_count,
        'cart':cart,
    })

# from django.http import JsonResponse
# from django.template.loader import render_to_string



def shop_details(request, pk):
    cart = Cart(request)
    categories = Category.objects.all()
    product = Product.objects.get(id = pk)
    id_subcategory = product.category_id


    
    # Hiển thị các sản phẩm liên quan
    related_products = Product.objects.filter(category_id = id_subcategory).exclude(id = pk).order_by('price')
    return render(request, 'store/shop-details.html',{
        'categories':categories,
        'product':product,
        'related_products': related_products[:12],
        'cart':cart
    })

# def shoping_cart(request):
#     categories = Category.objects.all()
#     return render(request, 'store/shoping-cart.html',
#     {
#         'categories':categories,
#     })


def contact(request):
    cart = Cart(request)
    categories = Category.objects.all()
    
    # successful_submit == False
    if request.POST.get('btnSend'):
        
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        # Khởi tạo class Contact
        contact = Contact(name = name, email = email, message = message)
        contact.save()
   
    return render(request, 'store/contact.html',{
        'categories':categories,
        'cart':cart,
    })



def search(request):
    cart = Cart(request)
    categories = Category.objects.all()
    title_search = ''
    if request.GET.get('keyword'):
        keyword = request.GET.get('keyword')
        # loại bỏ khoảng trắng nếu lỡ như có ai đó vô tình thêm khoảng trắng vào ô tìm kiếm
        keyword = re.sub(r'^\s+','', keyword.rstrip()) # rstring nhằm loại bỏ khoảng trắng ở cuối chuỗi
        objects = Product.objects.all().values()
        id_products = []
        for object in objects:
            object['content'] = re.sub(r'<[^<]+?>', '', object['content'])
            if keyword.lower() in object['name'].lower() or keyword.lower() in object['content'].lower():
                id_products.append(object['id'])
        else:
            products = Product.objects.filter(id__in = id_products).order_by('-price')
            title_search = 'CÓ %i SẢN PHẨM PHÙ HỢP VỚI KẾT QUẢ TÌM KIẾM: ' %(len(products)) + keyword
    return render(request, 'store/shop-grid.html',{
    'products':products,
    'title_search':title_search,
    'categories':categories,
    'keyword':keyword,
    'cart':cart,
})
