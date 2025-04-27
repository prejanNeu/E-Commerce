// Cart state
let cart = [];

// Get CSRF token from cookies
function getCSRFToken() {
    let csrfToken = null;
    document.cookie.split(';').forEach(cookie => {
        let [name, value] = cookie.trim().split('=');
        if (name === 'csrftoken') {
            csrfToken = value;
        }
    });
    return csrfToken;
}

// Fetch products from API
async function fetchProducts() {
    try {
        const response = await fetch('/api/product/trending');
        console.log(response)
        const products = await response.json();
        displayProducts(products);
        await fetchCart(); // Load initial cart state
    } catch (error) {
        console.error('Error fetching products:', error);
    }
}

// Fetch cart items from API
async function fetchCart() {
    try {
        const response = await fetch('/api/get/cart', {
            headers: {
                'X-CSRFToken': getCSRFToken()
            }
        });
        if (!response.ok) throw new Error(`HTTP error! Status: ${response.status}`);
        const cartData = await response.json();
        cart = cartData;
        updateCartUI();
    } catch (error) {
        console.error('Error fetching cart:', error);
    }
}

// Display products in grid
function displayProducts(products) {
    const container = document.getElementById('products-container');
    container.innerHTML = products.map(product => `
        <div class="product-card">
            <img src = "${product.image}" alt="${product.name}" class="product-image">
            <div class="product-info">
                <h3 class="product-name">${product.name}</h3>
                <p class="product-description">${product.description}</p>
                <p class="product-price">₨ ${product.price}</p>
                <button class="btn btn-add-to-cart" onclick="addToCart(${product.id})">
                    Add to Cart
                </button>
            </div>
        </div>
    `).join('');
}

// Add product to cart
async function addToCart(productId) {
    try {
        console.log(productId)
        const response = await fetch(`/api/product/add_to_cart/${productId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCSRFToken()
            }
        });

        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
            alert('Product added to cart successfully!');
        }

        await fetchCart(); // Refresh cart from server
        
    } catch (error) {
        console.error('Error adding to cart:', error);
        alert('Failed to add product to cart. Please try again.');
    }
}

// Update cart UI
function updateCartUI() {

    const cartContainer = document.getElementById('cart-items');
    const cartCount = document.getElementById('cart-count');
    const cartTotal = document.getElementById('cart-total');
    
    // Update cart count
    const totalItems = cart.reduce((total, item) => total + item.quantity, 0);
    cartCount.textContent = totalItems;
    // If cart is empty, show message
    if (cart.length === 0) {
        cartContainer.innerHTML = '<div class="empty-cart">Your cart is empty</div>';
        cartTotal.textContent = '₨ 0.00';
        return;
    }
    
    cartContainer.innerHTML = cart.map(item => `
        <div class="cart-item">
            <img src="${item.image}" alt="${item.name}">
            <div class="cart-item-info">
                <h3>${item.name}</h3>
                <p class="cart-item-price">₨ ${item.price}</p>
            </div>
            <div class="quantity-controls">
                <button class="quantity-btn" onclick="decrementQuantity(${item.product_id})">-</button>
                <span>${item.quantity}</span>
                <button class="quantity-btn" onclick="addToCart(${item.product_id})">+</button>
                <button class="btn" onclick="removeFromCart(${item.id})">
                    <i class="fas fa-trash"></i>
                </button>
            </div>
        </div>
    `).join('');
    
    const total = cart.reduce((sum, item) => sum + (parseFloat(item.price) * item.quantity), 0);
    cartTotal.textContent = `₨ ${total.toFixed(2)}`;
    
    // Update checkout button visibility
    const checkoutButton = document.querySelector('.btn-checkout');
    if (checkoutButton) {
        checkoutButton.style.display = cart.length > 0 ? 'block' : 'none';
    }
}

// Decrement item quantity
async function decrementQuantity(productId) {
    try {
        console.log(productId)
        const response = await fetch(`/api/cart/decrement/${productId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCSRFToken()
            }
        });

        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        await fetchCart(); // Refresh cart from server
    } catch (error) {
        console.error('Error updating quantity:', error);
        alert('Failed to update quantity. Please try again.');
    }
}

// Remove item from cart
async function removeFromCart(cartId) {
    try {
        const response = await fetch(`/api/delete/cart/${cartId}`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCSRFToken()
            }
        });

        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        await fetchCart(); // Refresh cart from server
    } catch (error) {
        console.error('Error removing item:', error);
        alert('Failed to remove item from cart. Please try again.');
    }
}

// Show/hide cart section
function toggleCart() {
    const productsSection = document.getElementById('products');
    const cartSection = document.getElementById('cart');
    cartSection.classList.toggle('hidden');
    productsSection.classList.toggle('hidden');
}

// Initialize eSewa payment
async function initiatePayment() {
    
    const total = cart.reduce((sum, item) => sum + (parseFloat(item.price) * item.quantity), 0);
    
    try {
        const response = await fetch(`/api/payment/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCSRFToken()
            },
            body: JSON.stringify({ total: calculateTotal().toFixed(2) })
        });
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        const payload = await response.json();
        const form = document.createElement('form');
        form.method = 'POST';
        // https://uat.esewa.com.np/api/epay
        // https://rc-epay.esewa.com.np/api/epay/main/v2/form
        form.action = 'https://rc-epay.esewa.com.np/api/epay/main/v2/form';
        for (const key in payload) {
        const input = document.createElement('input');
        input.type = 'hidden';
        input.name = key;
        input.value = payload[key];
        form.appendChild(input);
        }
        document.body.appendChild(form);
        form.submit();
    }
    catch (error) {
        console.error('Error:', error);
        alert('Payment initiation failed. Please try again.');
    }

}

function calculateTotal() {
    return cart.reduce((sum, item) => sum + parseFloat(item.price*item.quantity), 0);
}

function completeOrder() { console.log(calculateTotal())
    // Redirect to order details page
    window.location.href = '/order/confirmation';
}

// Event Listeners
document.addEventListener('DOMContentLoaded', () => {
    fetchProducts();
    
    // Navigation
    document.querySelectorAll('.nav-links a').forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const targetId = link.getAttribute('href').substring(1);
            if (targetId === 'cart') {
                toggleCart();
            }
        });
    });
    
    // Add click event listener for checkout button
    const checkoutButton = document.querySelector('.btn-checkout');
    if (checkoutButton) {
        checkoutButton.addEventListener('click', initiatePayment);
    }
});
