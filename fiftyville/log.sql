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
SELECT activity, license_plate FROM bakery_security_logs WHERE year = 2021 AND month = 7 AND day = 28 AND hour = 10 AND minute > 15 AND minute < 25;
-- Using Ruth's testimony, I looked up footage that took place within 10 minutes of the crime and it reveals (from 10:15 to 10:25) and it reveals these license plates exited the parking lot:
--+----------+---------------+
--| activity | license_plate |
--+----------+---------------+
--| exit     | 5P2BI95       |
--| exit     | 94KL13X       |
--| exit     | 6P58WS2       |
--| exit     | 4328GD8       |
--| exit     | G412CB7       |
--| exit     | L93JTIZ       |
--| exit     | 322W7JE       |
--| exit     | 0NTHK55       |
--+----------+---------------+
