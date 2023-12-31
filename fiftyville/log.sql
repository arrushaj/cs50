-- Keep a log of any SQL queries you execute as you solve the mystery.
SELECT description FROM crime_scene_reports WHERE year = 2021 AND month = 7 and day = 28 and street = "Humphrey Street";
-- We know the date of the crime and the street it took place on, now the logical thing to do is get a description of it.
-- Description revealed three witnesses who were present and the bakery is mentioned.
-- Crime took place at 10:15am
SELECT name, transcript FROM interviews WHERE year = 2021 AND month = 7 and day = 28;
-- We use this query to get transcripts of interviews from the date of the crime.
-- Ruth reveals that the thief left the scene of the crime shortly afterwards (within ten minutes of the theft) in a car and that we can use footage to see which car it was.
-- Eugene reveals that he saw the thief withdrawing money from an ATM on Leggett Street
-- Raymond reveals that as the thief was leaving the bakery, he talked to someone on the phone and he heard him say that he was planning on taking the earliest flight out of Fiftyville the next day
-- Raymond also reveals that the thief asked the person on the line to purchase the flight tickets
-- Emma, the bakery owner, heard someone whispering in the store for half an hour
SELECT activity, license_plate FROM bakery_security_logs WHERE year = 2021 AND month = 7 AND day = 28 AND hour = 10 AND minute > 10 AND minute < 20;
-- Using Ruth's testimony, I looked up footage that took place within 10 minutes of the crime and it reveals (from 10:05 to 10:25) and it reveals these license plates exited the parking lot:
+----------+---------------+
| activity | license_plate |
+----------+---------------+
| entrance | 13FNH73       |
| exit     | 5P2BI95       |
| exit     | 94KL13X       |
| exit     | 6P58WS2       |
| exit     | 4328GD8       |
+----------+---------------+
SELECT account_number, amount, transaction_type FROM atm_transactions WHERE year = 2021 AND month = 7 AND day = 28 AND atm_location = "Leggett Street";
-- The query above was used in accordance with Eugene's testimony about the ATM. It reveals all the transactions that took place on Leggett along with their account number and amount.
--+----------------+--------+------------------+
--| account_number | amount | transaction_type |
--+----------------+--------+------------------+
--| 28500762       | 48     | withdraw         |
--| 28296815       | 20     | withdraw         |
--| 76054385       | 60     | withdraw         |
--| 49610011       | 50     | withdraw         |
--| 16153065       | 80     | withdraw         |
--| 86363979       | 10     | deposit          |
--| 25506511       | 20     | withdraw         |
--| 81061156       | 30     | withdraw         |
--| 26013199       | 35     | withdraw         |
--+----------------+--------+------------------+
SELECT origin_airport_id, destination_airport_id, hour, minute FROM flights WHERE year = 2021 AND month = 7 AND day = 29 ORDER BY hour, minute;
-- Using the above query, we were able to get the earliest flight that took place at 8:20 the next day (the 29th)
-- The origin_airport_id is 8 and the destination_airport_id is 4
SELECT city FROM airports WHERE id = 4;
-- Using the above query, we discover that the city the thief most likely fled to was New York City!!
SELECT passport_number, seat FROM passengers WHERE flight_id IN (SELECT id FROM flights WHERE year = 2021 AND month = 7 AND day = 29 AND hour = 8 AND minute = 20);
-- Using the above query, we are able to find a list of passport numbers and seats on the flight the thief most likely was on:
+-----------------+------+
| passport_number | seat |
+-----------------+------+
| 7214083635      | 2A   |
| 1695452385      | 3B   |
| 5773159633      | 4A   |
| 1540955065      | 5C   |
| 8294398571      | 6C   |
| 1988161715      | 6D   |
| 9878712108      | 7A   |
| 8496433585      | 7B   |
+-----------------+------+
SELECT name, phone_number FROM people WHERE license_plate IN (SELECT license_plate FROM bakery_security_logs WHERE year = 2021 AND month = 7 and day = 28 AND hour = 10 AND minute > 5 AND minute < 25)
AND passport_number IN (SELECT passport_number FROM passengers WHERE flight_id IN (SELECT id FROM flights WHERE year = 2021 AND month = 7 AND day = 29 AND hour = 8 AND minute = 20));
-- This query reveals a list of people and phone numbers who are the suspects
+--------+----------------+
|  name  |  phone_number  |
+--------+----------------+
| Sofia  | (130) 555-0289 |
| Luca   | (389) 555-5198 |
| Kelsey | (499) 555-9472 |
| Bruce  | (367) 555-5533 |
+--------+----------------+
SELECT caller, receiver, duration FROM phone_calls WHERE year = 2021 AND month = 7 AND day = 28 AND caller IN (SELECT phone_number FROM people WHERE license_plate IN (SELECT license_plate FROM bakery_security_logs WHERE year = 2021 AND month = 7 and day = 28 AND hour = 10 AND minute > 5 AND minute < 25)
AND passport_number IN (SELECT passport_number FROM passengers WHERE flight_id IN (SELECT id FROM flights WHERE year = 2021 AND month = 7 AND day = 29 AND hour = 8 AND minute = 20)));
-- The above query provides a list of phone calls that took place the day of the crime involving the suspects
+----------------+----------------+----------+
|     caller     |    receiver    | duration |
+----------------+----------------+----------+
| (130) 555-0289 | (996) 555-8899 | 51       |
| (499) 555-9472 | (892) 555-8872 | 36       |
| (367) 555-5533 | (375) 555-8161 | 45       |
| (367) 555-5533 | (344) 555-9601 | 120      |
| (367) 555-5533 | (022) 555-4052 | 241      |
| (499) 555-9472 | (717) 555-1342 | 50       |
| (367) 555-5533 | (704) 555-5790 | 75       |
+----------------+----------------+----------+
SELECT name FROM people JOIN bank_accounts ON people.id = bank_accounts.person_id WHERE bank_accounts.account_number IN (SELECT account_number FROM atm_transactions WHERE year = 2021 AND month = 7 AND day = 28 AND atm_location = "Leggett Street")
AND (name = "Bruce" OR name = "Sofia" OR name = "Kelsey" OR name = "Luca");
-- The above query provides a list of people from the group of suspects that also used the ATM on the day of the crime
+-------+
| name  |
+-------+
| Bruce |
| Luca  |
+-------+
SELECT passport_number FROM passengers WHERE passport_number IN (SELECT passport_number FROM people WHERE (name = "Bruce" OR name = "Luca") AND (phone_number = "(367) 555-5533" OR phone_number = "(389) 555-5198"))
AND flight_id IN (SELECT id FROM flights WHERE year = 2021 AND month = 7 AND day = 29 AND hour = 8 AND minute = 20);
-- The above query reveals that both Bruce and Luca were on the flight that took place the next day (the earliest flight).
-- It is most likely that Bruce is the thief considering that Luca never placed a call the day of the crime.
SELECT name, passport_number, license_plate, phone_number FROM people WHERE phone_number IN (SELECT receiver FROM phone_calls WHERE year = 2021 AND month = 7 AND day = 28 AND caller = "(367) 555-5533");
-- This reveals the names of the people that Bruce placed a call to that day.
+---------+-----------------+---------------+----------------+
|  name   | passport_number | license_plate |  phone_number  |
+---------+-----------------+---------------+----------------+
| Gregory | 3355598951      | V4C670D       | (022) 555-4052 |
| Carl    | 7771405611      | 81MZ921       | (704) 555-5790 |
| Robin   |                 | 4V16VO0       | (375) 555-8161 |
| Deborah | 8714200946      | 10I5658       | (344) 555-9601 |
+---------+-----------------+---------------+----------------+
SELECT people.name, bank_accounts.account_number, bank_accounts.creation_year FROM people JOIN bank_accounts ON bank_accounts.person_id = people.id
WHERE (people.name = "Gregory" OR people.name = "Carl" OR people.name = "Robin" OR people.name = "Deborah");
-- This query reveals that only Robin has a bank account
+-------+----------------+---------------+
| name  | account_number | creation_year |
+-------+----------------+---------------+
| Robin | 94751264       | 2019          |
+-------+----------------+---------------+