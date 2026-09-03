-- 1. Overdue tool loans
-- Which tools are currently checked out and past their due_date (not yet returned)? 
-- Show tool name, borrower name, and how many days overdue.
SELECT tools.name, members.full_name, (CURRENT_DATE - tool_loans.due_date) as days_overdue
FROM tools JOIN tool_loans ON tools.tool_id = tool_loans.tool_id
JOIN members ON tool_loans.member_id = members.member_id
WHERE tool_loans.return_date IS NULL
AND tool_loans.due_date < CURRENT_DATE;

-- 2. Low stock parts warning
-- List all parts where stock_qty has fallen below min_threshold — this is exactly what should 
-- power the "Parts Warnings" stat in the header banner.
SELECT * FROM parts WHERE stock_qty < min_threshold;

-- 3. Volunteer workload
-- For each volunteer, how many repair tickets are currently assigned to them that are not 
-- yet completed? Order by workload descending — useful for figuring out who's overloaded.
SELECT volunteers.volunteer_id, volunteers.full_name, COUNT(rt.status) AS open_tickets
FROM volunteers LEFT JOIN repair_tickets AS rt -- Left Join to search for volunteers who are not working on any ticket
ON rt.assigned_volunteer_id = volunteers.volunteer_id
WHERE rt.status IN ('intake', 'diagnosing', 'in_progress', 'awaiting_parts')
GROUP BY volunteers.volunteer_id, volunteers.full_name
ORDER BY open_tickets DESC;

-- 4. Total carbon offset so far
-- What's the total carbon offset (in kg CO2) from all completed repair tickets? (Hint: this needs weight_kg from 
-- tickets joined against carbon_multiplier from categories, summed only where status = completed.)
SELECT SUM(rt.weight_kg * categories.carbon_multiplier) as total_carbon_offset 
FROM repair_tickets AS rt JOIN categories 
ON rt.category_id = categories.category_id
WHERE rt.status = 'completed';

-- 5. Skills-matched volunteer suggestion
-- For a given category (say, "Electronics"), list all volunteers who have that specialty AND are currently 
-- on_shift — this is the exact query the "Skills-Matched Volunteer Filtering" dropdown needs to run live.
SELECT volunteers.volunteer_id, volunteers.full_name, categories.name
FROM volunteers JOIN volunteer_specialties AS vs 
ON volunteers.volunteer_id = vs.volunteer_id
JOIN categories ON categories.category_id = vs.category_id
WHERE volunteers.on_shift = TRUE AND categories.name = "Electronics";

-- 6. Tools overdue for calibration
-- Which tools haven't had a calibration check in longer than their calibration_interval_days? (Hint: you'll 
-- need the most recent check_date per tool, then compare it against today's date minus the interval.)
SELECT tools.tool_id, tools.name, (CURRENT_DATE - latest.last_check) AS days_since_check
FROM tools JOIN ( SELECT tool_id, MAX(check_date) AS last_check
    FROM calibration_logs GROUP BY tool_id) 
AS latest ON tools.tool_id = latest.tool_id
WHERE (CURRENT_DATE - latest.last_check) > tools.calibration_interval_days;

-- 7. Most-consumed part
-- Which single part has been used the most (by total qty_used) across all repair tickets?
-- This is a classic "top consumer" report for restocking decisions.
SELECT SUM(qty_used) AS total_used, part_id FROM ticket_parts_used
GROUP BY part_id ORDER BY total_used DESC LIMIT 1;

-- 8. Member repair history
-- For a specific member, show every repair ticket they've ever submitted along with the item name, 
-- status, and the volunteer who worked on it (if assigned).
SELECT rt.ticket_id, rt.item_name, rt.status, volunteers.full_name AS assigned_to
FROM repair_tickets AS rt
JOIN members ON rt.member_id = members.member_id
LEFT JOIN volunteers ON rt.assigned_volunteer_id = volunteers.volunteer_id
WHERE members.member_id = 3;

-- 9. Average repair turnaround time
-- For completed tickets, what's the average number of days between created_at and completed_at?
-- Break it down by category to see which repair types take longest.
SELECT AVG(rt.completed_at - rt.created_at) AS Turn_Around_Time, categories.name
FROM repair_tickets AS rt JOIN categories ON
rt.category_id = categories.category_id
WHERE rt.status = 'completed'
GROUP BY categories.category_id;

