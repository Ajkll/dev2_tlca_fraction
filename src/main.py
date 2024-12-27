from module_perso.Fraction import (
    Fraction,
    NullDenominatorValueException,
    InvalidOperandTypeException,
)

def main():
    # quelques exempel génerer par chatgpt quand je lui ai passer ma class !
    f1 = Fraction(3, 4)
    f2 = Fraction(5, 4)
    print(f"Fraction 1: {f1}")
    print(f"Fraction 2: {f2}")

    print(f"Addition: {f1} + {f2} = {f1 + f2}")

    print(f"Soustraction: {f1} - {f2} = {f1 - f2}")

    print(f"Multiplication: {f1} * {f2} = {f1 * f2}")

    print(f"Division: {f1} / {f2} = {f1 / f2}")

    print(f"Fraction 1 en nombre mixte: {f1.as_mixed_number()}")

    try:
        invalid_fraction = Fraction(12, 0)
    except NullDenominatorValueException as e:
        print(f"Exception capturée: {e}")

    try:
        print(f"Addition avec un booléen: {f1 + True}")
    except InvalidOperandTypeException as e:
        print(f"Exception capturée: {e}")

    try:
        print(f"Division par zéro: {f1 / Fraction(0)}")
    except ZeroDivisionError as e:
        print(f"Exception capturée: {e}")

    # un exemple a moi pour montrer que les exceptions peuvent etre intercepter si elle sont dans un gestionnaire try except
    try:
        f = Fraction(12, 0)
    except NullDenominatorValueException as e:
        print(f"exemple ici on intercept cette exception - {e}")

    # d'autres exemple d'utilisation de la class Fraction
    f1 = Fraction(3, 4)
    f2 = Fraction(5, 4)
    f3 = Fraction(2, -6)  

    print(f1)
    print(f2)
    print(f3)

    print(f1 + f2)
    print(f1 - f2)
    print(f1 * f2)
    print(f1 / f2)

    print(f1.as_mixed_number())
    print(f3.as_mixed_number())

    print(f1 == f2)
    print(f1 < f2)
    print(f1 <= f2)
    print(f1 > f2)
    print(f1 >= f2)

    print(f1.numerator)
    print(f1.denominator)

    print(float(f1))

    print(f1.is_zero(      ))
    print(f1.is_integer(   ))
    print(f1.is_proper())
    print(f1.is_unit())

    print(abs(f3))

    print(f1 ** 2)
    print(f1 ** -1)


if __name__ == "__main__":
    main()
