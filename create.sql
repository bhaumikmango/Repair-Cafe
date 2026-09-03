CREATE TABLE categories (
    category_id       SERIAL PRIMARY KEY,
    name              VARCHAR(100) NOT NULL,
    carbon_multiplier NUMERIC(6,3) NOT NULL
);

CREATE TABLE members (
    member_id    SERIAL PRIMARY KEY,
    full_name    VARCHAR(150) NOT NULL,
    email        VARCHAR(255) NOT NULL,
    phone        VARCHAR(30),
    joined_date  DATE NOT NULL
);

CREATE TABLE volunteers (
    volunteer_id SERIAL PRIMARY KEY,
    full_name    VARCHAR(150) NOT NULL,
    email        VARCHAR(255) NOT NULL,
    is_active    BOOLEAN NOT NULL DEFAULT TRUE,
    on_shift     BOOLEAN NOT NULL DEFAULT FALSE
);

CREATE TABLE volunteer_specialties (
    volunteer_id INTEGER NOT NULL REFERENCES volunteers(volunteer_id),
    category_id  INTEGER NOT NULL REFERENCES categories(category_id),
    PRIMARY KEY (volunteer_id, category_id)
);

CREATE TYPE tool_status AS ENUM ('available', 'checked_out', 'in_repair', 'retired');

CREATE TABLE tools (
    tool_id                SERIAL PRIMARY KEY,
    name                   VARCHAR(120) NOT NULL,
    category_id            INTEGER REFERENCES categories(category_id),
    status                 tool_status NOT NULL DEFAULT 'available',
    shelf_location         VARCHAR(50) NOT NULL,
    calibration_interval_days INTEGER NOT NULL
);

CREATE TYPE calibration_result AS ENUM ('pass', 'fail');

CREATE TABLE calibration_logs (
    log_id         SERIAL PRIMARY KEY,
    tool_id        INTEGER NOT NULL REFERENCES tools(tool_id),
    technician_id  INTEGER NOT NULL REFERENCES volunteers(volunteer_id),
    check_date     DATE NOT NULL,
    result         calibration_result NOT NULL,
    notes          TEXT
);

CREATE TABLE tool_loans (
    loan_id        SERIAL PRIMARY KEY,
    tool_id        INTEGER NOT NULL REFERENCES tools(tool_id),
    member_id      INTEGER NOT NULL REFERENCES members(member_id),
    checkout_date  DATE NOT NULL,
    due_date       DATE NOT NULL,
    return_date    DATE
);

CREATE TYPE ticket_status AS ENUM ('intake', 'diagnosing', 'in_progress', 'awaiting_parts', 'completed');

CREATE TABLE repair_tickets (
    ticket_id             SERIAL PRIMARY KEY,
    member_id             INTEGER NOT NULL REFERENCES members(member_id),
    category_id           INTEGER NOT NULL REFERENCES categories(category_id),
    assigned_volunteer_id INTEGER REFERENCES volunteers(volunteer_id), -- nullable: unassigned at intake
    item_name             VARCHAR(150) NOT NULL,
    weight_kg             NUMERIC(8,3) NOT NULL,
    status                ticket_status NOT NULL DEFAULT 'intake',
    symptom_notes         TEXT,
    created_at            TIMESTAMP NOT NULL DEFAULT now(),
    completed_at          TIMESTAMP
);

CREATE TABLE parts (
    part_id        SERIAL PRIMARY KEY,
    name           VARCHAR(120) NOT NULL,
    drawer_location VARCHAR(50) NOT NULL,
    stock_qty      INTEGER NOT NULL DEFAULT 0,
    min_threshold  INTEGER NOT NULL
);

CREATE TABLE ticket_parts_used (
    ticket_id  INTEGER NOT NULL REFERENCES repair_tickets(ticket_id),
    part_id    INTEGER NOT NULL REFERENCES parts(part_id),
    qty_used   INTEGER NOT NULL,
    used_at    TIMESTAMP NOT NULL DEFAULT now(),
    PRIMARY KEY (ticket_id, part_id)
);