-- 10. Members who never returned a tool on time
-- Find members who have at least one loan where return_date was later than due_date (a returned-but-late loan) — 
-- different from question 1, since this is about past late returns, not currently overdue ones. Useful for a "reliability flag" on member profiles.
SELECT DISTINCT members.member_id, members.full_name
FROM members
JOIN tool_loans ON members.member_id = tool_loans.member_id
WHERE tool_loans.due_date < tool_loans.return_date;-- 1. Overdue tool loans
-- Which tools are currently checked out and past their due_date (not yet returned)? 
-- Show tool name, borrower name, and how many days overdue.
SELECT tools.name, members.full_name, (CURRENT_DATE - tool_loans.due_date) as days_overdue
FROM tools JOIN tool_loans ON tools.tool_id = tool_loans.tool_id
JOIN members ON tool_loans.member_id = members.member_id
WHERE tool_loans.return_date IS NULL
AND tool_loans.due_date < CURRENT_DATE;

-- 2. Low stock parts warning
-- List all parts where stock_qty has fallen below min_threshold — this is exactly what should 
-- power the "Parts Warnings" stat in the header banner.
SELECT * FROM parts WHERE stock_qty < min_threshold;

-- 3. Volunteer workload
-- For each volunteer, how many repair tickets are currently assigned to them that are not 
-- yet completed? Order by workload descending — useful for figuring out who's overloaded.
SELECT volunteers.volunteer_id, volunteers.full_name, COUNT(rt.status) AS open_tickets
FROM volunteers LEFT JOIN repair_tickets AS rt -- Left Join to search for volunteers who are not working on any ticket
ON rt.assigned_volunteer_id = volunteers.volunteer_id
WHERE rt.status IN ('intake', 'diagnosing', 'in_progress', 'awaiting_parts')
GROUP BY volunteers.volunteer_id, volunteers.full_name
ORDER BY open_tickets DESC;

-- 4. Total carbon offset so far
-- What's the total carbon offset (in kg CO2) from all completed repair tickets? (Hint: this needs weight_kg from 
-- tickets joined against carbon_multiplier from categories, summed only where status = completed.)
SELECT SUM(rt.weight_kg * categories.carbon_multiplier) as total_carbon_offset 
FROM repair_tickets AS rt JOIN categories 
ON rt.category_id = categories.category_id
WHERE rt.status = 'completed';

-- 5. Skills-matched volunteer suggestion
-- For a given category (say, "Electronics"), list all volunteers who have that specialty AND are currently 
-- on_shift — this is the exact query the "Skills-Matched Volunteer Filtering" dropdown needs to run live.
SELECT volunteers.volunteer_id, volunteers.full_name, categories.name
FROM volunteers JOIN volunteer_specialties AS vs 
ON volunteers.volunteer_id = vs.volunteer_id
JOIN categories ON categories.category_id = vs.category_id
WHERE volunteers.on_shift = TRUE AND categories.name = "Electronics";

-- 6. Tools overdue for calibration
-- Which tools haven't had a calibration check in longer than their calibration_interval_days? (Hint: you'll 
-- need the most recent check_date per tool, then compare it against today's date minus the interval.)
SELECT tools.tool_id, tools.name, (CURRENT_DATE - latest.last_check) AS days_since_check
FROM tools JOIN ( SELECT tool_id, MAX(check_date) AS last_check
    FROM calibration_logs GROUP BY tool_id) 
AS latest ON tools.tool_id = latest.tool_id
WHERE (CURRENT_DATE - latest.last_check) > tools.calibration_interval_days;

-- 7. Most-consumed part
-- Which single part has been used the most (by total qty_used) across all repair tickets?
-- This is a classic "top consumer" report for restocking decisions.
SELECT SUM(qty_used) AS total_used, part_id FROM ticket_parts_used
GROUP BY part_id ORDER BY total_used DESC LIMIT 1;

-- 8. Member repair history
-- For a specific member, show every repair ticket they've ever submitted along with the item name, 
-- status, and the volunteer who worked on it (if assigned).
SELECT rt.ticket_id, rt.item_name, rt.status, volunteers.full_name AS assigned_to
FROM repair_tickets AS rt
JOIN members ON rt.member_id = members.member_id
LEFT JOIN volunteers ON rt.assigned_volunteer_id = volunteers.volunteer_id
WHERE members.member_id = 3;

-- 9. Average repair turnaround time
-- For completed tickets, what's the average number of days between created_at and completed_at?
-- Break it down by category to see which repair types take longest.
SELECT AVG(rt.completed_at - rt.created_at) AS Turn_Around_Time, categories.name
FROM repair_tickets AS rt JOIN categories ON
rt.category_id = categories.category_id
WHERE rt.status = 'completed'
GROUP BY categories.category_id;

-- 10. Members who never returned a tool on time
-- Find members who have at least one loan where return_date was later than due_date (a returned-but-late loan) — 
-- different from question 1, since this is about past late returns, not currently overdue ones. Useful for a "reliability flag" on member profiles.
SELECT DISTINCT members.member_id, members.full_name
FROM members
JOIN tool_loans ON members.member_id = tool_loans.member_id
WHERE tool_loans.due_date < tool_loans.return_date;