
import requests
from config import Config


def get_woocommerce_products(store_url, consumer_key, consumer_secret):
    """Retrieve published products from a WooCommerce store."""

    if not store_url or not consumer_key or not consumer_secret:
        return None, "WooCommerce is not configured."

    try:
        response = requests.get(
            store_url.rstrip("/") + "/wp-json/wc/v3/products",
            params={
                "per_page": 20,
                "status": "publish"
            },
            auth=(consumer_key, consumer_secret),
            timeout=15
        )

        response.raise_for_status()
        products = response.json()

        if not products:
            return [], None

        product_list = []

        for product in products:
            product_list.append({
                "name": product.get("name"),
                "price": product.get("price"),
                "stock_status": product.get("stock_status"),
                "stock_quantity": product.get("stock_quantity"),
                "description": product.get("short_description", "")
            })

        return product_list, None

    except requests.exceptions.RequestException:
        return None, "Unable to connect to the WooCommerce store."

    except (ValueError, TypeError):
        return None, "Unexpected response from the WooCommerce store."


def generate_response(
    message,
    store_url=None,
    consumer_key=None,
    consumer_secret=None
):

    if not Config.GPT_API_KEY:
        raise RuntimeError("Groq API key is not configured.")

    system_prompt = (
        "You are a helpful AI shopping assistant. "
        "Provide clear, accurate and friendly answers. "
        "When WooCommerce product information is provided, "
        "use it as the source of truth. "
        "Never invent product names, prices or stock availability."
    )

    product_keywords = [
        "product", "products", "price", "prices", "cost",
        "stock", "available", "availability", "buy",
        "purchase", "catalog", "item", "items", "order",
        "headphone", "headphones"
    ]

    message_lower = message.lower()

    is_product_question = any(
        keyword in message_lower
        for keyword in product_keywords
    )

    if is_product_question and store_url:
        products, error = get_woocommerce_products(
            store_url,
            consumer_key,
            consumer_secret
        )

        if error:
            system_prompt += (
                "\nThe customer asked about the store, but the "
                "WooCommerce catalog could not be accessed. "
                "Tell the customer that product information is "
                "temporarily unavailable. Do not guess."
            )

        elif not products:
            system_prompt += (
                "\nThe WooCommerce store currently returned no "
                "published products. Do not invent products."
            )

        else:
            system_prompt += (
                "\n\nCURRENT WOOCOMMERCE STORE PRODUCTS:\n"
                + str(products)
                + "\n\nUse these actual product details when answering. "
                "Prices and stock must match the supplied data. "
                "If a requested product is not listed, say you could "
                "not find it in the current catalog."
            )

    headers = {
        "Authorization": f"Bearer {Config.GPT_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "openai/gpt-oss-120b",
        "messages": [
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": message
            }
        ],
        "temperature": 0.7,
        "max_completion_tokens": 500
    }

    try:
        response = requests.post(
            Config.GPT_API_URL,
            headers=headers,
            json=payload,
            timeout=45
        )

        response.raise_for_status()

        data = response.json()
        ai_reply = data["choices"][0]["message"]["content"]

        if not ai_reply:
            raise RuntimeError("The AI returned an empty response.")

        return ai_reply.strip()

    except requests.exceptions.Timeout:
        raise RuntimeError("Groq API request timed out.")

    except requests.exceptions.HTTPError as error:
        raise RuntimeError(
            f"Groq API returned HTTP {error.response.status_code}."
        )

    except requests.exceptions.RequestException:
        raise RuntimeError("Unable to connect to Groq API.")

    except (KeyError, IndexError, TypeError):
        raise RuntimeError("Unexpected response received from Groq API.")
