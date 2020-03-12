from kivy.app import App
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
import db


class MainWindow(Screen):
    def btn(self):
        self.wrong_pass_popup()

    def wrong_pass_popup(self):
        wrong_pass_window = Popup(title="Error!", content=Label(text="Incorrect Email or Password!"),
                                  size_hint=(None, None), size=(400, 400))
        wrong_pass_window.open()

    def user_finder(self, email, nickname, password):
        person_nickname = db.find_user(email, nickname, password)
        if person_nickname == 0 or person_nickname is None:
            return 0
        else:
            kind = db.kind_finder(nickname)
            if kind == "seller":
                SellerWindow.person_email = email
                SellerWindow.person_nickname = nickname
                SellerWindow.person_pass = password
            elif kind == "buyer":
                BuyerWindow.person_nickname = person_nickname
                GetLinksButton.person_nickname = nickname
                Bucket.person_nickname = nickname
                Payment.person_nickname = nickname
                Rate.person_nickname = nickname
            return kind
    def rgba(self, red, green, blue, alpha):
        return rgba_returner(red, green, blue, alpha)


class Statistics(Screen):
    def rgba(self, red, green, blue, alpha):
        return rgba_returner(red, green, blue, alpha)

    def statistic_find(self, key):
        if key == 0:
            result = db.statistic_finder(key, "all")
            return f"Count Of Tables And Views = {result[0]}"
        elif key == 1:
            result = db.statistic_finder(key, "backup_bucket")
            return f"Count Of Records in backup_bucket = {result[0]}"
        elif key == 2:
            result = db.statistic_finder(key, 'bucket')
            return f"Count Of Records in bucket = {result[0]}"
        elif key == 3:
            result = db.statistic_finder(key, 'buyer')
            return f"Count Of Records in buyer = {result[0]}"
        elif key == 4:
            result = db.statistic_finder(key, 'category')
            return f"Count Of Records in category = {result[0]}"
        elif key == 5:
            result = db.statistic_finder(key, 'creditcard')
            return f"Count Of Records in creditcard = {result[0]}"
        elif key == 6:
            result = db.statistic_finder(key, 'eft')
            return f"Count Of Records in eft = {result[0]}"
        elif key == 7:
            result = db.statistic_finder(key, 'payment')
            return f"Count Of Records in payment = {result[0]}"
        elif key == 8:
            result = db.statistic_finder(key, 'paypal')
            return f"Count Of Records in paypal = {result[0]}"
        elif key == 9:
            result = db.statistic_finder(key, 'person')
            return f"Count Of Records in person = {result[0]}"
        elif key == 10:
            result = db.statistic_finder(key, 'product')
            return f"Count Of Records in product = {result[0]}"
        elif key == 11:
            result = db.statistic_finder(key, 'product_rate')
            return f"Count Of Records in product_rate = {result[0]}"
        elif key == 12:
            result = db.statistic_finder(key, 'registration')
            return f"Count Of Records in registration = {result[0]}"
        elif key == 13:
            result = db.statistic_finder(key, 'seller')
            return f"Count Of Records in seller = {result[0]}"
        elif key == 14:
            result = db.statistic_finder(key, 'stock_product')
            return f"Count Of Records in stock_product = {result[0]}"


class GetLinksButton(Button):
    person_nickname = ObjectProperty(None)
    def get_links(self):
        products = db.products(0)
        self.button.clear_widgets()
        for elements in products.split("\n")[0:-1]:
            self.btn = Button(text=elements, size_hint_y=None, height=40, font_size=11)
            self.btn.bind(on_release=self.print_clicked)
            self.button.add_widget(self.btn)

    def print_clicked(self, instance):
        text_list = instance.text.split("|")
        self.id = text_list[0].split(" ")[0]
        brand = text_list[2].split(" ")[10]
        name = text_list[3].split("  ")[3]
        self.seller = text_list[4].split("  ")[3]
        self.stock = text_list[5].split("  ")[3]
        price = text_list[6].split("  ")[3]
        self.stock_input = TextInput(multiline=False, size_hint=(1, 0.8), pos_hint={"y": 1})
        str_product = f"Brand: {brand}\nName:{name}\nSeller:{self.seller}\nStock Amount:{self.stock}\nPrice:{price} TL\n"
        popup_box = BoxLayout(orientation="vertical", padding=20)
        popup_box.add_widget(Label(text=f"Do You Want to Add This Product To Your Bucket?\n\n{str_product}"))
        stock_box = BoxLayout(orientation="horizontal", size_hint=(0.5, 0.25), spacing=40)
        stock_box.add_widget(Label(text="Amount(Unit): ", pos_hint={"y": 1}))
        stock_box.add_widget(self.stock_input)
        popup_box.add_widget(stock_box)
        inside_box = BoxLayout(orientation="horizontal", size_hint=(1, 0.15))
        yes_button = Button(text="Yes")
        no_button = Button(text="No")
        inside_box.add_widget(yes_button)
        inside_box.add_widget(no_button)
        popup_box.add_widget(inside_box)
        popup = Popup(title="ADD TO MY BUCKET", content=popup_box,
                      size_hint=(None, None), size=(400, 400))
        no_button.on_release = popup.dismiss
        yes_button.bind(on_release=self.add_to_bucket)
        yes_button.on_release = popup.dismiss
        popup.open()

    def add_to_bucket(self, instance):
        seller = self.seller.split(" ")[1]
        if int(self.stock_input.text) > int(self.stock):
            popup_window = Popup(title="Error!", content=Label(text="You Can Not Buy More Than Stock Amount"),
                                      size_hint=(None, None), size=(400, 400))
            popup_window.open()
        else:
            db.bucket_adder(self.person_nickname,self.id,seller,self.stock_input.text)


