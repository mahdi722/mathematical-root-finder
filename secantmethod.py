import time
import math

class SecantMethod:

    def get_polynomial(self, string_polynomial):
        """Set the polynomial coefficients."""
        self.polynomial = string_polynomial
        self.adjust_order()

    def adjust_order(self):
        """Adjust the polynomial order by reducing the power of each term."""
        while self.min_order(self.polynomial) != 0:
            for term in self.polynomial:
                term[0] -= 1

    @staticmethod
    def min_order(poly):
        """Get the minimum order (highest power) from the polynomial."""
        return min(poly, key=lambda x: x[0])[0]

    @staticmethod
    def max_order(poly):
        """Get the maximum order (highest power) from the polynomial."""
        max_order = max(poly, key=lambda x: x[0])
        return [max_order[0], max_order[1]]

    def roots_quadratic(self, poly):
        """Calculate roots for a quadratic polynomial."""
        a, b, c = poly[0][1], poly[1][1], poly[2][1]
        discriminant = b**2 - 4*a*c
        if discriminant < 0:
            return []
        else:
            return [(-b - math.sqrt(discriminant)) / (2*a),
                    (-b + math.sqrt(discriminant)) / (2*a)]

    @staticmethod
    def evaluate_poly(poly, x):
        """Evaluate the polynomial at a given point x."""
        return sum(coef * (x ** exp) for exp, coef in poly)

    @staticmethod
    def factorial(n):
        """Calculate the factorial of a number n."""
        return math.factorial(n)

    def differentiate(self, poly):
        """Differentiate the polynomial."""
        return [[exp - 1, coef * self.factorial(exp) / self.factorial(exp - 1)]
                for exp, coef in poly if exp != 0]

    def find_starting_x(self, x, poly, positive):
        """Find a starting point for the secant method."""
        step = 10 ** (-5)
        n = 0
        while True:
            if (self.evaluate_poly(poly, x) > 0 and positive) or \
               (self.evaluate_poly(poly, x) < 0 and not positive):
                break
            if n == 100:
                step *= 10
                n = 0
            n += 1
            x -= step if positive else -step
        return x

    def secant_method(self, x0, x1, n, P):
        """Apply the secant method to find a root."""
        for _ in range(n - 1):
            if self.evaluate_poly(P, x1) - self.evaluate_poly(P, x0) != 0:
                new_x = (x0 * self.evaluate_poly(P, x1) - x1 * self.evaluate_poly(P, x0)) / \
                        (self.evaluate_poly(P, x1) - self.evaluate_poly(P, x0))
                x0, x1 = x1, new_x
            else:
                break
        return x1

    def polynomial_chain(self, poly):
        """Generate a chain of polynomials by differentiation."""
        roots = [poly]
        while self.max_order(roots[-1])[0] != 2:
            roots.append(self.differentiate(roots[-1]))
        return roots

    def filter_roots(self, poly, roots):
        """Filter the roots based on polynomial evaluation."""
        filtered = []
        for i, root in enumerate(roots):
            if i == 0 or i == len(roots) - 1:
                filtered.append(root)
            else:
                if self.evaluate_poly(poly, root) == 0 or \
                   self.evaluate_poly(poly, roots[i+1]) * self.evaluate_poly(poly, root) < 0:
                    filtered.append(root)
        return filtered

    def find_boundaries_with_n(self, poly, n):
        """Find boundaries using the secant method with a fixed number of iterations."""
        start_time = time.time()
        if self.max_order(poly)[0] == 2:
            return self.roots_quadratic(poly)
        elif self.max_order(poly)[0] == 1:
            return -self.evaluate_poly(poly, 0) / self.evaluate_poly(poly, 1)
        else:
            all_polynomials = self.polynomial_chain(poly)
            all_roots = []
            for i in range(len(all_polynomials)):
                current_poly = all_polynomials[-1]
                roots = [self.secant_method(all_roots[-1][j], all_roots[-1][j + 1], n, current_poly)
                         for j in range(len(all_roots[-1]) - 1)]
                all_roots.append(self.filter_roots(current_poly, roots))
            end_time = time.time()
            return all_roots[-1], "sec : ", (end_time - start_time)

    def find_boundaries_with_err(self, poly, err):
        """Find boundaries using the secant method with a given error tolerance."""
        start_time = time.time()
        if self.max_order(poly)[0] == 2:
            return self.roots_quadratic(poly)
        elif self.max_order(poly)[0] == 1:
            return -self.evaluate_poly(poly, 0) / self.evaluate_poly(poly, 1)
        else:
            all_polynomials = self.polynomial_chain(poly)
            all_roots = []
            counters = []
            for i in range(len(all_polynomials)):
                current_poly = all_polynomials[-1]
                roots = []
                counter = 0
                for j in range(len(all_roots[-1]) - 1):
                    if isinstance(all_roots[-1][j], list):
                        x0, x1 = all_roots[-1][j]
                        res = self.secant_method(x0, x1, 300, current_poly)
                        counter += 300
                    else:
                        res = self.secant_method(all_roots[-1][j], all_roots[-1][j + 1], 300, current_poly)
                        counter += 300
                    roots.append(res)
                roots = self.filter_roots(current_poly, roots)
                all_roots.append(roots)
                counters.append(counter)
            end_time = time.time()
            return all_roots[-1], counters[-1], "sec : ", (end_time - start_time)

    def final(self):
        """Final output based on polynomial order."""
        max_order = self.max_order(self.polynomial)[0]
        if max_order == 0:
            return "none"
        elif max_order == 1:
            return -self.evaluate_poly(self.polynomial, 0) / self.evaluate_poly(self.polynomial, 1)
        elif max_order == 2:
            if self.polynomial[1][1] ** 2 - self.polynomial[0][1] * self.polynomial[2][1] < 0:
                return "it has no real roots"
            else:
                return self.roots_quadratic(self.polynomial)
        elif max_order >= 3:
            return self.find_boundaries_with_n(self.polynomial)

# Example usage
m = SecantMethod()
m.get_polynomial([[8, 1], [7, 0], [6, -1], [5, 0.1], [4, -4], [3, 1], [2, 6], [1, -1], [0, -1]])
print(m.find_boundaries_with_err([[8, 1], [7, 0], [6, -1], [5, 0.1], [4, -4], [3, 1], [2, 6], [1, -1], [0, -1]], 1e-14))
print(m.find_boundaries_with_err([[7, 1], [6, -5], [5, 7], [4, -6], [3, 11], [2, -7], [1, 5], [0, -6]], 1e-14))
print(m.find_boundaries_with_err([[4, 1], [3, -1], [2, -3], [1, 1], [0, 1]], 1e-14))
