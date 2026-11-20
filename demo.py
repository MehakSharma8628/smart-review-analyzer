
from text_analyzer import print_report

REVIEWS = {
    "Review 1 - Restaurant (positive)": (
        "We visited Green Leaf Cafe in Ludhiana on 12 March 2026. "
        "The food was delicious and the staff were friendly and helpful. "
        "The pasta was excellent and the service was fast. "
        "I would recommend this cafe to everyone. "
        "Dinner for two cost Rs. 1,200, which is a great price."
    ),

    "Review 2 - Laptop (negative)": (
        "I bought a laptop from TechMart in January 2026 for $850. "
        "The battery is terrible and the screen is noisy and flickers. "
        "Support was rude and slow, and my refund request was never answered. "
        "This was a waste of money. "
        "Contact support@techmart.com if you have the same problem."
    ),

    "Review 3 - Hotel (mixed)": (
        "Our stay at Hotel Sunrise in Shimla was nice, and the view was beautiful. "
        "The room was clean and comfortable. "
        "However, the breakfast was cold and the wifi was not good. "
        "Check-in was slow, but the manager Ravi Kumar fixed the problem quickly."
    ),
}


if __name__ == "__main__":
    for title, text in REVIEWS.items():
        print_report(title, text)
