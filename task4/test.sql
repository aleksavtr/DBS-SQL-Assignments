TRUNCATE schema.Exhibition, schema.ExhibitionZone, schema.Item, schema.Exhibition_Item RESTART IDENTITY CASCADE;
INSERT INTO schema.Item (Name, Status, Owner) VALUES
('Historical Sword', 'in_storage', 'Medieval Artifacts'),
('Ancient Vase', 'in_exhibition', 'Greek Antiquities'),
('Rare Manuscript', 'in_restoration', 'Restoration Lab');
INSERT INTO schema.Exhibition_Item (Item_ID, Exhibition_ID, Status) VALUES
(1, 1, 'Planned'),
(2, 1, 'Planned');
INSERT INTO schema.QualityCheck (Item_id, DateSent, ReturnDate, StartDate, EndDate, ResultState) VALUES
(1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP + INTERVAL '5 days', CURRENT_TIMESTAMP + INTERVAL '2 days', CURRENT_TIMESTAMP + INTERVAL '4 days', FALSE),
(2, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP + INTERVAL '5 days', CURRENT_TIMESTAMP + INTERVAL '2 days', CURRENT_TIMESTAMP + INTERVAL '4 days', TRUE);
INSERT INTO schema.Loans (Item_id, DateLoan, ReturnDate, Real_ret_date, Borrower, Is_permanent) VALUES
(3, CURRENT_TIMESTAMP, NULL, NULL, 'Our Museum', TRUE);
INSERT INTO schema.Item (Name, Status, Owner) VALUES
('Medieval Shield', 'in_storage', 'Medieval Artifacts'),
('Egyptian Sarcophagus', 'in_exhibition', 'Egyptian Artifacts'),
('Renaissance Painting', 'in_restoration', 'European Art Department');
INSERT INTO schema.Exhibition_Item (Item_ID, Exhibition_ID, Status) VALUES
(3, 2, 'Planned'),
(4, 2, 'Planned'),
(5, 2, 'Planned');
INSERT INTO schema.QualityCheck (Item_id, DateSent, ReturnDate, StartDate, EndDate, ResultState) VALUES
(4, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP + INTERVAL '5 days', CURRENT_TIMESTAMP + INTERVAL '2 days', CURRENT_TIMESTAMP + INTERVAL '4 days', TRUE),
(5, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP + INTERVAL '5 days', CURRENT_TIMESTAMP + INTERVAL
INSERT INTO schema.Loans (Item_id, DateLoan, ReturnDate, Real_ret_date, Borrower, Is_permanent) VALUES
(4, CURRENT_TIMESTAMP, NULL, NULL, 'Local History Museum', TRUE),
(5, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP + INTERVAL '30 days', NULL, 'Private Collector', FALSE);
