-- Keep a log of any SQL queries you execute as you solve the mystery.
SELECT description FROM crime_scene_reports WHERE year = 2021 AND month = 7 and day = 28 and street = "Humphrey Street";
-- We know the date of the crime and the street it took place on, now the logical thing to do is get a description of it. Description revealed three witnesses who were present and the bakery is mentioned.
SELECT name, transcript FROM interviews WHERE year = 2021 AND month = 7 and day = 28;
-- 
