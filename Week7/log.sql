-- Keep a log of any SQL queries you execute as you solve the mystery.
-- The queries below are just setup to get a basic understanding of the data.
.tables
SELECT * FROM airports;
SELECT * FROM crime_scene_reports LIMIT 5;
SELECT * FROM people LIMIT 5;
SELECT * FROM atm_transactions LIMIT 5;
SELECT * FROM flights LIMIT 5;
SELECT * FROM phone_calls LIMIT 5;
SELECT * FROM bakery_security_logs LIMIT 5;
SELECT * FROM bank_accounts LIMIT 5;
SELECT * FROM passengers LIMIT 5;
SELECT * FROM interviews LIMIT 100;

-- This is to get the crime scene report on the theft.
SELECT * FROM crime_scene_reports WHERE year=2024 AND month=7 AND street='Humphrey Street';
-- This will serve as a bookmark for me!
SELECT * FROM crime_scene_reports WHERE id=295;
-- I hope to get some useful data from the interviews conducted on the same day.
SELECT * FROM interviews WHERE year=2024 AND month=7 AND day=28;
-- Another bookmark on the interviews.
SELECT * FROM interviews WHERE id>160 AND id<164;
-- Bakery security logs contain data on the car licence plates, I can run them along with calls to see if I can find the suspect.
SELECT * FROM bakery_security_logs WHERE year=2024 AND month=7 AND day=28 AND activity='exit';
-- ATM withdraws done in the given location and the given day.
SELECT * FROM atm_transactions
WHERE year=2024 AND month=7 AND day=28
AND atm_location='Humphrey Lane' AND transaction_type='withdraw';
--Getting the licence plate to get a list of people who left the parking lot on that day.
SELECT license_plate FROM bakery_security_logs WHERE year=2024 AND month=7 AND day=28 AND activity='exit';
--A pretty long query that gets a list of people who withdrew money on that day in Humphrey Lane and also left the bakery parking lot.
SELECT DISTINCT p.id, p.name
           FROM people AS p
           JOIN bank_accounts AS ba ON p.id=ba.person_id
          WHERE license_plate IN
        (SELECT license_plate
           FROM bakery_security_logs
          WHERE year=2024 AND month=7 AND day=28 AND activity='exit')
            AND ba.account_number IN
        (SELECT account_number
           FROM atm_transactions
          WHERE year=2024 AND month=7 AND day=28
            AND atm_location='Leggett Street' AND transaction_type='withdraw');
--The result is Bruce, Diana, Iman. Luca, Taylor.
--This gives me flights on July 29th and I can see that the earliest flight was at 8:20 in the morning with id 36.
SELECT * FROM flights WHERE year=2024 AND month=7 AND day=29 AND origin_airport_id=8 ORDER BY hour LIMIT 1;
-- This returns a list of passengers who were on that flight.
SELECT * FROM passengers WHERE flight_id IN (SELECT id FROM flights WHERE year=2024 AND month=7 AND day=29 AND origin_airport_id=8 ORDER BY hour LIMIT 1);
-- This gets the names and information of the people.
SELECT * FROM people JOIN passengers ON people.passport_number=passengers.passport_number WHERE passengers.flight_id=36;
--And to combite the 2 queries:
SELECT DISTINCT *
           FROM people AS p
           JOIN bank_accounts AS ba ON p.id=ba.person_id
           JOIN passengers AS p2 ON p.passport_number=p2.passport_number
          WHERE p2.flight_id=36
            AND license_plate IN
        (SELECT license_plate
           FROM bakery_security_logs
          WHERE year=2024 AND month=7 AND day=28 AND activity='exit')
            AND ba.account_number IN
        (SELECT account_number
           FROM atm_transactions
          WHERE year=2024 AND month=7 AND day=28
            AND atm_location='Leggett Street' AND transaction_type='withdraw');
--This displays all phone calls from the suspects on July 28th. Which tells us its most likely Bruce or Taylor. As the querie is getting too long I will save the ID instead, 686048 and 449774.
--I will also find the people they called and see if they withdrew money that day. Their ID's are 233 and 254.
SELECT * FROM phone_calls AS ps WHERE ps.caller IN (
SELECT DISTINCT p.phone_number
           FROM people AS p
           JOIN bank_accounts AS ba ON p.id=ba.person_id
           JOIN passengers AS p2 ON p.passport_number=p2.passport_number
          WHERE p2.flight_id=36
            AND license_plate IN
        (SELECT license_plate
           FROM bakery_security_logs
          WHERE year=2024 AND month=7 AND day=28 AND activity='exit')
            AND ba.account_number IN
        (SELECT account_number
           FROM atm_transactions
          WHERE year=2024 AND month=7 AND day=28
            AND atm_location='Leggett Street' AND transaction_type='withdraw'))
            AND ps.day=28 AND ps.duration<60;
--This gives us 2 names!
SELECT name FROM people as p JOIN phone_calls AS ps ON p.phone_number=ps.receiver  WHERE ps.id=233 OR ps.id=254;
--We can find their account number using this querie. Also notice that James does not have an account.
SELECT account_number FROM bank_accounts AS ba WHERE person_id IN(SELECT people.id FROM people JOIN phone_calls ON people.phone_number=phone_calls.receiver WHERE phone_calls.id IN (233,254));
--As the querie above gave no useful insight, I decided to focus on when the withdrawals, car and phone call were made instead.
--This will show when the 2 suspects left the bakery.
SELECT * FROM bakery_security_logs WHERE license_plate IN(SELECT license_plate FROM people WHERE id IN (686048,449774));
--I found out that the theft took place at 10:15am so the thief is Bruce who's licene plate is 94KL13X.
