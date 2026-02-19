import pandas as pd
import numpy as np
from olist.utils import haversine_distance
from olist.data import Olist


class Order:
    '''
    DataFrames containing all orders as index,
    and various properties of these orders as columns
    '''
    def __init__(self):
        # Assign an attribute ".data" to all new instances of Order
        self.data = Olist().get_data()

    def get_wait_time(self, is_delivered=True):
        """
        Returns a DataFrame with:
        [order_id, wait_time, expected_wait_time, delay_vs_expected, order_status]
        and filters out non-delivered orders unless specified
        """
        # Hint: Within this instance method, you have access to the instance of the class Order in the variable self, as well as all its attributes
        data = self.data
        orders = data["orders"].copy()

        if is_delivered:
            orders = orders[orders["order_status"] == "delivered"].copy()

        # datetime conversion
        date_cols = [
        "order_purchase_timestamp",
        "order_delivered_customer_date",
        "order_estimated_delivery_date"
        ]

        for col in date_cols:
            orders[col] = pd.to_datetime(orders[col])

        # wait_time
        orders["wait_time"] = (
        orders["order_delivered_customer_date"]
        - orders["order_purchase_timestamp"]
        ) / np.timedelta64(1, "D")

        # expected_wait_time
        orders["expected_wait_time"] = (
        orders["order_estimated_delivery_date"]
        - orders["order_purchase_timestamp"]
        ) / np.timedelta64(1, "D")

        # delay_vs_expected
        delay = (
        orders["order_delivered_customer_date"]
        - orders["order_estimated_delivery_date"]
        ) / np.timedelta64(1, "D")

        orders["delay_vs_expected"] = delay.clip(lower=0)

        return orders[[
        "order_id",
        "wait_time",
        "expected_wait_time",
        "delay_vs_expected",
        "order_status"
        ]]

    def get_review_score(self):
        """
        Returns a DataFrame with:
        order_id, dim_is_five_star, dim_is_one_star, review_score
        """
        data = self.data
        reviews = data["order_reviews"].copy()
        reviews["dim_is_five_star"] = reviews["review_score"].map({
        5: 1}).fillna(0).astype(int)
        reviews["dim_is_one_star"] = np.where(reviews["review_score"]==1, 1, 0)
        return reviews[["order_id","dim_is_five_star","dim_is_one_star","review_score"]]

    def get_number_items(self):
        """
        Returns a DataFrame with:
        order_id, number_of_items
        """
        data = self.data
        order_items = data["order_items"].copy()
        df_items = (
            order_items
            .groupby("order_id")["product_id"]
            .count()
            .reset_index(name="number_of_items")
            )
        return df_items

    def get_number_sellers(self):
        """
        Returns a DataFrame with:
        order_id, number_of_sellers
        """
        data = self.data
        order_sellers = data["order_items"].copy()
        df_items = (
            order_sellers
            .groupby("order_id")["seller_id"]
            .nunique()
            .reset_index(name="number_of_sellers")
            )
        return df_items

    def get_price_and_freight(self):
        """
        Returns a DataFrame with:
        order_id, price, freight_value
        """
        pass  # YOUR CODE HERE

    # Optional
    def get_distance_seller_customer(self):
        """
        Returns a DataFrame with:
        order_id, distance_seller_customer
        """
        pass  # YOUR CODE HERE

    def get_training_data(self,
                          is_delivered=True,
                          with_distance_seller_customer=False):
        """
        Returns a clean DataFrame (without NaN), with the all following columns:
        ['order_id', 'wait_time', 'expected_wait_time', 'delay_vs_expected',
        'order_status', 'dim_is_five_star', 'dim_is_one_star', 'review_score',
        'number_of_items', 'number_of_sellers', 'price', 'freight_value',
        'distance_seller_customer']
        """
        # Hint: make sure to re-use your instance methods defined above
        pass  # YOUR CODE HERE
