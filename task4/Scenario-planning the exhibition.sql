-- Deklarácia funkcie s parametrami: pole ID exponátov, ID výstavy, začiatočný a konečný dátum a ID zóny
CREATE OR REPLACE FUNCTION schema.plan_exhibition1(
    exhibit_ids INT[],
    exhibition_id INT,
    start_date DATE,
    end_date DATE,
    zone_id INT
)
RETURNS VARCHAR AS $$

-- Lokálne deklarácie premenných
DECLARE
    exhibit_id INT;
    item_status VARCHAR;
    item_qual_check BOOLEAN;
    error_msg VARCHAR := '';
    last_exhibition_end_date DATE;

BEGIN
    -- Získanie dátumu ukončenia poslednej výstavy v danej zóne
    SELECT MAX(E.EndDate) INTO last_exhibition_end_date
    FROM schema.ExhibitionZone EZ
    JOIN schema.Exhibition E ON EZ.ID_Exh = E.ID
    WHERE EZ.ID_Zone = zone_id AND EZ.Status IN ('reserved', 'active');

    -- Kontrola, či nová výstava môže byť naplánovaná v zóne
    IF last_exhibition_end_date IS NULL OR last_exhibition_end_date < start_date THEN
        -- Kontrola a pridanie každého exponátu do výstavy
        FOREACH exhibit_id IN ARRAY exhibit_ids LOOP
            SELECT status, Qual_check INTO item_status, item_qual_check FROM schema.Item WHERE ID = exhibit_id;
            IF item_status IN ('available', 'in_storage') AND item_qual_check THEN
                INSERT INTO schema.Exhibition_Item (Item_ID, Exhibition_ID, Status)
                VALUES (exhibit_id, exhibition_id, 'Planned');
            ELSE
                error_msg := error_msg || 'Error: Exhibit ID ' || exhibit_id || ' is not available for display or not quality checked. ';
            END IF;
        END LOOP;
    ELSE
        RETURN 'Error: Zone is still occupied or reserved for the selected dates.';
    END IF;

    IF error_msg <> '' THEN
        RETURN error_msg;
    ELSE
        RETURN 'All eligible exhibits added successfully to the exhibition.';
    END IF;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION schema.update_item_status_on_exhibition()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE schema.Item
    SET Status = 'on_the_exhibition'
    WHERE ID = NEW.Item_ID;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_update_status_after_adding_to_exhibition
AFTER INSERT ON schema.Exhibition_Item
FOR EACH ROW
EXECUTE FUNCTION schema.update_item_status_on_exhibition();

