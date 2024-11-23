from django.shortcuts import render,redirect, get_object_or_404
from cart.cart import Cart
from customer.models import Customer
from store.models import *
from cart.models import *
from cart.forms import FormOrder
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from XiaomiStore.settings import EMAIL_HOST_USER
from django.core.mail import send_mail, EmailMultiAlternatives
import json
from django.http import JsonResponse

# Create your views here.

def apply_coupon(cart, coupon_code):
    list_ma_giam_gia = {
        "Python": 0.7,
        "Django": 0.8,
    }
    giam_gia = list_ma_giam_gia.get(coupon_code, 1)  # Mặc định là 1 nếu mã không hợp lệ
    print(giam_gia)
    cart_new = {}
    for c in cart:
        product_cart = {
            str(c["product"].pk): {
                "quantity": c["quantity"],
                "price": str(c["product"].price),
                "coupon": str(giam_gia),
            }
        }
        cart_new.update(product_cart)
        c["coupon"] = giam_gia

    return cart_new, giam_gia



def update_cart(cart, data):
    """
    Cập nhật giỏ hàng dựa trên dữ liệu được gửi.
    """
    cart_new = {}
    for c in cart:  # Duyệt qua giỏ hàng hiện tại
        quantity_key = f"quantity2{c['product'].pk}"
        quantity_new = int(data.get(quantity_key, c["quantity"]))

        if quantity_new == 0:
            # Xóa sản phẩm nếu số lượng bằng 0
            cart.remove(c["product"])
        else:
            # Cập nhật sản phẩm với số lượng mới
            product_cart = {
                str(c["product"].pk): {
                    "quantity": quantity_new,
                    "price": str(c["product"].price),
                    "coupon": str(c.get("coupon", 1)),
                }
            }
            cart_new.update(product_cart)
            c["quantity"] = quantity_new

    return cart_new



##### Giữ lại
def cart_detail(request):
    categories = Category.objects.all()
    cart = Cart(request)
    discount_price = 0

    # Kiểm tra nếu là AJAX request
    if request.headers.get("x-requested-with") == "XMLHttpRequest" and request.method == "POST":
        data = json.loads(request.body)
        
        # Xử lý áp dụng mã giảm giá
        if data.get("btnMaGiamGia"):
            ma_giam_gia = data.get("ma_giam_gia", "").strip()
            cart_new, giam_gia = apply_coupon(cart, ma_giam_gia)
            request.session["cart"] = cart_new

            # Tính lại tổng giá sau giảm giá
            original_price = float(sum(float(item["price"]) * item["quantity"]  for item in cart))
            discount_price = float(sum(float(item["price"]) * item["quantity"] * (1 - float(item["coupon"])) for item in cart))
            total_price = original_price - discount_price
            

            return JsonResponse({
                "success": giam_gia < 1,
                "discount_rate": giam_gia,
                "original_price": original_price,
                "discount_price": discount_price,
                "total_price": total_price,
                "message": "Áp dụng mã thành công!" if giam_gia < 1 else "Mã giảm giá không hợp lệ.",
            })
    
    # Xử lý request thông thường
    if request.method == "POST":
        # Xử lý cập nhật giỏ hàng (nếu không phải AJAX request)
        if "btnCapNhat" in request.POST:
            cart_new = update_cart(cart, request.POST)
            request.session["cart"] = cart_new


    return render(request, "store/shoping-cart.html", {
        "cart": cart,
        "categories": categories,
        "ma_giam_gia": '',
        
    })


# def cart_detail(request):
#     categories = Category.objects.all()
#     cart = Cart(request)

#     # Kiểm tra nếu là AJAX request
#     if request.headers.get("x-requested-with") == "XMLHttpRequest" and request.method == "POST":
#         data = json.loads(request.body)

#         # Xử lý áp dụng mã giảm giá
#         if data.get("btnMaGiamGia"):
#             ma_giam_gia = data.get("ma_giam_gia", "").strip()
#             cart_new, giam_gia = apply_coupon(cart, ma_giam_gia)
#             request.session["cart"] = cart_new

            

#             # Tính lại tổng giá sau giảm giá
#             total_price = sum(float(item["price"]) * item["quantity"] * float(item["coupon"]) for item in cart)
#             discount_price = sum(float(item["price"]) * item["quantity"] * (1 - float(item["coupon"])) for item in cart)

#             # Lưu thông tin mã giảm giá vào session
#             request.session["discount"] = {
#                 "code": ma_giam_gia,
#                 "rate": giam_gia,
#                 "discount_price": discount_price
#             }

