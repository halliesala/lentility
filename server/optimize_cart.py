from app import app
import models
import getAllProductPriceInfo from calculate_price

if __name__ == '__main__':
    with app.app_context(): 
        # Get cart
        
