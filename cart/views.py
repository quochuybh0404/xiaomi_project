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

# Create your views here.

def cart_detail(request):
    categories = Category.objects.all()
    cart = Cart(request)

    # Mã giảm giá
    list_ma_giam_gia = [
        {
        'thập tứ a ca': 0.86
        },

        {
            'linh14': 0.86
        },

        {
            'vùng đất cấm': 0.88
        },

        {
            'tiên lũ': 0.7
        }]
    ma_giam_gia = ''
    giam_gia = 1
    if request.POST.get('btnMaGiamGia'):
        ma_giam_gia = request.POST.get('ma_giam_gia')
        for dict_ma_giam_gia in list_ma_giam_gia:
            if ma_giam_gia in dict_ma_giam_gia:
                cart_new = {}
                giam_gia = dict_ma_giam_gia[ma_giam_gia]
                for c in cart: # Duyệt giỏ hàng đang có
                    product_cart = {
                        str(c['product'].pk) : {
                                    'quantity': c['quantity'],
                                    'price': str(c['product'].price),
                                    'coupon': str(giam_gia)
                                }
                    }
                    cart_new.update(product_cart)
                    # Giữ lại số lượng mới trên ô tại thời điểm click nút
                    c['coupon'] = dict_ma_giam_gia[ma_giam_gia]
                else:
                    # Cập nhật session giỏ hàng(cart)
                    request.session['cart'] = cart_new
                break
        else:
            cart_new = {}
            giam_gia = 1
            for c in cart: # Duyệt giỏ hàng đang có
                product_cart = {
                    str(c['product'].pk) : {
                                'quantity': c['quantity'],
                                'price': str(c['product'].price),
                                'coupon': str(giam_gia)
                            }
                }
                cart_new.update(product_cart)
                # Giữ lại số lượng mới trên ô tại thời điểm click nút
                c['coupon'] = giam_gia
            else:
                request.session['cart'] = cart_new

    # Trường hợp này là để khi ai đó muốn tăng giảm sản phẩm rồi bấm vào cập nhật giỏ hàng thì sẽ bị load lại trang
    # Khi đó sẽ ko còn mã coupoun lúc đó giá tiền giảm trở về 0.
    else:
        cart_new = {}
        giam_gia = 1
        for c in cart: # Duyệt giỏ hàng đang có
            product_cart = {
                str(c['product'].pk) : {
                            'quantity': c['quantity'],
                            'price': str(c['product'].price),
                            'coupon': str(giam_gia)
                        }
            }
            cart_new.update(product_cart)
            # Giữ lại số lượng mới trên ô tại thời điểm click nút
            c['coupon'] = giam_gia
        else:
            request.session['cart'] = cart_new

    # Cập nhật giỏ hàng
    if request.POST.get('btnCapNhat'):
        cart_new = {}
        for c in cart: # Duyệt giỏ hàng đang có
            quantity_new = int(request.POST.get('quantity2'+ str(c['product'].pk)))
            if quantity_new == 0:
                cart.remove(c['product'])
            else:
                product_cart = {
                    str(c['product'].pk) : {
                                'quantity': quantity_new,
                                'price': str(c['product'].price),
                                'coupon': str(c['coupon'])
                            }
                }
                cart_new.update(product_cart)
            #Giữ lại số lượng mới trên ô tại thời điểm click nút
            c['quantity'] = quantity_new
        # Cập nhật session giỏ hàng(Cart)
        request.session['cart'] = cart_new


    return render(request, 'store/shoping-cart.html',{
        'cart':cart,
        'categories':categories,
        'ma_giam_gia':ma_giam_gia,
    })


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

