CREATE OR REPLACE FUNCTION schema.Retrieved_item(
    name VARCHAR,
    status schema.status_item,
    owner VARCHAR
)
RETURNS VARCHAR AS $$
DECLARE
    new_item_id INT;
BEGIN
      -- Pridanie novej položky do tabuľky Item a získanie jej ID
    INSERT INTO schema.Item (Name, Status, Owner)
    VALUES (name, status, owner)
    RETURNING ID INTO new_item_id;

   -- Pridanie údajov o kontrole kvality pre novú položku
    INSERT INTO schema.QualityCheck (
        Item_id,
        DateSent,
        ReturnDate,
        StartDate,
        EndDate,
        ResultState
    ) VALUES (
        new_item_id,
        CURRENT_TIMESTAMP,
        CURRENT_TIMESTAMP + INTERVAL '5 days',
        CURRENT_TIMESTAMP + INTERVAL '2 days',
        CURRENT_TIMESTAMP + INTERVAL '4 days',
        FALSE
    );

  -- Pridanie záznamu o požičaní do tabuľky Loans
    INSERT INTO schema.Loans (
        Item_id,
        DateLoan,
        ReturnDate,
        Real_ret_date,
        Borrower,
        Is_permanent
    ) VALUES (
        new_item_id,
        CURRENT_TIMESTAMP,
        'NULL',  -- Nešpecifikovaný dátum vrátenia, keďže požičanie je trvalé
        'NULL',-- Nešpecifikovaný reálny dátum vrátenia
        'Our Museum',  -- Pozíčateľ je naše múzeum
        TRUE -- Požičanie je trvalé
    );
    RETURN 'Item and initial quality check added successfully. Loan entry created.';
EXCEPTION WHEN OTHERS THEN
    RETURN 'Error: ' || SQLERRM;
END;
$$ LANGUAGE plpgsql;