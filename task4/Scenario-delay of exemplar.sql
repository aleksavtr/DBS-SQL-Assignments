CREATE OR REPLACE FUNCTION schema.Loaned_item(
    item_id INT
)
RETURNS VARCHAR AS $$
DECLARE
    new_item_id INT;
BEGIN
    -- Aktualizácia stavu položky na "loaned" v databáze
    UPDATE schema.Item
    SET Status = 'loaned'
    WHERE ID = item_id;
    -- Pridanie záznamu o požičaní do tabuľky Loans
    INSERT INTO schema.Loans (Item_id, DateLoan, ReturnDate, Real_ret_date, Borrower)
    VALUES (new_item_id, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP+INTERVAL '10 days', 'NULL', 'Another Museum');
    RETURN 'Loan entry created.';
EXCEPTION WHEN OTHERS THEN
    RETURN 'Error: ' || SQLERRM;
END
$$ LANGUAGE plpgsql;