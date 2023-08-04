# 1. Boolean Identities
Boolean logic refresher as described in unit 1.1 of "Nand to Tetris Part I".

## Commutative Laws

* $ x \text{ AND } y = y \text{ AND } x $
* $ x \text{ OR } y = y \text{ OR } x $

## Associative Laws

* $ x \text{ AND } (y \text{ AND } z) = (x \text{ AND } y) \text{ AND } z $
* $ x \text{ OR } (y \text{ OR } z) = (x \text{ OR } y) \text{ OR } z $

## Distributive Laws

* $ x \text{ AND } (y \text{ OR } z) = (x \text{ AND } y) \text{ OR } (x \text{ AND } z) $
* $ x \text{ OR } (y \text{ AND } z) = (x \text{ OR } y) \text{ AND } (x \text{ OR } z) $

## De Morgan Laws

* $ \text{NOT} (x \text{ AND } y) = \text{NOT} (x) \text{ OR } \text{NOT} (y) $
* $ \text{NOT} (x \text{ OR } y) = \text{NOT} (x) \text{ AND } \text{NOT} (y) $

## Double Negation Law

* $ \text{NOT} (\text{NOT} (x)) = x $

## Idempotent Law

Idempotence is the property of certain operations in mathematics and computer science that they can be applied multiple times without changing the result beyond the initial application.

Boolean logic has idempotence within both AND and OR gates. A logical AND gate with two inputs A will also have an output of A. (1 AND 1 = 1, 0 AND 0 = 0). An OR gate has idempotence because 0 OR 0 = 0, and 1 OR 1 = 1.

* $ A + A = A $
* $ A * A = A $

* ex.:
$$ \text{NOT} (x) \text{ AND } \text{NOT} (x) = \text{NOT} (x) $$


# 2. Boolean Function Synthesis
Construct boolean functions from primitive operations.

## Truth Table to Boolean Functions

1. Identify *all* rows in the truth table that contain *any* **1**
2. Construct one boolean function per row, giving the desired output
    * these functions will *not* give the other rows' desired output
3. Concatenate functions using **OR** operations
4. *Optional:* Simplify using laws presented above 

## Nand Is All You Need

**Theorem**: *Any* boolean function can be represented using an expression containing only **NAND** operations.

* $ \text{NOT}(x) = x \text{ NAND } x $
    * $ \text{NAND(x, x)} $
* $ x \text{ AND } y = \text{NOT}(x \text{ NAND } y) $
    * $ \text{NAND(\text{ NAND(x, x) }, \text{ NAND(y, y) })} $