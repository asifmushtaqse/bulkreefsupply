from csv import DictReader


class Statistics:
    def __init__(self):
        self.get_statistics()

    def get_statistics(self):
        quantities = self.get_quantities()

        print(f"Total Products = {len(quantities)}")

        p_100 = [p for p in quantities if p <= 100]  # 1605
        p_300 = [p for p in quantities if p > 100 and p <= 300]  # 288
        p_500 = [p for p in quantities if p > 300 and p <= 500]  # 68
        p_700 = [p for p in quantities if p > 500 and p <= 700]  # 20
        p_800 = [p for p in quantities if p > 700 and p <= 800]  # 11
        p_900 = [p for p in quantities if p > 800 and p <= 900]  # 13
        p_1000 = [p for p in quantities if p > 900]  # 40

        self.display(p_100, 0, 100)
        self.display(p_300, 100, 300)
        self.display(p_500, 300, 500)
        self.display(p_700, 500, 700)
        self.display(p_800, 700, 800)
        self.display(p_900, 800, 900)
        self.display(p_1000, 900, "or more than 1000")

    def apply_binary_search(self):
        mx = 1000
        mid = mx / 2

    def display(self, quantity, start, end):
        print(f"{len(quantity)} Products have Quantity from {start} to {end}")

    def get_quantities(self):
        quantity_str = ",".join(r['quantity_29Mar2023'] for r in DictReader(open('../output/statistics.csv')))
        quantities = [int(n.strip()) for n in quantity_str.split(',') if n.strip()]
        return quantities


if __name__ == "__main__":
    pass
    # Statistics()
