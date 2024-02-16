import json
import argparse
import time


def read_json_file(file_path):
    """Read and return the JSON content from a file."""
    try:
        with open(file_path, "r") as file:
            return json.load(file)
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return None


def compute_total_sales(products, sales):
    """Compute the total cost of all sales."""
    total_cost = 0
    product_price_mapping = {product["title"]: product["price"] for product in products}

    for sale in sales:
        product_name = sale["Product"]
        quantity = sale["Quantity"]
        # Matching product names in sales with titles in product list
        # Assuming product titles in sales records might be slightly different (e.g., missing 'sweet' in 'Sweet fresh stawberry')
        matched_product = next(
            (
                title
                for title in product_price_mapping
                if product_name.lower() in title.lower()
            ),
            None,
        )

        if matched_product:
            total_cost += product_price_mapping[matched_product] * quantity
        else:
            print(f"Warning: Product '{product_name}' not found in price catalog.")
    return total_cost


def main():
    """Main function to parse arguments, compute sales, and log results."""
    parser = argparse.ArgumentParser(description="Compute total sales from JSON data.")
    parser.add_argument(
        "priceCatalogue", type=str, help="Path to price catalogue JSON file"
    )
    parser.add_argument("salesRecord", type=str, help="Path to sales record JSON file")
    args = parser.parse_args()

    start_time = time.time()

    products = read_json_file(args.priceCatalogue)
    sales = read_json_file(args.salesRecord)

    if products is None or sales is None:
        return

    total_sales = compute_total_sales(products, sales)

    elapsed_time = time.time() - start_time

    result_message = (
        f"Total Sales: ${total_sales:.2f}\nExecution Time: {elapsed_time:.2f} seconds"
    )
    print(result_message)

    with open("SalesResults.txt", "w") as file:
        file.write(result_message)


if __name__ == "__main__":
    main()
