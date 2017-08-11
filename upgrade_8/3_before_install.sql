-- Delete new create stock picking type
DELETE
FROM stock_picking_type
WHERE company_id is null and name='PoS Orders';

-- Disable stock_picking_type "internal"
UPDATE stock_picking_type
SET active=false
WHERE id not in (
        SELECT picking_type_id
        FROM stock_picking
        GROUP BY picking_type_id)
    AND active = true
    AND name = 'Internal Transfers';

-- Disable stock picking type from inactive PoS config
UPDATE stock_picking_type
SET active=false
WHERE id IN (
        SELECT picking_type_id
        FROM pos_config
        WHERE state != 'active')

-- Disable fucking 3PP picking type
update stock_picking_type set active=false where company_id = 1 and warehouse_id != 1;
