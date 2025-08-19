#product_service/app/serializers.py
from rest_framework import serializers
from .models import Category, Product, ProductImage, Review, AuctionBid, Favorite
import requests
from django.conf import settings
import logging
from django.utils.timezone import now

logger = logging.getLogger(__name__)

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'parent', 'category_image', 'category_href']

    def validate_name(self, value):
        parent_id = self.initial_data.get('parent')
        if Category.objects.filter(name=value, parent_id=parent_id).exists():
            raise serializers.ValidationError("Category with this name already exists in the parent category")
        return value

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'product_id', 'image_url', 'user_id', 'created_at']

class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True, source='productimage_set')
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'name', 'vendor_id', 'category', 'price', 'discount_price', 'stock', 'sale_type',
                  'auction_end_time', 'is_approved', 'rating_count', 'created_at', 'product_href', 'images', 'rating']
        read_only_fields = ['created_at', 'product_href', 'rating_count']

    def validate(self, data):
        if data['sale_type'] == 'auction' and not data.get('auction_end_time'):
            raise serializers.ValidationError({"auction_end_time": "Auction end time is required for auction products"})
        if data.get('discount_price') and data['discount_price'] >= data['price']:
            raise serializers.ValidationError({"discount_price": "Discount price must be less than regular price"})
        if data.get('stock', 0) < 0:
            raise serializers.ValidationError({"stock": "Stock cannot be negative"})
        return data

    def validate_vendor_id(self, value):
        try:
            response = requests.get(f"{settings.USER_SERVICE_URL}/users/{value}", timeout=5)
            response.raise_for_status()
            return value
        except requests.RequestException as e:
            logger.error(f"Failed to validate vendor_id {value}: {str(e)}")
            raise serializers.ValidationError("Invalid vendor_id")

    def get_rating(self, obj):
        reviews = Review.objects.filter(product_id=obj.id, is_approved=True)
        return reviews.aggregate(rating=serializers.models.Avg('rating'))['rating'] or 0

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'product_id', 'user_id', 'rating', 'comment', 'created_at', 'is_approved']
        read_only_fields = ['created_at', 'is_approved']

    def validate(self, data):
        user_id = data['user_id']
        product_id = data['product_id']
        try:
            response = requests.get(
                f"{settings.ORDER_SERVICE_URL}/orders/?customer_id={user_id}&product_id={product_id}",
                timeout=5
            )
            response.raise_for_status()
            if not response.json()['results']:
                raise serializers.ValidationError("You must purchase the product to leave a review")
        except requests.RequestException as e:
            logger.error(f"Failed to validate purchase for user {user_id}, product {product_id}: {str(e)}")
            raise serializers.ValidationError("Unable to verify purchase")
        return data

    def validate_user_id(self, value):
        try:
            response = requests.get(f"{settings.USER_SERVICE_URL}/users/{value}", timeout=5)
            response.raise_for_status()
            return value
        except requests.RequestException as e:
            logger.error(f"Failed to validate user_id {value}: {str(e)}")
            raise serializers.ValidationError("Invalid user_id")

class AuctionBidSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuctionBid
        fields = ['id', 'product_id', 'user_id', 'amount', 'created_at']
        read_only_fields = ['created_at']

    def validate(self, data):
        product_id = data['product_id']
        try:
            product = Product.objects.get(id=product_id, sale_type='auction', is_approved=True)
            if product.auction_end_time < now():
                raise serializers.ValidationError("Auction has ended")
            if data['amount'] <= product.price:
                raise serializers.ValidationError("Bid must be higher than current price")
        except Product.DoesNotExist:
            raise serializers.ValidationError("Invalid product_id or product is not an auction")
        return data

    def validate_user_id(self, value):
        try:
            response = requests.get(f"{settings.USER_SERVICE_URL}/users/{value}", timeout=5)
            response.raise_for_status()
            return value
        except requests.RequestException as e:
            logger.error(f"Failed to validate user_id {value}: {str(e)}")
            raise serializers.ValidationError("Invalid user_id")

class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = ['id', 'user_id', 'product_id', 'created_at']
        read_only_fields = ['created_at']

    def validate_user_id(self, value):
        try:
            response = requests.get(f"{settings.USER_SERVICE_URL}/users/{value}", timeout=5)
            response.raise_for_status()
            return value
        except requests.RequestException as e:
            logger.error(f"Failed to validate user_id {value}: {str(e)}")
            raise serializers.ValidationError("Invalid user_id")

    def validate_product_id(self, value):
        try:
            Product.objects.get(id=value, is_approved=True)
            return value
        except Product.DoesNotExist:
            logger.error(f"Product with ID {value} not found or not approved")
            raise serializers.ValidationError("Invalid product_id")

class ProductImageUploadSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    image = serializers.ImageField()

    def validate(self, data):
        product_id = data.get('product_id')
        try:
            Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            logger.error(f"Product with ID {product_id} not found")
            raise serializers.ValidationError({"product_id": "Product not found"})
        image = data.get('image')
        if image.size > 32 * 1024 * 1024:
            raise serializers.ValidationError({"image": "Image size must not exceed 32MB"})
        if not image.name.lower().endswith(('.jpg', '.jpeg', '.png', '.gif')):
            raise serializers.ValidationError({"image": "Allowed formats: JPG, JPEG, PNG, GIF"})
        return data