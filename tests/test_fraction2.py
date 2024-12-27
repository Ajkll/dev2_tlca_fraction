import pytest
from module_perso.Fraction import (
    Fraction,
    NullDenominatorValueException,
    InvalidOperandTypeException,
)

class TestUnitaireFraction:
    def test_fraction_initialization(self):

        # tests valeurs positives
        original_num, original_den = 222, 12334
        frac = Fraction(original_num, original_den)

        simplified_num = frac.numerator
        simplified_den = frac.denominator

        recalculated_num = simplified_num * (original_den // simplified_den)
        recalculated_den = simplified_den * (original_num // simplified_num)

        assert recalculated_num == original_num
        assert recalculated_den == original_den

        # tests valeurs negatives
        original_num, original_den = -11, -22
        frac = Fraction(original_num, original_den)

        simplified_num = frac.numerator
        simplified_den = frac.denominator

        recalculated_num = simplified_num * (original_den // simplified_den)
        recalculated_den = simplified_den * (original_num // simplified_num)

        assert recalculated_num == original_num
        assert recalculated_den == original_den

        frac = Fraction(0, 5)
        assert frac.numerator == 0
        assert frac.denominator == 1

        assert Fraction(4, 8).__str__() == "1/2" # test str simple
        assert Fraction(-3, -6).__str__() == "1/2" # test str fraction positive attendue
        assert Fraction(-2, 3).__str__() == "-2/3" # test str fraction negative attendue
        assert Fraction(3, -7).__str__() == "-3/7" # test str fraction negative attendue
        assert Fraction(0, 5).__str__() == "0" # test str fraction nulle
        assert Fraction(5, 5).__str__() == "1" # test str fraction unitaire

        with pytest.raises(NullDenominatorValueException):
            Fraction(1, 0)


    @pytest.mark.parametrize(
        "numerator, denominator, expected_result, expected_exception",
        [
            (1, 1, "1", None),  # cas limite avec 2 int
            (1, 4, "1/4", None),  # fraction positive 
            (8, 4, "2", None),  # fraction simplifiable en un int
            (0, 5, "0", None),  # fraction null (0)
            (-8, 4, "-2", None),  # fraction simplifiable en un int negative
            (5, 4, "1 1/4", None),  # mixte positif
            (-5, 4, "-1 1/4", None),  # mixte negatif
        ],
    )
    def test_as_mixed_number(self,numerator, denominator, expected_result, expected_exception):
        if expected_exception:
            with pytest.raises(expected_exception):
                frac = Fraction(numerator, denominator)
                frac.as_mixed_number() #ici exemple pour lever une exception mais Fraction avec la mehtode as_mixed_number ne dois pas lever d'exception donc test par l'absurde en quelques sorte
        else:
            frac = Fraction(numerator, denominator)
            assert frac.as_mixed_number() == expected_result


    @pytest.mark.parametrize(
        "input_value, expected_result, expected_exception",
        [
            (5, Fraction(5, 1), None),  # cas normale avec un int
            (Fraction(3, 4), Fraction(3, 4), None),  # as normale avec un int
            (2.5, None, InvalidOperandTypeException),  # erreur avec float  
            ("hhh", None, InvalidOperandTypeException),  # erreur avec chaîne de caractères
            (True, None, InvalidOperandTypeException),  # erreur avec booléen  
            (None, None, InvalidOperandTypeException),  # erreur avec None
        ],  #ont pourrais en soit tester avec d'autre type() mais cela devrais suffire
    )
    def test_check_fraction_or_int(self,input_value, expected_result, expected_exception):
        frac = Fraction(
            1, 2
        )  # Fraction de base pour tester les exception ici et pas dans @pytest.mark.parametrize( sans quoi le test serais effectuers en dehors de test_check_fraction_or_int et donc non pris en compt par pytest

        if expected_exception:
            with pytest.raises(expected_exception):
                frac._check_fraction_or_int(input_value)
        else:
            result = frac._check_fraction_or_int(input_value)
            assert isinstance(result, Fraction)
            assert result == expected_result


    @pytest.mark.parametrize(
        "fraction1, fraction2, expected_result",
        [
            (1, 1, Fraction(2, 1)),  # cas limite - additions de deux int
            (Fraction(1, 2), Fraction(1, 3), Fraction(5, 6)),  # addition normale
            (Fraction(1, 2), 1, Fraction(3, 2)),  # addition avec un entier
            (Fraction(0, 1), Fraction(1, 3), Fraction(1, 3)),  # addition avec une fraction nulle (0)
        ],
    )
    def test_add(self,fraction1, fraction2, expected_result):
        result = fraction1 + fraction2
        assert result == expected_result


    @pytest.mark.parametrize(
        "fraction1, fraction2, expected_result",
        [
            (4, 2, Fraction(2, 1)),  # cas limite - soustraction entre 2 int
            (Fraction(3, 4), Fraction(1, 4), Fraction(1, 2)),  # soustraction normale
            (Fraction(5, 3), 2, Fraction(-1, 3)),  # soustraction avec un entier
            (Fraction(3, 4), Fraction(0, 1), Fraction(3, 4)),  # soustraction avec zéro
        ],
    )
    def test_sub(self,fraction1, fraction2, expected_result):
        result = fraction1 - fraction2
        assert result == expected_result


    @pytest.mark.parametrize(
        "fraction1, fraction2, expected_result",
        [
            (2, 3, Fraction(6, 1)),  # cas limite - multiplication de deux int
            (Fraction(1, 2), Fraction(2, 3), Fraction(2, 6)),  # multiplication normale
            (Fraction(1, 2), 3, Fraction(3, 2)),  # multiplication avec un entier
            (Fraction(1, 2), Fraction(0, 1), Fraction(0, 1)),  # multiplication avec zéro on attend donc 0 ou une fraction equivalent a 0
        ],
    )
    def test_mul(self,fraction1, fraction2, expected_result):
        result = fraction1 * fraction2
        assert result == expected_result


    @pytest.mark.parametrize(
        "self_fraction, another_fraction, expected_result, expected_exception",
        [
            (Fraction(3, 4), Fraction(2, 5), Fraction(15, 8), None),  # division normale
            (Fraction(3, 4), 2, Fraction(3, 8), None),  # division avec un entier
            (
                Fraction(3, 4),
                Fraction(0, 1),
                None,
                ZeroDivisionError,
            ),  # une division par zero (den=0)
            (
                Fraction(0, 1),
                Fraction(2, 3),
                Fraction(0, 1),
                None,
            ),  # division avec zero (num=0)
            (Fraction(3, 4), -2, Fraction(-3, 8), None),  # division par un entier négatif
        ],
    )
    def test_truediv(self,self_fraction, another_fraction, expected_result, expected_exception):
        if expected_exception:
            with pytest.raises(expected_exception):
                self_fraction / another_fraction #Encore une fois cela devrait lever l'exception quand elle est attendue par pytest
        else:
            result = self_fraction / another_fraction
            assert result == expected_result


    @pytest.mark.parametrize(
        "fraction_instance, power, expected_result, expected_exception",
        [
            (Fraction(3, 4), 1, Fraction(3, 4), None),  # puissance 1
            (Fraction(3, 4), 2, Fraction(9, 16), None),  # puissance 2 (positive)
            (Fraction(3, 4), 0, Fraction(1, 1), None),  # puissance nulle on s'attend a 1 ou fraction equivalente
            (
                Fraction(3, 4),
                -2,
                Fraction(16, 9),
                None,
            ),  # puissance -2 négative
            (
                Fraction(0, 1),
                -1,
                None,
                ZeroDivisionError,
            ),  # puissance negative avec num nul
            (Fraction(3, 4), 2.5, None, ValueError),  # puissance float (invalide)
            (Fraction(3, 4), "testo", None, ValueError),  # puissance invalide
        ],
    )
    def test_pow(self,fraction_instance, power, expected_result, expected_exception):
        if expected_exception:
            with pytest.raises(expected_exception):
                fraction_instance**power
        else:
            result = fraction_instance**power
            assert result == expected_result


    @pytest.mark.parametrize(
        "self_fraction, another_fraction, expected_result",
        [
            (Fraction(1, 1), Fraction(1, 1), True),  # cas limite avec 2 int
            (Fraction(1, 2), Fraction(1, 2), True),  # fractions identiques
            (Fraction(1, 2), Fraction(3, 4), False),  # fractions différentes
            (Fraction(2, 1), 2, True),  # comparaison avec un int equivalent
            (Fraction(2, 1), 3, False),  # comparaison avec un int non equivalent
            (
                Fraction(1, 2),
                Fraction(-1, 2),
                False,
            ),  # cas limitte comparaison avec une fraction négative
        ],
    )
    def test_eq(self,self_fraction, another_fraction, expected_result):
        assert (self_fraction == another_fraction) == expected_result


    @pytest.mark.parametrize(
        "self_fraction, expected_result",
        [
            (Fraction(1, 1), 1),  # cas limite avec 2 int
            (Fraction(3, 4), 0.75),  # Fraction positive
            (Fraction(-3, 4), -0.75),  # Fraction négative
            (Fraction(0, 1), 0.0),  # cas limite fraction égale à zéro
        ],
    )
    def test_float(self,self_fraction, expected_result):
        result = float(self_fraction)
        assert pytest.approx(result, 0.0001) == expected_result


    @pytest.mark.parametrize(
        "self_fraction, another_fraction, expected_result",
        [
            (1, 1, False),  # cas limite
            (Fraction(1, 2), Fraction(3, 4), True),  # Fraction 1/2 < Fraction 3/4
            (Fraction(1, 2), Fraction(2, 4), False),  # Fraction 1/2 < Fraction 2/4 (egales)
            (Fraction(1, 3), 1, True),  # Fraction 1/3 < 1
            (Fraction(1, 2), 0, False),  # Fraction 1/2 < 0
            (Fraction(1, 3), -1, False),  # Fraction 1/3 < -1
        ],
    )
    def test_lt(self,self_fraction, another_fraction, expected_result):
        assert (self_fraction < another_fraction) == expected_result


    @pytest.mark.parametrize(
        "fraction1, fraction2, expected_result",
        [
            (Fraction(1, 2), Fraction(3, 4), True),  # comparaison simple (1/2 <= 3/4)
            (Fraction(1, 2), 1, True),  # comparaison 1/2 <= 1
            (1, 2, True),  # comparaison entre deux entiers 1 <= 2
            (
                Fraction(0, 1),
                Fraction(0, 1),
                True,
            ),  # comparaison entre deux fractions egales à zero 
        ],
    )
    def test_fraction_le_valid(self,fraction1, fraction2, expected_result):
        assert (fraction1 <= fraction2) == expected_result


    @pytest.mark.parametrize(
        "fraction, expected_result",
        [
            (-1, 1),  # cas limite avec 2 int
            (Fraction(3, 4), Fraction(3, 4)),  # fraction positive
            (Fraction(-3, 4), Fraction(3, 4)),  # fraction negative
            (Fraction(0, 1), Fraction(0, 1)),  # fraction zero
        ],
    )
    def test_abs_fraction_valid(self,fraction, expected_result):
        result = abs(fraction)
        assert result == expected_result


    @pytest.mark.parametrize(
        "fraction, expected_result",
        [
            (Fraction(0, 1), True),  # fraction egale à zero
            (Fraction(1, 2), False),  # fraction non egale à zero
        ],
    )
    def test_is_zero(self,fraction, expected_result):
        result = fraction.is_zero()
        assert result == expected_result


    @pytest.mark.parametrize(
        "num, den, expected_result",
        [
            (3, 1, True),  # fraction simplifiable en int
            (3, 2, False),  # fraction simple
            (0, 1, True),  # fraction zero
            (-4, 1, True),  # fraction negative
        ],
    )
    def test_is_integer(self,num, den, expected_result):
        fraction = Fraction(num, den)
        assert fraction.is_integer() == expected_result


    @pytest.mark.parametrize(
        "num, den, expected_result",
        [
            (1, 2, True),  # fraction positive
            (-1, 3, True),  # fraction négative
            (3, 3, False),  # fraction egale à 1
            (0, 5, True),  # fraction zero
        ],
    )
    def test_is_proper(self,num, den, expected_result):
        fraction = Fraction(num, den)
        assert fraction.is_proper() == expected_result


    @pytest.mark.parametrize(
        "num, den, expected_result",
        [
            (1, 2, True),  # fraction unitaire positive
            (-1, 3, True),  # fraction unitaire négative
            (2, 3, False),  # num autre que 11
            (0, 5, False),  # fraction zero
        ],
    )
    def test_is_unit(self,num, den, expected_result):
        fraction = Fraction(num, den)
        assert fraction.is_unit() == expected_result


    # amélioration notable , ajout de tests pour  __ge__ et __gt__ ajouter des journaux de log , ajouter plus de cas limite , et des tests sur des fractions tres grandes , etc
    """
    ici les tests unitaire n'ont pas selon moi à tester les diférents exception qui peuvent etre génerer par l'appel d'autre fonctions , 
    pour moi cela attrait à des test d'integration qui pourrais etre ajouter comme par exemple 

        def __add__(self, another_fraction) -> "Fraction":
            
            Add two fractions

            PRE -

            POST - Returns a Fraction instance:
                Return the addition of two fractions

            
            another_fraction = self._check_fraction_or_int(another_fraction)
            return Fraction(
                self._num * another_fraction._den + another_fraction._num * self._den,
                self._den * another_fraction._den,
            )
        
        ici les tests pour cette methode ne vérifie pas si another_fraction = self._check_fraction_or_int(another_fraction) va bien lever l'exception attendue , 
        cela attrait aux tests unitaire de check_fraction_or_int selon moi , donc un ajout interresant serais simplement des test d'integration pour verifier cela !
        
    """
    #note : l'outils black à mis en page bizarement certaines lignes de code dans ce fichier mais apparement ca respect mieux la norme pep8 comme ca ..