class GuestWindow(Screen):
    def rgba(self, red, green, blue, alpha):
        return rgba_returner(red, green, blue, alpha)

    def myFunc(self, key):
        return db.products(key)

    def products_sort(self, order):
        return db.sort_products(order)
    def show_categories(self):
        return db.category_show()


class BuyerWindow(Screen):
    person_nickname = ObjectProperty(None)
    def make_payment(self):
        popup_box = BoxLayout(orientation="vertical",padding=20)
        popup_box.add_widget(Label(text=f"Do You Confirm Your Bucket And Make Payment?\n\n"))
        inside_box = BoxLayout(orientation="horizontal", size_hint=(1, 0.15))
        yes_button = Button(text="Yes")
        no_button = Button(text="No")
        inside_box.add_widget(yes_button)
        inside_box.add_widget(no_button)
        popup_box.add_widget(inside_box)
        popup = Popup(title="MAKE PAYMENT", content=popup_box,
                      size_hint=(None, None), size=(400, 400))
        no_button.on_release = popup.dismiss
        yes_button.bind(on_release=self.on_click_yes)
        yes_button.on_release = popup.dismiss
        popup.open()

    def on_click_yes(self, instance):
        screen_manager.current = "payment"

    def show_profile_buyer(self, key):
        return_value = db.buyer_profile(self.person_nickname)
        if key == 0:
            return f'Name: {return_value[0] + " " + return_value[1]}'
        elif key == 2:
            return f'Nickname: {return_value[2]}'
        elif key == 3:
            return f'Email: {return_value[3]}'
        elif key == 4:
            return f'Address: {return_value[4]}'
        elif key == 5:
            return f'Phone: {return_value[5]}'
        elif key == 6:
            return f'Date of Birth: {return_value[6]}'
        elif key == 7:
            return f'Score: {return_value[7]}'

    def rgba(self, red, green, blue, alpha):
        return rgba_returner(red, green, blue, alpha)


class Bucket(Button):
    person_nickname = ObjectProperty(None)
    def get_links(self):
        products = db.bucket_finder(self.person_nickname)
        self.button.clear_widgets()
        for elements in products.split("\n"):
            if elements != "":
                self.btn = Button(text=elements, size_hint_y=None, height=40, font_size=14)
                self.btn.bind(on_release=self.print_clicked)
                self.button.add_widget(self.btn)

    def print_clicked(self, instance):
        text_list = instance.text.split("|")
        id = text_list[0].split("  ")[0]
        brand = text_list[2].split("  ")[2]
        name = text_list[4].split("  ")[2]
        seller = text_list[6].split("  ")[2]
        amount = text_list[8].split("  ")[2]
        price = text_list[10].split("  ")[2]
        totol_price = text_list[12].split("  ")[2]
        str_product = f"  Brand: {brand}\n  Name: {name}\n  Seller: {seller}\n  Amount: {amount}\n  Price: {price} \n  Total Price: {totol_price} \n"
        popup_box = BoxLayout(orientation="vertical",padding=20)
        popup_box.add_widget(Label(text=f"Do You Want to Delete This Product From Your Bucket?\n\n{str_product}"))
        inside_box = BoxLayout(orientation="horizontal", size_hint=(1, 0.15))
        yes_button = Button(text="Yes")
        no_button = Button(text="No")
        inside_box.add_widget(yes_button)
        inside_box.add_widget(no_button)
        popup_box.add_widget(inside_box)
        popup = Popup(title="DELETE FROM MY BUCKET", content=popup_box,
                      size_hint=(None, None), size=(400, 400))
        no_button.on_release = popup.dismiss
        yes_button.bind(on_release=self.delete_bucket)
        yes_button.on_release = popup.dismiss
        popup.open()

    def delete_bucket(self, instance):
        db.remove_from_bucket(self.person_nickname)


