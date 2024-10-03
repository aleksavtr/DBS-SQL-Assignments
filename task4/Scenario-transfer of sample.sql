CREATE OR REPLACE FUNCTION schema.move_item_to_new_zone(
    p_item_id INT,
    new_zone_id INT
)
RETURNS VARCHAR AS $$
DECLARE
    current_exhibition_id INT;
BEGIN
     -- Kontrola existencie novej zóny
    IF NOT EXISTS (SELECT 1 FROM schema.Zone WHERE ID = new_zone_id) THEN
        RETURN 'Error: Specified zone does not exist.';
    END IF;

   -- Zistenie ID súčasnej výstavy, na ktorej je položka vystavená
    SELECT Exhibition_Id INTO current_exhibition_id FROM schema.Exhibition_Item
    WHERE Item_id = p_item_id;

    -- Overenie, či nová zóna hostí súčasnú výstavu tejto položky
    IF EXISTS (
        SELECT 1 FROM schema.ExhibitionZone
        WHERE ID_Zone = new_zone_id AND ID_Exh = current_exhibition_id
    ) THEN
       -- Aktualizácia zóny položky v databáze
        UPDATE schema.Item
        SET ZoneID = new_zone_id
        WHERE ID = p_item_id;
        RETURN 'Item successfully moved to the new zone.';
    ELSE
        RETURN 'Error: The new zone does not host the current exhibition of the item.';
    END IF;
EXCEPTION WHEN OTHERS THEN
    -- Zachytenie a spracovanie akýchkoľvek výnimiek
    RETURN 'Error: ' || SQLERRM;
END;
$$ LANGUAGE plpgsql;