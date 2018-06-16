# -*- coding: utf-8 -*-

import os
import unittest

from database.db_wrapper import DBwrapper
from geizhals.product import Product
from geizhals.wishlist import Wishlist


class DBWrapperTest(unittest.TestCase):

    def setUp(self):
        self.db_name = "test.db"
        self.db_name_test_create = "test_create.db"
        self.db = DBwrapper.get_instance(self.db_name)

        # Define sample wishlist and product
        self.wl = Wishlist(123456, "Wishlist", "https://geizhals.de/?cat=WL-123456", 123.45)
        self.p = Product(123456, "Product", "https://geizhals.de/a123456", 123.45)

    def tearDown(self):
        self.db.delete_all_tables()
        self.db.close_conn()
        try:
            test_db = os.path.join(self.db.dir_path, self.db_name)
            test_create_db = os.path.join(self.db.dir_path, self.db_name_test_create)
            os.remove(test_db)
            os.remove(test_create_db)
        except OSError as e:
            pass

        DBwrapper.instance = None

    def test_create_database(self):
        """Test for checking if the database gets created correctly"""
        # Use another path, since we want to check that method independendly from the initialization
        path = self.db.dir_path
        db_path = os.path.join(path, self.db_name_test_create)

        # Check if db file doesn't already exist
        self.assertFalse(os.path.exists(db_path))

        # Create database file
        self.db.create_database(db_path)

        # Check if the db file was created in the directory
        self.assertTrue(os.path.exists(db_path))

    def test_create_tables(self):
        """Test for checking if the database tables are created correctly"""
        table_names = ["users", "products", "wishlists", "product_prices", "wishlist_prices", "product_subscribers", "wishlist_subscribers"]

        # Use another path, since we want to check that method independendly from the initialization
        path = self.db.dir_path
        db_path = os.path.join(path, self.db_name_test_create)

        # Create database file
        self.db.create_database(db_path)
        self.db.setup_connection(db_path)

        # Make sure that tables are not already present in the database
        for table_name in table_names:
            result = self.db.cursor.execute("SELECT count(*) FROM sqlite_master WHERE type='table' AND name=?;", [table_name]).fetchone()[0]
            self.assertEqual(result, 0, msg="Table '{}' does already exist!".format(table_name))

        # Create tables in the database
        self.db.create_tables()

        # Make sure that all the tables are correctly created
        for table_name in table_names:
            result = self.db.cursor.execute("SELECT count(*) FROM sqlite_master WHERE type='table' AND name=?;", [table_name]).fetchone()[0]
            self.assertEqual(result, 1, msg="Table '{}' does not exist!".format(table_name))



    def test_get_all_wishlists(self):
        """Test to check if all wishlists can be retreived from the db"""
        wishlists = [{"id": 962572, "name": "NIU2E0RRWX", "url": "https://geizhals.de/?cat=WL-962572", "price": 62.80},
                     {"id": 924729, "name": "3W5NQ1QIHT", "url": "https://geizhals.de/?cat=WL-924729", "price": 46.00},
                     {"id": 614044, "name": "CTYCTW798V", "url": "https://geizhals.de/?cat=WL-614044", "price": 96.95},
                     {"id": 245759, "name": "VDY66U0AWM", "url": "https://geizhals.de/?cat=WL-245759", "price": 53.94},
                     {"id": 490792, "name": "N6MCC1Z38O", "url": "https://geizhals.de/?cat=WL-490792", "price": 144.85},
                     {"id": 533484, "name": "NOJJ8KVE9T", "url": "https://geizhals.de/?cat=WL-533484", "price": 122.77},
                     {"id": 577007, "name": "ELV51DSL2A", "url": "https://geizhals.de/?cat=WL-577007", "price": 62.68},
                     {"id": 448441, "name": "6RM9F6IWIO", "url": "https://geizhals.de/?cat=WL-448441", "price": 45.97},
                     {"id": 567418, "name": "C2W75RPRFS", "url": "https://geizhals.de/?cat=WL-567418", "price": 137.53},
                     {"id": 590717, "name": "JEXP2E5Y06", "url": "https://geizhals.de/?cat=WL-590717", "price": 117.84}]

        for wl in wishlists:
            self.db.add_wishlist(id=wl.get("id"), name=wl.get("name"), url=wl.get("url"), price=wl.get("price"))

        db_wishlists = self.db.get_all_wishlists()

        for db_wl in db_wishlists:
            found = False
            for wl in wishlists:
                if db_wl.id == wl.get("id"):
                    found = True

            self.assertTrue(found, msg="Inserted wishlist was not found!")

    def test_get_all_products(self):
        """Test to check if retreiving all products works"""
        products = [{"id": 962572, "name": "NIU2E0RRWX", "url": "https://geizhals.de/a962572", "price": 62.80},
                    {"id": 924729, "name": "3W5NQ1QIHT", "url": "https://geizhals.de/a924729", "price": 46.00},
                    {"id": 614044, "name": "CTYCTW798V", "url": "https://geizhals.de/a614044", "price": 96.95},
                    {"id": 245759, "name": "VDY66U0AWM", "url": "https://geizhals.de/a245759", "price": 53.94},
                    {"id": 490792, "name": "N6MCC1Z38O", "url": "https://geizhals.de/a490792", "price": 144.85},
                    {"id": 533484, "name": "NOJJ8KVE9T", "url": "https://geizhals.de/a533484", "price": 122.77},
                    {"id": 577007, "name": "ELV51DSL2A", "url": "https://geizhals.de/a577007", "price": 62.68},
                    {"id": 448441, "name": "6RM9F6IWIO", "url": "https://geizhals.de/a448441", "price": 45.97},
                    {"id": 567418, "name": "C2W75RPRFS", "url": "https://geizhals.de/a567418", "price": 137.53},
                    {"id": 590717, "name": "JEXP2E5Y06", "url": "https://geizhals.de/a590717", "price": 117.84}]
        for p in products:
            self.db.add_product(id=p.get("id"), name=p.get("name"), url=p.get("url"), price=p.get("price"))

        db_products = self.db.get_all_products()

        for db_p in db_products:
            found = False
            for p in products:
                if db_p.id == p.get("id"):
                    found = True

            self.assertTrue(found, msg="Inserted product was not found!")

    def test_get_wishlist_info(self):
        """Test to check if fetching information for a wishlist works"""
        self.assertFalse(self.db.is_wishlist_saved(self.wl.id), "Wishlist is already saved!")

        self.db.add_wishlist(self.wl.id, self.wl.name, self.wl.price, self.wl.url)
        wishlist = self.db.get_wishlist_info(self.wl.id)

        self.assertEqual(wishlist.id, self.wl.id)
        self.assertEqual(wishlist.name, self.wl.name)
        self.assertEqual(wishlist.url, self.wl.url)
        self.assertEqual(wishlist.price, self.wl.price)

    def test_is_wishlist_saved(self):
        # Check if wishlist is already saved
        self.assertFalse(self.db.is_wishlist_saved(self.wl.id), "Wishlist is already saved!")

        # Add wishlist to the database
        self.db.add_wishlist(self.wl.id, self.wl.name, self.wl.price, self.wl.url)

        # Check if wishlist is now saved in the db
        self.assertTrue(self.db.is_wishlist_saved(self.wl.id), "Wishlist is not saved in the db!")

    def test_is_product_saved(self):
        # Make sure product is not already saved
        self.assertFalse(self.db.is_product_saved(self.p.id), "Product should not be saved yet!")

        # Add product to the db
        self.db.add_product(self.p.id, self.p.name, self.p.price, self.p.url)

        # Check if product is saved afterwards
        self.assertTrue(self.db.is_product_saved(self.p.id), "Product is not saved in the db!")

    def test_add_wishlist(self):
        """Test for checking if wishlists are being added correctly"""
        # Make sure that element is not already in database
        result = self.db.cursor.execute("SELECT count(*) FROM wishlists WHERE wishlist_id=?", [self.wl.id]).fetchone()[0]
        self.assertEqual(result, 0)

        self.db.add_wishlist(id=self.wl.id, name=self.wl.name, url=self.wl.url, price=self.wl.price)
        result = self.db.cursor.execute("SELECT wishlist_id, name, url, price  FROM wishlists WHERE wishlist_id=?", [self.wl.id]).fetchone()

        self.assertEqual(result[0], self.wl.id, msg="ID is not equal!")
        self.assertEqual(result[1], self.wl.name, msg="Name is not equal!")
        self.assertEqual(result[2], self.wl.url, msg="Url is not equal!")
        self.assertEqual(result[3], self.wl.price, msg="Price is not equal!")

    def test_add_product(self):
        """Test for checking if products are being added correctly"""
        # Make sure that element is not already in database
        result = self.db.cursor.execute("SELECT count(*) FROM products WHERE product_id=?", [self.p.id]).fetchone()[0]
        self.assertEqual(result, 0)

        # Check if product is saved afterwards
        self.db.add_product(id=self.p.id, name=self.p.name, url=self.p.url, price=self.p.price)
        result = self.db.cursor.execute("SELECT product_id, name, url, price FROM products WHERE product_id=?", [self.p.id]).fetchone()

        self.assertEqual(result[0], self.p.id, msg="ID is not equal!")
        self.assertEqual(result[1], self.p.name, msg="Name is not equal!")
        self.assertEqual(result[2], self.p.url, msg="Url is not equal!")
        self.assertEqual(result[3], self.p.price, msg="Price is not equal!")

    def test_rm_wishlist(self):
        # Add wishlist and check if it's in the db
        self.assertFalse(self.db.is_wishlist_saved(self.wl.id))
        self.db.add_wishlist(self.wl.id, self.wl.name, self.wl.price, self.wl.url)
        self.assertTrue(self.db.is_wishlist_saved(self.wl.id))

        # Check if wishlist gets removed properly
        self.db.rm_wishlist(self.wl.id)
        self.assertFalse(self.db.is_wishlist_saved(self.wl.id))

    def test_rm_product(self):
        # Add product and check if it's in the db
        self.assertFalse(self.db.is_product_saved(self.p.id))
        self.db.add_product(self.p.id, self.p.name, self.p.price, self.p.url)
        self.assertTrue(self.db.is_product_saved(self.p.id))

        # Check if product gets removed properly
        self.db.rm_product(self.p.id)
        self.assertFalse(self.db.is_product_saved(self.p.id))

    def test_subscribe_wishlist(self):
        user_id = 11223344
        first_name = "John"
        username = "JohnDoe"

        self.db.add_wishlist(id=self.wl.id, name=self.wl.name, url=self.wl.url, price=self.wl.price)
        self.db.add_user(user_id, first_name, username)

        result = self.db.cursor.execute("SELECT wishlist_id FROM wishlist_subscribers AS ws WHERE ws.user_id=? AND ws.wishlist_id=?;", [str(user_id), str(self.wl.id)]).fetchone()
        self.assertEqual(result, None)

        self.db.subscribe_wishlist(self.wl.id, user_id)
        result = self.db.cursor.execute("SELECT wishlist_id FROM wishlist_subscribers AS ws WHERE ws.user_id=? AND ws.wishlist_id=?;", [str(user_id), str(self.wl.id)]).fetchone()

        self.assertEqual(len(result), 1)

    def test_subscribe_product(self):
        user_id = 11223344
        first_name = "John"
        username = "JohnDoe"

        self.db.add_product(id=self.p.id, name=self.p.name, url=self.p.url, price=self.p.price)
        self.db.add_user(user_id, first_name, username)

        result = self.db.cursor.execute("SELECT product_id FROM product_subscribers AS ps WHERE ps.user_id=? AND ps.product_id=?;", [str(user_id), str(self.p.id)]).fetchone()
        self.assertEqual(result, None)

        self.db.subscribe_product(self.p.id, user_id)
        result = self.db.cursor.execute("SELECT product_id FROM product_subscribers AS ps WHERE ps.user_id=? AND ps.product_id=?;", [str(user_id), str(self.p.id)]).fetchone()

        self.assertEqual(len(result), 1)
    def test_update_wishlist_name(self):
        self.db.add_wishlist(self.wl.id, self.wl.name, self.wl.price, self.wl.url)
        self.assertEqual(self.db.get_wishlist_info(self.wl.id).name, self.wl.name)

        self.db.update_wishlist_name(self.wl.id, "New Wishlist")
        self.assertEqual(self.db.get_wishlist_info(self.wl.id).name, "New Wishlist")

    def test_update_product_name(self):
        self.db.add_product(self.p.id, self.p.name, self.p.price, self.p.url)
        self.assertEqual(self.db.get_product_info(self.p.id).name, self.p.name)

        self.db.update_product_name(self.p.id, "New Product")
        self.assertEqual(self.db.get_product_info(self.p.id).name, "New Product")



    def test_get_all_users(self):
        """Test to check if retreiving all users from the database works"""
        users = [{"id": 415641, "first_name": "Peter", "username": "name2", "lang_code": "en_US"},
                 {"id": 564864654, "first_name": "asdf", "username": "AnotherUser", "lang_code": "en_US"},
                 {"id": 54564162, "first_name": "NoName", "username": "Metallica", "lang_code": "en_US"},
                 {"id": 5555333, "first_name": "1234", "username": "d_Rickyy_b", "lang_code": "en_US"}]

        # Check that database is empty
        all_users_db = self.db.get_all_users()
        self.assertEqual(len(all_users_db), 0, msg="There are already users in the db!")

        for user in users:
            self.db.add_user(user.get("id"), user.get("first_name"), user.get("username"), user.get("lang_code"))

        all_users_db = self.db.get_all_users()

        self.assertEqual(len(all_users_db), len(users), msg="Users in database is not same amount as users in test!")

        for db_user in all_users_db:
            found = False

            for user in users:
                if user.get("id") == db_user.get("id"):
                    found = True
                    self.assertEqual(user.get("first_name"), db_user.get("first_name"))
                    self.assertEqual(user.get("username"), db_user.get("username"))
                    self.assertEqual(user.get("lang_code"), db_user.get("lang_code"))
                    break

            self.assertTrue(found)

    def test_get_lang_id(self):
        """Test to check if receiving the lang_code works"""
        user = {"id": 123456, "first_name": "John", "username": "testUsername", "lang_code": "en_US"}

        # Check that user does not already exist
        user_db = self.db.get_user(user.get("id"))
        self.assertEqual(user_db, None)

        # Add user to database
        self.db.add_user(user.get("id"), user.get("first_name"), user.get("username"), user.get("lang_code"))

        lang_id = self.db.get_lang_id(user.get("id"))
        self.assertEqual(lang_id, user.get("lang_code"))

    def test_add_user(self):
        """Test to check if adding users works as expected"""
        user = {"id": 123456, "first_name": "John", "username": "testUsername", "lang_code": "en_US"}

        # Check that user does not already exist
        user_db = self.db.get_user(user.get("id"))
        self.assertEqual(user_db, None)

        # Add user to database
        self.db.add_user(user.get("id"), user.get("first_name"), user.get("username"), user.get("lang_code"))

        # Check if user was added
        user_db = self.db.get_user(user.get("id"))
        self.assertEqual(user_db.get("id"), user.get("id"))

    def test_is_user_saved(self):
        """Test to check if the 'check if a user exists' works as expected"""
        user = {"id": 123456, "first_name": "John", "username": "testUsername", "lang_code": "en_US"}

        # Check that user does not already exist
        user_db = self.db.get_user(user.get("id"))
        self.assertIsNone(user_db, "User is not None!")
        self.assertFalse(self.db.is_user_saved(user.get("id")))

        self.db.add_user(user.get("id"), user.get("first_name"), user.get("username"), user.get("lang_code"))

        self.assertTrue(self.db.is_user_saved(user.get("id")))