class Rate(Button):
    person_nickname = ObjectProperty(None)

    def get_links(self):
        products = db.paid_bucket_finder(self.person_nickname)
        self.button.clear_widgets()
        for elements in products.split("\n"):
            if elements != "":
                self.btn = Button(text=elements, size_hint_y=None, height=30, font_size=14)
                self.btn.bind(on_release=self.give_rate)
                self.button.add_widget(self.btn)

    def give_rate(self, instance):
        text_list = instance.text.split("|")
        self.id = text_list[0].split("  ")[0]
        brand = text_list[2].split("  ")[2]
        name = text_list[4].split("  ")[2]
        self.seller = text_list[6].split("  ")[2]
        amount = text_list[8].split("  ")[2]
        price = text_list[10].split("  ")[2]
        totol_price = text_list[12].split("  ")[2]
        str_product = f"  Brand: {brand}\n  Name: {name}\n  Seller: {self.seller}\n  Amount: {amount}\n  Price: {price} \n  Total Price: {totol_price} \n"
        popup_box = BoxLayout(orientation="vertical", padding=20)
        popup_box.add_widget(Label(text=f"Do You Want to Give Rate to This Product?\n\n{str_product}", font_size=14))
        input_layout = GridLayout(cols=2, size_hint=(0.8, 0.5))
        input_layout.add_widget(Label(text="Rate(0-5): ", font_size=14))
        self.rate_input = TextInput(multiline=False)
        input_layout.add_widget(self.rate_input)
        input_layout.add_widget(Label(text="Comment: ", font_size=14))
        self.comment = TextInput()
        input_layout.add_widget(self.comment)
        popup_box.add_widget(input_layout)
        inside_box = BoxLayout(orientation="horizontal", size_hint=(1, 0.25))
        yes_button = Button(text="Yes")
        no_button = Button(text="No")
        inside_box.add_widget(yes_button)
        inside_box.add_widget(no_button)
        popup_box.add_widget(inside_box)
        popup = Popup(title="GİVE RATE", content=popup_box,
                      size_hint=(None, None), size=(400, 400))
        no_button.on_release = popup.dismiss
        yes_button.bind(on_release=self.rate_call)
        yes_button.on_release = popup.dismiss
        popup.open()

    def rate_call(self, instance):
        return_value = db.rate_giver(self.id, self.seller, self.person_nickname, self.comment.text, self.rate_input.text)
        if return_value == 0:
            content_box = BoxLayout(orientation="vertical", padding=40)
            content_box.add_widget(Label(text="You already have given rate to this product!"))
            return_button = Button(text="Return", size_hint=(0.8, 0.4), pos_hint={'center_x': .5, 'center_y': .5})
            content_box.add_widget(return_button)
            popup_window = Popup(content=content_box, title="Error!",
                                 size_hint=(None, None), size=(400, 400))
            return_button.on_release = popup_window.dismiss
            popup_window.open()
        else:
            content_boxie = BoxLayout(orientation="vertical", padding=40)
            content_boxie.add_widget(Label(text="Thank You For Rating This Product!"))
            return_buttonie = Button(text="Return", size_hint=(0.8,0.4), pos_hint={"center_x": 0.5, "center_y": 0.5})
            content_boxie.add_widget(return_buttonie)
            popup_window = Popup(content=content_boxie, title="Success!",
                                 size_hint=(None, None), size=(400, 400))
            return_buttonie.on_release = popup_window.dismiss
            popup_window.open()


class Payment(Screen):
    person_nickname = ObjectProperty(None)
    def rgba(self, red, green, blue, alpha):
        return rgba_returner(red, green, blue, alpha)

    def confirm_payment(self, pay_type, name, no, cvc):
        db.payment_maker(self.person_nickname, pay_type, name, no, cvc)
        popup_box = BoxLayout(orientation="vertical", padding=20)
        popup_box.add_widget(Label(text=f"Successful Payment!\n\n", bold=True))
        return_button = Button(text="Return To Menu", size_hint_y=0.5)
        popup_box.add_widget(return_button)
        popup = Popup(title="Success", content=popup_box,
                      size_hint=(None, None), size=(400, 400))
        return_button.bind(on_release=self.on_click)
        return_button.on_release = popup.dismiss
        popup.open()

    def on_click(self, instance):
        screen_manager.current = "BuyerWindow"


