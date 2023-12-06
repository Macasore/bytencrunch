# from .cart import add_to_cart_handler
# from .search import search_handlerfrom .checkout import check_out_handler, direct_transfer_handler, confirm_direct_transfer 
from .user import edit_room_handler
from .complaint import complaint_handler
from .start import start_handler, setup_user_handler, back_to_home
from .browse_vendors import browse_vendor_handler, browse_vendor_ext_handler
from .browse_food import browse_product_handler, browse_product_ext_handler
from .cart import add_to_cart_handler, cart_quantity_handler, confirm_cart, manage_cart_handler , edit_cart_handler
from .payment import flutterwave_payment_handler
from .checkout import check_out_handler, direct_transfer_handler,confirm_direct_transfer_handler

all_handlers = [
    #user handlers
    edit_room_handler,

    # Start up Handlers
    start_handler,
    setup_user_handler,
    back_to_home,

    # Vendor Handlers
    browse_vendor_handler,
    browse_vendor_ext_handler,

    #complaint
    complaint_handler,
    
    #Product handlers
    browse_product_handler,
    browse_product_ext_handler,

    #Cart   
    add_to_cart_handler,
    cart_quantity_handler,
    confirm_cart,
    manage_cart_handler,
    edit_cart_handler,

    #checkout
    check_out_handler,
    direct_transfer_handler,
    confirm_direct_transfer_handler,
    
    #flutterwave
    flutterwave_payment_handler,

]