#             return JsonResponse({
#                 "success": giam_gia < 1,
#                 "discount_rate": giam_gia,
#                 "discount_price": discount_price,
#                 "total_price": total_price,
#                 "message": "Áp dụng mã thành công!" if giam_gia < 1 else "Mã giảm giá không hợp lệ.",
#             })

#     # Xử lý request thông thường
#     if request.method == "POST":
#         # Xử lý cập nhật giỏ hàng (nếu không phải AJAX request)
#         if "btnCapNhat" in request.POST:
#             cart_new = update_cart(cart, request.POST)
#             request.session["cart"] = cart_new

            
#             if "discount" in request.session:
#                 print(request.session["discount"])
#                 del request.session["discount"]
                

#             # Đặt lại giá trị giảm giá trong view
#             giam_gia = 1  # Không áp dụng giảm giá
#             discount_price = 0
#             total_price = sum(float(item["price"]) * item["quantity"] for item in cart)


#     # Kiểm tra mã giảm giá trong session khi tải lại trang
#     discount_info = request.session.get("discount", None)
#     if discount_info:
#         giam_gia = discount_info.get("rate", 1)
#         ma_giam_gia = discount_info.get("code", "")
#         discount_price = sum(
#             float(item["price"]) * item["quantity"] * (1 - giam_gia) for item in cart
#         )
#         total_price = sum(
#             float(item["price"]) * item["quantity"] * giam_gia for item in cart
#         )
#     else:
#         giam_gia = 1
#         ma_giam_gia = ""
#         discount_price = 0
#         total_price = sum(float(item["price"]) * item["quantity"] for item in cart)

#     return render(request, "store/shoping-cart.html", {
#         "cart": cart,
#         "categories": categories,
#         "ma_giam_gia": ma_giam_gia,
#         "discount_price": discount_price,
#         "total_price": total_price,
#     })


@require_POST
def buy_now(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id = product_id)
    if request.POST.get('quantity'): # 1
        cart.add(product, int(request.POST.get('quantity')))
    return redirect('cart:cart_detail')


@require_POST
def remove_cart(request,product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id = product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')

# @login_required
# def cart_add(request, id):
#     cart = Cart(request)
#     product = Product.objects.get(id=id)
#     if request.POST.get('quantity'):
#         cart.add(product=product)
#     return redirect("store:index")

def checkout(request):
    categories = Category.objects.all()
    cart = Cart(request)

    # Kiểm tra trạng thái đăng nhập của khách hàng
    if 'session_KhachHang' not in request.session:
        return redirect('shop:shop_detail')

    # Thực hiện đặt hàng
    form_order =  FormOrder()
    if request.POST.get('btnDatHang'):
        form_order = FormOrder(request.POST, OrderConfirm)
        if form_order.is_valid():
            request.POST._mutable = True
            post = form_order.save(commit=False)
            post.first_name = form_order.cleaned_data['first_name']
            post.last_name = form_order.cleaned_data['last_name']
            post.address = form_order.cleaned_data['address']
            post.email = form_order.cleaned_data['email']
            post.tel = form_order.cleaned_data['tel']
            post.save()
        # Lấy thông tin khách hàng(người đặt hàng)
        customer = Customer.objects.get(pk = request.session.get('session_KhachHang')['id'])
        # Order
        order = Order()
        order.total = cart.get_final_total_price()
        order.customer = customer
        order.save()

        # OrderItem
        for c in cart:
            OrderItem.objects.create(order=order,
            product= c['product'],
            price = c['price'],
            quantity = c['quantity'])

        # Gửi mail
        # Có định dạng html
        message = '''<b>Cảm ơn bạn đã mua điện thoại ở cửa hàng chúng tôi. 
        Đơn hàng của bạn sẽ được vận chuyển trong thời gian sớm nhất:</b><br>'''
        for c in cart:
            if len(cart) > 1:
                message += c['product'].name + '. ' + 'Số lượng: ' + str(c['quantity'])
                message += '<br>'
            else:
                message += c['product'].name + '. ' + 'Số lượng: ' + str(c['quantity'])
                message += '<br>'

        message += '<b> - Tổng số tiền bạn phải thanh toán là: </b>' + str(cart.get_final_total_price()) + ' đ'
        subject = 'Xác nhận đơn hàng'
        msg = EmailMultiAlternatives(subject, message, EMAIL_HOST_USER, [request.session.get('session_KhachHang')['email']])
        msg.attach_alternative(message, 'text/html')
        msg.send()

        # Xóa session cart khi đặt hàng thành công
        cart.clear()

        return render(request, 'cart/result.html', {
            'cart':cart,
        })
    return render(request, 'store/checkout.html',{
        'categories':categories,
        'cart':cart,
        'form_order':form_order,
    }
    )