class SellerWindow(Screen):
    person_email = ObjectProperty(None)
    person_nickname = ObjectProperty(None)
    person_pass = ObjectProperty(None)
    def rgba(self, red, green, blue, alpha):
        return rgba_returner(red, green, blue, alpha)
    def seller_products(self):
        return db.find_sellers_products(self.person_nickname)
    def show_products(self, key):
        return db.products(key)
    def update_product(self,id,cat,brand,name,stock,price):
        return_value = db.product_updater_adder(brand,name,cat,self.person_nickname,stock,price,id)
        if return_value == 0:
            self.popup_creater(3)
        elif return_value == 1:
            self.popup_creater(1)
    def delete_product(self,id):
        if id == "":
            self.popup_creater(0)
        else:
            return_value = db.product_deleter(id,self.person_nickname)
            # Check Here Later
            if return_value == 0:
                self.popup_creater(5)
            elif return_value == 1:
                self.popup_creater(2)
    def add_product(self,id,cat,brand,name,stock,price):
        return_value = db.product_updater_adder(brand,name,cat,self.person_nickname,stock,price,id)
        if return_value == 0:
            self.popup_creater(3)
        elif return_value == 1:
            self.popup_creater(4)
    def popup_creater(self,case):
        if case == 0:
            popup_window = Popup(title="Error!", content=Label(text="ID Can Not Be Empty!"),
                                      size_hint=(None, None), size=(400, 400))
            popup_window.open()
        elif case == 1:
            popup_window = Popup(title="Success!", content=Label(text="Successfully Updated The Product"),
                                      size_hint=(None, None), size=(400, 400))
            popup_window.open()
        elif case == 2:
            popup_window = Popup(title="Success!", content=Label(text="Successfully Deleted The Product"),
                                      size_hint=(None, None), size=(400, 400))
            popup_window.open()
        elif case == 3:
            popup_window = Popup(title="Error!", content=Label(text="Column(s) Can Not Be Empty!"),
                                      size_hint=(None, None), size=(400, 400))
            popup_window.open()
        elif case == 4:
            popup_window = Popup(title="Success!", content=Label(text="Successfully New Product Added"),
                                      size_hint=(None, None), size=(400, 400))
            popup_window.open()
        elif case == 3:
            popup_window = Popup(title="Error!", content=Label(text="Wrong ID or You Can Not Delete Another Person's Product"),
                                      size_hint=(None, None), size=(400, 400))
            popup_window.open()
    def show_categories(self):
        pass

    def show_profile(self, key):
        return_value = db.seller_profile(self.person_nickname)
        if key == 0:
            return f'Name: {return_value[0] + " " + return_value[1]}'
        elif key == 2:
            return f'Nickname: {return_value[2]}'
        elif key == 3:
            return f'Email: {return_value[3]}'
        elif key == 4:
            return f'Address: {return_value[4]}'
        elif key == 5:
            return f'Phone: {return_value[5]}'
        elif key == 6:
            return f'Date of Birth: {return_value[6]}'
        elif key == 7:
            return f'Rate: {return_value[7]}'

class WindowManager(ScreenManager):
    pass


class RegisterWindow(Screen):
    def user_add(self, email, password, nickname, name, last_name, address, phone, birth_date, kind):
        special_characters = ["*", ",", "+", "/", "#"]
        special_characters.sort()
        name_check = list(set(special_characters).difference(name))
        nickname_check = list(set(special_characters).difference(nickname))
        last_name_check = list(set(special_characters).difference(last_name))
        password_check = list(set(special_characters).difference(password))
        address_check = list(set(special_characters).difference(address))
        name_check.sort()
        nickname_check.sort()
        password_check.sort()
        address_check.sort()
        last_name_check.sort()

        return_value = db.add_user(email, password, nickname, name, last_name, address, phone, birth_date, kind)
        if return_value == 0:
            return "empty_column"
        elif ('@' not in email and '.' not in email) or "," in email:
            return "email_typo"

        elif name_check != special_characters or last_name_check != special_characters or \
                nickname_check != special_characters or password_check != special_characters or \
                address_check != special_characters:
            return "special_chars"

    def btn(self, var):
        if var == "email_typo":
            wrong_pass_window = Popup(title="Error!", content=Label(text="Incorrect Email \nRegistration Failed!"),
                                      size_hint=(None, None), size=(400, 400))
            wrong_pass_window.open()
            return 0
        elif var == "empty_column":
            wrong_pass_window = Popup(title="Error!", content=Label(text="Column(s) Can Not Be Empty!"),
                                      size_hint=(None, None), size=(400, 400))
            wrong_pass_window.open()
            return 0
        elif var == "special_chars":
            wrong_pass_window = Popup(title="Error!", content=Label(text="Please Do Not Use Special Characters"),
                                      size_hint=(None, None), size=(400, 400))
            wrong_pass_window.open()
            return 0
        return 1

    def rgba(self, red, green, blue, alpha):
        return rgba_returner(red, green, blue, alpha)


def rgba_returner(red, green, blue, alpha):
    red = float(red / 255)
    green = float(green / 255)
    blue = float(blue / 255)
    return (red, green, blue, alpha)


class snb(App):
    kv = Builder.load_file("snb.kv")
    def build(self):
        global screen_manager
        screen_manager = WindowManager()
        return screen_manager


if __name__ == "__main__":
    snb().run()
