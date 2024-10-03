SELECT schema.add_item() AS RESULT;
CREATE OR REPLACE FUNCTION schema.add_item(
    name VARCHAR,
    status schema.status_item,
    owner VARCHAR
)
RETURNS VARCHAR AS $$
DECLARE
    new_item_id INT;
BEGIN
    INSERT INTO schema.Item (Name, Status, Owner)
    VALUES (name, status, owner)
    RETURNING ID INTO new_item_id;

    INSERT INTO schema.QualityCheck (Item_id, DateSent, ReturnDate,StartDate, EndDate, ResultState)
    VALUES (new_item_id, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP+Interval '5 days', CURRENT_TIMESTAMP + INTERVAL '2 days',CURRENT_TIMESTAMP + INTERVAL '4 days', FALSE);
     RETURN 'Item and initial quality check added successfully.';
EXCEPTION WHEN OTHERS THEN
    RETURN 'Error: ' || SQLERRM;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION schema.update_item_quality_status()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE schema.Item
    SET Qual_check = NEW.ResultState,
        Status = CASE
                    WHEN NEW.ResultState = TRUE THEN 'in_stock'::schema.status_item
                    WHEN NEW.ResultState = FALSE THEN 'not qualitative'::schema.status_item
                 END
    WHERE ID = NEW.Item_id;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_update_item_quality
AFTER UPDATE OF ResultState ON schema.QualityCheck
FOR EACH ROW
EXECUTE FUNCTION schema.update_item_quality_status();