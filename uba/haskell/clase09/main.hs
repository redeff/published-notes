mcd :: Integer -> Integer -> Integer
mcd a 0
    | a > 0     = a
    | otherwise = -a
mcd a b = mcd b (a `mod` b)

mcd' a b
    | a > b     = mcd' (a-b) b
    | a < b     = mcd' a (b-a)
    | otherwise = a

divide :: Integer -> Integer -> Bool
divide a b = b == 0 || b `mod` a == 0
mcd'' a b = last $ filter (\x -> x `divide` a && x `divide` b) [1..a]

esPar :: Integer -> Bool
esPar n = n `mod` 2 == 0

mcd''' a b
    | a == 0             = b
    | b == 0             = a
    | esPar a && esPar b = 2 * mcd''' (a `div` 2) (b `div` 2)
    | esPar a            = mcd''' (a `div` 2) b
    | esPar b            = mcd''' a (b `div` 2)
    | a > b              = mcd''' b (a-b)
    | a < b              = mcd''' a (b-a)
    | otherwise          = a

emcd :: Integer -> Integer -> (Integer, Integer, Integer)
emcd a 0
    | a > 0     = (a, 1, 0)
    | a < 0     = (-a, -1, 0)

emcd a b = (g, t, s - t*q) where
    q = a `div` b
    (g, s, t) = emcd b (a - q*b)
    -- fb + s(a-qb) = g
    -- fb + sa - sqb = g
    -- sa + (f-sq)b = g

-- Ecuaciones Diofánticas
-- x = a_i (mod m_i)
-- x = k * m_i + a_i
-- km + a = k'm' + a'
-- km + k'm' = a' - a

solve :: Integer -> Integer -> Integer -> (Integer, Integer)
solve a b k = (s * d, t * d) where
    (g, s, t) = emcd a b
    d = if k `mod` g == 0 then k `div` g else undefined

join :: (Integer, Integer) -> (Integer, Integer) -> (Integer, Integer)
join (a, m) (a', m') = ((k*m + a) `mod` mm, mm) where
    mm = (m*m') `div` mcd m m'
    (k, _) = solve m m' (a' - a)

joinMany :: [(Integer, Integer)] -> (Integer, Integer)
joinMany = foldl join (0, 1)
